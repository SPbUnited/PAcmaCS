import math
from grsim.model import BallReplacement, RobotReplacement
from grsim.client import GrSimClient, ActionCommand
from common.vision_model import Team
from attrs import define, field
from typing import Any, Dict
import struct
from cattrs import structure, unstructure

from . import robot_command_model as rcm


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
        if detection.balls is not None and len(detection.balls) > 0:
            self.__field_state["ball"] = {
                "x": detection.balls[0].x,
                "y": detection.balls[0].y,
            }
        else:
            self.__field_state["ball"] = None

    def update_robots(self):
        for team in Team:
            for i in range(16):
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

    def signal_handler(self, signal: Dict) -> bool:
        signal_type = signal["transnet"]

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

            return True

        elif signal_type == "set_ball":
            x = signal["data"]["x"]
            y = signal["data"]["y"]
            vx = signal["data"]["vx"]
            vy = signal["data"]["vy"]
            self.set_ball(x, y, vx, vy)

            return True

        return False


@define
class GrSimRobotControl:
    client: GrSimClient

    wheel_diameter: float = field(default=0.027)

    def actuate_robot(self, cmd: rcm.RobotCommandExt):
        ac = ActionCommand(
            team=Team.YELLOW if cmd.isteamyellow else Team.BLUE, robot_id=cmd.id
        )

        if cmd.move_command is not None:
            if cmd.move_command.wheel_velocity is not None:
                m_s_to_rad_s = 1 / self.wheel_diameter

                ac.wheelsspeed = True
                ac.wheel1 = cmd.move_command.wheel_velocity.front_left / m_s_to_rad_s
                ac.wheel2 = cmd.move_command.wheel_velocity.back_left / m_s_to_rad_s
                ac.wheel3 = cmd.move_command.wheel_velocity.back_right / m_s_to_rad_s
                ac.wheel4 = cmd.move_command.wheel_velocity.front_right / m_s_to_rad_s
            if cmd.move_command.local_velocity is not None:
                ac.velnormal = cmd.move_command.local_velocity.left
                ac.veltangent = cmd.move_command.local_velocity.forward
                ac.velangular = cmd.move_command.local_velocity.angular
            if cmd.move_command.global_velocity is not None:
                raise Exception("Global velocity not implemented")

        if cmd.kick_speed is not None:
            if cmd.kick_angle is not None:
                ac.kickspeedx = cmd.kick_speed * math.cos(cmd.kick_angle)
                ac.kickspeedz = cmd.kick_speed * math.sin(cmd.kick_angle)
            else:
                ac.kickspeedx = cmd.kick_speed
                ac.kickspeedz = 0

        if cmd.dribbler_speed is not None:
            ac.spinner = cmd.dribbler_speed > 0

        self.client.send_action_command(ac)


@define
class RobotControl:
    client: Any

    def decypher_commands(self, data: bytes) -> Dict:
        """
        Convert byte stream from get_rules() back into robot control dictionaries.

        Returns:
            dict: {'blue': [robot0_dict, ...], 'yellow': [robot0_dict, ...]}
            Each robot_dict contains control parameters for one robot.
        """

        # Unpack bytes into list of floats (double precision)
        num_values = len(data) // 8
        if len(data) % 8 != 0 or num_values % 13 != 0:
            raise ValueError("Invalid data length. Expected multiple of 13*8 bytes.")

        values = struct.unpack(f"{num_values}d", data)

        # Organize into teams and robots
        control_data = {"blue": [], "yellow": []}
        team_size = len(values) // 13 // 2  # 16 robots per team for standard setup

        for team_idx, team in enumerate(["blue", "yellow"]):
            for robot_idx in range(team_size):
                # Extract 13 parameters per robot
                start = (team_idx * team_size + robot_idx) * 13
                params = values[start : start + 13]

                k = 1 / 100 * 6
                k /= 4
                # Map parameters to their meanings (ignore first/last zero values)
                control_data[team].append(
                    {
                        "speed_x": params[1] * k,
                        "speed_y": params[2] * k,
                        #!v Could be speed_r or angle info
                        "speed_r_or_angle": params[3] * k,
                        "kick_up": params[4],
                        "kick_forward": params[5],
                        "auto_kick": params[6],
                        "kicker_voltage": params[7],
                        "dribbler_enable": params[8],
                        "dribbler_speed": params[9],
                        "kicker_charge_enable": params[10],
                        "beep": params[11],
                    }
                )

        # import json

        # print(json.dumps(control_data, indent=4))

        return control_data

    def apply_commands(self, commands: rcm.RobotControlExt):
        """
        Send robot control commands to GrSim.

        Args:
            commands (dict): {'blue': [robot0_dict, ...], 'yellow': [robot0_dict, ...]}
                Each robot_dict contains control parameters for one robot.
        """
        team = Team.YELLOW if commands.isteamyellow else Team.BLUE

        for robot_command in commands.robot_commands:
            robot_command_ext = rcm.RobotCommandExt(
                isteamyellow=commands.isteamyellow,
                id=robot_command.id,
                move_command=robot_command.move_command,
                kick_speed=robot_command.kick_speed,
                kick_angle=robot_command.kick_angle,
                dribbler_speed=robot_command.dribbler_speed,
            )
            self.client.actuate_robot(robot_command_ext)

    def signal_handler(self, signal: Dict) -> bool:
        signal_type = signal["transnet"]

        if signal_type == "actuate_robot":
            # print(signal["data"])
            commands = structure(signal["data"], rcm.RobotControlExt)
            self.apply_commands(commands)
            # print(commands)
            return True

        return False
