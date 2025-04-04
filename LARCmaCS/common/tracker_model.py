from enum import Enum
from typing import List, Optional
from attrs import define, field


@define
class Vector2:
    x: float
    y: float


@define
class Vector3:
    x: float
    y: float
    z: float


class TeamColor(Enum):
    TEAM_COLOR_UNKNOWN = 0
    TEAM_COLOR_YELLOW = 1
    TEAM_COLOR_BLUE = 2


@define
class RobotId:
    id: int
    team_color: TeamColor


class Capability(Enum):
    CAPABILITY_UNKNOWN = 0
    CAPABILITY_DETECT_FLYING_BALLS = 1
    CAPABILITY_DETECT_MULTIPLE_BALLS = 2
    CAPABILITY_DETECT_KICKED_BALLS = 3


@define
class TrackedBall:
    pos: Vector3
    vel: Optional[Vector3]
    visibility: Optional[float]


@define
class KickedBall:
    pos: Vector2
    vel: Vector3
    start_timestamp: float
    stop_timestamp: Optional[float]
    stop_pos: Optional[Vector2]
    robot_id: Optional[RobotId]


@define
class TrackedRobot:
    robot_id: RobotId
    pos: Vector2
    orientation: float
    vel: Optional[Vector2]
    vel_angular: Optional[float]
    visibility: Optional[float]


@define
class TrackedFrame:
    frame_number: int
    timestamp: float
    balls: List[TrackedBall]
    robots: List[TrackedRobot]

    kicked_ball: Optional[KickedBall]
    capabilities: Capability


@define
class TrackerWrapperPacket:
    uuid: str
    source_name: Optional[str]
    tracked_frame: Optional[TrackedFrame]
