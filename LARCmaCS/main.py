from attrs import define, field
import zmq
import time

from common.tracker_client import TrackerClient
from common.tracker_model import TeamColor
from grsim.client import GrSimClient

from argparse import ArgumentParser
import yaml

import pprint

parser = ArgumentParser()
parser.add_argument("--config", default="config.yml")
args = parser.parse_args()

config = yaml.safe_load(open(args.config))

if config["ether"]["api_version"] != 2:
    raise Exception("Only Ether v2 is supported")

context = zmq.Context()
s_draw = context.socket(zmq.PUSH)
s_draw.connect(config["ether"]["s_draw_url"])

s_signals = context.socket(zmq.SUB)
s_signals.connect(config["ether"]["s_signals_url"])
s_signals.setsockopt_string(zmq.SUBSCRIBE, '{"larcmacs":')
s_signals.setsockopt_string(zmq.SUBSCRIBE, "{'larcmacs':")

s_command_sink = context.socket(zmq.SUB)
s_command_sink.connect(config["larcmacs"]["s_command_sink_url"])
s_command_sink.setsockopt_string(zmq.SUBSCRIBE, "")

poller = zmq.Poller()
poller.register(s_signals, zmq.POLLIN)
poller.register(s_command_sink, zmq.POLLIN)

from common.vision_model import Team
from viscont import (
    SSLVision,
    SimControl,
    GrSimRobotControl,
    RobotActuateModel,
    RobotControl,
)


@define
class zmqVisionRelayTemplate:
    context: zmq.Context = field(init=False)
    relay: zmq.Socket = field(init=False)

    def __attrs_post_init__(self):
        self.context = zmq.Context()
        self.relay = self.context.socket(zmq.PUB)
        self.relay.bind(config["larcmacs"]["s_vision_fan_url"])
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
        self.relay.bind(config["larcmacs"]["s_tracker_fan_url"])
        print("Tracker relay init on ", config["larcmacs"]["s_tracker_fan_url"])
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
        if robot.robot_id.team_color == TeamColor.TEAM_COLOR_BLUE:
            sprite_type = "robot_blu"
        elif robot.robot_id.team_color == TeamColor.TEAM_COLOR_YELLOW:
            sprite_type = "robot_yel"
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

    print("Enter LARCmaCS")

    client = GrSimClient(zmq_relay_template=zmqVisionRelayTemplate)
    tracker_client = TrackerClient(zmq_relay_template=zmqTrackerRelayTemplate)

    vision = SSLVision(client=client)
    simControl = SimControl(client=client)
    robotControl = RobotControl(client=GrSimRobotControl(client=client))

    time.sleep(2)

    tracker_client.init()

    s_telemetry = context.socket(zmq.PUSH)
    s_telemetry.connect(config["ether"]["s_telemetry_url"])

    start = 0
    while True:

        # Process vision
        vision.update_vision()
        field_info = vision.get_field_info()
        data = {"vision_feed": {"data": field_info, "is_visible": True}}
        s_draw.send_json(data)

        s_telemetry.send_json({list(data.keys())[0]: pprint.pformat(data, width=400)})

        end = time.time()
        # print((end - start) * 1000)

        start = time.time()

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

                if not is_signal_valid:
                    print("Invalid signal: ", signal)

            if s_command_sink in socks:
                # print("Command socket received something")
                commands = s_command_sink.recv()
                # print(len(commands))
                # print("============")
                robotControl.apply_commands(robotControl.decypher_commands(commands))

        # robotControl.actuate_robot(
        #     RobotActuateModel(
        #         team=Team.YELLOW,
        #         robot_id=2,
        #         vx=2,
        #         vy=0,
        #         w=2,
        #     )
        # )

        time.sleep(0.001)
