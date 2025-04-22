"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dgrsim/grSim_Robotstatus.proto"5\n\rRobots_Status\x12$\n\rrobots_status\x18\x01 \x03(\x0b2\r.Robot_Status"X\n\x0cRobot_Status\x12\x10\n\x08robot_id\x18\x01 \x02(\x05\x12\x10\n\x08infrared\x18\x02 \x02(\x08\x12\x11\n\tflat_kick\x18\x03 \x02(\x08\x12\x11\n\tchip_kick\x18\x04 \x02(\x08')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'grsim.grSim_Robotstatus_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _ROBOTS_STATUS._serialized_start = 33
    _ROBOTS_STATUS._serialized_end = 86
    _ROBOT_STATUS._serialized_start = 88
    _ROBOT_STATUS._serialized_end = 176