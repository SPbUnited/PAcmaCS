import zmq
import time

from grsim.client import GrSimClient
from grsim.model import BallReplacement, RobotReplacement, Team
from common.vision_model import Detection

from typing import Dict

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect("ipc:///tmp/serviz.sock")

signal_socket = context.socket(zmq.SUB)
signal_socket.connect("ipc:///tmp/serviz.pub.sock")
# signal_socket.setsockopt_string(zmq.SUBSCRIBE, "test_signal")
signal_socket.setsockopt_string(zmq.SUBSCRIBE, "{\"larcmacs\":")
signal_socket.setsockopt_string(zmq.SUBSCRIBE, "{\'larcmacs\':")

poller = zmq.Poller()
poller.register(signal_socket, zmq.POLLIN)

class Vision:
    __field_state = {
        "ball": None,
        Team.BLUE.name: [None for _ in range(12)],
        Team.YELLOW.name: [None for _ in range(12)],
    }

    def __init__(self):
        self.client = GrSimClient()
        self.client.init()

    def get_detection(self) -> Detection:
        return self.client.get_detection()

    def get_ball(self):
        return self.client.get_ball()

    def get_robot(self, team, index):
        return self.client.get_robot(team, index)

    def get_robots(self, team):
        robots = []
        for i in range(0, 6):
            robot = self.get_robot(team, i)
            if robot:
                robots.append(robot)
        return robots

    def set_ball(self, x, y, vx, vy):
        self.client.send_ball_replacement(BallReplacement(x=x/1000, y=y/1000, vx=vx/1000, vy=vy/1000))

    def set_robot(self, team, index, x, y, direction):
        self.client.send_robot_replacement(RobotReplacement(x=x/1000, y=y/1000, direction=direction, robot_id=index, team=team))

    def update_vision(self):
        self.update_ball()
        self.update_robots()

    def update_ball(self):
        detection = self.get_detection()
        if detection.balls is not None:
            self.__field_state["ball"] = {
                "x": detection.balls[0].x,
                "y": detection.balls[0].y,
            }
        else:
            self.__field_state["ball"] = None

    def update_robots(self):
        for team in Team:
            for i in range(12):
                robot = self.get_robot(team, i)
                if robot is not None:
                    self.__field_state[team.name][robot.robot_id] = {
                        "x": robot.x,
                        "y": robot.y,
                        "rotation": robot.orientation,
                        "robot_id": robot.robot_id,
                    }
                else:
                    self.__field_state[team.name][i] = None

    def get_field_info(self):
        field_info = []
        if self.__field_state["ball"] is not None:
            field_info.append({
                "type": "ball",
                "x": self.__field_state["ball"]["x"],
                "y": self.__field_state["ball"]["y"],
            })
        for robot in self.__field_state[Team.BLUE.name]:
            if robot is None:
                continue
            field_info.append({
                "type": "robot_blu",
                "robot_id": robot["robot_id"],
                "x": robot["x"],
                "y": robot["y"],
                "rotation": robot["rotation"],
            })
        for robot in self.__field_state[Team.YELLOW.name]:
            if robot is None:
                continue
            field_info.append({
                "type": "robot_yel",
                "robot_id": robot["robot_id"],
                "x": robot["x"],
                "y": robot["y"],
                "rotation": robot["rotation"],
            })
        return field_info

    def close(self):
        self.client.close()

def signal_handler(signal: Dict, vision: Vision):
    signal_type = signal["larcmacs"]

    if signal_type == "test_signal":
        test_formation = {
            Team.YELLOW.name: [
                {"robot_id": 0, "x": -2000, "y": 0, "rotation": 0},
                {"robot_id": 1, "x": -700, "y": 600, "rotation": 0},
                {"robot_id": 2, "x": -700, "y": -600, "rotation": 0},
            ],
            Team.BLUE.name: [
                {"robot_id": 3, "x": 2000, "y": 0, "rotation": 3.14},
                {"robot_id": 4, "x": 700, "y": 600, "rotation": 3.14},
                {"robot_id": 5, "x": 700, "y": -600, "rotation": 3.14},
            ],
        }
        graveyard = {"x": -2000, "y": 3000, "rotation": 0}

        # Send all robots to the graveyard
        for i in range(16):
            vision.set_robot(Team.YELLOW, i, graveyard["x"], graveyard["y"], graveyard["rotation"])
            graveyard["x"] += 200
        for i in range(16):
            vision.set_robot(Team.BLUE, i, graveyard["x"], graveyard["y"], graveyard["rotation"])
            graveyard["x"] += 200

        # Send all known robots to the test formation
        for robot in test_formation[Team.YELLOW.name]:
            vision.set_robot(Team.YELLOW, robot["robot_id"], robot["x"], robot["y"], robot["rotation"])
        for robot in test_formation[Team.BLUE.name]:
            vision.set_robot(Team.BLUE, robot["robot_id"], robot["x"], robot["y"], robot["rotation"])

        vision.set_ball(1000, 1000, -2000, -2000)

    elif signal_type == "set_ball":
        x = signal["data"]["x"]
        y = signal["data"]["y"]
        vx = signal["data"]["vx"]
        vy = signal["data"]["vy"]
        vision.set_ball(x, y, vx, vy)

    else:
        print("Unknown signal")



if __name__ == '__main__':

    print("Enter LARCmaCS")
    vision = Vision()

    time.sleep(2)

    x = 0

    while True:

        # Process vision
        vision.update_vision()
        field_info = vision.get_field_info()
        data = {"grsim_feed": {"data": field_info, "is_visible": True}}
        socket.send_json(data)

        # Generate test data
        data = {"zmq_feed": {"data":[
            {"type": "robot_yel", "robot_id": 14, "x": x, "y": 100, "rotation": 0},
        ], "is_visible": True},
        }

        socket.send_json(data)

        x += 10
        x %= 1000

        # Process incoming signals
        try:
            socks = dict(poller.poll(timeout=1))
        except KeyboardInterrupt:
            break

        if signal_socket in socks:
            signal = signal_socket.recv_json()
            print(signal)
            signal_handler(signal, vision)

        time.sleep(0.02)
