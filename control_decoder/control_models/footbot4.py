import math
import socket
import threading
import time
from typing import Any, Callable, Optional

import zmq
from attrs import asdict, evolve
from google.protobuf.message import DecodeError

from decoder import control_decoder_command_model as cdcm
from decoder.robot_control_proto import control_pb2, telemetry_pb2
from control_models.base_model import ControlModel
from control_models.footbot4_radio import build_radio_packet

MAX_TELEMETRY_MESSAGES_PER_TICK = 200
# A robot is driven over WiFi only while it has a discovered IP and its telemetry
# came no longer than this ago; otherwise its commands go to the radio box
DEFAULT_WIFI_FEEDBACK_TIMEOUT = 1.0  # [s]
BOX_WARNING_INTERVAL = 1.0  # [s] radio box send errors are printed at most this often
LINK_WIFI = "wifi"
LINK_BOX = "box"
COMMAND_TELEMETRY_COLUMNS = (
    "r_id",
    "link",
    "speedX",
    "speedY",
    "speedW",
    "dribler",
    "voltage",
    "kickUP",
    "kickDWN",
    "angMode",
    "beep",
    "dribEN",
    "charEN",
    "autokck",
)
COMMAND_TELEMETRY_HEADER = 'SENDING COMMANDS IN "FB4" MODE\n'


def fill_kicker_and_dribbler(
    kicker_and_dribbler: control_pb2.KickerAndDribbler,
    robot: cdcm.AnyDecoderCommand,
) -> None:
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

    kicker_and_dribbler.kicker_mode = kicker_mode
    kicker_and_dribbler.kicker_voltage = robot.kicker_setting
    kicker_and_dribbler.dribbler_setting = round(robot.dribbler_setting)


def build_robot_command(robot: cdcm.AnyDecoderCommand) -> control_pb2.RobotCommand:
    command = control_pb2.RobotCommand()
    command.robot_id = robot.robot_id
    if isinstance(robot, cdcm.DecoderCoefficientsCommand):
        command.robot_control_type = control_pb2.RobotControlType.SET_COEFFICIENTS
        command.coefficients.SetInParent()  # sent even with no field set
        for name, value in asdict(robot).items():
            if name != "robot_id" and value is not None:
                setattr(command.coefficients, name, value)
        return command
    command.beep = robot.beep

    match robot:
        case cdcm.DecoderRicochetCommand():
            command.robot_control_type = control_pb2.RobotControlType.RICOCHET
            # DecoderRicochetCommand coordinates are in mm, the robot takes m
            command.ricochet.x = robot.x / 1000
            command.ricochet.y = robot.y / 1000
            command.ricochet.angle = robot.angle
            fill_kicker_and_dribbler(command.ricochet.kicker_and_dribbler, robot)

        case cdcm.DecoderCatchBallCommand():
            command.robot_control_type = control_pb2.RobotControlType.CATCH_BALL
            command.catch_ball.angle = robot.angle
            fill_kicker_and_dribbler(command.catch_ball.kicker_and_dribbler, robot)

        case cdcm.DecoderCommand():
            command.robot_control_type = control_pb2.RobotControlType.NEW_FORMAT
            # DecoderCommand speeds are in mm/s, the robot takes m/s.
            # Robot frame: vel_y > 0 is left, angular_velocity > 0 is counterclockwise,
            # the same as DecoderCommand
            command.new_format.speed_control.vel_x = robot.forward_vel / 1000
            command.new_format.speed_control.vel_y = robot.left_vel / 1000
            if robot.angle is not None:
                command.new_format.speed_control.delta_angle = robot.angle
            else:
                command.new_format.speed_control.angular_velocity = robot.angular_vel or 0.0
            fill_kicker_and_dribbler(command.new_format.kicker_and_dribbler, robot)

    return command


def robot_hostname(robot_id: int) -> str:
    return f"fb4-{robot_id:02}.local"


def build_command_telemetry_row(robot: cdcm.DecoderCommand, link: str) -> tuple[str, ...]:
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
        link,
        f"{robot.left_vel:.0f}",
        f"{robot.forward_vel:.0f}",
        "null" if speed_w is None else f"{speed_w:.1f}",
        str(robot.dribbler_setting),
        str(robot.kicker_setting),
        str(int(robot.kick_up)),
        str(int(robot.kick_forward)),
        str(angle_mode),
        str(int(robot.beep)),
        str(int(robot.dribbler_setting > 0)),
        str(int(robot.kicker_setting > 0)),
        str(autokick),
    )
    return values


def build_target_telemetry_line(robot: cdcm.AnyDecoderCommand, link: str) -> str:
    match robot:
        case cdcm.DecoderRicochetCommand():
            target = f"x={robot.x:.0f}  y={robot.y:.0f}  angle={robot.angle:.2f}"
        case cdcm.DecoderCatchBallCommand():
            target = f"angle={robot.angle:.2f}"
        case _:
            target = ""
    return (
        f"r_id {robot.robot_id} {link} {cdcm.CONTROL_TYPES[type(robot)]}  {target}  "
        f"voltage={robot.kicker_setting}  dribler={robot.dribbler_setting}  "
        f"beep={int(robot.beep)}"
    )


