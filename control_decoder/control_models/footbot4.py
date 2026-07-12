import json
import socket
import threading
import time
from typing import Any, Callable, Optional

import zmq

from decoder import control_decoder_command_model as cdcm
from decoder.robot_control_proto import control_pb2
from control_models.base_model import ControlModel

STALE_AFTER_SECONDS = 2.0
STATUS_EMIT_INTERVAL_SECONDS = 0.1
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


def build_new_format_command(robot: cdcm.DecoderCommand) -> control_pb2.NewFormat:
    command = control_pb2.NewFormat()

    command.speed_control.vel_x = robot.left_vel
    command.speed_control.vel_y = robot.forward_vel
    if robot.angle is not None:
        command.speed_control.delta_angle = robot.angle
    else:
        command.speed_control.angular_velocity = robot.angular_vel or 0.0

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

    command.kicker_and_dribbler.kicker_mode = kicker_mode
    command.kicker_and_dribbler.kicker_setting = robot.kicker_setting
    command.kicker_and_dribbler.dribbler_setting = round(robot.dribbler_setting)

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


def record_telemetry(state: dict[int, dict], payload: dict, now: float) -> int | None:
    if not isinstance(payload, dict):
        return None

    robot_id = payload.get("robot_id")
    if type(robot_id) is not int or not 0 <= robot_id <= 15:
        return None

    state[robot_id] = {
        "voltage": payload.get("voltage"),
        "ball_sensor": payload.get("ball_sensor"),
        "last_seen": now,
    }
    return robot_id


def build_status_message(
    state: dict[int, dict], robot_team: dict[int, bool], now: float
) -> dict:
    message = {"blue": [], "yellow": []}
    for robot_id, record in state.items():
        team = robot_team.get(robot_id, False)

        entry = {
            "robot_id": robot_id,
            "online": now - record["last_seen"] < STALE_AFTER_SECONDS,
        }
        if record.get("ball_sensor") is not None:
            entry["ball_sensor"] = record["ball_sensor"]
        if record.get("voltage") is not None:
            entry["voltage"] = record["voltage"]
        message["yellow" if team else "blue"].append(entry)

    return message


def should_emit_status(
    fresh_robot_ids: set[int], now: float, last_emit: float, min_interval: float
) -> bool:
    return bool(fresh_robot_ids) and now - last_emit >= min_interval


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
        self.robot_team: dict[int, bool] = {}
        self.robot_telemetry_state: dict[int, dict] = {}
        self.fresh_robot_ids: set[int] = set()
        self.last_robot_status_emit = 0.0

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
            self.robot_team[robot.robot_id] = signal_data.isteamyellow
            ip = discovered_ips.get(robot.robot_id)
            if ip is None:
                print(f"[fb4] robot {robot.robot_id} has no discovered IP; skipping")
                continue
            data = build_new_format_command(robot).SerializeToString()
            try:
                self.robot_cmd_socket.sendto(data, (ip, self.command_port))
            except OSError as error:
                print(f"[fb4] send error for robot {robot.robot_id} at {ip}: {error}")
        self.last_update = time.time()

    def process_signal(self, raw: Any):
        self.udpie_processor.process_udpie(raw)

    def broadcast_command(self, command: cdcm.DecoderCommand) -> None:
        data = build_new_format_command(command).SerializeToString()
        for robot_id, ip in self._snapshot_discovered_ips().items():
            try:
                self.robot_cmd_socket.sendto(data, (ip, self.command_port))
            except OSError as error:
                print(
                    f"[fb4] broadcast send error for robot {robot_id} at {ip}: "
                    f"{error}"
                )

    def process_telemetry(self) -> None:
        ip_to_robot = {
            ip: robot_id for robot_id, ip in self._snapshot_discovered_ips().items()
        }
        for _ in range(MAX_TELEMETRY_MESSAGES_PER_TICK):
            try:
                data, (src_ip, _src_port) = self.robot_telemetry_socket.recvfrom(4096)
            except BlockingIOError:
                break
            except OSError as error:
                print("Robot telemetry receive error:", error)
                break

            try:
                robot_id = ip_to_robot.get(src_ip)
                if robot_id is None:
                    raise ValueError(f"unknown telemetry source IP {src_ip}")

                payload = json.loads(data)
                if not isinstance(payload, dict):
                    raise ValueError("telemetry payload must be a JSON object")
                payload["robot_id"] = robot_id

                now = time.time()
                robot_id = record_telemetry(
                    self.robot_telemetry_state, payload, now
                )
                if robot_id is None:
                    raise ValueError(
                        "telemetry robot_id must be an integer from 0 to 15"
                    )
                self.fresh_robot_ids.add(robot_id)
            except (
                json.JSONDecodeError,
                UnicodeDecodeError,
                ValueError,
                TypeError,
            ) as error:
                print("Invalid robot telemetry message:", error)

        now = time.time()
        if should_emit_status(
            self.fresh_robot_ids,
            now,
            self.last_robot_status_emit,
            STATUS_EMIT_INTERVAL_SECONDS,
        ):
            status_message = build_status_message(
                self.robot_telemetry_state, self.robot_team, now
            )
            try:
                self.robot_status_socket.send_json(
                    {"serviz": "update_robot_status", "data": status_message}
                )
            except zmq.ZMQError as error:
                print("Robot status publish error:", error)
            else:
                self.last_robot_status_emit = now
                self.fresh_robot_ids.clear()

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
