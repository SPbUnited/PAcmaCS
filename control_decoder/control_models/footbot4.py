import math
import socket
import threading
import time
from typing import Any, Callable, Optional

import zmq

from decoder import control_decoder_command_model as cdcm
from decoder.robot_control_proto import control_pb2
from control_models.base_model import ControlModel
MAX_TELEMETRY_MESSAGES_PER_TICK = 200
COMMAND_TELEMETRY_COLUMNS = (
    "r_id",
    "speedX",
    "speedY",
    "speedW",
    "dribler",
    "voltage",
    "kickUP",
    "kickDWN",
    "beep",
    "dribEN",
    "charEN",
    "autokck",
)
COMMAND_TELEMETRY_HEADER = 'SENDING COMMANDS IN "FB4" MODE\n'


def build_robot_command(robot: cdcm.DecoderCommand) -> control_pb2.RobotCommand:
    command = control_pb2.RobotCommand()

    command.new_format.speed_control.vel_x = robot.forward_vel
    command.new_format.speed_control.vel_y = -robot.left_vel
    if robot.angle is not None:
        command.new_format.speed_control.delta_angle = robot.angle
    else:
        command.new_format.speed_control.angular_velocity = robot.angular_vel or 0.0
        command.new_format.speed_control.angular_velocity *= -1

    if robot.kick_up:
        kicker_mode = control_pb2.KICK_HIGH
    elif robot.kick_forward:
        kicker_mode = control_pb2.KICK_STRAIGHT
    elif robot.auto_kick_up:
        kicker_mode = control_pb2.AUTOKICK_HIGH
    elif robot.auto_kick_forward:
        kicker_mode = control_pb2.AUTOKICK_STRAIGHT
    elif robot.auto_kick_momentum:
        kicker_mode = control_pb2.AUTOKICK_MOMENTUM
    else:
        kicker_mode = control_pb2.IDLE

    command.new_format.kicker_and_dribbler.kicker_mode = kicker_mode
    command.new_format.kicker_and_dribbler.kicker_voltage = robot.kicker_setting
    command.new_format.kicker_and_dribbler.dribbler_setting = round(robot.dribbler_setting)
    command.robot_id = robot.robot_id
    command.robot_control_type = control_pb2.RobotControlType.NEW_FORMAT
    return command


def robot_hostname(robot_id: int) -> str:
    return f"fb4-{robot_id:02}.local"


def build_command_telemetry_row(robot: cdcm.DecoderCommand) -> tuple[str, ...]:
    speed_w = robot.angular_vel if robot.angular_vel is not None else robot.angle
    angle_mode = int(robot.angle is not None)

    if robot.auto_kick_forward:
        autokick = 1
    elif robot.auto_kick_up:
        autokick = 2
    elif robot.auto_kick_momentum:
        autokick = 3
    else:
        autokick = 0

    values = (
        str(robot.robot_id),
        f"{robot.left_vel:.0f}",
        f"{robot.forward_vel:.0f}",
        "null" if speed_w is None else f"{speed_w:.1f}",
        str(robot.dribbler_setting),
        str(robot.kicker_setting),
        str(int(robot.kick_up)),
        str(int(robot.kick_forward)),
        str(angle_mode),
        str(int(robot.dribbler_setting > 0)),
        str(int(robot.kicker_setting > 0)),
        str(autokick),
    )
    return values


def build_command_telemetry(robots: list[cdcm.DecoderCommand]) -> str:
    rows = [build_command_telemetry_row(robot) for robot in robots]
    widths = [
        max([
            len(column),
            *(len(row[index]) for row in rows),
        ])
        for index, column in enumerate(COMMAND_TELEMETRY_COLUMNS)
    ]

    def format_row(row) -> str:
        return "  ".join(
            value.rjust(width) for value, width in zip(row, widths)
        )

    lines = [format_row(COMMAND_TELEMETRY_COLUMNS)]
    lines.extend(format_row(row) for row in rows)
    return COMMAND_TELEMETRY_HEADER + "\n".join(lines) + "\n"


