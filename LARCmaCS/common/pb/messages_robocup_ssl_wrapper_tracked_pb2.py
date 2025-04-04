"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from . import messages_robocup_ssl_detection_tracked_pb2 as messages__robocup__ssl__detection__tracked__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*messages_robocup_ssl_wrapper_tracked.proto\x1a,messages_robocup_ssl_detection_tracked.proto"_\n\x14TrackerWrapperPacket\x12\x0c\n\x04uuid\x18\x01 \x02(\t\x12\x13\n\x0bsource_name\x18\x02 \x01(\t\x12$\n\rtracked_frame\x18\x03 \x01(\x0b2\r.TrackedFrame')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messages_robocup_ssl_wrapper_tracked_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _TRACKERWRAPPERPACKET._serialized_start = 92
    _TRACKERWRAPPERPACKET._serialized_end = 187