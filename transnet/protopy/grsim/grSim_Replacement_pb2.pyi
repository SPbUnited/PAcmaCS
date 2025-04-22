from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class grSim_BallReplacement(_message.Message):
    __slots__ = ['vx', 'vy', 'x', 'y']
    VX_FIELD_NUMBER: _ClassVar[int]
    VY_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    vx: float
    vy: float
    x: float
    y: float

    def __init__(self, x: _Optional[float]=..., y: _Optional[float]=..., vx: _Optional[float]=..., vy: _Optional[float]=...) -> None:
        ...

class grSim_Replacement(_message.Message):
    __slots__ = ['ball', 'robots']
    BALL_FIELD_NUMBER: _ClassVar[int]
    ROBOTS_FIELD_NUMBER: _ClassVar[int]
    ball: grSim_BallReplacement
    robots: _containers.RepeatedCompositeFieldContainer[grSim_RobotReplacement]

    def __init__(self, ball: _Optional[_Union[grSim_BallReplacement, _Mapping]]=..., robots: _Optional[_Iterable[_Union[grSim_RobotReplacement, _Mapping]]]=...) -> None:
        ...

class grSim_RobotReplacement(_message.Message):
    __slots__ = ['dir', 'id', 'turnon', 'x', 'y', 'yellowteam']
    DIR_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TURNON_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    YELLOWTEAM_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    dir: float
    id: int
    turnon: bool
    x: float
    y: float
    yellowteam: bool

    def __init__(self, x: _Optional[float]=..., y: _Optional[float]=..., dir: _Optional[float]=..., id: _Optional[int]=..., yellowteam: bool=..., turnon: bool=...) -> None:
        ...