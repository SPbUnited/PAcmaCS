from state import ssl_gc_state_pb2 as _ssl_gc_state_pb2
from statemachine import ssl_gc_change_pb2 as _ssl_gc_change_pb2
from engine import ssl_gc_engine_pb2 as _ssl_gc_engine_pb2
from engine import ssl_gc_engine_config_pb2 as _ssl_gc_engine_config_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Input(_message.Message):
    __slots__ = ['change', 'config_delta', 'continue_action', 'reset_match']
    CHANGE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_DELTA_FIELD_NUMBER: _ClassVar[int]
    CONTINUE_ACTION_FIELD_NUMBER: _ClassVar[int]
    RESET_MATCH_FIELD_NUMBER: _ClassVar[int]
    change: _ssl_gc_change_pb2.Change
    config_delta: _ssl_gc_engine_config_pb2.Config
    continue_action: _ssl_gc_engine_pb2.ContinueAction
    reset_match: bool

    def __init__(self, change: _Optional[_Union[_ssl_gc_change_pb2.Change, _Mapping]]=..., reset_match: bool=..., config_delta: _Optional[_Union[_ssl_gc_engine_config_pb2.Config, _Mapping]]=..., continue_action: _Optional[_Union[_ssl_gc_engine_pb2.ContinueAction, _Mapping]]=...) -> None:
        ...

class Output(_message.Message):
    __slots__ = ['config', 'gc_state', 'match_state', 'protocol']
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    GC_STATE_FIELD_NUMBER: _ClassVar[int]
    MATCH_STATE_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    config: _ssl_gc_engine_config_pb2.Config
    gc_state: _ssl_gc_engine_pb2.GcState
    match_state: _ssl_gc_state_pb2.State
    protocol: Protocol

    def __init__(self, match_state: _Optional[_Union[_ssl_gc_state_pb2.State, _Mapping]]=..., gc_state: _Optional[_Union[_ssl_gc_engine_pb2.GcState, _Mapping]]=..., protocol: _Optional[_Union[Protocol, _Mapping]]=..., config: _Optional[_Union[_ssl_gc_engine_config_pb2.Config, _Mapping]]=...) -> None:
        ...

class Protocol(_message.Message):
    __slots__ = ['delta', 'entry']
    DELTA_FIELD_NUMBER: _ClassVar[int]
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    delta: bool
    entry: _containers.RepeatedCompositeFieldContainer[ProtocolEntry]

    def __init__(self, delta: bool=..., entry: _Optional[_Iterable[_Union[ProtocolEntry, _Mapping]]]=...) -> None:
        ...

class ProtocolEntry(_message.Message):
    __slots__ = ['change', 'id', 'match_time_elapsed', 'stage_time_elapsed']
    CHANGE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_TIME_ELAPSED_FIELD_NUMBER: _ClassVar[int]
    STAGE_TIME_ELAPSED_FIELD_NUMBER: _ClassVar[int]
    change: _ssl_gc_change_pb2.Change
    id: int
    match_time_elapsed: _duration_pb2.Duration
    stage_time_elapsed: _duration_pb2.Duration

    def __init__(self, id: _Optional[int]=..., change: _Optional[_Union[_ssl_gc_change_pb2.Change, _Mapping]]=..., match_time_elapsed: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=..., stage_time_elapsed: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=...) -> None:
        ...