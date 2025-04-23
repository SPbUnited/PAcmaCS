from flask import Flask, render_template
from flask_socketio import SocketIO

import threading
from multiprocessing import Manager

from argparse import ArgumentParser
import yaml

parser = ArgumentParser()
parser.add_argument("--config", default="config.yml")
args = parser.parse_args()

config = yaml.safe_load(open(args.config))

if config["ether"]["api_version"] != 3:
    raise Exception("Only Ether v3 is supported")

app = Flask(
    __name__,
    template_folder="static",
)
app.config["SECRET_KEY"] = "secret!"
sio = SocketIO(app, cors_allowed_origins="*")

version = "version unknown"
import os

if os.environ.get("VERSION"):
    version = "v" + os.environ.get("VERSION").replace('"', "")

currentDivision = "divB"
if os.environ.get("DIV"):
    currentDivision = os.environ.get("DIV")

import zmq
import copy

manager = Manager()
# Shared sprite data
sprite_data = manager.dict({})
sprite_lock = manager.Lock()

telemetry_data = manager.dict({})
telemetry_lock = manager.Lock()

context = zmq.Context()
s_signals = context.socket(zmq.PUB)
s_signals.connect(config["ether"]["s_signals_sub_url"])


def update_layer(layer_name, data):
    with sprite_lock:
        if layer_name not in sprite_data:
            sprite_data[layer_name] = manager.dict(data)
        else:
            sprite_data[layer_name]["data"] = data["data"]


def update_telemetry_data(data):
    with telemetry_lock:
        for key in data:
            telemetry_data[key] = data[key]


@app.route("/")
def index():
    return render_template("index.html")


# SocketIO events
@sio.on("connect")
def connect():
    print(f"Client connected")
    sio.emit("update_division", currentDivision)
    sio.emit("update_version", version)


@sio.on("disconnect")
def disconnect():
    print(f"Client disconnected")


@sio.on("updated_ui_state")
def update_ui_state(data):
    # print(data)
    pass


@sio.on("send_signal")
def send_signal(data):
    # print("Send signal")
    s_signals.send_json(data)


@sio.on("clear_layers")
def clear_layers(data):
    with sprite_lock:
        sprite_data.clear()


@sio.on("clear_telemetry")
def clear_telemetry(data):
    with telemetry_lock:
        telemetry_data.clear()


@sio.on("toggle_layer_visibility")
def toggle_layer_visibility(data):
    # print(data)
    with sprite_lock:
        sprite_data[data]["is_visible"] = not sprite_data[data]["is_visible"]


def update_sprites(manager, sprite_data, state_lock):
    print("Update sprites enter")

    context = zmq.Context()
    s_draw = context.socket(zmq.SUB)
    s_draw.connect(config["ether"]["s_draw_pub_url"])
    s_draw.setsockopt_string(zmq.SUBSCRIBE, "")

    print("Draw socket setup as SUB at ", config["ether"]["s_draw_pub_url"])

    while True:
        sio.sleep(0.01)
        for _ in range(100):
            print("|", end="")
            try:
                message = s_draw.recv_json(flags=zmq.NOBLOCK)
                for key, value in message.items():
                    update_layer(key, value)
                    print(":", end="")
            except zmq.ZMQError as e:
                if e.errno == zmq.EAGAIN:
                    print("!!!!!", end="")
                    break
                else:
                    raise

        print("\\//\\")


def update_telemetry(manager, telemetry_data, telemetry_lock):
    print("Update telemetry enter")

    context = zmq.Context()

    s_telemetry = context.socket(zmq.SUB)
    s_telemetry.connect(config["ether"]["s_telemetry_pub_url"])
    s_telemetry.setsockopt_string(zmq.SUBSCRIBE, "")

    print("Telemetry socket setup as SUB at ", config["ether"]["s_telemetry_pub_url"])

    while True:
        sio.sleep(0.01)
        for _ in range(100):
            # print("~", end="")
            try:
                message = s_telemetry.recv_json(flags=zmq.NOBLOCK)
                update_telemetry_data(message)
                # print("=", end="")
            except zmq.ZMQError as e:
                if e.errno == zmq.EAGAIN:
                    break
                else:
                    raise

        # print("/\\\\/")


def emit_data(sio):
    while True:
        sio.sleep(0.01)
        with sprite_lock:
            sio.emit("update_sprites", copy.deepcopy(sprite_data.copy()))
        with telemetry_lock:
            sio.emit("update_telemetry", copy.deepcopy(telemetry_data.copy()))


# Run the app
if __name__ == "__main__":
    sio.sleep(1)
    print("Starting server")
    # threading.Thread(target=update_sprites).start()

    # import os
    # if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    sio.start_background_task(
        target=lambda: update_sprites(manager, sprite_data, sprite_lock)
    )
    sio.start_background_task(
        target=lambda: update_telemetry(manager, telemetry_data, telemetry_lock)
    )
    sio.start_background_task(target=lambda: emit_data(sio))
    sio.run(
        app, host="0.0.0.0", port=8000, debug=False, allow_unsafe_werkzeug=True
    )  # , host='localhost', port=8000, debug=True)
