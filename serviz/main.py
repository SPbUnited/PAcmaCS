from flask import Flask, render_template
from flask_socketio import SocketIO

import threading
from multiprocessing import Manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app, cors_allowed_origins="*")

version = 'version unknown'
import os
if os.environ.get('VERSION'):
    version = "v" + os.environ.get('VERSION').replace('"', '')

import zmq
import copy

manager = Manager()
# Shared sprite data
sprite_data = manager.dict({
"test_vision": manager.dict({"data":[
    {"type": "robot_yel", "robot_id": 0, "x": 100, "y": 100, "rotation": 0},
    {"type": "robot_blu", "robot_id": 0, "x": 1400, "y": 100, "rotation": 3.14},
    {"type": "robot_blu", "robot_id": 3, "x": -1400, "y": -100, "rotation": 0},
    {"type": "ball", "x": 200, "y": 400}
],  "is_visible": True}),
"test_vision2": manager.dict({"data":[
    {"type": "robot_yel", "robot_id": 5, "x": -300, "y": -900, "rotation": 0},
],  "is_visible": True}),
# "zmq_feed": {"data":[
#     {"type": "robot_yel", "x": 100, "y": 100, "rotation": 0},
# ], "is_visible": True},
})
state_lock = manager.Lock()

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("ipc:///tmp/serviz.pub.sock")

def update_layer(layer_name, data):
    with state_lock:
        if layer_name not in sprite_data:
            sprite_data[layer_name] = manager.dict(data)
        else:
            sprite_data[layer_name]["data"] = data["data"]

@app.route('/')
def index():
    return render_template('index.html', VERSION=version)

# SocketIO events
@sio.on('connect')
def connect():
    print(f"Client connected")

@sio.on('disconnect')
def disconnect():
    print(f"Client disconnected")

@sio.on('updated_ui_state')
def update_ui_state(data):
    # print(data)
    pass

@sio.on('test_signal')
def test_signal(data):
    print("Test signal")
    socket.send_string("test_signal")
    with state_lock:
        buf = sprite_data["test_vision"]["data"].copy()
        buf[1]['x'] *= -1
        sprite_data["test_vision"]["data"] = buf

@sio.on('toggle_layer_visibility')
def toggle_layer_visibility(data):
    # print(data)
    with state_lock:
        sprite_data[data]["is_visible"] = not sprite_data[data]["is_visible"]


def update_sprites(sio, manager, sprite_data, state_lock):
    print("Update sprites enter")
    angle = 0

    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("ipc:///tmp/serviz.sock")

    while True:
        sio.sleep(0.02)
        for _ in range(100):
            try:
                message = socket.recv_json(flags=zmq.NOBLOCK)
                # print("Received:", message)
                # Update sprite_data with new_data
                for key, value in message.items():
                    update_layer(key, value)
            except zmq.ZMQError as e:
                if e.errno == zmq.EAGAIN:
                    # print("No messages available.")
                    break
                else:
                    raise

        data = sprite_data
        data["test_vision"]["data"][0]["rotation"] = angle
        # print(sprite_data)
        sio.emit("update_sprites", copy.deepcopy(data.copy()))

        angle += 0.1

# Run the app
if __name__ == "__main__":
    sio.sleep(1)
    print("Starting server")
    # threading.Thread(target=update_sprites).start()

    # import os
    # if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    sio.start_background_task(target=lambda: update_sprites(sio, manager, sprite_data, state_lock))
    sio.run(app, host='0.0.0.0', port=8000, debug=False, allow_unsafe_werkzeug=True)#, host='localhost', port=8000, debug=True)
