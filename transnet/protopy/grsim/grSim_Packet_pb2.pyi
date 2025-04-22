from grsim import grSim_Commands_pb2 as _grSim_Commands_pb2
from grsim import grSim_Replacement_pb2 as _grSim_Replacement_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class grSim_Packet(_message.Message):
    __slots__ = ['commands', 'replacement']
    COMMANDS_FIELD_NUMBER: _ClassVar[int]
    REPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    commands: _grSim_Commands_pb2.grSim_Commands
    replacement: _grSim_Replacement_pb2.grSim_Replacement

    def __init__(self, commands: _Optional[_Union[_grSim_Commands_pb2.grSim_Commands, _Mapping]]=..., replacement: _Optional[_Union[_grSim_Replacement_pb2.grSim_Replacement, _Mapping]]=...) -> None:
        ...