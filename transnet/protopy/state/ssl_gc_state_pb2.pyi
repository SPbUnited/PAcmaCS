from state import ssl_gc_common_pb2 as _ssl_gc_common_pb2
from geom import ssl_gc_geometry_pb2 as _ssl_gc_geometry_pb2
from state import ssl_gc_game_event_pb2 as _ssl_gc_game_event_pb2
from state import ssl_gc_referee_message_pb2 as _ssl_gc_referee_message_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Command(_message.Message):
    __slots__ = ['for_team', 'type']

    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BALL_PLACEMENT: Command.Type
    DIRECT: Command.Type
    FORCE_START: Command.Type
    FOR_TEAM_FIELD_NUMBER: _ClassVar[int]
    HALT: Command.Type
    KICKOFF: Command.Type
    NORMAL_START: Command.Type
    PENALTY: Command.Type
    STOP: Command.Type
    TIMEOUT: Command.Type
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: Command.Type
    for_team: _ssl_gc_common_pb2.Team
    type: Command.Type

    def __init__(self, type: _Optional[_Union[Command.Type, str]]=..., for_team: _Optional[_Union[_ssl_gc_common_pb2.Team, str]]=...) -> None:
        ...

class Foul(_message.Message):
    __slots__ = ['caused_by_game_event', 'id', 'timestamp']
    CAUSED_BY_GAME_EVENT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    caused_by_game_event: _ssl_gc_game_event_pb2.GameEvent
    id: int
    timestamp: _timestamp_pb2.Timestamp

    def __init__(self, id: _Optional[int]=..., caused_by_game_event: _Optional[_Union[_ssl_gc_game_event_pb2.GameEvent, _Mapping]]=..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...

class GameState(_message.Message):
    __slots__ = ['for_team', 'type']

    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BALL_PLACEMENT: GameState.Type
    FOR_TEAM_FIELD_NUMBER: _ClassVar[int]
    FREE_KICK: GameState.Type
    HALT: GameState.Type
    KICKOFF: GameState.Type
    PENALTY: GameState.Type
    RUNNING: GameState.Type
    STOP: GameState.Type
    TIMEOUT: GameState.Type
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN: GameState.Type
    for_team: _ssl_gc_common_pb2.Team
    type: GameState.Type

    def __init__(self, type: _Optional[_Union[GameState.Type, str]]=..., for_team: _Optional[_Union[_ssl_gc_common_pb2.Team, str]]=...) -> None:
        ...

class Proposal(_message.Message):
    __slots__ = ['game_event', 'timestamp']
    GAME_EVENT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    game_event: _ssl_gc_game_event_pb2.GameEvent
    timestamp: _timestamp_pb2.Timestamp

    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., game_event: _Optional[_Union[_ssl_gc_game_event_pb2.GameEvent, _Mapping]]=...) -> None:
        ...

class ProposalGroup(_message.Message):
    __slots__ = ['accepted', 'id', 'proposals']
    ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PROPOSALS_FIELD_NUMBER: _ClassVar[int]
    accepted: bool
    id: str
    proposals: _containers.RepeatedCompositeFieldContainer[Proposal]

    def __init__(self, id: _Optional[str]=..., proposals: _Optional[_Iterable[_Union[Proposal, _Mapping]]]=..., accepted: bool=...) -> None:
        ...

class RedCard(_message.Message):
    __slots__ = ['caused_by_game_event', 'id']
    CAUSED_BY_GAME_EVENT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    caused_by_game_event: _ssl_gc_game_event_pb2.GameEvent
    id: int

    def __init__(self, id: _Optional[int]=..., caused_by_game_event: _Optional[_Union[_ssl_gc_game_event_pb2.GameEvent, _Mapping]]=...) -> None:
        ...

class ShootoutState(_message.Message):
    __slots__ = ['next_team', 'number_of_attempts']

    class NumberOfAttemptsEntry(_message.Message):
        __slots__ = ['key', 'value']
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int

        def __init__(self, key: _Optional[str]=..., value: _Optional[int]=...) -> None:
            ...
    NEXT_TEAM_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    next_team: _ssl_gc_common_pb2.Team
    number_of_attempts: _containers.ScalarMap[str, int]

    def __init__(self, next_team: _Optional[_Union[_ssl_gc_common_pb2.Team, str]]=..., number_of_attempts: _Optional[_Mapping[str, int]]=...) -> None:
        ...

