from state import ssl_gc_common_pb2 as _ssl_gc_common_pb2
from rcon import ssl_gc_rcon_pb2 as _ssl_gc_rcon_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
CONTINUE: AdvantageChoice
DESCRIPTOR: _descriptor.FileDescriptor
STOP: AdvantageChoice

class ControllerToTeam(_message.Message):
    __slots__ = ['controller_reply']
    CONTROLLER_REPLY_FIELD_NUMBER: _ClassVar[int]
    controller_reply: _ssl_gc_rcon_pb2.ControllerReply

    def __init__(self, controller_reply: _Optional[_Union[_ssl_gc_rcon_pb2.ControllerReply, _Mapping]]=...) -> None:
        ...

class TeamRegistration(_message.Message):
    __slots__ = ['signature', 'team', 'team_name']
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    signature: _ssl_gc_rcon_pb2.Signature
    team: _ssl_gc_common_pb2.Team
    team_name: str

    def __init__(self, team_name: _Optional[str]=..., signature: _Optional[_Union[_ssl_gc_rcon_pb2.Signature, _Mapping]]=..., team: _Optional[_Union[_ssl_gc_common_pb2.Team, str]]=...) -> None:
        ...

class TeamToController(_message.Message):
    __slots__ = ['advantage_choice', 'desired_keeper', 'ping', 'signature', 'substitute_bot']
    ADVANTAGE_CHOICE_FIELD_NUMBER: _ClassVar[int]
    DESIRED_KEEPER_FIELD_NUMBER: _ClassVar[int]
    PING_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    SUBSTITUTE_BOT_FIELD_NUMBER: _ClassVar[int]
    advantage_choice: AdvantageChoice
    desired_keeper: int
    ping: bool
    signature: _ssl_gc_rcon_pb2.Signature
    substitute_bot: bool

    def __init__(self, signature: _Optional[_Union[_ssl_gc_rcon_pb2.Signature, _Mapping]]=..., desired_keeper: _Optional[int]=..., advantage_choice: _Optional[_Union[AdvantageChoice, str]]=..., substitute_bot: bool=..., ping: bool=...) -> None:
        ...

class AdvantageChoice(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []