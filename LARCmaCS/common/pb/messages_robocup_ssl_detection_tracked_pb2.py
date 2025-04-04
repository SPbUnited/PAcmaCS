"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,messages_robocup_ssl_detection_tracked.proto"\x1f\n\x07Vector2\x12\t\n\x01x\x18\x01 \x02(\x02\x12\t\n\x01y\x18\x02 \x02(\x02"*\n\x07Vector3\x12\t\n\x01x\x18\x01 \x02(\x02\x12\t\n\x01y\x18\x02 \x02(\x02\x12\t\n\x01z\x18\x03 \x02(\x02"5\n\x07RobotId\x12\n\n\x02id\x18\x01 \x02(\r\x12\x1e\n\nteam_color\x18\x02 \x02(\x0e2\n.TeamColor"O\n\x0bTrackedBall\x12\x15\n\x03pos\x18\x01 \x02(\x0b2\x08.Vector3\x12\x15\n\x03vel\x18\x02 \x01(\x0b2\x08.Vector3\x12\x12\n\nvisibility\x18\x03 \x01(\x02"\xa3\x01\n\nKickedBall\x12\x15\n\x03pos\x18\x01 \x02(\x0b2\x08.Vector2\x12\x15\n\x03vel\x18\x02 \x02(\x0b2\x08.Vector3\x12\x17\n\x0fstart_timestamp\x18\x03 \x02(\x01\x12\x16\n\x0estop_timestamp\x18\x04 \x01(\x01\x12\x1a\n\x08stop_pos\x18\x05 \x01(\x0b2\x08.Vector2\x12\x1a\n\x08robot_id\x18\x06 \x01(\x0b2\x08.RobotId"\x96\x01\n\x0cTrackedRobot\x12\x1a\n\x08robot_id\x18\x01 \x02(\x0b2\x08.RobotId\x12\x15\n\x03pos\x18\x02 \x02(\x0b2\x08.Vector2\x12\x13\n\x0borientation\x18\x03 \x02(\x02\x12\x15\n\x03vel\x18\x04 \x01(\x0b2\x08.Vector2\x12\x13\n\x0bvel_angular\x18\x05 \x01(\x02\x12\x12\n\nvisibility\x18\x06 \x01(\x02"\xb8\x01\n\x0cTrackedFrame\x12\x14\n\x0cframe_number\x18\x01 \x02(\r\x12\x11\n\ttimestamp\x18\x02 \x02(\x01\x12\x1b\n\x05balls\x18\x03 \x03(\x0b2\x0c.TrackedBall\x12\x1d\n\x06robots\x18\x04 \x03(\x0b2\r.TrackedRobot\x12 \n\x0bkicked_ball\x18\x05 \x01(\x0b2\x0b.KickedBall\x12!\n\x0ccapabilities\x18\x06 \x03(\x0e2\x0b.Capability*O\n\tTeamColor\x12\x16\n\x12TEAM_COLOR_UNKNOWN\x10\x00\x12\x15\n\x11TEAM_COLOR_YELLOW\x10\x01\x12\x13\n\x0fTEAM_COLOR_BLUE\x10\x02*\x92\x01\n\nCapability\x12\x16\n\x12CAPABILITY_UNKNOWN\x10\x00\x12"\n\x1eCAPABILITY_DETECT_FLYING_BALLS\x10\x01\x12$\n CAPABILITY_DETECT_MULTIPLE_BALLS\x10\x02\x12"\n\x1eCAPABILITY_DETECT_KICKED_BALLS\x10\x03')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messages_robocup_ssl_detection_tracked_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _TEAMCOLOR._serialized_start = 767
    _TEAMCOLOR._serialized_end = 846
    _CAPABILITY._serialized_start = 849
    _CAPABILITY._serialized_end = 995
    _VECTOR2._serialized_start = 48
    _VECTOR2._serialized_end = 79
    _VECTOR3._serialized_start = 81
    _VECTOR3._serialized_end = 123
    _ROBOTID._serialized_start = 125
    _ROBOTID._serialized_end = 178
    _TRACKEDBALL._serialized_start = 180
    _TRACKEDBALL._serialized_end = 259
    _KICKEDBALL._serialized_start = 262
    _KICKEDBALL._serialized_end = 425
    _TRACKEDROBOT._serialized_start = 428
    _TRACKEDROBOT._serialized_end = 578
    _TRACKEDFRAME._serialized_start = 581
    _TRACKEDFRAME._serialized_end = 765