class State(_message.Message):
    __slots__ = ['command', 'current_action_time_remaining', 'division', 'first_kickoff_team', 'game_events', 'game_state', 'match_time_start', 'match_type', 'max_bots_per_team', 'next_command', 'placement_pos', 'proposal_groups', 'ready_continue_time', 'shootout_state', 'stage', 'stage_time_elapsed', 'stage_time_left', 'status_message', 'team_state']

    class TeamStateEntry(_message.Message):
        __slots__ = ['key', 'value']
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: TeamInfo

        def __init__(self, key: _Optional[str]=..., value: _Optional[_Union[TeamInfo, _Mapping]]=...) -> None:
            ...
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    CURRENT_ACTION_TIME_REMAINING_FIELD_NUMBER: _ClassVar[int]
    DIVISION_FIELD_NUMBER: _ClassVar[int]
    FIRST_KICKOFF_TEAM_FIELD_NUMBER: _ClassVar[int]
    GAME_EVENTS_FIELD_NUMBER: _ClassVar[int]
    GAME_STATE_FIELD_NUMBER: _ClassVar[int]
    MATCH_TIME_START_FIELD_NUMBER: _ClassVar[int]
    MATCH_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAX_BOTS_PER_TEAM_FIELD_NUMBER: _ClassVar[int]
    NEXT_COMMAND_FIELD_NUMBER: _ClassVar[int]
    PLACEMENT_POS_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_GROUPS_FIELD_NUMBER: _ClassVar[int]
    READY_CONTINUE_TIME_FIELD_NUMBER: _ClassVar[int]
    SHOOTOUT_STATE_FIELD_NUMBER: _ClassVar[int]
    STAGE_FIELD_NUMBER: _ClassVar[int]
    STAGE_TIME_ELAPSED_FIELD_NUMBER: _ClassVar[int]
    STAGE_TIME_LEFT_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TEAM_STATE_FIELD_NUMBER: _ClassVar[int]
    command: Command
    current_action_time_remaining: _duration_pb2.Duration
    division: _ssl_gc_common_pb2.Division
    first_kickoff_team: _ssl_gc_common_pb2.Team
    game_events: _containers.RepeatedCompositeFieldContainer[_ssl_gc_game_event_pb2.GameEvent]
    game_state: GameState
    match_time_start: _timestamp_pb2.Timestamp
    match_type: _ssl_gc_referee_message_pb2.MatchType
    max_bots_per_team: int
    next_command: Command
    placement_pos: _ssl_gc_geometry_pb2.Vector2
    proposal_groups: _containers.RepeatedCompositeFieldContainer[ProposalGroup]
    ready_continue_time: _timestamp_pb2.Timestamp
    shootout_state: ShootoutState
    stage: _ssl_gc_referee_message_pb2.Referee.Stage
    stage_time_elapsed: _duration_pb2.Duration
    stage_time_left: _duration_pb2.Duration
    status_message: str
    team_state: _containers.MessageMap[str, TeamInfo]

    def __init__(self, stage: _Optional[_Union[_ssl_gc_referee_message_pb2.Referee.Stage, str]]=..., command: _Optional[_Union[Command, _Mapping]]=..., game_state: _Optional[_Union[GameState, _Mapping]]=..., stage_time_elapsed: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=..., stage_time_left: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=..., match_time_start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., team_state: _Optional[_Mapping[str, TeamInfo]]=..., placement_pos: _Optional[_Union[_ssl_gc_geometry_pb2.Vector2, _Mapping]]=..., next_command: _Optional[_Union[Command, _Mapping]]=..., current_action_time_remaining: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=..., game_events: _Optional[_Iterable[_Union[_ssl_gc_game_event_pb2.GameEvent, _Mapping]]]=..., proposal_groups: _Optional[_Iterable[_Union[ProposalGroup, _Mapping]]]=..., division: _Optional[_Union[_ssl_gc_common_pb2.Division, str]]=..., first_kickoff_team: _Optional[_Union[_ssl_gc_common_pb2.Team, str]]=..., match_type: _Optional[_Union[_ssl_gc_referee_message_pb2.MatchType, str]]=..., ready_continue_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., shootout_state: _Optional[_Union[ShootoutState, _Mapping]]=..., status_message: _Optional[str]=..., max_bots_per_team: _Optional[int]=...) -> None:
        ...

