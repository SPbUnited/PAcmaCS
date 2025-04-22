"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19state/ssl_gc_common.proto"*\n\x07RobotId\x12\n\n\x02id\x18\x01 \x01(\r\x12\x13\n\x04team\x18\x02 \x01(\x0e2\x05.Team*)\n\x04Team\x12\x0b\n\x07UNKNOWN\x10\x00\x12\n\n\x06YELLOW\x10\x01\x12\x08\n\x04BLUE\x10\x02*1\n\x08Division\x12\x0f\n\x0bDIV_UNKNOWN\x10\x00\x12\t\n\x05DIV_A\x10\x01\x12\t\n\x05DIV_B\x10\x02')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'state.ssl_gc_common_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _TEAM._serialized_start = 73
    _TEAM._serialized_end = 114
    _DIVISION._serialized_start = 116
    _DIVISION._serialized_end = 165
    _ROBOTID._serialized_start = 29
    _ROBOTID._serialized_end = 71