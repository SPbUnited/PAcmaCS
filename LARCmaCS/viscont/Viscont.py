from grsim.model import BallReplacement, RobotReplacement
from grsim.client import GrSimClient, ActionCommand
from common.vision_model import Team
from attrs import define, field
from typing import Any, Dict


@define
class SSLVision:
    client: Any

    __field_state = {
        "ball": None,
        Team.BLUE.name: [None for _ in range(16)],
        Team.YELLOW.name: [None for _ in range(16)],
    }

    def __attrs_post_init__(self) -> None:
        self.client.init()

    def update_vision(self):
        self.update_ball()
        self.update_robots()

    def update_ball(self):
        detection = self.client.get_detection()
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
                robot = self.client.get_robot(team, i)
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
            field_info.append(
                {
                    "type": "ball",
                    "x": self.__field_state["ball"]["x"],
                    "y": self.__field_state["ball"]["y"],
                }
            )
        for robot in self.__field_state[Team.BLUE.name]:
            if robot is None:
                continue
            field_info.append(
                {
                    "type": "robot_blu",
                    "robot_id": robot["robot_id"],
                    "x": robot["x"],
                    "y": robot["y"],
                    "rotation": robot["rotation"],
                }
            )
        for robot in self.__field_state[Team.YELLOW.name]:
            if robot is None:
                continue
            field_info.append(
                {
                    "type": "robot_yel",
                    "robot_id": robot["robot_id"],
                    "x": robot["x"],
                    "y": robot["y"],
                    "rotation": robot["rotation"],
                }
            )
        return field_info


@define
class SimControl:
    client: Any

    def set_formation(self, formation):
        graveyard = {"x": -2000, "y": 3000, "rotation": 0}

        # Send all robots to the graveyard
        for team in [Team.YELLOW, Team.BLUE]:
            for i in range(16):
                self.client.send_robot_replacement(
                    RobotReplacement(
                        x=graveyard["x"] / 1000,
                        y=graveyard["y"] / 1000,
                        direction=graveyard["rotation"],
                        robot_id=i,
                        team=team,
                    )
                )
                graveyard["x"] += 200

        # Send all known robots to the test formation
        for team in [Team.YELLOW, Team.BLUE]:
            for robot in formation[team.name]:
                self.client.send_robot_replacement(
                    RobotReplacement(
                        x=robot["x"] / 1000,
                        y=robot["y"] / 1000,
                        direction=robot["rotation"],
                        robot_id=robot["robot_id"],
                        team=team,
                    )
                )

    def set_ball(self, x, y, vx, vy):
        self.client.send_ball_replacement(
            BallReplacement(
                x=x / 1000,
                y=y / 1000,
                vx=vx / 1000,
                vy=vy / 1000,
            )
        )

    def set_robot(self, team, index, x, y, direction):
        self.client.send_robot_replacement(
            RobotReplacement(
                x=x / 1000,
                y=y / 1000,
                direction=direction,
                robot_id=index,
                team=team,
            )
        )

    def signal_handler(self, signal: Dict):
        signal_type = signal["larcmacs"]

        if signal_type == "test_signal":
            test_formation = {
                "YELLOW": [
                    {"robot_id": 0, "x": -2000, "y": 0, "rotation": 0},
                    {"robot_id": 1, "x": -700, "y": 600, "rotation": 0},
                    {"robot_id": 2, "x": -700, "y": -600, "rotation": 0},
                ],
                "BLUE": [
                    {"robot_id": 3, "x": 2000, "y": 0, "rotation": 180},
                    {"robot_id": 4, "x": 700, "y": 600, "rotation": 180},
                    {"robot_id": 5, "x": 700, "y": -600, "rotation": 180},
                ],
            }

            self.set_formation(test_formation)

            self.set_ball(1000, 750, -2000, -2000)

        elif signal_type == "set_ball":
            x = signal["data"]["x"]
            y = signal["data"]["y"]
            vx = signal["data"]["vx"]
            vy = signal["data"]["vy"]
            self.set_ball(x, y, vx, vy)

        else:
            print("Unknown signal")


@define
class RobotActuateModel:
    team: Team = field(default=Team.YELLOW)
    robot_id: int = field(default=0)
    vx: float = field(default=0)
    vy: float = field(default=0)
    w: float = field(default=0)
    kicklow: bool = field(default=False)
    kickhigh: bool = field(default=False)


@define
class GrSimRobotControl:
    client: GrSimClient

    def actuate_robot(self, command: RobotActuateModel):
        self.client.send_action_command(
            ActionCommand(
                team=command.team,
                robot_id=command.robot_id,
                timestamp=0,
                kickspeedx=0,
                kickspeedz=0,
                veltangent=command.vy,
                velnormal=command.vx,
                velangular=command.w,
                spinner=0,
                wheelsspeed=False,
                wheel1=None,
                wheel2=None,
                wheel3=None,
                wheel4=None,
            )
        )


@define
class RobotControl:
    client = None

    def actuate_robot(self, command: RobotActuateModel):
        self.client.actuate_robot(command)