class TeamInfo(_message.Message):
    __slots__ = ['ball_placement_failures', 'ball_placement_failures_reached', 'bot_substitution_allowed', 'bot_substitution_time_left', 'bot_substitutions_left', 'can_place_ball', 'challenge_flags', 'fouls', 'goalkeeper', 'goals', 'hull_color', 'max_allowed_bots', 'name', 'on_positive_half', 'red_cards', 'requests_bot_substitution_since', 'requests_emergency_stop_since', 'requests_timeout_since', 'timeout_time_left', 'timeouts_left', 'yellow_cards']
    BALL_PLACEMENT_FAILURES_FIELD_NUMBER: _ClassVar[int]
    BALL_PLACEMENT_FAILURES_REACHED_FIELD_NUMBER: _ClassVar[int]
    BOT_SUBSTITUTIONS_LEFT_FIELD_NUMBER: _ClassVar[int]
    BOT_SUBSTITUTION_ALLOWED_FIELD_NUMBER: _ClassVar[int]
    BOT_SUBSTITUTION_TIME_LEFT_FIELD_NUMBER: _ClassVar[int]
    CAN_PLACE_BALL_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    FOULS_FIELD_NUMBER: _ClassVar[int]
    GOALKEEPER_FIELD_NUMBER: _ClassVar[int]
    GOALS_FIELD_NUMBER: _ClassVar[int]
    HULL_COLOR_FIELD_NUMBER: _ClassVar[int]
    MAX_ALLOWED_BOTS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ON_POSITIVE_HALF_FIELD_NUMBER: _ClassVar[int]
    RED_CARDS_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_BOT_SUBSTITUTION_SINCE_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_EMERGENCY_STOP_SINCE_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_TIMEOUT_SINCE_FIELD_NUMBER: _ClassVar[int]
    TIMEOUTS_LEFT_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_TIME_LEFT_FIELD_NUMBER: _ClassVar[int]
    YELLOW_CARDS_FIELD_NUMBER: _ClassVar[int]
    ball_placement_failures: int
    ball_placement_failures_reached: bool
    bot_substitution_allowed: bool
    bot_substitution_time_left: _duration_pb2.Duration
    bot_substitutions_left: int
    can_place_ball: bool
    challenge_flags: int
    fouls: _containers.RepeatedCompositeFieldContainer[Foul]
    goalkeeper: int
    goals: int
    hull_color: _ssl_gc_referee_message_pb2.HullColor
    max_allowed_bots: int
    name: str
    on_positive_half: bool
    red_cards: _containers.RepeatedCompositeFieldContainer[RedCard]
    requests_bot_substitution_since: _timestamp_pb2.Timestamp
    requests_emergency_stop_since: _timestamp_pb2.Timestamp
    requests_timeout_since: _timestamp_pb2.Timestamp
    timeout_time_left: _duration_pb2.Duration
    timeouts_left: int
    yellow_cards: _containers.RepeatedCompositeFieldContainer[YellowCard]

    def __init__(self, name: _Optional[str]=..., goals: _Optional[int]=..., goalkeeper: _Optional[int]=..., yellow_cards: _Optional[_Iterable[_Union[YellowCard, _Mapping]]]=..., red_cards: _Optional[_Iterable[_Union[RedCard, _Mapping]]]=..., timeouts_left: _Optional[int]=..., timeout_time_left: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=..., on_positive_half: bool=..., fouls: _Optional[_Iterable[_Union[Foul, _Mapping]]]=..., ball_placement_failures: _Optional[int]=..., ball_placement_failures_reached: bool=..., can_place_ball: bool=..., max_allowed_bots: _Optional[int]=..., requests_bot_substitution_since: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., requests_timeout_since: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., requests_emergency_stop_since: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., challenge_flags: _Optional[int]=..., bot_substitution_allowed: bool=..., bot_substitutions_left: _Optional[int]=..., bot_substitution_time_left: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=..., hull_color: _Optional[_Union[_ssl_gc_referee_message_pb2.HullColor, str]]=...) -> None:
        ...

class YellowCard(_message.Message):
    __slots__ = ['caused_by_game_event', 'id', 'time_remaining']
    CAUSED_BY_GAME_EVENT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TIME_REMAINING_FIELD_NUMBER: _ClassVar[int]
    caused_by_game_event: _ssl_gc_game_event_pb2.GameEvent
    id: int
    time_remaining: _duration_pb2.Duration

    def __init__(self, id: _Optional[int]=..., caused_by_game_event: _Optional[_Union[_ssl_gc_game_event_pb2.GameEvent, _Mapping]]=..., time_remaining: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=...) -> None:
        ...