class FB4Decoder(ControlModel):
    def __init__(self, config, telemetry_sender):
        super().__init__(config, telemetry_sender)

        control_config = config["control_decoder"]
        self.udpie_port = control_config.get("fb4_port", 10000)
        self.udpie_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.command_port = control_config.get("fb4_command_port", 5555)
        self.telemetry_port = control_config.get("fb4_telemetry_port", 5556)
        self.robot_count = control_config.get("fb4_robot_count", 16)

        self.robot_cmd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.robot_telemetry_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.robot_telemetry_socket.bind(("0.0.0.0", self.telemetry_port))
        self.robot_telemetry_socket.setblocking(False)

        # We resolve fb4-NN.local ourselves rather than resolving hostnames on the
        # command/telemetry hot path. An absent fb4-NN.local takes ~10s to fail via
        # mDNS, so resolving off-thread keeps control-loop sends non-blocking; a
        # periodic re-resolve still follows hostname/IP changes and picks robots up
        # as they appear or disappear.
        self._discovered_ips: dict[int, str] = {}   # rid -> ip, written by discovery
        self._discovery_lock = threading.Lock()
        self._discovery_stop = threading.Event()
        self._discovery_thread = threading.Thread(
            target=self._discovery_loop, daemon=True
        )
        self._discovery_thread.start()

        context = zmq.Context()
        self.robot_status_socket = context.socket(zmq.PUB)
        self.robot_status_socket.connect(config["ether"]["s_signals_sub_url"])
        # Every RobotTelemetry packet from the robots is republished here as is, one per
        # message; strategy and serviz (Robot status) both read this one stream.
        self.strategy_telemetry_socket = context.socket(zmq.PUB)
        self.strategy_telemetry_socket.bind(control_config["s_telemetry_fan_url"])

        def udpie_sender(robot_id: int, data: bytes):
            self.udpie_socket.sendto(
                data, (robot_hostname(robot_id), self.udpie_port)
            )

        self.udpie_processor = UdPieProcessor(udpie_sender, telemetry_sender)

    def _resolve_robot_ip(self, robot_id: int) -> Optional[str]:
        try:
            infos = socket.getaddrinfo(
                robot_hostname(robot_id), None,
                socket.AF_INET, socket.SOCK_STREAM,
            )
        except OSError:
            return None
        return infos[0][4][0] if infos else None

    def _discovery_loop(self) -> None:
        # Resolve all candidate hostnames concurrently so that dead .local lookups
        # (~10s each) do not serialise; one cycle is bounded by the slowest lookup.
        while not self._discovery_stop.is_set():
            threads = []

            def worker(rid: int) -> None:
                ip = self._resolve_robot_ip(rid)
                with self._discovery_lock:
                    if ip is None:
                        self._discovered_ips.pop(rid, None)
                    else:
                        self._discovered_ips[rid] = ip

            for rid in range(self.robot_count):
                thread = threading.Thread(target=worker, args=(rid,), daemon=True)
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()
            self._discovery_stop.wait(5.0)

    def _snapshot_discovered_ips(self) -> dict[int, str]:
        with self._discovery_lock:
            return dict(self._discovered_ips)

    def process(self, signal_data: cdcm.DecoderTeamCommand) -> None:
        self.telemetry_text = build_command_telemetry(signal_data.robot_commands)
        discovered_ips = self._snapshot_discovered_ips()
        for robot in signal_data.robot_commands:
            ip = discovered_ips.get(robot.robot_id)
            if ip is None:
                print(f"[fb4] robot {robot.robot_id} has no discovered IP; skipping")
                continue
            data = build_robot_command(robot).SerializeToString()
            try:
                self.robot_cmd_socket.sendto(data, (ip, self.command_port))
            except OSError as error:
                print(f"[fb4] send error for robot {robot.robot_id} at {ip}: {error}")
        self.last_update = time.time()

    def process_signal(self, raw: Any):
        self.udpie_processor.process_udpie(raw)

    def broadcast_command(self, command: cdcm.DecoderCommand) -> None:
        data = build_robot_command(command).SerializeToString()
        for robot_id, ip in self._snapshot_discovered_ips().items():
            try:
                self.robot_cmd_socket.sendto(data, (ip, self.command_port))
            except OSError as error:
                print(
                    f"[fb4] broadcast send error for robot {robot_id} at {ip}: "
                    f"{error}"
                )

    def process_telemetry(self) -> None:
        for _ in range(MAX_TELEMETRY_MESSAGES_PER_TICK):
            try:
                data, _src = self.robot_telemetry_socket.recvfrom(4096)
            except BlockingIOError:
                break
            except OSError as error:
                print("Robot telemetry receive error:", error)
                break

            try:
                self.strategy_telemetry_socket.send(data)
            except zmq.ZMQError as error:
                print("Robot telemetry publish error:", error)

    def process_formation(self,formation)->None:
        for team in ["YELLOW","BLUE"]:
            if team not in formation:
                continue
            for robot in formation[team]:
                command = control_pb2.RobotCommand()
                command.robot_id = robot["robot_id"]
                command.robot_control_type = control_pb2.RobotControlType.GLOBAL_COORDINATES
                command.global_coordinates.x = robot["x"]/1000
                command.global_coordinates.y = robot["y"]/1000
                # serviz sends rotation in degrees (grSim convention); proto expects radians
                command.global_coordinates.angle = math.radians(robot["rotation"])
                data = command.SerializeToString()
                discovered_ips = self._snapshot_discovered_ips()
                ip = discovered_ips.get(robot["robot_id"])
                if ip is None:
                    print(f"[fb4] robot {robot["robot_id"]} has no discovered IP; skipping")
                    continue
                try:
                    self.robot_cmd_socket.sendto(data, (ip, self.command_port))
                except OSError as error:
                    print(f"[fb4] send error for robot {robot["robot_id"]} at {ip}: {error}")

        
