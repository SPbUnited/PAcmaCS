"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1agrsim/grSim_Commands.proto"\xea\x01\n\x13grSim_Robot_Command\x12\n\n\x02id\x18\x01 \x02(\r\x12\x12\n\nkickspeedx\x18\x02 \x02(\x02\x12\x12\n\nkickspeedz\x18\x03 \x02(\x02\x12\x12\n\nveltangent\x18\x04 \x02(\x02\x12\x11\n\tvelnormal\x18\x05 \x02(\x02\x12\x12\n\nvelangular\x18\x06 \x02(\x02\x12\x0f\n\x07spinner\x18\x07 \x02(\x08\x12\x13\n\x0bwheelsspeed\x18\x08 \x02(\x08\x12\x0e\n\x06wheel1\x18\t \x01(\x02\x12\x0e\n\x06wheel2\x18\n \x01(\x02\x12\x0e\n\x06wheel3\x18\x0b \x01(\x02\x12\x0e\n\x06wheel4\x18\x0c \x01(\x02"g\n\x0egrSim_Commands\x12\x11\n\ttimestamp\x18\x01 \x02(\x01\x12\x14\n\x0cisteamyellow\x18\x02 \x02(\x08\x12,\n\x0erobot_commands\x18\x03 \x03(\x0b2\x14.grSim_Robot_Command')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'grsim.grSim_Commands_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _GRSIM_ROBOT_COMMAND._serialized_start = 31
    _GRSIM_ROBOT_COMMAND._serialized_end = 265
    _GRSIM_COMMANDS._serialized_start = 267
    _GRSIM_COMMANDS._serialized_end = 370