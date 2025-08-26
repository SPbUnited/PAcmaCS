import threading
from attrs import define, field
import zmq
import time
import json

from game_controller import game_controller_relay as gcr
from common.tracker_client import TrackerClient
from common.tracker_model import Team
from grsim.client import GrSimClient

from argparse import ArgumentParser
import yaml

import pprint

parser = ArgumentParser()
parser.add_argument("--config", default="config.yml")
args = parser.parse_args()

config = yaml.safe_load(open(args.config))

if config["ether"]["api_version"] != 3:
    raise Exception("Only Ether v3 is supported")

context = zmq.Context()

s_draw = context.socket(zmq.PUB)
s_draw.connect(config["ether"]["s_draw_sub_url"])


s_signals = context.socket(zmq.SUB)
s_signals.connect(config["ether"]["s_signals_pub_url"])
s_signals.setsockopt_string(zmq.SUBSCRIBE, '{"transnet":')
s_signals.setsockopt_string(zmq.SUBSCRIBE, "{'transnet':")

poller = zmq.Poller()
poller.register(s_signals, zmq.POLLIN)


def setup_draw_proxy(context: zmq.Context):
    print("DRAW proxy SETUP")

    # DRAW proxy
    s_proxy_draw_pub = context.socket(zmq.XPUB)
    s_proxy_draw_pub.bind(config["ether"]["s_draw_pub_url"])

    s_proxy_draw_sub = context.socket(zmq.XSUB)
    s_proxy_draw_sub.bind(config["ether"]["s_draw_sub_url"])
    zmq.proxy(s_proxy_draw_pub, s_proxy_draw_sub)


def setup_telemetry_proxy(context: zmq.Context):
    print("TELEMETRY proxy SETUP")

    # TELEMETRY proxy
    s_proxy_telemetry_pub = context.socket(zmq.XPUB)
    s_proxy_telemetry_pub.bind(config["ether"]["s_telemetry_pub_url"])

    s_proxy_telemetry_sub = context.socket(zmq.XSUB)
    s_proxy_telemetry_sub.bind(config["ether"]["s_telemetry_sub_url"])
    zmq.proxy(s_proxy_telemetry_pub, s_proxy_telemetry_sub)

def setup_geometry_proxy(context: zmq.Context):
    print("GEOMETRY proxy SETUP")

    # GEOMETRY proxy
    s_proxy_geometry_pub = context.socket(zmq.XPUB)
    s_proxy_geometry_pub.bind(config["ether"]["s_geometry_pub_url"])

    s_proxy_geometry_sub = context.socket(zmq.XSUB)
    s_proxy_geometry_sub.bind(config["ether"]["s_geometry_sub_url"])
    zmq.proxy(s_proxy_geometry_pub, s_proxy_geometry_sub)


def setup_signals_proxy(context: zmq.Context):
    print("SIGNALS proxy SETUP")

    # SIGNALS proxy
    s_proxy_signals_pub = context.socket(zmq.XPUB)
    s_proxy_signals_pub.bind(config["ether"]["s_signals_pub_url"])

    s_proxy_signals_sub = context.socket(zmq.XSUB)
    s_proxy_signals_sub.bind(config["ether"]["s_signals_sub_url"])
    zmq.proxy(s_proxy_signals_pub, s_proxy_signals_sub)


def setup_proxy(context: zmq.Context):
    print("Setting up proxy")
    draw_proxy = threading.Thread(target=setup_draw_proxy, args=(context,))
    telemetry_proxy = threading.Thread(target=setup_telemetry_proxy, args=(context,))
    geometry_proxy = threading.Thread(target=setup_geometry_proxy, args=(context,))
    signals_proxy = threading.Thread(target=setup_signals_proxy, args=(context,))
    draw_proxy.start()
    telemetry_proxy.start()
    geometry_proxy.start()
    signals_proxy.start()
    print("Proxy UP")


from common.vision_model import Team
from viscont import Viscont as vc


@define
class zmqVisionRelayTemplate:
    context: zmq.Context = field(init=False)
    relay: zmq.Socket = field(init=False)

    def __attrs_post_init__(self):
        self.context = zmq.Context()
        self.relay = self.context.socket(zmq.PUB)
        self.relay.bind(config["transnet"]["s_vision_fan_url"])
        print("Vision relay init")

    def send(self, raw_frame):
        self.relay.send(raw_frame)


@define
class zmqTrackerRelayTemplate:
    context: zmq.Context = field(init=False)
    relay: zmq.Socket = field(init=False)

    def __attrs_post_init__(self):
        self.context = zmq.Context()
        self.relay = self.context.socket(zmq.PUB)
        self.relay.bind(config["transnet"]["s_tracker_fan_url"])
        print("Tracker relay init on ", config["transnet"]["s_tracker_fan_url"])
        self.relay.send_json({"Tracker relay init": True})

    def send(self, processed_frame):
        self.relay.send_json(processed_frame)
        # self.relay.send_json({"Updated": True})
        pass


