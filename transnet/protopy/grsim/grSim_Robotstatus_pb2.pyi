from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Robot_Status(_message.Message):
    __slots__ = ['chip_kick', 'flat_kick', 'infrared', 'robot_id']
    CHIP_KICK_FIELD_NUMBER: _ClassVar[int]
    FLAT_KICK_FIELD_NUMBER: _ClassVar[int]
    INFRARED_FIELD_NUMBER: _ClassVar[int]
    ROBOT_ID_FIELD_NUMBER: _ClassVar[int]
    chip_kick: bool
    flat_kick: bool
    infrared: bool
    robot_id: int

    def __init__(self, robot_id: _Optional[int]=..., infrared: bool=..., flat_kick: bool=..., chip_kick: bool=...) -> None:
        ...

class Robots_Status(_message.Message):
    __slots__ = ['robots_status']
    ROBOTS_STATUS_FIELD_NUMBER: _ClassVar[int]
    robots_status: _containers.RepeatedCompositeFieldContainer[Robot_Status]

    def __init__(self, robots_status: _Optional[_Iterable[_Union[Robot_Status, _Mapping]]]=...) -> None:
        ...