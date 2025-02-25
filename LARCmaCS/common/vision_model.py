import typing
from enum import Enum

import attr


class Team(Enum):
    BLUE = 1
    YELLOW = 2


@attr.s(auto_attribs=True)
class FrameInfo:
    frame_number: int
    # TODO: Convert to datetime
    t_capture: float
    t_sent: float
    camera_id: int


@attr.s(auto_attribs=True)
class RobotDetection:
    frame_info: FrameInfo
    team: Team
    confidence: float
    robot_id: int
    x: float
    y: float
    orientation: float
    # TODO: Are these additional coordinates needed?
    pixel_x: float
    pixel_y: float


@attr.s(auto_attribs=True)
class BallDetection:
    frame_info: FrameInfo
    confidence: float
    x: float
    y: float
    z: float
    # TODO: Are these additional coordinates needed?
    pixel_x: float
    pixel_y: float


@attr.s(auto_attribs=True)
class Geometry:
    # TODO: Implement
    pass


@attr.s(auto_attribs=True)
class Detection:
    balls: typing.List[BallDetection]
    robots: typing.List[RobotDetection]
    geometry: typing.Optional[Geometry]

    def get_robot(self, team: Team, robot_id: int) -> typing.Optional[RobotDetection]:
        robot = [r for r in self.robots if r.team.value == team.value and r.robot_id == robot_id]
        return robot[0] if robot else None

    def get_ball(self) -> typing.Optional[BallDetection]:
        return self.balls[0] if self.balls else None