from common.tracker_model import (
    TrackerWrapperPacket as TrackerWrapperPacketModel,
)


def convert_trackers_to_serviz(trackers: TrackerWrapperPacketModel):
    layer_name = trackers.source_name + "_tracker_feed"
    data = {
        layer_name: {
            "data": [],
            "is_visible": True,
        }
    }

    for ball in trackers.tracked_frame.balls:
        data[layer_name]["data"].append(
            {
                "type": "ball",
                "x": ball.pos.x * 1000,
                "y": ball.pos.y * 1000,
                "vx": ball.vel.x * 1000,
                "vy": ball.vel.y * 1000,
            }
        )

    for robot in trackers.tracked_frame.robots:
        sprite_type = "ball"
        # WARN: This is a hack due to proto enum field swap in new ssl packets
        if robot.robot_id.team.value == Team.BLUE.value:
            sprite_type = "robot_yel"
        elif robot.robot_id.team.value == Team.YELLOW.value:
            sprite_type = "robot_blu"
        data[layer_name]["data"].append(
            {
                "type": sprite_type,
                "robot_id": robot.robot_id.id,
                "x": robot.pos.x * 1000,
                "y": robot.pos.y * 1000,
                "vx": robot.vel.x * 1000,
                "vy": robot.vel.y * 1000,
                "rotation": robot.orientation,
            }
        )
    return data

def format_message(data: dict) -> str:
    lines = []
    for _, layer in data.items():
        for obj in layer["data"]:
            if obj["type"] == "ball":
                lines.append(
                    f"BALL: x={round(obj['x'])}, y={round(obj['y'])}, "
                    + (f"vx={round(obj['vx'])}, vy={round(obj['vy'])}" if "vx" in obj else "")
                )
            elif obj["type"] in ("robot_blu", "robot_yel"):
                    line = (
                        f"{obj['type'].upper():<10} {obj['robot_id']:>2} | "
                        f"x={obj['x']:>5.0f}  y={obj['y']:>5.0f}  "
                    )
                    if "vx" in obj and "vy" in obj:
                        line += f"vx={obj['vx']:>5.0f}  vy={obj['vy']:>5.0f}  "
                    line += f"rot={obj['rotation']:>5.2f}"
                    lines.append(line)

            else:
                lines.append(str(obj))
    return "\n".join(lines)



if __name__ == "__main__":

    print("Enter Transnet")

    client = GrSimClient(zmq_relay_template=zmqVisionRelayTemplate)
    tracker_client = TrackerClient(zmq_relay_template=zmqTrackerRelayTemplate)

    vision = vc.SSLVision(client=client)
    simControl = vc.SimControl(client=client)
    robotControl = vc.RobotControl(client=vc.GrSimRobotControl(client=client))

    setup_proxy(context)

    game_controller_relay = gcr.GameControllerRelay(
        game_controller_fan_url=config["transnet"]["s_game_controller_fan_url"],
    )

    time.sleep(2)

    tracker_client.init()
    game_controller_relay.init()

    s_telemetry = context.socket(zmq.PUB)
    s_telemetry.connect(config["ether"]["s_telemetry_sub_url"])

    s_geometry = context.socket(zmq.PUB)
    s_geometry.connect(config["ether"]["s_geometry_sub_url"])

    print("Transnet ready")
    while True:

        # Process vision
        vision.update_vision()
        field_info = vision.get_field_info()
        data = {"vision_feed": {"data": field_info, "is_visible": True}}
        s_draw.send_json(data)

        field_geometry = client.get_detection().geometry
        if field_geometry is not None:
            s_geometry.send_json(field_geometry.__dict__)

        s_telemetry.send_json({list(data.keys())[0]: format_message(data)})

        trackers = tracker_client.get_detections()
        for tracker_key in trackers:
            data = convert_trackers_to_serviz(trackers[tracker_key])
            s_draw.send_json(data)

            data_str = format_message(data)
            s_telemetry.send_json({list(data.keys())[0]: data_str})


        for i in range(100):
            # Process incoming signals
            try:
                socks = dict(poller.poll(timeout=0))
            except KeyboardInterrupt:
                break

            if socks == {}:
                break

            if s_signals in socks:
                signal = s_signals.recv_json()
                # print(signal)
                is_signal_valid = False
                is_signal_valid |= simControl.signal_handler(signal)
                is_signal_valid |= robotControl.signal_handler(signal)

                if not is_signal_valid:
                    print("Invalid signal: ", signal)

        time.sleep(0.001)
