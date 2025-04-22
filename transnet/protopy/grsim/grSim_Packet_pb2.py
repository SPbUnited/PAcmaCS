"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ..grsim import grSim_Commands_pb2 as grsim_dot_grSim__Commands__pb2
from ..grsim import grSim_Replacement_pb2 as grsim_dot_grSim__Replacement__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18grsim/grSim_Packet.proto\x1a\x1agrsim/grSim_Commands.proto\x1a\x1dgrsim/grSim_Replacement.proto"Z\n\x0cgrSim_Packet\x12!\n\x08commands\x18\x01 \x01(\x0b2\x0f.grSim_Commands\x12\'\n\x0breplacement\x18\x02 \x01(\x0b2\x12.grSim_Replacement')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'grsim.grSim_Packet_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _GRSIM_PACKET._serialized_start = 87
    _GRSIM_PACKET._serialized_end = 177