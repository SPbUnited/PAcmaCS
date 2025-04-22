"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ..state import ssl_gc_game_event_pb2 as state_dot_ssl__gc__game__event__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n"state/ssl_gc_referee_message.proto\x1a\x1dstate/ssl_gc_game_event.proto"\xd5\x0e\n\x07Referee\x12\x19\n\x11source_identifier\x18\x12 \x01(\t\x12-\n\nmatch_type\x18\x13 \x01(\x0e2\n.MatchType:\rUNKNOWN_MATCH\x12\x18\n\x10packet_timestamp\x18\x01 \x02(\x04\x12\x1d\n\x05stage\x18\x02 \x02(\x0e2\x0e.Referee.Stage\x12\x17\n\x0fstage_time_left\x18\x03 \x01(\x12\x12!\n\x07command\x18\x04 \x02(\x0e2\x10.Referee.Command\x12\x17\n\x0fcommand_counter\x18\x05 \x02(\r\x12\x19\n\x11command_timestamp\x18\x06 \x02(\x04\x12!\n\x06yellow\x18\x07 \x02(\x0b2\x11.Referee.TeamInfo\x12\x1f\n\x04blue\x18\x08 \x02(\x0b2\x11.Referee.TeamInfo\x12+\n\x13designated_position\x18\t \x01(\x0b2\x0e.Referee.Point\x12"\n\x1ablue_team_on_positive_half\x18\n \x01(\x08\x12&\n\x0cnext_command\x18\x0c \x01(\x0e2\x10.Referee.Command\x12\x1f\n\x0bgame_events\x18\x10 \x03(\x0b2\n.GameEvent\x125\n\x14game_event_proposals\x18\x11 \x03(\x0b2\x17.GameEventProposalGroup\x12%\n\x1dcurrent_action_time_remaining\x18\x0f \x01(\x03\x12\x16\n\x0estatus_message\x18\x14 \x01(\t\x1a\xe4\x03\n\x08TeamInfo\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\r\n\x05score\x18\x02 \x02(\r\x12\x11\n\tred_cards\x18\x03 \x02(\r\x12\x1d\n\x11yellow_card_times\x18\x04 \x03(\rB\x02\x10\x01\x12\x14\n\x0cyellow_cards\x18\x05 \x02(\r\x12\x10\n\x08timeouts\x18\x06 \x02(\r\x12\x14\n\x0ctimeout_time\x18\x07 \x02(\r\x12\x12\n\ngoalkeeper\x18\x08 \x02(\r\x12\x14\n\x0cfoul_counter\x18\t \x01(\r\x12\x1f\n\x17ball_placement_failures\x18\n \x01(\r\x12\x16\n\x0ecan_place_ball\x18\x0c \x01(\x08\x12\x18\n\x10max_allowed_bots\x18\r \x01(\r\x12\x1f\n\x17bot_substitution_intent\x18\x0e \x01(\x08\x12\'\n\x1fball_placement_failures_reached\x18\x0f \x01(\x08\x12 \n\x18bot_substitution_allowed\x18\x10 \x01(\x08\x12\x1e\n\x16bot_substitutions_left\x18\x11 \x01(\r\x12"\n\x1abot_substitution_time_left\x18\x12 \x01(\r\x12\x1e\n\nhull_color\x18\x13 \x01(\x0e2\n.HullColor\x1a\x1d\n\x05Point\x12\t\n\x01x\x18\x01 \x02(\x02\x12\t\n\x01y\x18\x02 \x02(\x02"\xd1\x02\n\x05Stage\x12\x19\n\x15NORMAL_FIRST_HALF_PRE\x10\x00\x12\x15\n\x11NORMAL_FIRST_HALF\x10\x01\x12\x14\n\x10NORMAL_HALF_TIME\x10\x02\x12\x1a\n\x16NORMAL_SECOND_HALF_PRE\x10\x03\x12\x16\n\x12NORMAL_SECOND_HALF\x10\x04\x12\x14\n\x10EXTRA_TIME_BREAK\x10\x05\x12\x18\n\x14EXTRA_FIRST_HALF_PRE\x10\x06\x12\x14\n\x10EXTRA_FIRST_HALF\x10\x07\x12\x13\n\x0fEXTRA_HALF_TIME\x10\x08\x12\x19\n\x15EXTRA_SECOND_HALF_PRE\x10\t\x12\x15\n\x11EXTRA_SECOND_HALF\x10\n\x12\x1a\n\x16PENALTY_SHOOTOUT_BREAK\x10\x0b\x12\x14\n\x10PENALTY_SHOOTOUT\x10\x0c\x12\r\n\tPOST_GAME\x10\r"\x96\x03\n\x07Command\x12\x08\n\x04HALT\x10\x00\x12\x08\n\x04STOP\x10\x01\x12\x10\n\x0cNORMAL_START\x10\x02\x12\x0f\n\x0bFORCE_START\x10\x03\x12\x1a\n\x16PREPARE_KICKOFF_YELLOW\x10\x04\x12\x18\n\x14PREPARE_KICKOFF_BLUE\x10\x05\x12\x1a\n\x16PREPARE_PENALTY_YELLOW\x10\x06\x12\x18\n\x14PREPARE_PENALTY_BLUE\x10\x07\x12\x16\n\x12DIRECT_FREE_YELLOW\x10\x08\x12\x14\n\x10DIRECT_FREE_BLUE\x10\t\x12\x1c\n\x14INDIRECT_FREE_YELLOW\x10\n\x1a\x02\x08\x01\x12\x1a\n\x12INDIRECT_FREE_BLUE\x10\x0b\x1a\x02\x08\x01\x12\x12\n\x0eTIMEOUT_YELLOW\x10\x0c\x12\x10\n\x0cTIMEOUT_BLUE\x10\r\x12\x13\n\x0bGOAL_YELLOW\x10\x0e\x1a\x02\x08\x01\x12\x11\n\tGOAL_BLUE\x10\x0f\x1a\x02\x08\x01\x12\x19\n\x15BALL_PLACEMENT_YELLOW\x10\x10\x12\x17\n\x13BALL_PLACEMENT_BLUE\x10\x11J\x04\x08\x0b\x10\x0cJ\x04\x08\r\x10\x0eJ\x04\x08\x0e\x10\x0f"W\n\x16GameEventProposalGroup\x12\n\n\x02id\x18\x03 \x01(\t\x12\x1f\n\x0bgame_events\x18\x01 \x03(\x0b2\n.GameEvent\x12\x10\n\x08accepted\x18\x02 \x01(\x08*T\n\tMatchType\x12\x11\n\rUNKNOWN_MATCH\x10\x00\x12\x0f\n\x0bGROUP_PHASE\x10\x01\x12\x15\n\x11ELIMINATION_PHASE\x10\x02\x12\x0c\n\x08FRIENDLY\x10\x03*N\n\tHullColor\x12\x16\n\x12HULL_COLOR_UNKNOWN\x10\x00\x12\x13\n\x0fHULL_COLOR_DARK\x10\x01\x12\x14\n\x10HULL_COLOR_LIGHT\x10\x02')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'state.ssl_gc_referee_message_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _REFEREE_TEAMINFO.fields_by_name['yellow_card_times']._options = None
    _REFEREE_TEAMINFO.fields_by_name['yellow_card_times']._serialized_options = b'\x10\x01'
    _REFEREE_COMMAND.values_by_name['INDIRECT_FREE_YELLOW']._options = None
    _REFEREE_COMMAND.values_by_name['INDIRECT_FREE_YELLOW']._serialized_options = b'\x08\x01'
    _REFEREE_COMMAND.values_by_name['INDIRECT_FREE_BLUE']._options = None
    _REFEREE_COMMAND.values_by_name['INDIRECT_FREE_BLUE']._serialized_options = b'\x08\x01'
    _REFEREE_COMMAND.values_by_name['GOAL_YELLOW']._options = None
    _REFEREE_COMMAND.values_by_name['GOAL_YELLOW']._serialized_options = b'\x08\x01'
    _REFEREE_COMMAND.values_by_name['GOAL_BLUE']._options = None
    _REFEREE_COMMAND.values_by_name['GOAL_BLUE']._serialized_options = b'\x08\x01'
    _MATCHTYPE._serialized_start = 2038
    _MATCHTYPE._serialized_end = 2122
    _HULLCOLOR._serialized_start = 2124
    _HULLCOLOR._serialized_end = 2202
    _REFEREE._serialized_start = 70
    _REFEREE._serialized_end = 1947
    _REFEREE_TEAMINFO._serialized_start = 665
    _REFEREE_TEAMINFO._serialized_end = 1149
    _REFEREE_POINT._serialized_start = 1151
    _REFEREE_POINT._serialized_end = 1180
    _REFEREE_STAGE._serialized_start = 1183
    _REFEREE_STAGE._serialized_end = 1520
    _REFEREE_COMMAND._serialized_start = 1523
    _REFEREE_COMMAND._serialized_end = 1929
    _GAMEEVENTPROPOSALGROUP._serialized_start = 1949
    _GAMEEVENTPROPOSALGROUP._serialized_end = 2036