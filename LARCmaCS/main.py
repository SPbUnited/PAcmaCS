from attrs import define, field
import zmq
import time

from common.tracker_client import TrackerClient
from common.tracker_model import TeamColor
from grsim.client import GrSimClient

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect("ipc:///tmp/serviz.sock")

signal_socket = context.socket(zmq.SUB)
signal_socket.connect("ipc:///tmp/serviz.pub.sock")
signal_socket.setsockopt_string(zmq.SUBSCRIBE, '{"larcmacs":')
signal_socket.setsockopt_string(zmq.SUBSCRIBE, "{'larcmacs':")

command_socket = context.socket(zmq.SUB)
command_socket.connect("tcp://localhost:5667")
command_socket.setsockopt_string(zmq.SUBSCRIBE, "")

poller = zmq.Poller()
poller.register(signal_socket, zmq.POLLIN)
poller.register(command_socket, zmq.POLLIN)

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
        self.relay.bind("tcp://*:4242")
        print("Relay init")

    def send(self, raw_frame):
        self.relay.send(raw_frame)


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
        if robot.robot_id.team_color == TeamColor.TEAM_COLOR_BLUE.value:
            sprite_type = "robot_blu"
        elif robot.robot_id.team_color == TeamColor.TEAM_COLOR_YELLOW.value:
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
    tracker_client = TrackerClient()

    vision = SSLVision(client=client)
    simControl = SimControl(client=client)
    robotControl = RobotControl(client=GrSimRobotControl(client=client))

    time.sleep(2)

    tracker_client.init()

    trackers_list = set()
    trackers_list_buf = set()

    while True:

        # Process vision
        vision.update_vision()
        field_info = vision.get_field_info()
        data = {"grsim_feed": {"data": field_info, "is_visible": True}}
        socket.send_json(data)

        trackers = tracker_client.get_detection()

        trackers_list.add(trackers.source_name)
        if len(trackers_list) != len(trackers_list_buf):
            print("Received trackers: ", trackers_list)
        trackers_list_buf.add(trackers.source_name)

        data = convert_trackers_to_serviz(trackers)
        socket.send_json(data)

        for i in range(100):
            # Process incoming signals
            try:
                socks = dict(poller.poll(timeout=0))
            except KeyboardInterrupt:
                break

            if socks == {}:
                break

            if signal_socket in socks:
                signal = signal_socket.recv_json()
                # print(signal)
                is_signal_valid = False
                is_signal_valid |= simControl.signal_handler(signal)
                is_signal_valid |= robotControl.signal_handler(signal)

                if not is_signal_valid:
                    print("Invalid signal: ", signal)

            if command_socket in socks:
                # print("Command socket received something")
                commands = command_socket.recv()
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

        time.sleep(0.005)
