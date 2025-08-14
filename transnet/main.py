from enum import Enum
import threading
from typing import Dict
from attrs import define, field
import zmq
from thread_proxy_switch import ThreadProxySwitch
import time

from game_controller import game_controller_relay as gcr
from common.tracker_client import TrackerClient
from common.tracker_model import Team
from grsim.client import GrSimClient
from ether.signal_bus import SignalBus

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

s_signals_ctrl = context.socket(zmq.REQ)
s_draw_ctrl = context.socket(zmq.REQ)
s_telemetry_ctrl = context.socket(zmq.REQ)


class PhantomCtrl(Enum):
    ETHER = 0
    PHANTOM = 1


def steer_send_cmd(sock: zmq.Socket, cmd: str):
    sock.send(cmd.encode())
    return sock.recv()


def ether_switch_handler(mode: PhantomCtrl):
    # steer_send_cmd(s_signals_ctrl, mode.name)
    steer_send_cmd(s_telemetry_ctrl, mode.name)
    steer_send_cmd(s_draw_ctrl, mode.name)


def setup_proxy(context: zmq.Context, signal_bus: SignalBus = None):

    s_signals_ctrl.bind(config["transnet"]["s_signals_ctrl_url"])
    s_draw_ctrl.bind(config["transnet"]["s_draw_ctrl_url"])
    s_telemetry_ctrl.bind(config["transnet"]["s_telemetry_ctrl_url"])

    print("Setting up proxy")

    signals_proxy = ThreadProxySwitch(
        zmq.XSUB, zmq.XSUB, zmq.XPUB, zmq.XPUB, ctrl_type=zmq.REP
    )
    signals_proxy.bind_real(config["ether"]["s_signals_sub_url"])
    signals_proxy.bind_phantom(
        config["ether"]["s_signals_sub_url"] + config["ether"]["phantom_suffix"]
    )
    signals_proxy.bind_out(config["ether"]["s_signals_pub_url"])
    signals_proxy.bind_monitor(
        config["ether"]["s_signals_pub_url"] + config["ether"]["monitor_suffix"]
    )
    signals_proxy.connect_ctrl(config["transnet"]["s_signals_ctrl_url"])

    signals_proxy.start()

    print("Signal proxy UP")

    telemetry_proxy = ThreadProxySwitch(
        zmq.XSUB, zmq.XSUB, zmq.XPUB, zmq.XPUB, ctrl_type=zmq.REP
    )
    telemetry_proxy.bind_real(config["ether"]["s_telemetry_sub_url"])
    telemetry_proxy.bind_phantom(
        config["ether"]["s_telemetry_sub_url"] + config["ether"]["phantom_suffix"]
    )
    telemetry_proxy.bind_out(config["ether"]["s_telemetry_pub_url"])
    telemetry_proxy.bind_monitor(
        config["ether"]["s_telemetry_pub_url"] + config["ether"]["monitor_suffix"]
    )
    telemetry_proxy.connect_ctrl(config["transnet"]["s_telemetry_ctrl_url"])
    telemetry_proxy.start()

    print("Telemetry proxy UP")

    draw_proxy = ThreadProxySwitch(
        zmq.XSUB, zmq.XSUB, zmq.XPUB, zmq.XPUB, ctrl_type=zmq.REP
    )
    draw_proxy.bind_real(config["ether"]["s_draw_sub_url"])
    draw_proxy.bind_phantom(
        config["ether"]["s_draw_sub_url"] + config["ether"]["phantom_suffix"]
    )
    draw_proxy.bind_out(config["ether"]["s_draw_pub_url"])
    draw_proxy.bind_monitor(
        config["ether"]["s_draw_pub_url"] + config["ether"]["monitor_suffix"]
    )
    draw_proxy.connect_ctrl(config["transnet"]["s_draw_ctrl_url"])
    draw_proxy.start()

    print("Draw proxy UP")

    ether_switch_handler(PhantomCtrl.ETHER)

    # signal_bus.on("ether_disable",
    #     lambda signal: s_ether_ctrl.send("PAUSE")
    # )
    # signal_bus.on("ether_enable",
    #     lambda signal: s_ether_ctrl.send("RESUME")
    # )

    print("Proxy UP")


def proxy_ctrl_handler(signal: Dict):
    signal_type = signal["transnet"]
    print(signal)

    if signal_type == "ether_select":
        print("Ether select")
        ether_switch_handler(PhantomCtrl.ETHER)
        return True
    elif signal_type == "phantom_select":
        print("Phantom select")
        ether_switch_handler(PhantomCtrl.PHANTOM)
        return True
    # if signal_type == "ether_enable":
    #     print("Ether enable")
    #     s_ether_ctrl.send("RESUME".encode())
    #     print(s_ether_ctrl.recv_multipart())
    #     s_ether_ctrl.send("RESUME".encode())
    #     print(s_ether_ctrl.recv_multipart())
    #     return True
    # elif signal_type == "ether_disable":
    #     print("Ether disable")
    #     s_ether_ctrl.send("PAUSE".encode())
    #     print(s_ether_ctrl.recv())
    #     s_ether_ctrl.send("PAUSE".encode())
    #     print(s_ether_ctrl.recv())
    #     return True
    # elif signal_type == "ether_terminate":
    #     print("Ether disable")
    #     s_ether_ctrl.send("TERMINATE".encode())
    #     print(s_ether_ctrl.recv())
    #     return True
    # elif signal_type == "ether_stats":
    #     print("Ether stats")
    #     s_ether_ctrl.send("STATISTICS".encode())
    #     print(s_ether_ctrl.recv_multipart())
    #     return True

    return False


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


if __name__ == "__main__":

    print("Enter Transnet")

    client = GrSimClient(zmq_relay_template=zmqVisionRelayTemplate)
    tracker_client = TrackerClient(zmq_relay_template=zmqTrackerRelayTemplate)

    vision = vc.SSLVision(client=client)
    simControl = vc.SimControl(client=client)
    robotControl = vc.RobotControl(client=vc.GrSimRobotControl(client=client))

    # signal_bus = SignalBus("transnet", config["ether"]["s_signals_pub_url"])

    setup_proxy(context)  # , signal_bus)

    game_controller_relay = gcr.GameControllerRelay(
        game_controller_fan_url=config["transnet"]["s_game_controller_fan_url"],
    )

    time.sleep(2)

    tracker_client.init()
    game_controller_relay.init()

    s_telemetry = context.socket(zmq.PUB)
    s_telemetry.connect(config["ether"]["s_telemetry_sub_url"])

    print("Transnet ready")
    while True:

        # Process vision
        vision.update_vision()
        field_info = vision.get_field_info()
        data = {"vision_feed": {"data": field_info, "is_visible": True}}
        s_draw.send_json(data)

        s_telemetry.send_json({list(data.keys())[0]: pprint.pformat(data, width=400)})

        trackers = tracker_client.get_detections()
        for tracker_key in trackers:
            data = convert_trackers_to_serviz(trackers[tracker_key])
            s_draw.send_json(data)
            data_str = pprint.pformat(
                data,
                width=400,
            )
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
                is_signal_valid |= proxy_ctrl_handler(signal)

                if not is_signal_valid:
                    print("Invalid signal: ", signal)

        time.sleep(0.001)
