from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class AutoRefConfig(_message.Message):
    __slots__ = ['game_event_behavior']

    class Behavior(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []

    class GameEventBehaviorEntry(_message.Message):
        __slots__ = ['key', 'value']
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: AutoRefConfig.Behavior

        def __init__(self, key: _Optional[str]=..., value: _Optional[_Union[AutoRefConfig.Behavior, str]]=...) -> None:
            ...
    BEHAVIOR_ACCEPT: AutoRefConfig.Behavior
    BEHAVIOR_IGNORE: AutoRefConfig.Behavior
    BEHAVIOR_LOG: AutoRefConfig.Behavior
    BEHAVIOR_UNKNOWN: AutoRefConfig.Behavior
    GAME_EVENT_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    game_event_behavior: _containers.ScalarMap[str, AutoRefConfig.Behavior]

    def __init__(self, game_event_behavior: _Optional[_Mapping[str, AutoRefConfig.Behavior]]=...) -> None:
        ...

class Config(_message.Message):
    __slots__ = ['active_tracker_source', 'auto_continue', 'auto_ref_configs', 'game_event_behavior', 'teams']

    class Behavior(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []

    class AutoRefConfigsEntry(_message.Message):
        __slots__ = ['key', 'value']
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: AutoRefConfig

        def __init__(self, key: _Optional[str]=..., value: _Optional[_Union[AutoRefConfig, _Mapping]]=...) -> None:
            ...

    class GameEventBehaviorEntry(_message.Message):
        __slots__ = ['key', 'value']
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Config.Behavior

        def __init__(self, key: _Optional[str]=..., value: _Optional[_Union[Config.Behavior, str]]=...) -> None:
            ...
    ACTIVE_TRACKER_SOURCE_FIELD_NUMBER: _ClassVar[int]
    AUTO_CONTINUE_FIELD_NUMBER: _ClassVar[int]
    AUTO_REF_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOR_ACCEPT: Config.Behavior
    BEHAVIOR_ACCEPT_MAJORITY: Config.Behavior
    BEHAVIOR_IGNORE: Config.Behavior
    BEHAVIOR_LOG: Config.Behavior
    BEHAVIOR_PROPOSE_ONLY: Config.Behavior
    BEHAVIOR_UNKNOWN: Config.Behavior
    GAME_EVENT_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    active_tracker_source: str
    auto_continue: bool
    auto_ref_configs: _containers.MessageMap[str, AutoRefConfig]
    game_event_behavior: _containers.ScalarMap[str, Config.Behavior]
    teams: _containers.RepeatedScalarFieldContainer[str]

    def __init__(self, game_event_behavior: _Optional[_Mapping[str, Config.Behavior]]=..., auto_ref_configs: _Optional[_Mapping[str, AutoRefConfig]]=..., active_tracker_source: _Optional[str]=..., teams: _Optional[_Iterable[str]]=..., auto_continue: bool=...) -> None:
        ...