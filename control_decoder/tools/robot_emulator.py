import argparse
import json
import time

import zmq


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


def decode_command(payload: bytes) -> dict | None:
    try:
        command = json.loads(payload)
    except (json.JSONDecodeError, TypeError, UnicodeDecodeError):
        return None
    return command if isinstance(command, dict) else None


def main() -> None:
    parser = argparse.ArgumentParser(description="Emulate an FB4 robot over ZMQ")
    parser.add_argument("--robot-id", type=int, required=True)
    parser.add_argument("--bind-host", default="*")
    parser.add_argument("--cmd-port", type=int, default=5555)
    parser.add_argument("--tel-port", type=int, default=5556)
    parser.add_argument("--rate", type=float, default=50.0)
    args = parser.parse_args()

    if not 0 <= args.robot_id <= 15:
        parser.error("--robot-id must be in range 0-15")
    if args.rate <= 0:
        parser.error("--rate must be greater than zero")

    context = zmq.Context()
    command_socket = context.socket(zmq.SUB)
    command_socket.setsockopt(zmq.RCVHWM, 3)
    command_socket.setsockopt(zmq.LINGER, 0)
    command_socket.setsockopt_string(zmq.SUBSCRIBE, "cmd/all")
    command_socket.setsockopt_string(zmq.SUBSCRIBE, f"cmd/{args.robot_id}")
    command_socket.bind(f"tcp://{args.bind_host}:{args.cmd_port}")

    telemetry_socket = context.socket(zmq.PUB)
    telemetry_socket.setsockopt(zmq.SNDHWM, 50)
    telemetry_socket.setsockopt(zmq.LINGER, 0)
    telemetry_socket.bind(f"tcp://{args.bind_host}:{args.tel_port}")

    get_timestamp = None
    seq = 0
    interval = 1.0 / args.rate
    next_telemetry = time.monotonic()
    try:
        while True:
            while True:
                try:
                    frames = command_socket.recv_multipart(flags=zmq.NOBLOCK)
                except zmq.Again:
                    break
                except zmq.ZMQError as error:
                    print("Command receive error:", error)
                    break

                try:
                    if len(frames) != 2:
                        raise ValueError(f"expected 2 frames, got {len(frames)}")
                    topic = frames[0].decode("utf-8")
                    print("Command topic:", topic)
                    command = decode_command(frames[1])
                    if command is None:
                        raise ValueError("invalid command JSON")
                    get_timestamp = command.get("timestamp")
                    print(json.dumps(command, indent=2, sort_keys=True))
                except (UnicodeDecodeError, ValueError) as error:
                    print("Command parse error:", error)

            monotonic_now = time.monotonic()
            if monotonic_now >= next_telemetry:
                payload = build_telemetry_payload(
                    args.robot_id, time.time(), seq, get_timestamp
                )
                try:
                    telemetry_socket.send_multipart(
                        [
                            f"tel/{args.robot_id}".encode(),
                            json.dumps(payload).encode(),
                        ],
                        flags=zmq.NOBLOCK,
                    )
                except (TypeError, ValueError, zmq.ZMQError) as error:
                    print("Telemetry send error:", error)
                seq += 1
                next_telemetry = monotonic_now + interval

            time.sleep(min(0.005, interval / 2))
    except KeyboardInterrupt:
        print("Robot emulator stopped")
    finally:
        command_socket.close()
        telemetry_socket.close()
        context.term()


if __name__ == "__main__":
    main()