udpies_history: list[tuple[str, int, str]] = []


class UdPieProcessor:
    def __init__(
        self,
        robot_sender: Callable[[int, bytes], None],
        telemetry_sender: Callable[[str, str], None],
    ):
        self.robot_sender = robot_sender
        self.telemetry_sender = telemetry_sender

    def process_udpie(self, raw_data):
        try:
            data = bytes(int(x) & 0xFF for x in raw_data)
        except Exception as e:
            print("send_udpie: cannot convert data to bytes:", e)
            return

        if len(data) < 2:
            print("send_udpie: packet is too short")
            return

        print("Get new udpie:", data)
        robot_id = data[1] & 0x0F

        try:
            self.robot_sender(robot_id, data)
            self.log_udpie_packet(data)
        except OSError as e:
            print("Can't send UDPie, no route to host:", e)
            self.telemetry_sender("SENDED UDPIES", "Can't send UDPie, no route to host")

    def log_udpie_packet(self, data: bytes) -> None:
        global udpies_history

        now_str = time.strftime("%H:%M:%S", time.localtime())
        hex_str = " ".join(f"{b:02X}" for b in data)

        if udpies_history and udpies_history[0][0] == hex_str:
            last_hex, last_count, first_time = udpies_history[0]
            udpies_history[0] = (last_hex, last_count + 1, first_time)
        else:
            udpies_history.insert(0, (hex_str, 1, now_str))
            if len(udpies_history) > 20:
                udpies_history = udpies_history[:20]
                udpies_history.append(("...", 1, ""))

        lines: list[str] = []
        for pkt_hex, count, time_str in udpies_history:
            if count == 1:
                line = f"{time_str}\t{pkt_hex}"
            else:
                line = f"{time_str}\t{pkt_hex}"
                line += " " * (40 - len(line)) + f"x{count}"
            lines.append(line)

        udpies_text = "\n".join(lines)

        self.telemetry_sender("SENDED UDPIES", udpies_text)
