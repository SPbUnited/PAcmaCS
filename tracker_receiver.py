import zmq
from typing import Any, Dict

context = zmq.Context()
s_tracker = context.socket(zmq.SUB)
s_tracker.connect("tcp://localhost:4243")
s_tracker.setsockopt_string(zmq.SUBSCRIBE, "")

print("Tracker receiver init")

last_frame_number = 0

while True:
    print(".")
    data = s_tracker.recv_json()
    print(data["tracked_frame"]["frame_number"])
    print(data["tracked_frame"]["frame_number"] - last_frame_number)
    print(data["tracked_frame"]["balls"][0])

    last_frame_number = data["tracked_frame"]["frame_number"]
