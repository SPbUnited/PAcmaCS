import zmq
import time

from grsim.client import GrSimClient
from grsim.model import BallReplacement, Team
from common.vision_model import Detection

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect("ipc:///tmp/serviz.sock")

class Vision:
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

    def close(self):
        self.client.close()


if __name__ == '__main__':

    print("Enter LARCmaCS")
    vision = Vision()

    time.sleep(2)

    x = 0

    field_state = {
        "ball": None,
        "robots_blu": [None for _ in range(12)],
        "robots_yel": [None for _ in range(12)],
    }

    while True:
        # detection: Detection = Vision.get_detection()

        # # Balls
        # for ball in detection.balls:
        #     field_state["ball"] = {
        #         "x": ball.x,
        #         "y": ball.y,
        #     }
        # # Robots
        # for robot in detection.robots:
        #     field_state["robots_blu" if robot.team == Team.BLUE else "robots_yel"
        #                 ][robot.robot_id] = {
        #         "x": robot.x,
        #         "y": robot.y,
        #         "rotation": robot.orientation,
        #     }

        ball = vision.get_ball()
        if ball:
            field_state["ball"] = {
                "x": ball.x,
                "y": ball.y,
            }

        robots = vision.get_robots(Team.BLUE)
        for robot in robots:
            field_state["robots_blu"][robot.robot_id] = {
                "x": robot.x,
                "y": robot.y,
                "rotation": robot.orientation,
                "robot_id": robot.robot_id,
            }

        robots = vision.get_robots(Team.YELLOW)
        for robot in robots:
            field_state["robots_yel"][robot.robot_id] = {
                "x": robot.x,
                "y": robot.y,
                "rotation": robot.orientation,
                "robot_id": robot.robot_id,
            }

        field_info = []
        if field_state["ball"] is not None:
            field_info.append({
                "type": "ball",
                "x": field_state["ball"]["x"],
                "y": field_state["ball"]["y"],
            })
        for robot in field_state["robots_blu"]:
            if robot is None:
                continue
            field_info.append({
                "type": "robot_blu",
                "robot_id": robot["robot_id"],
                "x": robot["x"],
                "y": robot["y"],
                "rotation": robot["rotation"],
            })
        for robot in field_state["robots_yel"]:
            if robot is None:
                continue
            field_info.append({
                "type": "robot_yel",
                "robot_id": robot["robot_id"],
                "x": robot["x"],
                "y": robot["y"],
                "rotation": robot["rotation"],
            })

        data = {"grsim_feed": {"data": field_info, "is_visible": True}}

        # print(data)

        socket.send_json(data)


        data = {"zmq_feed": {"data":[
            {"type": "robot_yel", "robot_id": 14, "x": x, "y": 100, "rotation": 0},
        ], "is_visible": True},
        }

        socket.send_json(data)

        x += 10
        x %= 1000

        time.sleep(0.02)
