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

poller = zmq.Poller()
poller.register(signal_socket, zmq.POLLIN)

from common.vision_model import Team
from viscont import SSLVision, SimControl, GrSimRobotControl, RobotActuateModel


if __name__ == "__main__":

    print("Enter LARCmaCS")

    client = GrSimClient()

    vision = SSLVision(client=client)
    simControl = SimControl(client=client)
    robotControl = GrSimRobotControl(client=client)

    time.sleep(2)

    while True:

        # Process vision
        vision.update_vision()
        field_info = vision.get_field_info()
        data = {"grsim_feed": {"data": field_info, "is_visible": True}}
        socket.send_json(data)

        # Process incoming signals
        try:
            socks = dict(poller.poll(timeout=1))
        except KeyboardInterrupt:
            break

        if signal_socket in socks:
            signal = signal_socket.recv_json()
            print(signal)
            simControl.signal_handler(signal)

        robotControl.actuate_robot(
            RobotActuateModel(
                team=Team.YELLOW,
                robot_id=2,
                vx=2,
                vy=0,
                w=2,
            )
        )

        time.sleep(0.02)
