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
    capabilities: List[Capability]


@define
class TrackerWrapperPacket:
    uuid: str
    source_name: Optional[str]
    tracked_frame: Optional[TrackedFrame]


def proto_to_vector2(proto) -> Vector2:
    return Vector2(x=proto.x, y=proto.y)


def proto_to_vector3(proto) -> Vector3:
    return Vector3(x=proto.x, y=proto.y, z=proto.z)


def proto_to_robot_id(proto) -> RobotId:
    return RobotId(id=proto.id, team_color=TeamColor(proto.team_color))


def proto_to_tracked_ball(proto) -> TrackedBall:
    return TrackedBall(
        pos=proto_to_vector3(proto.pos),
        vel=proto_to_vector3(proto.vel) if proto.HasField("vel") else None,
        visibility=proto.visibility if proto.HasField("visibility") else None,
    )


def proto_to_kicked_ball(proto) -> Optional[KickedBall]:
    if not proto.IsInitialized():
        return None
    return KickedBall(
        pos=proto_to_vector2(proto.pos),
        vel=proto_to_vector3(proto.vel),
        start_timestamp=proto.start_timestamp,
        stop_timestamp=(
            proto.stop_timestamp if proto.HasField("stop_timestamp") else None
        ),
        stop_pos=(
            proto_to_vector2(proto.stop_pos) if proto.HasField("stop_pos") else None
        ),
        robot_id=(
            proto_to_robot_id(proto.robot_id) if proto.HasField("robot_id") else None
        ),
    )


def proto_to_tracked_robot(proto) -> TrackedRobot:
    return TrackedRobot(
        robot_id=proto_to_robot_id(proto.robot_id),
        pos=proto_to_vector2(proto.pos),
        orientation=proto.orientation,
        vel=proto_to_vector2(proto.vel) if proto.HasField("vel") else None,
        vel_angular=proto.vel_angular if proto.HasField("vel_angular") else None,
        visibility=proto.visibility if proto.HasField("visibility") else None,
    )


def proto_to_tracked_frame(proto) -> Optional[TrackedFrame]:
    if not proto.IsInitialized():
        return None
    return TrackedFrame(
        frame_number=proto.frame_number,
        timestamp=proto.timestamp,
        # balls=[],
        # robots=[],
        balls=[proto_to_tracked_ball(b) for b in proto.balls],
        robots=[proto_to_tracked_robot(r) for r in proto.robots],
        kicked_ball=proto_to_kicked_ball(proto.kicked_ball),
        capabilities=[Capability(c) for c in proto.capabilities],
    )


def proto_to_wrapper_packet(proto) -> TrackerWrapperPacket:
    return TrackerWrapperPacket(
        uuid=proto.uuid,
        source_name=proto.source_name if proto.HasField("source_name") else None,
        tracked_frame=(
            # proto.tracked_frame
            proto_to_tracked_frame(proto.tracked_frame)
            if proto.HasField("tracked_frame")
            else None
        ),
    )


# # Usage example:
# tracking_data_parser = TrackerWrapperPacketModel()
# tracking_data_parser.ParseFromString(data)
# converted = proto_to_wrapper_packet(tracking_data_parser)
