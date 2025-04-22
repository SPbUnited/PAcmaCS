"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16rcon/ssl_gc_rcon.proto"\xa1\x02\n\x0fControllerReply\x120\n\x0bstatus_code\x18\x01 \x01(\x0e2\x1b.ControllerReply.StatusCode\x12\x0e\n\x06reason\x18\x02 \x01(\t\x12\x12\n\nnext_token\x18\x03 \x01(\t\x123\n\x0cverification\x18\x04 \x01(\x0e2\x1d.ControllerReply.Verification";\n\nStatusCode\x12\x17\n\x13UNKNOWN_STATUS_CODE\x10\x00\x12\x06\n\x02OK\x10\x01\x12\x0c\n\x08REJECTED\x10\x02"F\n\x0cVerification\x12\x18\n\x14UNKNOWN_VERIFICATION\x10\x00\x12\x0c\n\x08VERIFIED\x10\x01\x12\x0e\n\nUNVERIFIED\x10\x02",\n\tSignature\x12\r\n\x05token\x18\x01 \x02(\t\x12\x10\n\x08pkcs1v15\x18\x02 \x02(\x0c')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'rcon.ssl_gc_rcon_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _CONTROLLERREPLY._serialized_start = 27
    _CONTROLLERREPLY._serialized_end = 316
    _CONTROLLERREPLY_STATUSCODE._serialized_start = 185
    _CONTROLLERREPLY_STATUSCODE._serialized_end = 244
    _CONTROLLERREPLY_VERIFICATION._serialized_start = 246
    _CONTROLLERREPLY_VERIFICATION._serialized_end = 316
    _SIGNATURE._serialized_start = 318
    _SIGNATURE._serialized_end = 362