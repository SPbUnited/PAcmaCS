"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ..state import ssl_gc_state_pb2 as state_dot_ssl__gc__state__pb2
from ..state import ssl_gc_common_pb2 as state_dot_ssl__gc__common__pb2
from ..geom import ssl_gc_geometry_pb2 as geom_dot_ssl__gc__geometry__pb2
from ..state import ssl_gc_game_event_pb2 as state_dot_ssl__gc__game__event__pb2
from ..state import ssl_gc_referee_message_pb2 as state_dot_ssl__gc__referee__message__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n statemachine/ssl_gc_change.proto\x1a\x18state/ssl_gc_state.proto\x1a\x19state/ssl_gc_common.proto\x1a\x1ageom/ssl_gc_geometry.proto\x1a\x1dstate/ssl_gc_game_event.proto\x1a"state/ssl_gc_referee_message.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/wrappers.proto"\x93\x01\n\x0bStateChange\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x19\n\tstate_pre\x18\x02 \x01(\x0b2\x06.State\x12\x15\n\x05state\x18\x03 \x01(\x0b2\x06.State\x12\x17\n\x06change\x18\x04 \x01(\x0b2\x07.Change\x12-\n\ttimestamp\x18\x05 \x01(\x0b2\x1a.google.protobuf.Timestamp"\xf4\x16\n\x06Change\x12\x0e\n\x06origin\x18\x01 \x01(\t\x12\x12\n\nrevertible\x18\x10 \x01(\x08\x120\n\x12new_command_change\x18\x02 \x01(\x0b2\x12.Change.NewCommandH\x00\x122\n\x13change_stage_change\x18\x03 \x01(\x0b2\x13.Change.ChangeStageH\x00\x12D\n\x1dset_ball_placement_pos_change\x18\x04 \x01(\x0b2\x1b.Change.SetBallPlacementPosH\x00\x127\n\x16add_yellow_card_change\x18\x05 \x01(\x0b2\x15.Change.AddYellowCardH\x00\x121\n\x13add_red_card_change\x18\x06 \x01(\x0b2\x12.Change.AddRedCardH\x00\x129\n\x17yellow_card_over_change\x18\x07 \x01(\x0b2\x16.Change.YellowCardOverH\x00\x125\n\x15add_game_event_change\x18\x08 \x01(\x0b2\x14.Change.AddGameEventH\x00\x12D\n\x1dadd_passive_game_event_change\x18\x13 \x01(\x0b2\x1b.Change.AddPassiveGameEventH\x00\x122\n\x13add_proposal_change\x18\t \x01(\x0b2\x13.Change.AddProposalH\x00\x124\n\x14update_config_change\x18\x0c \x01(\x0b2\x14.Change.UpdateConfigH\x00\x12;\n\x18update_team_state_change\x18\r \x01(\x0b2\x17.Change.UpdateTeamStateH\x00\x124\n\x14switch_colors_change\x18\x0e \x01(\x0b2\x14.Change.SwitchColorsH\x00\x12\'\n\rrevert_change\x18\x0f \x01(\x0b2\x0e.Change.RevertH\x00\x125\n\x15new_game_state_change\x18\x11 \x01(\x0b2\x14.Change.NewGameStateH\x00\x12C\n\x1caccept_proposal_group_change\x18\x12 \x01(\x0b2\x1b.Change.AcceptProposalGroupH\x00\x12=\n\x19set_status_message_change\x18\x14 \x01(\x0b2\x18.Change.SetStatusMessageH\x00\x1a\'\n\nNewCommand\x12\x19\n\x07command\x18\x01 \x01(\x0b2\x08.Command\x1a0\n\x0bChangeStage\x12!\n\tnew_stage\x18\x01 \x01(\x0e2\x0e.Referee.Stage\x1a,\n\x13SetBallPlacementPos\x12\x15\n\x03pos\x18\x01 \x01(\x0b2\x08.Vector2\x1aR\n\rAddYellowCard\x12\x17\n\x08for_team\x18\x01 \x01(\x0e2\x05.Team\x12(\n\x14caused_by_game_event\x18\x02 \x01(\x0b2\n.GameEvent\x1aO\n\nAddRedCard\x12\x17\n\x08for_team\x18\x01 \x01(\x0e2\x05.Team\x12(\n\x14caused_by_game_event\x18\x02 \x01(\x0b2\n.GameEvent\x1a)\n\x0eYellowCardOver\x12\x17\n\x08for_team\x18\x01 \x01(\x0e2\x05.Team\x1a.\n\x0cAddGameEvent\x12\x1e\n\ngame_event\x18\x01 \x01(\x0b2\n.GameEvent\x1a5\n\x13AddPassiveGameEvent\x12\x1e\n\ngame_event\x18\x01 \x01(\x0b2\n.GameEvent\x1a*\n\x0bAddProposal\x12\x1b\n\x08proposal\x18\x01 \x01(\x0b2\t.Proposal\x1a<\n\x13AcceptProposalGroup\x12\x10\n\x08group_id\x18\x03 \x01(\t\x12\x13\n\x0baccepted_by\x18\x02 \x01(\t\x1a\xae\x01\n\x0cUpdateConfig\x12\x1b\n\x08division\x18\x01 \x01(\x0e2\t.Division\x12!\n\x12first_kickoff_team\x18\x02 \x01(\x0e2\x05.Team\x12\x1e\n\nmatch_type\x18\x04 \x01(\x0e2\n.MatchType\x128\n\x13max_robots_per_team\x18\x05 \x01(\x0b2\x1b.google.protobuf.Int32ValueJ\x04\x08\x03\x10\x04\x1a\xc6\x08\n\x0fUpdateTeamState\x12\x17\n\x08for_team\x18\x01 \x01(\x0e2\x05.Team\x12/\n\tteam_name\x18\x02 \x01(\x0b2\x1c.google.protobuf.StringValue\x12*\n\x05goals\x18\x03 \x01(\x0b2\x1b.google.protobuf.Int32Value\x12/\n\ngoalkeeper\x18\x04 \x01(\x0b2\x1b.google.protobuf.Int32Value\x122\n\rtimeouts_left\x18\x05 \x01(\x0b2\x1b.google.protobuf.Int32Value\x127\n\x11timeout_time_left\x18\x06 \x01(\x0b2\x1c.google.protobuf.StringValue\x124\n\x10on_positive_half\x18\x07 \x01(\x0b2\x1a.google.protobuf.BoolValue\x12<\n\x17ball_placement_failures\x18\x08 \x01(\x0b2\x1b.google.protobuf.Int32Value\x122\n\x0ecan_place_ball\x18\t \x01(\x0b2\x1a.google.protobuf.BoolValue\x129\n\x14challenge_flags_left\x18\x15 \x01(\x0b2\x1b.google.protobuf.Int32Value\x12;\n\x16bot_substitutions_left\x18\x16 \x01(\x0b2\x1b.google.protobuf.Int32Value\x12=\n\x19requests_bot_substitution\x18\n \x01(\x0b2\x1a.google.protobuf.BoolValue\x124\n\x10requests_timeout\x18\x11 \x01(\x0b2\x1a.google.protobuf.BoolValue\x126\n\x12requests_challenge\x18\x12 \x01(\x0b2\x1a.google.protobuf.BoolValue\x12;\n\x17requests_emergency_stop\x18\x13 \x01(\x0b2\x1a.google.protobuf.BoolValue\x12 \n\x0byellow_card\x18\x14 \x01(\x0b2\x0b.YellowCard\x12\x1a\n\x08red_card\x18\x0c \x01(\x0b2\x08.RedCard\x12\x13\n\x04foul\x18\r \x01(\x0b2\x05.Foul\x128\n\x12remove_yellow_card\x18\x0e \x01(\x0b2\x1c.google.protobuf.UInt32Value\x125\n\x0fremove_red_card\x18\x0f \x01(\x0b2\x1c.google.protobuf.UInt32Value\x121\n\x0bremove_foul\x18\x10 \x01(\x0b2\x1c.google.protobuf.UInt32Value\x12\x1e\n\nhull_color\x18\x17 \x01(\x0e2\n.HullColor\x1a\x0e\n\x0cSwitchColors\x1a\x1b\n\x06Revert\x12\x11\n\tchange_id\x18\x01 \x01(\x05\x1a.\n\x0cNewGameState\x12\x1e\n\ngame_state\x18\x01 \x01(\x0b2\n.GameState\x1a*\n\x10SetStatusMessage\x12\x16\n\x0estatus_message\x18\x01 \x01(\tB\x08\n\x06change')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'statemachine.ssl_gc_change_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _STATECHANGE._serialized_start = 250
    _STATECHANGE._serialized_end = 397
    _CHANGE._serialized_start = 400
    _CHANGE._serialized_end = 3332
    _CHANGE_NEWCOMMAND._serialized_start = 1359
    _CHANGE_NEWCOMMAND._serialized_end = 1398
    _CHANGE_CHANGESTAGE._serialized_start = 1400
    _CHANGE_CHANGESTAGE._serialized_end = 1448
    _CHANGE_SETBALLPLACEMENTPOS._serialized_start = 1450
    _CHANGE_SETBALLPLACEMENTPOS._serialized_end = 1494
    _CHANGE_ADDYELLOWCARD._serialized_start = 1496
    _CHANGE_ADDYELLOWCARD._serialized_end = 1578
    _CHANGE_ADDREDCARD._serialized_start = 1580
    _CHANGE_ADDREDCARD._serialized_end = 1659
    _CHANGE_YELLOWCARDOVER._serialized_start = 1661
    _CHANGE_YELLOWCARDOVER._serialized_end = 1702
    _CHANGE_ADDGAMEEVENT._serialized_start = 1704
    _CHANGE_ADDGAMEEVENT._serialized_end = 1750
    _CHANGE_ADDPASSIVEGAMEEVENT._serialized_start = 1752
    _CHANGE_ADDPASSIVEGAMEEVENT._serialized_end = 1805
    _CHANGE_ADDPROPOSAL._serialized_start = 1807
    _CHANGE_ADDPROPOSAL._serialized_end = 1849
    _CHANGE_ACCEPTPROPOSALGROUP._serialized_start = 1851
    _CHANGE_ACCEPTPROPOSALGROUP._serialized_end = 1911
    _CHANGE_UPDATECONFIG._serialized_start = 1914
    _CHANGE_UPDATECONFIG._serialized_end = 2088
    _CHANGE_UPDATETEAMSTATE._serialized_start = 2091
    _CHANGE_UPDATETEAMSTATE._serialized_end = 3185
    _CHANGE_SWITCHCOLORS._serialized_start = 3187
    _CHANGE_SWITCHCOLORS._serialized_end = 3201
    _CHANGE_REVERT._serialized_start = 3203
    _CHANGE_REVERT._serialized_end = 3230
    _CHANGE_NEWGAMESTATE._serialized_start = 3232
    _CHANGE_NEWGAMESTATE._serialized_end = 3278
    _CHANGE_SETSTATUSMESSAGE._serialized_start = 3280
    _CHANGE_SETSTATUSMESSAGE._serialized_end = 3322