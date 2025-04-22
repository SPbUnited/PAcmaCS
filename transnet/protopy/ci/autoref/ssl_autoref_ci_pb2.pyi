from tracker import ssl_vision_wrapper_tracked_pb2 as _ssl_vision_wrapper_tracked_pb2
from vision import ssl_vision_detection_pb2 as _ssl_vision_detection_pb2
from vision import ssl_vision_geometry_pb2 as _ssl_vision_geometry_pb2
from state import ssl_gc_referee_message_pb2 as _ssl_gc_referee_message_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class AutoRefCiInput(_message.Message):
    __slots__ = ['detection', 'geometry', 'referee_message', 'tracker_wrapper_packet']
    DETECTION_FIELD_NUMBER: _ClassVar[int]
    GEOMETRY_FIELD_NUMBER: _ClassVar[int]
    REFEREE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TRACKER_WRAPPER_PACKET_FIELD_NUMBER: _ClassVar[int]
    detection: _containers.RepeatedCompositeFieldContainer[_ssl_vision_detection_pb2.SSL_DetectionFrame]
    geometry: _ssl_vision_geometry_pb2.SSL_GeometryData
    referee_message: _ssl_gc_referee_message_pb2.Referee
    tracker_wrapper_packet: _ssl_vision_wrapper_tracked_pb2.TrackerWrapperPacket

    def __init__(self, referee_message: _Optional[_Union[_ssl_gc_referee_message_pb2.Referee, _Mapping]]=..., tracker_wrapper_packet: _Optional[_Union[_ssl_vision_wrapper_tracked_pb2.TrackerWrapperPacket, _Mapping]]=..., detection: _Optional[_Iterable[_Union[_ssl_vision_detection_pb2.SSL_DetectionFrame, _Mapping]]]=..., geometry: _Optional[_Union[_ssl_vision_geometry_pb2.SSL_GeometryData, _Mapping]]=...) -> None:
        ...

class AutoRefCiOutput(_message.Message):
    __slots__ = ['tracker_wrapper_packet']
    TRACKER_WRAPPER_PACKET_FIELD_NUMBER: _ClassVar[int]
    tracker_wrapper_packet: _ssl_vision_wrapper_tracked_pb2.TrackerWrapperPacket

    def __init__(self, tracker_wrapper_packet: _Optional[_Union[_ssl_vision_wrapper_tracked_pb2.TrackerWrapperPacket, _Mapping]]=...) -> None:
        ...