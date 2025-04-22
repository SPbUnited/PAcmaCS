from state import ssl_gc_state_pb2 as _ssl_gc_state_pb2
from state import ssl_gc_common_pb2 as _ssl_gc_common_pb2
from geom import ssl_gc_geometry_pb2 as _ssl_gc_geometry_pb2
from state import ssl_gc_game_event_pb2 as _ssl_gc_game_event_pb2
from state import ssl_gc_referee_message_pb2 as _ssl_gc_referee_message_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Change(_message.Message):
    __slots__ = ['accept_proposal_group_change', 'add_game_event_change', 'add_passive_game_event_change', 'add_proposal_change', 'add_red_card_change', 'add_yellow_card_change', 'change_stage_change', 'new_command_change', 'new_game_state_change', 'origin', 'revert_change', 'revertible', 'set_ball_placement_pos_change', 'set_status_message_change', 'switch_colors_change', 'update_config_change', 'update_team_state_change', 'yellow_card_over_change']

    class AcceptProposalGroup(_message.Message):
        __slots__ = ['accepted_by', 'group_id']
        ACCEPTED_BY_FIELD_NUMBER: _ClassVar[int]
        GROUP_ID_FIELD_NUMBER: _ClassVar[int]
        accepted_by: str
        group_id: str

        def __init__(self, group_id: _Optional[str]=..., accepted_by: _Optional[str]=...) -> None:
            ...

    class AddGameEvent(_message.Message):
        __slots__ = ['game_event']
        GAME_EVENT_FIELD_NUMBER: _ClassVar[int]
        game_event: _ssl_gc_game_event_pb2.GameEvent

        def __init__(self, game_event: _Optional[_Union[_ssl_gc_game_event_pb2.GameEvent, _Mapping]]=...) -> None:
            ...

    class AddPassiveGameEvent(_message.Message):
        __slots__ = ['game_event']
        GAME_EVENT_FIELD_NUMBER: _ClassVar[int]
        game_event: _ssl_gc_game_event_pb2.GameEvent

        def __init__(self, game_event: _Optional[_Union[_ssl_gc_game_event_pb2.GameEvent, _Mapping]]=...) -> None:
            ...

    class AddProposal(_message.Message):
        __slots__ = ['proposal']
        PROPOSAL_FIELD_NUMBER: _ClassVar[int]
        proposal: _ssl_gc_state_pb2.Proposal

        def __init__(self, proposal: _Optional[_Union[_ssl_gc_state_pb2.Proposal, _Mapping]]=...) -> None:
            ...

    class AddRedCard(_message.Message):
        __slots__ = ['caused_by_game_event', 'for_team']
        CAUSED_BY_GAME_EVENT_FIELD_NUMBER: _ClassVar[int]
        FOR_TEAM_FIELD_NUMBER: _ClassVar[int]
        caused_by_game_event: _ssl_gc_game_event_pb2.GameEvent
        for_team: _ssl_gc_common_pb2.Team

        def __init__(self, for_team: _Optional[_Union[_ssl_gc_common_pb2.Team, str]]=..., caused_by_game_event: _Optional[_Union[_ssl_gc_game_event_pb2.GameEvent, _Mapping]]=...) -> None:
            ...

    class AddYellowCard(_message.Message):
        __slots__ = ['caused_by_game_event', 'for_team']
        CAUSED_BY_GAME_EVENT_FIELD_NUMBER: _ClassVar[int]
        FOR_TEAM_FIELD_NUMBER: _ClassVar[int]
        caused_by_game_event: _ssl_gc_game_event_pb2.GameEvent
        for_team: _ssl_gc_common_pb2.Team

        def __init__(self, for_team: _Optional[_Union[_ssl_gc_common_pb2.Team, str]]=..., caused_by_game_event: _Optional[_Union[_ssl_gc_game_event_pb2.GameEvent, _Mapping]]=...) -> None:
            ...

    class ChangeStage(_message.Message):
        __slots__ = ['new_stage']
        NEW_STAGE_FIELD_NUMBER: _ClassVar[int]
        new_stage: _ssl_gc_referee_message_pb2.Referee.Stage

        def __init__(self, new_stage: _Optional[_Union[_ssl_gc_referee_message_pb2.Referee.Stage, str]]=...) -> None:
            ...

    class NewCommand(_message.Message):
        __slots__ = ['command']
        COMMAND_FIELD_NUMBER: _ClassVar[int]
        command: _ssl_gc_state_pb2.Command

        def __init__(self, command: _Optional[_Union[_ssl_gc_state_pb2.Command, _Mapping]]=...) -> None:
            ...

    class NewGameState(_message.Message):
        __slots__ = ['game_state']
        GAME_STATE_FIELD_NUMBER: _ClassVar[int]
        game_state: _ssl_gc_state_pb2.GameState

        def __init__(self, game_state: _Optional[_Union[_ssl_gc_state_pb2.GameState, _Mapping]]=...) -> None:
            ...

    class Revert(_message.Message):
        __slots__ = ['change_id']
        CHANGE_ID_FIELD_NUMBER: _ClassVar[int]
        change_id: int

        def __init__(self, change_id: _Optional[int]=...) -> None:
            ...

    class SetBallPlacementPos(_message.Message):
        __slots__ = ['pos']
        POS_FIELD_NUMBER: _ClassVar[int]
        pos: _ssl_gc_geometry_pb2.Vector2

        def __init__(self, pos: _Optional[_Union[_ssl_gc_geometry_pb2.Vector2, _Mapping]]=...) -> None:
            ...

    class SetStatusMessage(_message.Message):
        __slots__ = ['status_message']
        STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
        status_message: str

        def __init__(self, status_message: _Optional[str]=...) -> None:
            ...

    class SwitchColors(_message.Message):
        __slots__ = []

        def __init__(self) -> None:
            ...

    class UpdateConfig(_message.Message):
        __slots__ = ['division', 'first_kickoff_team', 'match_type', 'max_robots_per_team']
        DIVISION_FIELD_NUMBER: _ClassVar[int]
        FIRST_KICKOFF_TEAM_FIELD_NUMBER: _ClassVar[int]
        MATCH_TYPE_FIELD_NUMBER: _ClassVar[int]
        MAX_ROBOTS_PER_TEAM_FIELD_NUMBER: _ClassVar[int]
        division: _ssl_gc_common_pb2.Division
        first_kickoff_team: _ssl_gc_common_pb2.Team
        match_type: _ssl_gc_referee_message_pb2.MatchType
        max_robots_per_team: _wrappers_pb2.Int32Value

        def __init__(self, division: _Optional[_Union[_ssl_gc_common_pb2.Division, str]]=..., first_kickoff_team: _Optional[_Union[_ssl_gc_common_pb2.Team, str]]=..., match_type: _Optional[_Union[_ssl_gc_referee_message_pb2.MatchType, str]]=..., max_robots_per_team: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]]=...) -> None:
            ...

    class UpdateTeamState(_message.Message):
        __slots__ = ['ball_placement_failures', 'bot_substitutions_left', 'can_place_ball', 'challenge_flags_left', 'for_team', 'foul', 'goalkeeper', 'goals', 'hull_color', 'on_positive_half', 'red_card', 'remove_foul', 'remove_red_card', 'remove_yellow_card', 'requests_bot_substitution', 'requests_challenge', 'requests_emergency_stop', 'requests_timeout', 'team_name', 'timeout_time_left', 'timeouts_left', 'yellow_card']
        BALL_PLACEMENT_FAILURES_FIELD_NUMBER: _ClassVar[int]
        BOT_SUBSTITUTIONS_LEFT_FIELD_NUMBER: _ClassVar[int]
        CAN_PLACE_BALL_FIELD_NUMBER: _ClassVar[int]
        CHALLENGE_FLAGS_LEFT_FIELD_NUMBER: _ClassVar[int]
        FOR_TEAM_FIELD_NUMBER: _ClassVar[int]
        FOUL_FIELD_NUMBER: _ClassVar[int]
        GOALKEEPER_FIELD_NUMBER: _ClassVar[int]
        GOALS_FIELD_NUMBER: _ClassVar[int]
        HULL_COLOR_FIELD_NUMBER: _ClassVar[int]
        ON_POSITIVE_HALF_FIELD_NUMBER: _ClassVar[int]
        RED_CARD_FIELD_NUMBER: _ClassVar[int]
        REMOVE_FOUL_FIELD_NUMBER: _ClassVar[int]
        REMOVE_RED_CARD_FIELD_NUMBER: _ClassVar[int]
        REMOVE_YELLOW_CARD_FIELD_NUMBER: _ClassVar[int]
        REQUESTS_BOT_SUBSTITUTION_FIELD_NUMBER: _ClassVar[int]
        REQUESTS_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
        REQUESTS_EMERGENCY_STOP_FIELD_NUMBER: _ClassVar[int]
        REQUESTS_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
        TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        TIMEOUTS_LEFT_FIELD_NUMBER: _ClassVar[int]
        TIMEOUT_TIME_LEFT_FIELD_NUMBER: _ClassVar[int]
        YELLOW_CARD_FIELD_NUMBER: _ClassVar[int]
        ball_placement_failures: _wrappers_pb2.Int32Value
        bot_substitutions_left: _wrappers_pb2.Int32Value
        can_place_ball: _wrappers_pb2.BoolValue
        challenge_flags_left: _wrappers_pb2.Int32Value
        for_team: _ssl_gc_common_pb2.Team
        foul: _ssl_gc_state_pb2.Foul
        goalkeeper: _wrappers_pb2.Int32Value
        goals: _wrappers_pb2.Int32Value
        hull_color: _ssl_gc_referee_message_pb2.HullColor
        on_positive_half: _wrappers_pb2.BoolValue
        red_card: _ssl_gc_state_pb2.RedCard
        remove_foul: _wrappers_pb2.UInt32Value
        remove_red_card: _wrappers_pb2.UInt32Value
        remove_yellow_card: _wrappers_pb2.UInt32Value
        requests_bot_substitution: _wrappers_pb2.BoolValue
        requests_challenge: _wrappers_pb2.BoolValue
        requests_emergency_stop: _wrappers_pb2.BoolValue
        requests_timeout: _wrappers_pb2.BoolValue
        team_name: _wrappers_pb2.StringValue
        timeout_time_left: _wrappers_pb2.StringValue
        timeouts_left: _wrappers_pb2.Int32Value
        yellow_card: _ssl_gc_state_pb2.YellowCard

        def __init__(self, for_team: _Optional[_Union[_ssl_gc_common_pb2.Team, str]]=..., team_name: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]]=..., goals: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]]=..., goalkeeper: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]]=..., timeouts_left: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]]=..., timeout_time_left: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]]=..., on_positive_half: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]]=..., ball_placement_failures: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]]=..., can_place_ball: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]]=..., challenge_flags_left: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]]=..., bot_substitutions_left: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]]=..., requests_bot_substitution: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]]=..., requests_timeout: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]]=..., requests_challenge: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]]=..., requests_emergency_stop: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]]=..., yellow_card: _Optional[_Union[_ssl_gc_state_pb2.YellowCard, _Mapping]]=..., red_card: _Optional[_Union[_ssl_gc_state_pb2.RedCard, _Mapping]]=..., foul: _Optional[_Union[_ssl_gc_state_pb2.Foul, _Mapping]]=..., remove_yellow_card: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]]=..., remove_red_card: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]]=..., remove_foul: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]]=..., hull_color: _Optional[_Union[_ssl_gc_referee_message_pb2.HullColor, str]]=...) -> None:
            ...

    class YellowCardOver(_message.Message):
        __slots__ = ['for_team']
        FOR_TEAM_FIELD_NUMBER: _ClassVar[int]
        for_team: _ssl_gc_common_pb2.Team

        def __init__(self, for_team: _Optional[_Union[_ssl_gc_common_pb2.Team, str]]=...) -> None:
            ...
    ACCEPT_PROPOSAL_GROUP_CHANGE_FIELD_NUMBER: _ClassVar[int]
    ADD_GAME_EVENT_CHANGE_FIELD_NUMBER: _ClassVar[int]
    ADD_PASSIVE_GAME_EVENT_CHANGE_FIELD_NUMBER: _ClassVar[int]
    ADD_PROPOSAL_CHANGE_FIELD_NUMBER: _ClassVar[int]
    ADD_RED_CARD_CHANGE_FIELD_NUMBER: _ClassVar[int]
    ADD_YELLOW_CARD_CHANGE_FIELD_NUMBER: _ClassVar[int]
    CHANGE_STAGE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    NEW_COMMAND_CHANGE_FIELD_NUMBER: _ClassVar[int]
    NEW_GAME_STATE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    REVERTIBLE_FIELD_NUMBER: _ClassVar[int]
    REVERT_CHANGE_FIELD_NUMBER: _ClassVar[int]
    SET_BALL_PLACEMENT_POS_CHANGE_FIELD_NUMBER: _ClassVar[int]
    SET_STATUS_MESSAGE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    SWITCH_COLORS_CHANGE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_CONFIG_CHANGE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TEAM_STATE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    YELLOW_CARD_OVER_CHANGE_FIELD_NUMBER: _ClassVar[int]
    accept_proposal_group_change: Change.AcceptProposalGroup
    add_game_event_change: Change.AddGameEvent
    add_passive_game_event_change: Change.AddPassiveGameEvent
    add_proposal_change: Change.AddProposal
    add_red_card_change: Change.AddRedCard
    add_yellow_card_change: Change.AddYellowCard
    change_stage_change: Change.ChangeStage
    new_command_change: Change.NewCommand
    new_game_state_change: Change.NewGameState
    origin: str
    revert_change: Change.Revert
    revertible: bool
    set_ball_placement_pos_change: Change.SetBallPlacementPos
    set_status_message_change: Change.SetStatusMessage
    switch_colors_change: Change.SwitchColors
    update_config_change: Change.UpdateConfig
    update_team_state_change: Change.UpdateTeamState
    yellow_card_over_change: Change.YellowCardOver

    def __init__(self, origin: _Optional[str]=..., revertible: bool=..., new_command_change: _Optional[_Union[Change.NewCommand, _Mapping]]=..., change_stage_change: _Optional[_Union[Change.ChangeStage, _Mapping]]=..., set_ball_placement_pos_change: _Optional[_Union[Change.SetBallPlacementPos, _Mapping]]=..., add_yellow_card_change: _Optional[_Union[Change.AddYellowCard, _Mapping]]=..., add_red_card_change: _Optional[_Union[Change.AddRedCard, _Mapping]]=..., yellow_card_over_change: _Optional[_Union[Change.YellowCardOver, _Mapping]]=..., add_game_event_change: _Optional[_Union[Change.AddGameEvent, _Mapping]]=..., add_passive_game_event_change: _Optional[_Union[Change.AddPassiveGameEvent, _Mapping]]=..., add_proposal_change: _Optional[_Union[Change.AddProposal, _Mapping]]=..., update_config_change: _Optional[_Union[Change.UpdateConfig, _Mapping]]=..., update_team_state_change: _Optional[_Union[Change.UpdateTeamState, _Mapping]]=..., switch_colors_change: _Optional[_Union[Change.SwitchColors, _Mapping]]=..., revert_change: _Optional[_Union[Change.Revert, _Mapping]]=..., new_game_state_change: _Optional[_Union[Change.NewGameState, _Mapping]]=..., accept_proposal_group_change: _Optional[_Union[Change.AcceptProposalGroup, _Mapping]]=..., set_status_message_change: _Optional[_Union[Change.SetStatusMessage, _Mapping]]=...) -> None:
        ...

class StateChange(_message.Message):
    __slots__ = ['change', 'id', 'state', 'state_pre', 'timestamp']
    CHANGE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    STATE_PRE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    change: Change
    id: int
    state: _ssl_gc_state_pb2.State
    state_pre: _ssl_gc_state_pb2.State
    timestamp: _timestamp_pb2.Timestamp

    def __init__(self, id: _Optional[int]=..., state_pre: _Optional[_Union[_ssl_gc_state_pb2.State, _Mapping]]=..., state: _Optional[_Union[_ssl_gc_state_pb2.State, _Mapping]]=..., change: _Optional[_Union[Change, _Mapping]]=..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...