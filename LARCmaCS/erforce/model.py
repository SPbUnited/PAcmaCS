import typing

import attr


@attr.s(auto_attribs=True, kw_only=True)
class MoveWheelVelocity:
    front_right: float
    back_right: float
    back_left: float
    front_left: float


@attr.s(auto_attribs=True, kw_only=True)
class MoveLocalVelocity:
    forward: float
    left: float
    angular: float


@attr.s(auto_attribs=True, kw_only=True)
class MoveGlobalVelocity:
    x: float
    y: float
    angular: float


RobotMoveCommand = typing.Union[MoveWheelVelocity, MoveLocalVelocity, MoveGlobalVelocity]


@attr.s(auto_attribs=True, kw_only=True)
class RobotCommand:
    robot_id: int
    move_command: typing.Optional[RobotMoveCommand] = None
    kick_speed: typing.Optional[float] = None
    kick_angle: typing.Optional[float] = None
    dribbler_speed: typing.Optional[float] = None

