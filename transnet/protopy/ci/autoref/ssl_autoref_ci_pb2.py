"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ...tracker import ssl_vision_wrapper_tracked_pb2 as tracker_dot_ssl__vision__wrapper__tracked__pb2
from ...vision import ssl_vision_detection_pb2 as vision_dot_ssl__vision__detection__pb2
from ...vision import ssl_vision_geometry_pb2 as vision_dot_ssl__vision__geometry__pb2
from ...state import ssl_gc_referee_message_pb2 as state_dot_ssl__gc__referee__message__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fci/autoref/ssl_autoref_ci.proto\x1a(tracker/ssl_vision_wrapper_tracked.proto\x1a!vision/ssl_vision_detection.proto\x1a vision/ssl_vision_geometry.proto\x1a"state/ssl_gc_referee_message.proto"\xb7\x01\n\x0eAutoRefCiInput\x12!\n\x0freferee_message\x18\x01 \x01(\x0b2\x08.Referee\x125\n\x16tracker_wrapper_packet\x18\x02 \x01(\x0b2\x15.TrackerWrapperPacket\x12&\n\tdetection\x18\x03 \x03(\x0b2\x13.SSL_DetectionFrame\x12#\n\x08geometry\x18\x04 \x01(\x0b2\x11.SSL_GeometryData"H\n\x0fAutoRefCiOutput\x125\n\x16tracker_wrapper_packet\x18\x01 \x01(\x0b2\x15.TrackerWrapperPacket')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ci.autoref.ssl_autoref_ci_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _AUTOREFCIINPUT._serialized_start = 183
    _AUTOREFCIINPUT._serialized_end = 366
    _AUTOREFCIOUTPUT._serialized_start = 368
    _AUTOREFCIOUTPUT._serialized_end = 440