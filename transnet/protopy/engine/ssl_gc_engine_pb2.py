"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ..geom import ssl_gc_geometry_pb2 as geom_dot_ssl__gc__geometry__pb2
from ..state import ssl_gc_common_pb2 as state_dot_ssl__gc__common__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1aengine/ssl_gc_engine.proto\x1a\x1ageom/ssl_gc_geometry.proto\x1a\x19state/ssl_gc_common.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\x9d\x03\n\x07GcState\x12+\n\nteam_state\x18\x01 \x03(\x0b2\x17.GcState.TeamStateEntry\x122\n\x0eauto_ref_state\x18\x02 \x03(\x0b2\x1a.GcState.AutoRefStateEntry\x12(\n\x08trackers\x18\x03 \x03(\x0b2\x16.GcState.TrackersEntry\x12)\n\x10continue_actions\x18\x04 \x03(\x0b2\x0f.ContinueAction\x12%\n\x0econtinue_hints\x18\x05 \x03(\x0b2\r.ContinueHint\x1a>\n\x0eTeamStateEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1b\n\x05value\x18\x02 \x01(\x0b2\x0c.GcStateTeam:\x028\x01\x1aD\n\x11AutoRefStateEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1e\n\x05value\x18\x02 \x01(\x0b2\x0f.GcStateAutoRef:\x028\x01\x1a/\n\rTrackersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x028\x01"\xbb\x01\n\x0bGcStateTeam\x12\x11\n\tconnected\x18\x01 \x01(\x08\x12\x1b\n\x13connection_verified\x18\x02 \x01(\x08\x12 \n\x18remote_control_connected\x18\x03 \x01(\x08\x12*\n"remote_control_connection_verified\x18\x04 \x01(\x08\x12.\n\x10advantage_choice\x18\x05 \x01(\x0b2\x14.TeamAdvantageChoice"v\n\x13TeamAdvantageChoice\x124\n\x06choice\x18\x01 \x01(\x0e2$.TeamAdvantageChoice.AdvantageChoice")\n\x0fAdvantageChoice\x12\x08\n\x04STOP\x10\x00\x12\x0c\n\x08CONTINUE\x10\x01"-\n\x0eGcStateAutoRef\x12\x1b\n\x13connection_verified\x18\x01 \x01(\x08"`\n\x0eGcStateTracker\x12\x13\n\x0bsource_name\x18\x01 \x01(\t\x12\x0c\n\x04uuid\x18\x04 \x01(\t\x12\x13\n\x04ball\x18\x02 \x01(\x0b2\x05.Ball\x12\x16\n\x06robots\x18\x03 \x03(\x0b2\x06.Robot"4\n\x04Ball\x12\x15\n\x03pos\x18\x01 \x01(\x0b2\x08.Vector3\x12\x15\n\x03vel\x18\x02 \x01(\x0b2\x08.Vector3"4\n\x05Robot\x12\x14\n\x02id\x18\x01 \x01(\x0b2\x08.RobotId\x12\x15\n\x03pos\x18\x02 \x01(\x0b2\x08.Vector2"\xc4\x05\n\x0eContinueAction\x12"\n\x04type\x18\x01 \x02(\x0e2\x14.ContinueAction.Type\x12\x17\n\x08for_team\x18\x02 \x02(\x0e2\x05.Team\x12\x1b\n\x13continuation_issues\x18\x03 \x03(\t\x12,\n\x08ready_at\x18\x04 \x01(\x0b2\x1a.google.protobuf.Timestamp\x12$\n\x05state\x18\x05 \x01(\x0e2\x15.ContinueAction.State"\x9d\x03\n\x04Type\x12\x10\n\x0cTYPE_UNKNOWN\x10\x00\x12\x08\n\x04HALT\x10\x01\x12\x14\n\x10RESUME_FROM_HALT\x10\n\x12\r\n\tSTOP_GAME\x10\x02\x12\x0f\n\x0bFORCE_START\x10\x0b\x12\r\n\tFREE_KICK\x10\x11\x12\x10\n\x0cNEXT_COMMAND\x10\x03\x12\x18\n\x14BALL_PLACEMENT_START\x10\x04\x12\x19\n\x15BALL_PLACEMENT_CANCEL\x10\t\x12\x1b\n\x17BALL_PLACEMENT_COMPLETE\x10\x0e\x12\x17\n\x13BALL_PLACEMENT_FAIL\x10\x0f\x12\x11\n\rTIMEOUT_START\x10\x05\x12\x10\n\x0cTIMEOUT_STOP\x10\x06\x12\x14\n\x10BOT_SUBSTITUTION\x10\x07\x12\x0e\n\nNEXT_STAGE\x10\x08\x12\x0c\n\x08END_GAME\x10\x10\x12\x0f\n\x0bACCEPT_GOAL\x10\x0c\x12\x0f\n\x0bREJECT_GOAL\x10\x14\x12\x10\n\x0cNORMAL_START\x10\r\x12\x14\n\x10CHALLENGE_ACCEPT\x10\x12\x12\x14\n\x10CHALLENGE_REJECT\x10\x13"d\n\x05State\x12\x11\n\rSTATE_UNKNOWN\x10\x00\x12\x0b\n\x07BLOCKED\x10\x01\x12\x0b\n\x07WAITING\x10\x02\x12\x0e\n\nREADY_AUTO\x10\x03\x12\x10\n\x0cREADY_MANUAL\x10\x04\x12\x0c\n\x08DISABLED\x10\x05"\x1f\n\x0cContinueHint\x12\x0f\n\x07message\x18\x01 \x02(\t')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'engine.ssl_gc_engine_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _GCSTATE_TEAMSTATEENTRY._options = None
    _GCSTATE_TEAMSTATEENTRY._serialized_options = b'8\x01'
    _GCSTATE_AUTOREFSTATEENTRY._options = None
    _GCSTATE_AUTOREFSTATEENTRY._serialized_options = b'8\x01'
    _GCSTATE_TRACKERSENTRY._options = None
    _GCSTATE_TRACKERSENTRY._serialized_options = b'8\x01'
    _GCSTATE._serialized_start = 119
    _GCSTATE._serialized_end = 532
    _GCSTATE_TEAMSTATEENTRY._serialized_start = 351
    _GCSTATE_TEAMSTATEENTRY._serialized_end = 413
    _GCSTATE_AUTOREFSTATEENTRY._serialized_start = 415
    _GCSTATE_AUTOREFSTATEENTRY._serialized_end = 483
    _GCSTATE_TRACKERSENTRY._serialized_start = 485
    _GCSTATE_TRACKERSENTRY._serialized_end = 532
    _GCSTATETEAM._serialized_start = 535
    _GCSTATETEAM._serialized_end = 722
    _TEAMADVANTAGECHOICE._serialized_start = 724
    _TEAMADVANTAGECHOICE._serialized_end = 842
    _TEAMADVANTAGECHOICE_ADVANTAGECHOICE._serialized_start = 801
    _TEAMADVANTAGECHOICE_ADVANTAGECHOICE._serialized_end = 842
    _GCSTATEAUTOREF._serialized_start = 844
    _GCSTATEAUTOREF._serialized_end = 889
    _GCSTATETRACKER._serialized_start = 891
    _GCSTATETRACKER._serialized_end = 987
    _BALL._serialized_start = 989
    _BALL._serialized_end = 1041
    _ROBOT._serialized_start = 1043
    _ROBOT._serialized_end = 1095
    _CONTINUEACTION._serialized_start = 1098
    _CONTINUEACTION._serialized_end = 1806
    _CONTINUEACTION_TYPE._serialized_start = 1291
    _CONTINUEACTION_TYPE._serialized_end = 1704
    _CONTINUEACTION_STATE._serialized_start = 1706
    _CONTINUEACTION_STATE._serialized_end = 1806
    _CONTINUEHINT._serialized_start = 1808
    _CONTINUEHINT._serialized_end = 1839