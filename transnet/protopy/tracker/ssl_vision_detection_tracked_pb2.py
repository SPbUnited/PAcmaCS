"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ..state import ssl_gc_common_pb2 as state_dot_ssl__gc__common__pb2
from ..geom import ssl_gc_geometry_pb2 as geom_dot_ssl__gc__geometry__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*tracker/ssl_vision_detection_tracked.proto\x1a\x19state/ssl_gc_common.proto\x1a\x1ageom/ssl_gc_geometry.proto"O\n\x0bTrackedBall\x12\x15\n\x03pos\x18\x01 \x02(\x0b2\x08.Vector3\x12\x15\n\x03vel\x18\x02 \x01(\x0b2\x08.Vector3\x12\x12\n\nvisibility\x18\x03 \x01(\x02"\xa3\x01\n\nKickedBall\x12\x15\n\x03pos\x18\x01 \x02(\x0b2\x08.Vector2\x12\x15\n\x03vel\x18\x02 \x02(\x0b2\x08.Vector3\x12\x17\n\x0fstart_timestamp\x18\x03 \x02(\x01\x12\x16\n\x0estop_timestamp\x18\x04 \x01(\x01\x12\x1a\n\x08stop_pos\x18\x05 \x01(\x0b2\x08.Vector2\x12\x1a\n\x08robot_id\x18\x06 \x01(\x0b2\x08.RobotId"\x96\x01\n\x0cTrackedRobot\x12\x1a\n\x08robot_id\x18\x01 \x02(\x0b2\x08.RobotId\x12\x15\n\x03pos\x18\x02 \x02(\x0b2\x08.Vector2\x12\x13\n\x0borientation\x18\x03 \x02(\x02\x12\x15\n\x03vel\x18\x04 \x01(\x0b2\x08.Vector2\x12\x13\n\x0bvel_angular\x18\x05 \x01(\x02\x12\x12\n\nvisibility\x18\x06 \x01(\x02"\xb8\x01\n\x0cTrackedFrame\x12\x14\n\x0cframe_number\x18\x01 \x02(\r\x12\x11\n\ttimestamp\x18\x02 \x02(\x01\x12\x1b\n\x05balls\x18\x03 \x03(\x0b2\x0c.TrackedBall\x12\x1d\n\x06robots\x18\x04 \x03(\x0b2\r.TrackedRobot\x12 \n\x0bkicked_ball\x18\x05 \x01(\x0b2\x0b.KickedBall\x12!\n\x0ccapabilities\x18\x06 \x03(\x0e2\x0b.Capability*\x92\x01\n\nCapability\x12\x16\n\x12CAPABILITY_UNKNOWN\x10\x00\x12"\n\x1eCAPABILITY_DETECT_FLYING_BALLS\x10\x01\x12$\n CAPABILITY_DETECT_MULTIPLE_BALLS\x10\x02\x12"\n\x1eCAPABILITY_DETECT_KICKED_BALLS\x10\x03')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tracker.ssl_vision_detection_tracked_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _CAPABILITY._serialized_start = 689
    _CAPABILITY._serialized_end = 835
    _TRACKEDBALL._serialized_start = 101
    _TRACKEDBALL._serialized_end = 180
    _KICKEDBALL._serialized_start = 183
    _KICKEDBALL._serialized_end = 346
    _TRACKEDROBOT._serialized_start = 349
    _TRACKEDROBOT._serialized_end = 499
    _TRACKEDFRAME._serialized_start = 502
    _TRACKEDFRAME._serialized_end = 686