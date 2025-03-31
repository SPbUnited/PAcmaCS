from attrs import define, field
import zmq
import time

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


if __name__ == "__main__":

    print("Enter LARCmaCS")

    client = GrSimClient(zmq_relay_template=zmqVisionRelayTemplate)

    vision = SSLVision(client=client)
    simControl = SimControl(client=client)
    robotControl = RobotControl(client=GrSimRobotControl(client=client))

    time.sleep(2)

    while True:

        # Process vision
        vision.update_vision()
        field_info = vision.get_field_info()
        data = {"grsim_feed": {"data": field_info, "is_visible": True}}
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
