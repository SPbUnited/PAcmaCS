from state import ssl_gc_game_event_pb2 as _ssl_gc_game_event_pb2
from rcon import ssl_gc_rcon_pb2 as _ssl_gc_rcon_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class AutoRefRegistration(_message.Message):
    __slots__ = ['identifier', 'signature']
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    signature: _ssl_gc_rcon_pb2.Signature

    def __init__(self, identifier: _Optional[str]=..., signature: _Optional[_Union[_ssl_gc_rcon_pb2.Signature, _Mapping]]=...) -> None:
        ...

class AutoRefToController(_message.Message):
    __slots__ = ['game_event', 'signature']
    GAME_EVENT_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    game_event: _ssl_gc_game_event_pb2.GameEvent
    signature: _ssl_gc_rcon_pb2.Signature

    def __init__(self, signature: _Optional[_Union[_ssl_gc_rcon_pb2.Signature, _Mapping]]=..., game_event: _Optional[_Union[_ssl_gc_game_event_pb2.GameEvent, _Mapping]]=...) -> None:
        ...

class ControllerToAutoRef(_message.Message):
    __slots__ = ['controller_reply']
    CONTROLLER_REPLY_FIELD_NUMBER: _ClassVar[int]
    controller_reply: _ssl_gc_rcon_pb2.ControllerReply

    def __init__(self, controller_reply: _Optional[_Union[_ssl_gc_rcon_pb2.ControllerReply, _Mapping]]=...) -> None:
        ...