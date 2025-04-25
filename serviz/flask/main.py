import time
from flask import Flask, render_template
from flask_socketio import SocketIO

import threading

from blue_green_storage import BGStore

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

sprite_store = BGStore()
telemetry_store = BGStore()
visibility = {}

context = zmq.Context()
s_signals = context.socket(zmq.PUB)
s_signals.connect(config["ether"]["s_signals_sub_url"])


def update_layer(layer_name, data):
    if layer_name not in visibility:
        visibility[layer_name] = data["is_visible"]
    else:
        data["is_visible"] = visibility[layer_name]
    sprite_store.write({layer_name: data})


def update_telemetry_data(data):
    telemetry_store.write(data)


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
    pass


@sio.on("send_signal")
def send_signal(data):
    s_signals.send_json(data)


@sio.on("clear_layers")
def clear_layers(data):
    visibility.clear()
    sprite_store.clear()


@sio.on("clear_telemetry")
def clear_telemetry(data):
    telemetry_store.clear()


@sio.on("toggle_layer_visibility")
def toggle_layer_visibility(key):
    visibility[key] = not visibility[key]


def update_sprites():
    print("Update sprites enter")

    context = zmq.Context()
    s_draw = context.socket(zmq.SUB)
    s_draw.connect(config["ether"]["s_draw_pub_url"])
    s_draw.setsockopt_string(zmq.SUBSCRIBE, "")

    print("Draw socket setup as SUB at ", config["ether"]["s_draw_pub_url"])

    while True:
        sio.sleep(0.01)

        for _ in range(100):
            try:
                message = s_draw.recv_json(flags=zmq.NOBLOCK)
                for key, value in message.items():
                    update_layer(key, value)
                    pass
            except zmq.ZMQError as e:
                if e.errno == zmq.EAGAIN:
                    break
                else:
                    raise

        sprite_store.switch()


def update_telemetry():
    print("Update telemetry enter")

    context = zmq.Context()

    s_telemetry = context.socket(zmq.SUB)
    s_telemetry.connect(config["ether"]["s_telemetry_pub_url"])
    s_telemetry.setsockopt_string(zmq.SUBSCRIBE, "")

    print("Telemetry socket setup as SUB at ", config["ether"]["s_telemetry_pub_url"])

    while True:
        sio.sleep(0.01)

        for _ in range(100):
            try:
                message = s_telemetry.recv_json(flags=zmq.NOBLOCK)
                update_telemetry_data(message)
            except zmq.ZMQError as e:
                if e.errno == zmq.EAGAIN:
                    break
                else:
                    raise

        telemetry_store.switch()


def emit_data(sio):

    print("Data emitter enter")

    while True:
        sio.sleep(0.01)

        sio.emit("update_sprites", sprite_store.fetch())
        sio.emit("update_telemetry", telemetry_store.fetch())


# Run the app
if __name__ == "__main__":
    sio.sleep(1)
    print("Starting server")
    # threading.Thread(target=update_sprites).start()

    # import os
    # if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    sio.start_background_task(
        target=lambda: update_sprites()  # manager, sprite_data, sprite_lock)
    )
    sio.start_background_task(
        target=lambda: update_telemetry()  # manager, telemetry_data, telemetry_lock)
    )
    sio.start_background_task(target=lambda: emit_data(sio))
    sio.run(
        app, host="0.0.0.0", port=8000, debug=False, allow_unsafe_werkzeug=True
    )  # , host='localhost', port=8000, debug=True)
