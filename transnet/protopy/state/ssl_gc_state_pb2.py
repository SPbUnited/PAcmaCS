"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ..state import ssl_gc_common_pb2 as state_dot_ssl__gc__common__pb2
from ..geom import ssl_gc_geometry_pb2 as geom_dot_ssl__gc__geometry__pb2
from ..state import ssl_gc_game_event_pb2 as state_dot_ssl__gc__game__event__pb2
from ..state import ssl_gc_referee_message_pb2 as state_dot_ssl__gc__referee__message__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18state/ssl_gc_state.proto\x1a\x19state/ssl_gc_common.proto\x1a\x1ageom/ssl_gc_geometry.proto\x1a\x1dstate/ssl_gc_game_event.proto\x1a"state/ssl_gc_referee_message.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto"u\n\nYellowCard\x12\n\n\x02id\x18\x01 \x01(\r\x12(\n\x14caused_by_game_event\x18\x02 \x01(\x0b2\n.GameEvent\x121\n\x0etime_remaining\x18\x03 \x01(\x0b2\x19.google.protobuf.Duration"?\n\x07RedCard\x12\n\n\x02id\x18\x01 \x01(\r\x12(\n\x14caused_by_game_event\x18\x02 \x01(\x0b2\n.GameEvent"k\n\x04Foul\x12\n\n\x02id\x18\x01 \x01(\r\x12(\n\x14caused_by_game_event\x18\x02 \x01(\x0b2\n.GameEvent\x12-\n\ttimestamp\x18\x03 \x01(\x0b2\x1a.google.protobuf.Timestamp"\xd9\x01\n\x07Command\x12\x1b\n\x04type\x18\x01 \x02(\x0e2\r.Command.Type\x12\x17\n\x08for_team\x18\x02 \x02(\x0e2\x05.Team"\x97\x01\n\x04Type\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x08\n\x04HALT\x10\x01\x12\x08\n\x04STOP\x10\x02\x12\x10\n\x0cNORMAL_START\x10\x03\x12\x0f\n\x0bFORCE_START\x10\x04\x12\n\n\x06DIRECT\x10\x05\x12\x0b\n\x07KICKOFF\x10\x07\x12\x0b\n\x07PENALTY\x10\x08\x12\x0b\n\x07TIMEOUT\x10\t\x12\x12\n\x0eBALL_PLACEMENT\x10\n"\x04\x08\x06\x10\x06"\xc3\x01\n\tGameState\x12\x1d\n\x04type\x18\x01 \x02(\x0e2\x0f.GameState.Type\x12\x17\n\x08for_team\x18\x02 \x01(\x0e2\x05.Team"~\n\x04Type\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x08\n\x04HALT\x10\x01\x12\x08\n\x04STOP\x10\x02\x12\x0b\n\x07RUNNING\x10\x03\x12\r\n\tFREE_KICK\x10\x04\x12\x0b\n\x07KICKOFF\x10\x05\x12\x0b\n\x07PENALTY\x10\x06\x12\x0b\n\x07TIMEOUT\x10\x07\x12\x12\n\x0eBALL_PLACEMENT\x10\x08"Y\n\x08Proposal\x12-\n\ttimestamp\x18\x01 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x1e\n\ngame_event\x18\x02 \x01(\x0b2\n.GameEvent"Q\n\rProposalGroup\x12\n\n\x02id\x18\x04 \x01(\t\x12\x1c\n\tproposals\x18\x01 \x03(\x0b2\t.Proposal\x12\x10\n\x08accepted\x18\x02 \x01(\x08J\x04\x08\x03\x10\x04"\xf2\x05\n\x08TeamInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05goals\x18\x02 \x01(\x05\x12\x12\n\ngoalkeeper\x18\x03 \x01(\x05\x12!\n\x0cyellow_cards\x18\x04 \x03(\x0b2\x0b.YellowCard\x12\x1b\n\tred_cards\x18\x05 \x03(\x0b2\x08.RedCard\x12\x15\n\rtimeouts_left\x18\x06 \x01(\x05\x124\n\x11timeout_time_left\x18\x07 \x01(\x0b2\x19.google.protobuf.Duration\x12\x18\n\x10on_positive_half\x18\x08 \x01(\x08\x12\x14\n\x05fouls\x18\t \x03(\x0b2\x05.Foul\x12\x1f\n\x17ball_placement_failures\x18\n \x01(\x05\x12\'\n\x1fball_placement_failures_reached\x18\x0b \x01(\x08\x12\x16\n\x0ecan_place_ball\x18\x0c \x01(\x08\x12\x18\n\x10max_allowed_bots\x18\r \x01(\x05\x12C\n\x1frequests_bot_substitution_since\x18\x0e \x01(\x0b2\x1a.google.protobuf.Timestamp\x12:\n\x16requests_timeout_since\x18\x0f \x01(\x0b2\x1a.google.protobuf.Timestamp\x12A\n\x1drequests_emergency_stop_since\x18\x10 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12\x17\n\x0fchallenge_flags\x18\x11 \x01(\x05\x12 \n\x18bot_substitution_allowed\x18\x12 \x01(\x08\x12\x1e\n\x16bot_substitutions_left\x18\x13 \x01(\x05\x12=\n\x1abot_substitution_time_left\x18\x14 \x01(\x0b2\x19.google.protobuf.Duration\x12\x1e\n\nhull_color\x18\x15 \x01(\x0e2\n.HullColor"\xb1\x06\n\x05State\x12\x1d\n\x05stage\x18\x01 \x01(\x0e2\x0e.Referee.Stage\x12\x19\n\x07command\x18\x02 \x01(\x0b2\x08.Command\x12\x1e\n\ngame_state\x18\x13 \x01(\x0b2\n.GameState\x125\n\x12stage_time_elapsed\x18\x04 \x01(\x0b2\x19.google.protobuf.Duration\x122\n\x0fstage_time_left\x18\x05 \x01(\x0b2\x19.google.protobuf.Duration\x124\n\x10match_time_start\x18\x06 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12)\n\nteam_state\x18\x08 \x03(\x0b2\x15.State.TeamStateEntry\x12\x1f\n\rplacement_pos\x18\t \x01(\x0b2\x08.Vector2\x12\x1e\n\x0cnext_command\x18\n \x01(\x0b2\x08.Command\x12@\n\x1dcurrent_action_time_remaining\x18\x0c \x01(\x0b2\x19.google.protobuf.Duration\x12\x1f\n\x0bgame_events\x18\r \x03(\x0b2\n.GameEvent\x12\'\n\x0fproposal_groups\x18\x0e \x03(\x0b2\x0e.ProposalGroup\x12\x1b\n\x08division\x18\x0f \x01(\x0e2\t.Division\x12!\n\x12first_kickoff_team\x18\x11 \x01(\x0e2\x05.Team\x12\x1e\n\nmatch_type\x18\x12 \x01(\x0e2\n.MatchType\x127\n\x13ready_continue_time\x18\x14 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12&\n\x0eshootout_state\x18\x15 \x01(\x0b2\x0e.ShootoutState\x12\x16\n\x0estatus_message\x18\x16 \x01(\t\x12\x19\n\x11max_bots_per_team\x18\x17 \x01(\x05\x1a;\n\x0eTeamStateEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x18\n\x05value\x18\x02 \x01(\x0b2\t.TeamInfo:\x028\x01J\x04\x08\x10\x10\x11"\xa4\x01\n\rShootoutState\x12\x18\n\tnext_team\x18\x01 \x01(\x0e2\x05.Team\x12@\n\x12number_of_attempts\x18\x02 \x03(\x0b2$.ShootoutState.NumberOfAttemptsEntry\x1a7\n\x15NumberOfAttemptsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x028\x01')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'state.ssl_gc_state_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _STATE_TEAMSTATEENTRY._options = None
    _STATE_TEAMSTATEENTRY._serialized_options = b'8\x01'
    _SHOOTOUTSTATE_NUMBEROFATTEMPTSENTRY._options = None
    _SHOOTOUTSTATE_NUMBEROFATTEMPTSENTRY._serialized_options = b'8\x01'
    _YELLOWCARD._serialized_start = 215
    _YELLOWCARD._serialized_end = 332
    _REDCARD._serialized_start = 334
    _REDCARD._serialized_end = 397
    _FOUL._serialized_start = 399
    _FOUL._serialized_end = 506
    _COMMAND._serialized_start = 509
    _COMMAND._serialized_end = 726
    _COMMAND_TYPE._serialized_start = 575
    _COMMAND_TYPE._serialized_end = 726
    _GAMESTATE._serialized_start = 729
    _GAMESTATE._serialized_end = 924
    _GAMESTATE_TYPE._serialized_start = 798
    _GAMESTATE_TYPE._serialized_end = 924
    _PROPOSAL._serialized_start = 926
    _PROPOSAL._serialized_end = 1015
    _PROPOSALGROUP._serialized_start = 1017
    _PROPOSALGROUP._serialized_end = 1098
    _TEAMINFO._serialized_start = 1101
    _TEAMINFO._serialized_end = 1855
    _STATE._serialized_start = 1858
    _STATE._serialized_end = 2675
    _STATE_TEAMSTATEENTRY._serialized_start = 2610
    _STATE_TEAMSTATEENTRY._serialized_end = 2669
    _SHOOTOUTSTATE._serialized_start = 2678
    _SHOOTOUTSTATE._serialized_end = 2842
    _SHOOTOUTSTATE_NUMBEROFATTEMPTSENTRY._serialized_start = 2787
    _SHOOTOUTSTATE_NUMBEROFATTEMPTSENTRY._serialized_end = 2842