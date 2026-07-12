import argparse
import json
import socket
import time

from decoder.robot_control_proto import control_pb2
from google.protobuf import message
from google.protobuf.json_format import MessageToJson


def build_telemetry_payload(
    robot_id: int, now: float, seq: int, get_timestamp: float | None
) -> dict:
    return {
        "robot_id": robot_id,
        "timestamp": now,
        "seq": seq,
        "get_timestamp": get_timestamp,
        "voltage": 24.0,
        "ball_sensor": False,
        "status": "ok",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Emulate an FB4 robot over UDP")
    parser.add_argument("--robot-id", type=int, required=True)
    parser.add_argument("--bind-host", default="0.0.0.0")
    parser.add_argument("--cmd-port", type=int, default=5555)
    parser.add_argument("--tel-port", type=int, default=5556)
    parser.add_argument("--rate", type=float, default=50.0)
    args = parser.parse_args()

    if not 0 <= args.robot_id <= 15:
        parser.error("--robot-id must be in range 0-15")
    if args.rate <= 0:
        parser.error("--rate must be greater than zero")

    command_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    command_socket.bind((args.bind_host, args.cmd_port))
    command_socket.setblocking(False)

    telemetry_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    telemetry_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    get_timestamp = None
    seq = 0
    interval = 1.0 / args.rate
    next_telemetry = time.monotonic()
    try:
        while True:
            while True:
                try:
                    data, addr = command_socket.recvfrom(4096)
                except BlockingIOError:
                    break
                except OSError as error:
                    print("Command receive error:", error)
                    break

                try:
                    command = control_pb2.NewFormat()
                    command.ParseFromString(data)
                    get_timestamp = time.time()
                    print(f"Command from {addr[0]}:{addr[1]}:")
                    print(MessageToJson(command))
                except message.DecodeError as error:
                    print("Command parse error:", error)

            monotonic_now = time.monotonic()
            if monotonic_now >= next_telemetry:
                payload = build_telemetry_payload(
                    args.robot_id, time.time(), seq, get_timestamp
                )
                try:
                    telemetry_socket.sendto(
                        json.dumps(payload).encode(),
                        ("<broadcast>", args.tel_port),
                    )
                except (TypeError, ValueError, OSError) as error:
                    print("Telemetry send error:", error)
                seq += 1
                next_telemetry = monotonic_now + interval

            time.sleep(min(0.005, interval / 2))
    except KeyboardInterrupt:
        print("Robot emulator stopped")
    finally:
        command_socket.close()
        telemetry_socket.close()


if __name__ == "__main__":
    main()
