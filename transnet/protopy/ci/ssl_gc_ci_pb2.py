"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ..tracker import ssl_vision_wrapper_tracked_pb2 as tracker_dot_ssl__vision__wrapper__tracked__pb2
from ..api import ssl_gc_api_pb2 as api_dot_ssl__gc__api__pb2
from ..state import ssl_gc_referee_message_pb2 as state_dot_ssl__gc__referee__message__pb2
from ..vision import ssl_vision_geometry_pb2 as vision_dot_ssl__vision__geometry__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12ci/ssl_gc_ci.proto\x1a(tracker/ssl_vision_wrapper_tracked.proto\x1a\x14api/ssl_gc_api.proto\x1a"state/ssl_gc_referee_message.proto\x1a vision/ssl_vision_geometry.proto"\x8c\x01\n\x07CiInput\x12\x11\n\ttimestamp\x18\x01 \x01(\x03\x12-\n\x0etracker_packet\x18\x02 \x01(\x0b2\x15.TrackerWrapperPacket\x12\x1a\n\napi_inputs\x18\x03 \x03(\x0b2\x06.Input\x12#\n\x08geometry\x18\x04 \x01(\x0b2\x11.SSL_GeometryData")\n\x08CiOutput\x12\x1d\n\x0breferee_msg\x18\x01 \x01(\x0b2\x08.Referee')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ci.ssl_gc_ci_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _CIINPUT._serialized_start = 157
    _CIINPUT._serialized_end = 297
    _CIOUTPUT._serialized_start = 299
    _CIOUTPUT._serialized_end = 340