import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect("ipc:///tmp/serviz.sock")

x = 0

while True:

    data = {"zmq_feed": {"data":[
        {"type": "robot_yel", "x": x, "y": 100, "rotation": 0},
    ], "is_visible": True},
    }

    socket.send_json(data)

    x += 10
    x %= 1000

    time.sleep(0.01)
