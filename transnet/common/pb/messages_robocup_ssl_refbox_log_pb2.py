"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from . import messages_robocup_ssl_detection_pb2 as messages__robocup__ssl__detection__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%messages_robocup_ssl_refbox_log.proto\x1a$messages_robocup_ssl_detection.proto"C\n\tLog_Frame\x12"\n\x05frame\x18\x01 \x02(\x0b2\x13.SSL_DetectionFrame\x12\x12\n\nrefbox_cmd\x18\x02 \x02(\t"%\n\nRefbox_Log\x12\x17\n\x03log\x18\x01 \x03(\x0b2\n.Log_Frame')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messages_robocup_ssl_refbox_log_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _LOG_FRAME._serialized_start = 79
    _LOG_FRAME._serialized_end = 146
    _REFBOX_LOG._serialized_start = 148
    _REFBOX_LOG._serialized_end = 185