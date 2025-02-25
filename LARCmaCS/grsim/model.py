import typing

import attr

from common.vision_model import Team


@attr.s(auto_attribs=True, kw_only=True)
class RobotReplacement:
    robot_id: int
    team: Team
    x: float
    y: float
    direction: float


@attr.s(auto_attribs=True, kw_only=True)
class BallReplacement:
    x: float
    y: float
    vx: float = 0
    vy: float = 0


@attr.s(auto_attribs=True, kw_only=True)
class ActionCommand:
    team: Team
    robot_id: int
    timestamp: float = 0  # TODO:  What's the purpose? Convert to datetime?
    kickspeedx: float = 0
    kickspeedz: float = 0
    veltangent: float = 0
    velnormal: float = 0
    velangular: float = 0
    spinner: bool = False
    wheelsspeed: bool = False
    wheel1: typing.Optional[float] = None
    wheel2: typing.Optional[float] = None
    wheel3: typing.Optional[float] = None
    wheel4: typing.Optional[float] = None
