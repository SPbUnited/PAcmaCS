from state import ssl_gc_common_pb2 as _ssl_gc_common_pb2
from rcon import ssl_gc_rcon_pb2 as _ssl_gc_rcon_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
CHALLENGE_FLAG: RemoteControlRequestType
CHANGE_KEEPER_ID: RemoteControlRequestType
DESCRIPTOR: _descriptor.FileDescriptor
EMERGENCY_STOP: RemoteControlRequestType
FAIL_BALLPLACEMENT: RemoteControlRequestType
ROBOT_SUBSTITUTION: RemoteControlRequestType
STOP_TIMEOUT: RemoteControlRequestType
TIMEOUT: RemoteControlRequestType
UNKNOWN_REQUEST_TYPE: RemoteControlRequestType

class ControllerToRemoteControl(_message.Message):
    __slots__ = ['controller_reply', 'state']
    CONTROLLER_REPLY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    controller_reply: _ssl_gc_rcon_pb2.ControllerReply
    state: RemoteControlTeamState

    def __init__(self, controller_reply: _Optional[_Union[_ssl_gc_rcon_pb2.ControllerReply, _Mapping]]=..., state: _Optional[_Union[RemoteControlTeamState, _Mapping]]=...) -> None:
        ...

class RemoteControlRegistration(_message.Message):
    __slots__ = ['signature', 'team']
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    signature: _ssl_gc_rcon_pb2.Signature
    team: _ssl_gc_common_pb2.Team

    def __init__(self, team: _Optional[_Union[_ssl_gc_common_pb2.Team, str]]=..., signature: _Optional[_Union[_ssl_gc_rcon_pb2.Signature, _Mapping]]=...) -> None:
        ...

class RemoteControlTeamState(_message.Message):
    __slots__ = ['active_requests', 'available_requests', 'bot_substitution_time_left', 'bot_substitutions_left', 'can_substitute_robot', 'challenge_flags_left', 'emergency_stop_in', 'keeper_id', 'max_robots', 'robots_on_field', 'team', 'timeout_time_left', 'timeouts_left', 'yellow_cards_due']
    ACTIVE_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    BOT_SUBSTITUTIONS_LEFT_FIELD_NUMBER: _ClassVar[int]
    BOT_SUBSTITUTION_TIME_LEFT_FIELD_NUMBER: _ClassVar[int]
    CAN_SUBSTITUTE_ROBOT_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_FLAGS_LEFT_FIELD_NUMBER: _ClassVar[int]
    EMERGENCY_STOP_IN_FIELD_NUMBER: _ClassVar[int]
    KEEPER_ID_FIELD_NUMBER: _ClassVar[int]
    MAX_ROBOTS_FIELD_NUMBER: _ClassVar[int]
    ROBOTS_ON_FIELD_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    TIMEOUTS_LEFT_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_TIME_LEFT_FIELD_NUMBER: _ClassVar[int]
    YELLOW_CARDS_DUE_FIELD_NUMBER: _ClassVar[int]
    active_requests: _containers.RepeatedScalarFieldContainer[RemoteControlRequestType]
    available_requests: _containers.RepeatedScalarFieldContainer[RemoteControlRequestType]
    bot_substitution_time_left: float
    bot_substitutions_left: int
    can_substitute_robot: bool
    challenge_flags_left: int
    emergency_stop_in: float
    keeper_id: int
    max_robots: int
    robots_on_field: int
    team: _ssl_gc_common_pb2.Team
    timeout_time_left: float
    timeouts_left: int
    yellow_cards_due: _containers.RepeatedScalarFieldContainer[float]

    def __init__(self, team: _Optional[_Union[_ssl_gc_common_pb2.Team, str]]=..., available_requests: _Optional[_Iterable[_Union[RemoteControlRequestType, str]]]=..., active_requests: _Optional[_Iterable[_Union[RemoteControlRequestType, str]]]=..., keeper_id: _Optional[int]=..., emergency_stop_in: _Optional[float]=..., timeouts_left: _Optional[int]=..., timeout_time_left: _Optional[float]=..., challenge_flags_left: _Optional[int]=..., max_robots: _Optional[int]=..., robots_on_field: _Optional[int]=..., yellow_cards_due: _Optional[_Iterable[float]]=..., can_substitute_robot: bool=..., bot_substitutions_left: _Optional[int]=..., bot_substitution_time_left: _Optional[float]=...) -> None:
        ...

class RemoteControlToController(_message.Message):
    __slots__ = ['desired_keeper', 'request', 'request_emergency_stop', 'request_robot_substitution', 'request_timeout', 'signature']

    class Request(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CHALLENGE_FLAG: RemoteControlToController.Request
    DESIRED_KEEPER_FIELD_NUMBER: _ClassVar[int]
    FAIL_BALLPLACEMENT: RemoteControlToController.Request
    PING: RemoteControlToController.Request
    REQUEST_EMERGENCY_STOP_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ROBOT_SUBSTITUTION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    STOP_TIMEOUT: RemoteControlToController.Request
    UNKNOWN: RemoteControlToController.Request
    desired_keeper: int
    request: RemoteControlToController.Request
    request_emergency_stop: bool
    request_robot_substitution: bool
    request_timeout: bool
    signature: _ssl_gc_rcon_pb2.Signature

    def __init__(self, signature: _Optional[_Union[_ssl_gc_rcon_pb2.Signature, _Mapping]]=..., request: _Optional[_Union[RemoteControlToController.Request, str]]=..., desired_keeper: _Optional[int]=..., request_robot_substitution: bool=..., request_timeout: bool=..., request_emergency_stop: bool=...) -> None:
        ...

class RemoteControlRequestType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []