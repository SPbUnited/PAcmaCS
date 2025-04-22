"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!engine/ssl_gc_engine_config.proto"\xec\x03\n\x06Config\x12;\n\x13game_event_behavior\x18\x01 \x03(\x0b2\x1e.Config.GameEventBehaviorEntry\x125\n\x10auto_ref_configs\x18\x02 \x03(\x0b2\x1b.Config.AutoRefConfigsEntry\x12\x1d\n\x15active_tracker_source\x18\x03 \x01(\t\x12\r\n\x05teams\x18\x04 \x03(\t\x12\x15\n\rauto_continue\x18\x05 \x01(\x08\x1aJ\n\x16GameEventBehaviorEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1f\n\x05value\x18\x02 \x01(\x0e2\x10.Config.Behavior:\x028\x01\x1aE\n\x13AutoRefConfigsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1d\n\x05value\x18\x02 \x01(\x0b2\x0e.AutoRefConfig:\x028\x01"\x95\x01\n\x08Behavior\x12\x14\n\x10BEHAVIOR_UNKNOWN\x10\x00\x12\x13\n\x0fBEHAVIOR_ACCEPT\x10\x01\x12\x1c\n\x18BEHAVIOR_ACCEPT_MAJORITY\x10\x02\x12\x19\n\x15BEHAVIOR_PROPOSE_ONLY\x10\x03\x12\x10\n\x0cBEHAVIOR_LOG\x10\x04\x12\x13\n\x0fBEHAVIOR_IGNORE\x10\x05"\x84\x02\n\rAutoRefConfig\x12B\n\x13game_event_behavior\x18\x01 \x03(\x0b2%.AutoRefConfig.GameEventBehaviorEntry\x1aQ\n\x16GameEventBehaviorEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12&\n\x05value\x18\x02 \x01(\x0e2\x17.AutoRefConfig.Behavior:\x028\x01"\\\n\x08Behavior\x12\x14\n\x10BEHAVIOR_UNKNOWN\x10\x00\x12\x13\n\x0fBEHAVIOR_ACCEPT\x10\x01\x12\x10\n\x0cBEHAVIOR_LOG\x10\x02\x12\x13\n\x0fBEHAVIOR_IGNORE\x10\x03')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'engine.ssl_gc_engine_config_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _CONFIG_GAMEEVENTBEHAVIORENTRY._options = None
    _CONFIG_GAMEEVENTBEHAVIORENTRY._serialized_options = b'8\x01'
    _CONFIG_AUTOREFCONFIGSENTRY._options = None
    _CONFIG_AUTOREFCONFIGSENTRY._serialized_options = b'8\x01'
    _AUTOREFCONFIG_GAMEEVENTBEHAVIORENTRY._options = None
    _AUTOREFCONFIG_GAMEEVENTBEHAVIORENTRY._serialized_options = b'8\x01'
    _CONFIG._serialized_start = 38
    _CONFIG._serialized_end = 530
    _CONFIG_GAMEEVENTBEHAVIORENTRY._serialized_start = 233
    _CONFIG_GAMEEVENTBEHAVIORENTRY._serialized_end = 307
    _CONFIG_AUTOREFCONFIGSENTRY._serialized_start = 309
    _CONFIG_AUTOREFCONFIGSENTRY._serialized_end = 378
    _CONFIG_BEHAVIOR._serialized_start = 381
    _CONFIG_BEHAVIOR._serialized_end = 530
    _AUTOREFCONFIG._serialized_start = 533
    _AUTOREFCONFIG._serialized_end = 793
    _AUTOREFCONFIG_GAMEEVENTBEHAVIORENTRY._serialized_start = 618
    _AUTOREFCONFIG_GAMEEVENTBEHAVIORENTRY._serialized_end = 699
    _AUTOREFCONFIG_BEHAVIOR._serialized_start = 701
    _AUTOREFCONFIG_BEHAVIOR._serialized_end = 793