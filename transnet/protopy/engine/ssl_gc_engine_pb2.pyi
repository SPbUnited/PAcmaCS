from geom import ssl_gc_geometry_pb2 as _ssl_gc_geometry_pb2
from state import ssl_gc_common_pb2 as _ssl_gc_common_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Ball(_message.Message):
    __slots__ = ['pos', 'vel']
    POS_FIELD_NUMBER: _ClassVar[int]
    VEL_FIELD_NUMBER: _ClassVar[int]
    pos: _ssl_gc_geometry_pb2.Vector3
    vel: _ssl_gc_geometry_pb2.Vector3

    def __init__(self, pos: _Optional[_Union[_ssl_gc_geometry_pb2.Vector3, _Mapping]]=..., vel: _Optional[_Union[_ssl_gc_geometry_pb2.Vector3, _Mapping]]=...) -> None:
        ...

class ContinueAction(_message.Message):
    __slots__ = ['continuation_issues', 'for_team', 'ready_at', 'state', 'type']

    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []

    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ACCEPT_GOAL: ContinueAction.Type
    BALL_PLACEMENT_CANCEL: ContinueAction.Type
    BALL_PLACEMENT_COMPLETE: ContinueAction.Type
    BALL_PLACEMENT_FAIL: ContinueAction.Type
    BALL_PLACEMENT_START: ContinueAction.Type
    BLOCKED: ContinueAction.State
    BOT_SUBSTITUTION: ContinueAction.Type
    CHALLENGE_ACCEPT: ContinueAction.Type
    CHALLENGE_REJECT: ContinueAction.Type
    CONTINUATION_ISSUES_FIELD_NUMBER: _ClassVar[int]
    DISABLED: ContinueAction.State
    END_GAME: ContinueAction.Type
    FORCE_START: ContinueAction.Type
    FOR_TEAM_FIELD_NUMBER: _ClassVar[int]
    FREE_KICK: ContinueAction.Type
    HALT: ContinueAction.Type
    NEXT_COMMAND: ContinueAction.Type
    NEXT_STAGE: ContinueAction.Type
    NORMAL_START: ContinueAction.Type
    READY_AT_FIELD_NUMBER: _ClassVar[int]
    READY_AUTO: ContinueAction.State
    READY_MANUAL: ContinueAction.State
    REJECT_GOAL: ContinueAction.Type
    RESUME_FROM_HALT: ContinueAction.Type
    STATE_FIELD_NUMBER: _ClassVar[int]
    STATE_UNKNOWN: ContinueAction.State
    STOP_GAME: ContinueAction.Type
    TIMEOUT_START: ContinueAction.Type
    TIMEOUT_STOP: ContinueAction.Type
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TYPE_UNKNOWN: ContinueAction.Type
    WAITING: ContinueAction.State
    continuation_issues: _containers.RepeatedScalarFieldContainer[str]
    for_team: _ssl_gc_common_pb2.Team
    ready_at: _timestamp_pb2.Timestamp
    state: ContinueAction.State
    type: ContinueAction.Type

    def __init__(self, type: _Optional[_Union[ContinueAction.Type, str]]=..., for_team: _Optional[_Union[_ssl_gc_common_pb2.Team, str]]=..., continuation_issues: _Optional[_Iterable[str]]=..., ready_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., state: _Optional[_Union[ContinueAction.State, str]]=...) -> None:
        ...

class ContinueHint(_message.Message):
    __slots__ = ['message']
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str

    def __init__(self, message: _Optional[str]=...) -> None:
        ...

