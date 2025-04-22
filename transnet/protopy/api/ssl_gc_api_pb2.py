"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ..state import ssl_gc_state_pb2 as state_dot_ssl__gc__state__pb2
from ..statemachine import ssl_gc_change_pb2 as statemachine_dot_ssl__gc__change__pb2
from ..engine import ssl_gc_engine_pb2 as engine_dot_ssl__gc__engine__pb2
from ..engine import ssl_gc_engine_config_pb2 as engine_dot_ssl__gc__engine__config__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14api/ssl_gc_api.proto\x1a\x18state/ssl_gc_state.proto\x1a statemachine/ssl_gc_change.proto\x1a\x1aengine/ssl_gc_engine.proto\x1a!engine/ssl_gc_engine_config.proto\x1a\x1egoogle/protobuf/duration.proto"w\n\x06Output\x12\x1b\n\x0bmatch_state\x18\x01 \x01(\x0b2\x06.State\x12\x1a\n\x08gc_state\x18\x02 \x01(\x0b2\x08.GcState\x12\x1b\n\x08protocol\x18\x03 \x01(\x0b2\t.Protocol\x12\x17\n\x06config\x18\x04 \x01(\x0b2\x07.Config"8\n\x08Protocol\x12\r\n\x05delta\x18\x01 \x01(\x08\x12\x1d\n\x05entry\x18\x02 \x03(\x0b2\x0e.ProtocolEntry"\xa2\x01\n\rProtocolEntry\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x17\n\x06change\x18\x02 \x01(\x0b2\x07.Change\x125\n\x12match_time_elapsed\x18\x03 \x01(\x0b2\x19.google.protobuf.Duration\x125\n\x12stage_time_elapsed\x18\x04 \x01(\x0b2\x19.google.protobuf.Duration"~\n\x05Input\x12\x17\n\x06change\x18\x01 \x01(\x0b2\x07.Change\x12\x13\n\x0breset_match\x18\x02 \x01(\x08\x12\x1d\n\x0cconfig_delta\x18\x03 \x01(\x0b2\x07.Config\x12(\n\x0fcontinue_action\x18\x04 \x01(\x0b2\x0f.ContinueAction')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api.ssl_gc_api_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _OUTPUT._serialized_start = 179
    _OUTPUT._serialized_end = 298
    _PROTOCOL._serialized_start = 300
    _PROTOCOL._serialized_end = 356
    _PROTOCOLENTRY._serialized_start = 359
    _PROTOCOLENTRY._serialized_end = 521
    _INPUT._serialized_start = 523
    _INPUT._serialized_end = 649