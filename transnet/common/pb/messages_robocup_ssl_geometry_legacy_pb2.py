"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from . import messages_robocup_ssl_geometry_pb2 as messages__robocup__ssl__geometry__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*messages_robocup_ssl_geometry_legacy.proto\x12\x1aRoboCup2014Legacy.Geometry\x1a#messages_robocup_ssl_geometry.proto"\x8a\x03\n\x15SSL_GeometryFieldSize\x12\x12\n\nline_width\x18\x01 \x02(\x05\x12\x14\n\x0cfield_length\x18\x02 \x02(\x05\x12\x13\n\x0bfield_width\x18\x03 \x02(\x05\x12\x16\n\x0eboundary_width\x18\x04 \x02(\x05\x12\x15\n\rreferee_width\x18\x05 \x02(\x05\x12\x12\n\ngoal_width\x18\x06 \x02(\x05\x12\x12\n\ngoal_depth\x18\x07 \x02(\x05\x12\x17\n\x0fgoal_wall_width\x18\x08 \x02(\x05\x12\x1c\n\x14center_circle_radius\x18\t \x02(\x05\x12\x16\n\x0edefense_radius\x18\n \x02(\x05\x12\x17\n\x0fdefense_stretch\x18\x0b \x02(\x05\x12#\n\x1bfree_kick_from_defense_dist\x18\x0c \x02(\x05\x12)\n!penalty_spot_from_field_line_dist\x18\r \x02(\x05\x12#\n\x1bpenalty_line_from_spot_dist\x18\x0e \x02(\x05"\x83\x01\n\x10SSL_GeometryData\x12@\n\x05field\x18\x01 \x02(\x0b21.RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize\x12-\n\x05calib\x18\x02 \x03(\x0b2\x1e.SSL_GeometryCameraCalibration')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messages_robocup_ssl_geometry_legacy_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _SSL_GEOMETRYFIELDSIZE._serialized_start = 112
    _SSL_GEOMETRYFIELDSIZE._serialized_end = 506
    _SSL_GEOMETRYDATA._serialized_start = 509
    _SSL_GEOMETRYDATA._serialized_end = 640