class GcState(_message.Message):
    __slots__ = ['auto_ref_state', 'continue_actions', 'continue_hints', 'team_state', 'trackers']

    class AutoRefStateEntry(_message.Message):
        __slots__ = ['key', 'value']
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: GcStateAutoRef

        def __init__(self, key: _Optional[str]=..., value: _Optional[_Union[GcStateAutoRef, _Mapping]]=...) -> None:
            ...

    class TeamStateEntry(_message.Message):
        __slots__ = ['key', 'value']
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: GcStateTeam

        def __init__(self, key: _Optional[str]=..., value: _Optional[_Union[GcStateTeam, _Mapping]]=...) -> None:
            ...

    class TrackersEntry(_message.Message):
        __slots__ = ['key', 'value']
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str

        def __init__(self, key: _Optional[str]=..., value: _Optional[str]=...) -> None:
            ...
    AUTO_REF_STATE_FIELD_NUMBER: _ClassVar[int]
    CONTINUE_ACTIONS_FIELD_NUMBER: _ClassVar[int]
    CONTINUE_HINTS_FIELD_NUMBER: _ClassVar[int]
    TEAM_STATE_FIELD_NUMBER: _ClassVar[int]
    TRACKERS_FIELD_NUMBER: _ClassVar[int]
    auto_ref_state: _containers.MessageMap[str, GcStateAutoRef]
    continue_actions: _containers.RepeatedCompositeFieldContainer[ContinueAction]
    continue_hints: _containers.RepeatedCompositeFieldContainer[ContinueHint]
    team_state: _containers.MessageMap[str, GcStateTeam]
    trackers: _containers.ScalarMap[str, str]

    def __init__(self, team_state: _Optional[_Mapping[str, GcStateTeam]]=..., auto_ref_state: _Optional[_Mapping[str, GcStateAutoRef]]=..., trackers: _Optional[_Mapping[str, str]]=..., continue_actions: _Optional[_Iterable[_Union[ContinueAction, _Mapping]]]=..., continue_hints: _Optional[_Iterable[_Union[ContinueHint, _Mapping]]]=...) -> None:
        ...

class GcStateAutoRef(_message.Message):
    __slots__ = ['connection_verified']
    CONNECTION_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    connection_verified: bool

    def __init__(self, connection_verified: bool=...) -> None:
        ...

class GcStateTeam(_message.Message):
    __slots__ = ['advantage_choice', 'connected', 'connection_verified', 'remote_control_connected', 'remote_control_connection_verified']
    ADVANTAGE_CHOICE_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    REMOTE_CONTROL_CONNECTED_FIELD_NUMBER: _ClassVar[int]
    REMOTE_CONTROL_CONNECTION_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    advantage_choice: TeamAdvantageChoice
    connected: bool
    connection_verified: bool
    remote_control_connected: bool
    remote_control_connection_verified: bool

    def __init__(self, connected: bool=..., connection_verified: bool=..., remote_control_connected: bool=..., remote_control_connection_verified: bool=..., advantage_choice: _Optional[_Union[TeamAdvantageChoice, _Mapping]]=...) -> None:
        ...

class GcStateTracker(_message.Message):
    __slots__ = ['ball', 'robots', 'source_name', 'uuid']
    BALL_FIELD_NUMBER: _ClassVar[int]
    ROBOTS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    ball: Ball
    robots: _containers.RepeatedCompositeFieldContainer[Robot]
    source_name: str
    uuid: str

    def __init__(self, source_name: _Optional[str]=..., uuid: _Optional[str]=..., ball: _Optional[_Union[Ball, _Mapping]]=..., robots: _Optional[_Iterable[_Union[Robot, _Mapping]]]=...) -> None:
        ...

class Robot(_message.Message):
    __slots__ = ['id', 'pos']
    ID_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    id: _ssl_gc_common_pb2.RobotId
    pos: _ssl_gc_geometry_pb2.Vector2

    def __init__(self, id: _Optional[_Union[_ssl_gc_common_pb2.RobotId, _Mapping]]=..., pos: _Optional[_Union[_ssl_gc_geometry_pb2.Vector2, _Mapping]]=...) -> None:
        ...

class TeamAdvantageChoice(_message.Message):
    __slots__ = ['choice']

    class AdvantageChoice(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CHOICE_FIELD_NUMBER: _ClassVar[int]
    CONTINUE: TeamAdvantageChoice.AdvantageChoice
    STOP: TeamAdvantageChoice.AdvantageChoice
    choice: TeamAdvantageChoice.AdvantageChoice

    def __init__(self, choice: _Optional[_Union[TeamAdvantageChoice.AdvantageChoice, str]]=...) -> None:
        ...