"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from . import messages_robocup_ssl_detection_pb2 as messages__robocup__ssl__detection__pb2
from . import messages_robocup_ssl_geometry_pb2 as messages__robocup__ssl__geometry__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n"messages_robocup_ssl_wrapper.proto\x1a$messages_robocup_ssl_detection.proto\x1a#messages_robocup_ssl_geometry.proto"`\n\x11SSL_WrapperPacket\x12&\n\tdetection\x18\x01 \x01(\x0b2\x13.SSL_DetectionFrame\x12#\n\x08geometry\x18\x02 \x01(\x0b2\x11.SSL_GeometryData')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messages_robocup_ssl_wrapper_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _SSL_WRAPPERPACKET._serialized_start = 113
    _SSL_WRAPPERPACKET._serialized_end = 209