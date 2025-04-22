"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ..state import ssl_gc_common_pb2 as state_dot_ssl__gc__common__pb2
from ..rcon import ssl_gc_rcon_pb2 as rcon_dot_ssl__gc__rcon__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1brcon/ssl_gc_rcon_team.proto\x1a\x19state/ssl_gc_common.proto\x1a\x16rcon/ssl_gc_rcon.proto"Y\n\x10TeamRegistration\x12\x11\n\tteam_name\x18\x01 \x02(\t\x12\x1d\n\tsignature\x18\x02 \x01(\x0b2\n.Signature\x12\x13\n\x04team\x18\x03 \x01(\x0e2\x05.Team"\xaa\x01\n\x10TeamToController\x12\x1d\n\tsignature\x18\x01 \x01(\x0b2\n.Signature\x12\x18\n\x0edesired_keeper\x18\x02 \x01(\x05H\x00\x12,\n\x10advantage_choice\x18\x03 \x01(\x0e2\x10.AdvantageChoiceH\x00\x12\x18\n\x0esubstitute_bot\x18\x04 \x01(\x08H\x00\x12\x0e\n\x04ping\x18\x05 \x01(\x08H\x00B\x05\n\x03msg"M\n\x10ControllerToTeam\x12,\n\x10controller_reply\x18\x01 \x01(\x0b2\x10.ControllerReplyH\x00B\x05\n\x03msgJ\x04\x08\x02\x10\x03*)\n\x0fAdvantageChoice\x12\x08\n\x04STOP\x10\x00\x12\x0c\n\x08CONTINUE\x10\x01')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'rcon.ssl_gc_rcon_team_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _ADVANTAGECHOICE._serialized_start = 425
    _ADVANTAGECHOICE._serialized_end = 466
    _TEAMREGISTRATION._serialized_start = 82
    _TEAMREGISTRATION._serialized_end = 171
    _TEAMTOCONTROLLER._serialized_start = 174
    _TEAMTOCONTROLLER._serialized_end = 344
    _CONTROLLERTOTEAM._serialized_start = 346
    _CONTROLLERTOTEAM._serialized_end = 423