def build_command_telemetry(robots: list[cdcm.AnyDecoderCommand], links: dict[int, str]) -> str:
    rows = [
        build_command_telemetry_row(robot, links[robot.robot_id])
        for robot in robots
        if isinstance(robot, cdcm.DecoderCommand)
    ]
    target_lines = [
        build_target_telemetry_line(robot, links[robot.robot_id])
        for robot in robots
        if not isinstance(robot, (cdcm.DecoderCommand, cdcm.DecoderCoefficientsCommand))
    ]
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
    lines.extend(target_lines)
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
        self.wifi_feedback_timeout = control_config.get(
            "fb4_wifi_feedback_timeout", DEFAULT_WIFI_FEEDBACK_TIMEOUT
        )
        # Radio boxes take robots 0..7 (low) and 8..15 (high), as with FB2
        self.box_address_low = (control_config["fb4_ip_low"], self.udpie_port)
        self.box_address_high = (control_config["fb4_ip_high"], self.udpie_port)

        self.robot_cmd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.robot_telemetry_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.robot_telemetry_socket.bind(("0.0.0.0", self.telemetry_port))
        self.robot_telemetry_socket.setblocking(False)
        # Non-blocking: while the box's address is unresolved (ARP; a box that is off), the kernel queues the
        # packets against the socket's send buffer, and a blocking sendto then waits until ARP gives up (~3 s),
        # stalling the whole decoder. Packets that don't fit are dropped instead
        self.box_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.box_socket.setblocking(False)
        self._box_errors = 0  # box packets not sent since the last warning
        self._last_box_warning = time.time()

        self._last_feedback: dict[int, float] = {}  # rid -> time of its last telemetry
        self._links: dict[int, str] = {}  # rid -> link of its last command, to log switches

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
            ip = self._wifi_ip(robot_id, self._snapshot_discovered_ips())
            if ip is None:
                self.box_socket.sendto(data, self._box_address(robot_id))
            else:
                self.udpie_socket.sendto(data, (ip, self.udpie_port))

        self.udpie_processor = UdPieProcessor(udpie_sender, telemetry_sender)

    def _wifi_ip(self, robot_id: int, discovered_ips: dict[int, str]) -> Optional[str]:
        """IP to drive the robot over WiFi, None if it goes through the radio box"""
        ip = discovered_ips.get(robot_id)
        last_feedback = self._last_feedback.get(robot_id)
        if ip is None or last_feedback is None:
            return None
        if time.time() - last_feedback > self.wifi_feedback_timeout:
            return None
        return ip

    def _box_address(self, robot_id: int) -> tuple[str, int]:
        return self.box_address_low if robot_id < 8 else self.box_address_high

    def _update_link(self, robot_id: int, link: str) -> None:
        # The first command of a robot is printed as a switch from the other link too: "wifi -> box"
        previous = self._links.get(robot_id, LINK_BOX if link == LINK_WIFI else LINK_WIFI)
        if previous != link:
            print(f"[fb4] robot {robot_id}: {previous} -> {link}")
            self._links[robot_id] = link

    def _send_to_box(self, robot: cdcm.AnyDecoderCommand) -> None:
        if isinstance(robot, cdcm.DecoderCoefficientsCommand):
            return  # the strategy sends them every robot now and then, nothing to set over the box
        # The box only carries speed commands, onboard ones need WiFi
        if not isinstance(robot, cdcm.DecoderCommand):
            self.warn_unsupported(robot)
            return
        try:
            self.box_socket.sendto(build_radio_packet(robot), self._box_address(robot.robot_id))
        except OSError as error:  # BlockingIOError too: the box doesn't answer ARP
            self._warn_box_error(robot.robot_id, error)

    def _warn_box_error(self, robot_id: int, error: OSError) -> None:
        # Commands come at the strategy rate for every robot without WiFi, so print at most once per interval
        self._box_errors += 1
        now = time.time()
        if now - self._last_box_warning < BOX_WARNING_INTERVAL:
            return
        print(
            f"[fb4] {self._box_errors} box packets not sent in {now - self._last_box_warning:.0f} s "
            f"(last: robot {robot_id}, {self._box_address(robot_id)[0]}: {error!r}); is the radio box on?"
        )
        self._box_errors = 0
        self._last_box_warning = now

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
        discovered_ips = self._snapshot_discovered_ips()
        links: dict[int, str] = {}
        for robot in signal_data.robot_commands:
            ip = self._wifi_ip(robot.robot_id, discovered_ips)
            links[robot.robot_id] = LINK_BOX if ip is None else LINK_WIFI
            self._update_link(robot.robot_id, links[robot.robot_id])
            if ip is None:
                self._send_to_box(robot)
                continue
            data = build_robot_command(robot).SerializeToString()
            try:
                self.robot_cmd_socket.sendto(data, (ip, self.command_port))
            except OSError as error:
                print(f"[fb4] send error for robot {robot.robot_id} at {ip}: {error}")
        self.telemetry_text = build_command_telemetry(signal_data.robot_commands, links)
        self.last_update = time.time()

    def process_signal(self, raw: Any):
        self.udpie_processor.process_udpie(raw)

    def broadcast_command(self, command: cdcm.AnyDecoderCommand) -> None:
        data = build_robot_command(command).SerializeToString()
        discovered_ips = self._snapshot_discovered_ips()
        for robot_id in range(self.robot_count):
            ip = self._wifi_ip(robot_id, discovered_ips)
            if ip is None:
                self._send_to_box(evolve(command, robot_id=robot_id))
                continue
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

            # Telemetry is the WiFi feedback that keeps the robot off the radio box
            telemetry = telemetry_pb2.RobotTelemetry()
            try:
                telemetry.ParseFromString(data)
            except DecodeError:
                continue
            self._last_feedback[telemetry.robot_id] = time.time()

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
                ip = self._wifi_ip(robot["robot_id"], discovered_ips)
                if ip is None:
                    # The radio box has no GLOBAL_COORDINATES command
                    print(f"[fb4] robot {robot["robot_id"]} has no WiFi link; relocate skipped")
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
