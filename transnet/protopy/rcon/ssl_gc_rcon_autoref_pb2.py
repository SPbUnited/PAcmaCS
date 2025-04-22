"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ..state import ssl_gc_game_event_pb2 as state_dot_ssl__gc__game__event__pb2
from ..rcon import ssl_gc_rcon_pb2 as rcon_dot_ssl__gc__rcon__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ercon/ssl_gc_rcon_autoref.proto\x1a\x1dstate/ssl_gc_game_event.proto\x1a\x16rcon/ssl_gc_rcon.proto"H\n\x13AutoRefRegistration\x12\x12\n\nidentifier\x18\x01 \x02(\t\x12\x1d\n\tsignature\x18\x02 \x01(\x0b2\n.Signature"`\n\x13AutoRefToController\x12\x1d\n\tsignature\x18\x01 \x01(\x0b2\n.Signature\x12\x1e\n\ngame_event\x18\x02 \x01(\x0b2\n.GameEventJ\x04\x08\x03\x10\x04J\x04\x08\x04\x10\x05"J\n\x13ControllerToAutoRef\x12,\n\x10controller_reply\x18\x01 \x01(\x0b2\x10.ControllerReplyH\x00B\x05\n\x03msg')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'rcon.ssl_gc_rcon_autoref_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _AUTOREFREGISTRATION._serialized_start = 89
    _AUTOREFREGISTRATION._serialized_end = 161
    _AUTOREFTOCONTROLLER._serialized_start = 163
    _AUTOREFTOCONTROLLER._serialized_end = 259
    _CONTROLLERTOAUTOREF._serialized_start = 261
    _CONTROLLERTOAUTOREF._serialized_end = 335