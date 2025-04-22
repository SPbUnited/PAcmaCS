from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class ControllerReply(_message.Message):
    __slots__ = ['next_token', 'reason', 'status_code', 'verification']

    class StatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []

    class Verification(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    NEXT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    OK: ControllerReply.StatusCode
    REASON_FIELD_NUMBER: _ClassVar[int]
    REJECTED: ControllerReply.StatusCode
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_STATUS_CODE: ControllerReply.StatusCode
    UNKNOWN_VERIFICATION: ControllerReply.Verification
    UNVERIFIED: ControllerReply.Verification
    VERIFICATION_FIELD_NUMBER: _ClassVar[int]
    VERIFIED: ControllerReply.Verification
    next_token: str
    reason: str
    status_code: ControllerReply.StatusCode
    verification: ControllerReply.Verification

    def __init__(self, status_code: _Optional[_Union[ControllerReply.StatusCode, str]]=..., reason: _Optional[str]=..., next_token: _Optional[str]=..., verification: _Optional[_Union[ControllerReply.Verification, str]]=...) -> None:
        ...

class Signature(_message.Message):
    __slots__ = ['pkcs1v15', 'token']
    PKCS1V15_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    pkcs1v15: bytes
    token: str

    def __init__(self, token: _Optional[str]=..., pkcs1v15: _Optional[bytes]=...) -> None:
        ...