import json
import socket
import time
from typing import Any, Callable

import zmq
from cattrs import unstructure

from decoder import control_decoder_command_model as cdcm
from control_models.base_model import ControlModel

STALE_AFTER_SECONDS = 2.0
STATUS_EMIT_INTERVAL_SECONDS = 0.1
MAX_TELEMETRY_MESSAGES_PER_TICK = 200


def build_robot_command_payload(
    robot: cdcm.DecoderCommand, isteamyellow: bool, timestamp: float
) -> dict:
    payload = unstructure(robot)
    payload["isteamyellow"] = isteamyellow
    payload["timestamp"] = timestamp
    return payload


def parse_telemetry_topic(topic: bytes) -> str | None:
    try:
        return topic.decode("utf-8")
    except (AttributeError, UnicodeDecodeError):
        return None


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

        self.fb4_ip_port_low: tuple[str, int] = (
            config["control_decoder"]["fb4_ip_low"],
            config["control_decoder"]["fb4_port"],
        )
        self.fb4_ip_port_high: tuple[str, int] = (
            config["control_decoder"]["fb4_ip_high"],
            config["control_decoder"]["fb4_port"],
        )
        self.s_outbound_real_low = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s_outbound_real_high = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        context = zmq.Context()
        self.robot_cmd_socket = context.socket(zmq.PUB)
        self.robot_cmd_socket.setsockopt(zmq.SNDHWM, 3)
        self.robot_cmd_socket.setsockopt(zmq.LINGER, 0)
        self.robot_cmd_socket.bind(
            config["control_decoder"].get("robot_cmd_pub_url", "tcp://*:5555")
        )
        self.robot_telemetry_socket = context.socket(zmq.SUB)
        self.robot_telemetry_socket.setsockopt(zmq.RCVHWM, 100)
        self.robot_telemetry_socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self.robot_telemetry_socket.bind(
            config["control_decoder"].get(
                "robot_telemetry_sub_url", "tcp://*:5556"
            )
        )
        self.robot_status_socket = context.socket(zmq.PUB)
        self.robot_status_socket.connect(config["ether"]["s_signals_sub_url"])
        self.robot_team: dict[int, bool] = {}
        self.robot_telemetry_state: dict[int, dict] = {}
        self.fresh_robot_ids: set[int] = set()
        self.last_robot_status_emit = 0.0

        def robots_sender_low(data: bytes):
            self.s_outbound_real_low.sendto(data, self.fb4_ip_port_low)

        def robots_sender_high(data: bytes):
            self.s_outbound_real_high.sendto(data, self.fb4_ip_port_high)

        self.udpie_processor = UdPieProcessor(robots_sender_low, robots_sender_high, telemetry_sender)

    def process(self, signal_data: cdcm.DecoderTeamCommand) -> None:
        self.telemetry_text = 'SENDING COMMANDS IN "FB4" MODE\n'
        timestamp = time.time()
        for robot in signal_data.robot_commands:
            payload = build_robot_command_payload(
                robot, signal_data.isteamyellow, timestamp
            )
            self.robot_team[robot.robot_id] = signal_data.isteamyellow
            try:
                self.robot_cmd_socket.send_multipart(
                    [
                        f"cmd/{robot.robot_id}".encode(),
                        json.dumps(payload).encode(),
                    ],
                    flags=zmq.NOBLOCK,
                )
                self.telemetry_text += json.dumps(payload, sort_keys=True) + "\n"
            except zmq.Again:
                pass
        self.last_update = time.time()

    def process_signal(self, raw: Any):
        self.udpie_processor.process_udpie(raw)

    def process_telemetry(self) -> None:
        for _ in range(MAX_TELEMETRY_MESSAGES_PER_TICK):
            try:
                frames = self.robot_telemetry_socket.recv_multipart(flags=zmq.NOBLOCK)
            except zmq.Again:
                break
            except zmq.ZMQError as error:
                print("Robot telemetry receive error:", error)
                break

            try:
                if len(frames) != 2:
                    raise ValueError(f"expected 2 frames, got {len(frames)}")

                topic = parse_telemetry_topic(frames[0])
                if topic is None or not topic.startswith("tel/"):
                    raise ValueError("invalid telemetry topic")

                payload = json.loads(frames[1])
                if not isinstance(payload, dict):
                    raise ValueError("telemetry payload must be a JSON object")

                now = time.time()
                robot_id = record_telemetry(
                    self.robot_telemetry_state, payload, now
                )
                if robot_id is None:
                    raise ValueError(
                        "telemetry robot_id must be an integer from 0 to 15"
                    )
                self.fresh_robot_ids.add(robot_id)
                # print(f"Robot telemetry {robot_id} ({topic}):", payload)
            except (
                json.JSONDecodeError,
                UnicodeDecodeError,
                ValueError,
                TypeError,
                zmq.ZMQError,
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


###################################################################################################

udpies_history: list[tuple[str, int, str]] = []


class UdPieProcessor:
    def __init__(self, robots_sender_low, robots_sender_high, telemetry_sender: Callable[[str, str], None]):
        self.robots_sender_low = robots_sender_low
        self.robots_sender_high = robots_sender_high
        self.telemetry_sender = telemetry_sender

    def process_udpie(self, raw_data):
        try:
            data = bytes(int(x) & 0xFF for x in raw_data)
        except Exception as e:
            print("send_udpie: cannot convert data to bytes:", e)
            return

        print("Get new udpie:", data)
        robot_id = data[1] & 0x0F

        try:
            if robot_id < 8:
                self.robots_sender_low(data)
            else:
                self.robots_sender_high(data)
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
