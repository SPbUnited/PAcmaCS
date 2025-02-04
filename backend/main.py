from flask import Flask
from flask_socketio import SocketIO

import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app, cors_allowed_origins="*")

sprite_data = {"test_vision": {"data":[
    {"type": "robot_yel", "x": -1000, "y": 100, "rotation": 0},
    {"type": "robot_blu", "x": 1400, "y": 100, "rotation": 3.14},
    {"type": "robot_blu", "x": -1400, "y": -100, "rotation": 0},
    {"type": "ball", "x": 200, "y": 400}
],  "is_visible": True},
"test_vision2": {"data":[
    {"type": "robot_yel", "x": -300, "y": -900, "rotation": 0},
],  "is_visible": True}
}

@app.route('/')
def index():
    return "Hello World!"

# SocketIO events
@sio.on('connect')
def connect():
    print(f"Client connected")

@sio.on('disconnect')
def disconnect():
    print(f"Client disconnected")

@sio.on('updated_ui_state')
def update_ui_state(data):
    pass
    # print(data)

@sio.on('test_signal')
def test_signal(data):
    print("Test signal")
    sprite_data["test_vision"]["data"][1]["x"] *= -1

@sio.on('toggle_layer_visibility')
def toggle_layer_visibility(data):
    print(data)
    sprite_data[data]["is_visible"] = not sprite_data[data]["is_visible"]

def update_sprites():
    import time
    print("Update sprites enter")
    angle = 0
    while True:
        sio.sleep(0.02)
        # print("Update sprites")
        data = sprite_data
        data["test_vision"]["data"][0]["rotation"] = angle
        sio.emit("update_sprites", data)

        angle += 0.1

# Run the app
if __name__ == "__main__":
    sio.sleep(1)
    print("Starting server")
    # threading.Thread(target=update_sprites).start()
    sio.start_background_task(target=lambda: update_sprites())
    sio.run(app, host='0.0.0.0', port=8000, debug=True, allow_unsafe_werkzeug=True)#, host='localhost', port=8000, debug=True)
