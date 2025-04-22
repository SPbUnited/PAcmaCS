from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MoveGlobalVelocity(_message.Message):
    __slots__ = ['angular', 'x', 'y']
    ANGULAR_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    angular: float
    x: float
    y: float

    def __init__(self, x: _Optional[float]=..., y: _Optional[float]=..., angular: _Optional[float]=...) -> None:
        ...

class MoveLocalVelocity(_message.Message):
    __slots__ = ['angular', 'forward', 'left']
    ANGULAR_FIELD_NUMBER: _ClassVar[int]
    FORWARD_FIELD_NUMBER: _ClassVar[int]
    LEFT_FIELD_NUMBER: _ClassVar[int]
    angular: float
    forward: float
    left: float

    def __init__(self, forward: _Optional[float]=..., left: _Optional[float]=..., angular: _Optional[float]=...) -> None:
        ...

class MoveWheelVelocity(_message.Message):
    __slots__ = ['back_left', 'back_right', 'front_left', 'front_right']
    BACK_LEFT_FIELD_NUMBER: _ClassVar[int]
    BACK_RIGHT_FIELD_NUMBER: _ClassVar[int]
    FRONT_LEFT_FIELD_NUMBER: _ClassVar[int]
    FRONT_RIGHT_FIELD_NUMBER: _ClassVar[int]
    back_left: float
    back_right: float
    front_left: float
    front_right: float

    def __init__(self, front_right: _Optional[float]=..., back_right: _Optional[float]=..., back_left: _Optional[float]=..., front_left: _Optional[float]=...) -> None:
        ...

class RobotCommand(_message.Message):
    __slots__ = ['dribbler_speed', 'id', 'kick_angle', 'kick_speed', 'move_command']
    DRIBBLER_SPEED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    KICK_ANGLE_FIELD_NUMBER: _ClassVar[int]
    KICK_SPEED_FIELD_NUMBER: _ClassVar[int]
    MOVE_COMMAND_FIELD_NUMBER: _ClassVar[int]
    dribbler_speed: float
    id: int
    kick_angle: float
    kick_speed: float
    move_command: RobotMoveCommand

    def __init__(self, id: _Optional[int]=..., move_command: _Optional[_Union[RobotMoveCommand, _Mapping]]=..., kick_speed: _Optional[float]=..., kick_angle: _Optional[float]=..., dribbler_speed: _Optional[float]=...) -> None:
        ...

class RobotControl(_message.Message):
    __slots__ = ['robot_commands']
    ROBOT_COMMANDS_FIELD_NUMBER: _ClassVar[int]
    robot_commands: _containers.RepeatedCompositeFieldContainer[RobotCommand]

    def __init__(self, robot_commands: _Optional[_Iterable[_Union[RobotCommand, _Mapping]]]=...) -> None:
        ...

class RobotMoveCommand(_message.Message):
    __slots__ = ['global_velocity', 'local_velocity', 'wheel_velocity']
    GLOBAL_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    LOCAL_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    WHEEL_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    global_velocity: MoveGlobalVelocity
    local_velocity: MoveLocalVelocity
    wheel_velocity: MoveWheelVelocity

    def __init__(self, wheel_velocity: _Optional[_Union[MoveWheelVelocity, _Mapping]]=..., local_velocity: _Optional[_Union[MoveLocalVelocity, _Mapping]]=..., global_velocity: _Optional[_Union[MoveGlobalVelocity, _Mapping]]=...) -> None:
        ...