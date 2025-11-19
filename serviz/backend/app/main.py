from multiprocessing import Lock
import time
from typing import Optional
from flask import Flask, render_template
from flask_socketio import SocketIO

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


import zmq

sprite_store = BGStore()
telemetry_store = BGStore()
visibility = {}

feed_lock = Lock()
last_feed_update = time.time()

geometry_lock = Lock()
geometry_data: Optional[dict] = None
geometry_data_updated: bool = True

context = zmq.Context()
s_signals = context.socket(zmq.PUB)
s_signals.connect(config["ether"]["s_signals_sub_url"])


def update_layer(layer_name: str, data):
    if layer_name not in visibility:
        visibility[layer_name] = data["is_visible"]
    else:
        data["is_visible"] = visibility[layer_name]
    sprite_store.write({layer_name: data})
    if layer_name == "vision_feed":
        with feed_lock:
            global last_feed_update
            last_feed_update = time.time()

def update_telemetry_data(data):
    telemetry_store.write(data)

def update_geometry_data(data):
    with geometry_lock:
        global geometry_data, geometry_data_updated
        if geometry_data != data:
            geometry_data = data
            geometry_data_updated = True


@app.route("/")
def index():
    return render_template("index.html")


# SocketIO events
@sio.on("connect")
def connect():
    print(f"Client connected")
    if geometry_data is not None:
        sio.emit("update_geometry", geometry_data)
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

def update_geometry():
    print("Update geometry enter")

    context = zmq.Context()

    s_geometry = context.socket(zmq.SUB)
    s_geometry.connect(config["ether"]["s_geometry_pub_url"])
    s_geometry.setsockopt_string(zmq.SUBSCRIBE, "")

    print("Geometry socket setup as SUB at ", config["ether"]["s_geometry_pub_url"])

    while True:
        sio.sleep(0.01)

        for _ in range(100):
            try:
                message = s_geometry.recv_json(flags=zmq.NOBLOCK)
                update_geometry_data(message)
            except zmq.ZMQError as e:
                if e.errno == zmq.EAGAIN:
                    break
                else:
                    raise


def relay_data(sio: SocketIO):
    print("Data relay enter")

    context = zmq.Context()

    s_signals = context.socket(zmq.SUB)
    s_signals.connect(config["ether"]["s_signals_pub_url"])
    s_signals.setsockopt_string(zmq.SUBSCRIBE, '{"serviz":')
    s_signals.setsockopt_string(zmq.SUBSCRIBE, "{'serviz':")

    while True:
        sio.sleep(0.01)

        for _ in range(100):
            try:
                message = s_signals.recv_json(flags=zmq.NOBLOCK)
                # print("Signal received: ", message)
                sio.emit(message["serviz"], message["data"])
            except zmq.ZMQError as e:
                if e.errno == zmq.EAGAIN:
                    break
                else:
                    raise
        
        global last_feed_update
        sprites_data = sprite_store.fetch()
        for layer_name in visibility:
            sprites_data[layer_name]["is_visible"] = visibility[layer_name]
            
        sprites_data["_time_from_update"] = time.time() - last_feed_update
        sio.emit("update_sprites", sprites_data)

        sio.emit("update_telemetry", telemetry_store.fetch())
        
        global geometry_data_updated, geometry_data
        if geometry_data_updated:
            sio.emit("update_geometry", geometry_data)
            geometry_data_updated = False


# Run the app
if __name__ == "__main__":
    sio.sleep(1)
    print("Starting server")
    
    sio.start_background_task(
        target=lambda: update_sprites()
    )
    sio.start_background_task(
        target=lambda: update_telemetry()
    )
    sio.start_background_task(
        target=lambda: update_geometry()
    )
    sio.start_background_task(target=lambda: relay_data(sio))
    sio.run(
        app, host="0.0.0.0", port=8100, debug=False, allow_unsafe_werkzeug=True
    )
