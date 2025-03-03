import zmq
import time

from grsim.client import GrSimClient
from grsim.model import BallReplacement, Team
from common.vision_model import Detection

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect("ipc:///tmp/serviz.sock")

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
        self.client.send_ball_replacement(BallReplacement(x=x, y=y, vx=vx, vy=vy))

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


if __name__ == '__main__':

    print("Enter LARCmaCS")
    vision = Vision()

    time.sleep(2)

    x = 0

    while True:

        vision.update_vision()
        field_info = vision.get_field_info()

        data = {"grsim_feed": {"data": field_info, "is_visible": True}}

        socket.send_json(data)

        data = {"zmq_feed": {"data":[
            {"type": "robot_yel", "robot_id": 14, "x": x, "y": 100, "rotation": 0},
        ], "is_visible": True},
        }

        socket.send_json(data)

        x += 10
        x %= 1000

        time.sleep(0.02)
