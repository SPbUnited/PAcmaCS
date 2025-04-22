"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ..state import ssl_gc_common_pb2 as state_dot_ssl__gc__common__pb2
from ..rcon import ssl_gc_rcon_pb2 as rcon_dot_ssl__gc__rcon__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$rcon/ssl_gc_rcon_remotecontrol.proto\x1a\x19state/ssl_gc_common.proto\x1a\x16rcon/ssl_gc_rcon.proto"O\n\x19RemoteControlRegistration\x12\x13\n\x04team\x18\x01 \x02(\x0e2\x05.Team\x12\x1d\n\tsignature\x18\x02 \x01(\x0b2\n.Signature"\xd5\x02\n\x19RemoteControlToController\x12\x1d\n\tsignature\x18\x01 \x01(\x0b2\n.Signature\x125\n\x07request\x18\x02 \x01(\x0e2".RemoteControlToController.RequestH\x00\x12\x18\n\x0edesired_keeper\x18\x03 \x01(\x05H\x00\x12$\n\x1arequest_robot_substitution\x18\x04 \x01(\x08H\x00\x12\x19\n\x0frequest_timeout\x18\x05 \x01(\x08H\x00\x12 \n\x16request_emergency_stop\x18\x06 \x01(\x08H\x00"^\n\x07Request\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x08\n\x04PING\x10\x01\x12\x12\n\x0eCHALLENGE_FLAG\x10\x02\x12\x10\n\x0cSTOP_TIMEOUT\x10\x03\x12\x16\n\x12FAIL_BALLPLACEMENT\x10\x04B\x05\n\x03msg"o\n\x19ControllerToRemoteControl\x12*\n\x10controller_reply\x18\x01 \x01(\x0b2\x10.ControllerReply\x12&\n\x05state\x18\x02 \x01(\x0b2\x17.RemoteControlTeamState"\xbf\x03\n\x16RemoteControlTeamState\x12\x13\n\x04team\x18\x0c \x01(\x0e2\x05.Team\x125\n\x12available_requests\x18\x01 \x03(\x0e2\x19.RemoteControlRequestType\x122\n\x0factive_requests\x18\x02 \x03(\x0e2\x19.RemoteControlRequestType\x12\x11\n\tkeeper_id\x18\x03 \x01(\x05\x12\x19\n\x11emergency_stop_in\x18\x04 \x01(\x02\x12\x15\n\rtimeouts_left\x18\x05 \x01(\x05\x12\x19\n\x11timeout_time_left\x18\n \x01(\x02\x12\x1c\n\x14challenge_flags_left\x18\x06 \x01(\x05\x12\x12\n\nmax_robots\x18\x07 \x01(\x05\x12\x17\n\x0frobots_on_field\x18\t \x01(\x05\x12\x18\n\x10yellow_cards_due\x18\x08 \x03(\x02\x12\x1c\n\x14can_substitute_robot\x18\x0b \x01(\x08\x12\x1e\n\x16bot_substitutions_left\x18\r \x01(\r\x12"\n\x1abot_substitution_time_left\x18\x0e \x01(\x02*\xc1\x01\n\x18RemoteControlRequestType\x12\x18\n\x14UNKNOWN_REQUEST_TYPE\x10\x00\x12\x12\n\x0eEMERGENCY_STOP\x10\x01\x12\x16\n\x12ROBOT_SUBSTITUTION\x10\x02\x12\x0b\n\x07TIMEOUT\x10\x03\x12\x12\n\x0eCHALLENGE_FLAG\x10\x04\x12\x14\n\x10CHANGE_KEEPER_ID\x10\x05\x12\x10\n\x0cSTOP_TIMEOUT\x10\x06\x12\x16\n\x12FAIL_BALLPLACEMENT\x10\x07')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'rcon.ssl_gc_rcon_remotecontrol_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _REMOTECONTROLREQUESTTYPE._serialized_start = 1080
    _REMOTECONTROLREQUESTTYPE._serialized_end = 1273
    _REMOTECONTROLREGISTRATION._serialized_start = 91
    _REMOTECONTROLREGISTRATION._serialized_end = 170
    _REMOTECONTROLTOCONTROLLER._serialized_start = 173
    _REMOTECONTROLTOCONTROLLER._serialized_end = 514
    _REMOTECONTROLTOCONTROLLER_REQUEST._serialized_start = 413
    _REMOTECONTROLTOCONTROLLER_REQUEST._serialized_end = 507
    _CONTROLLERTOREMOTECONTROL._serialized_start = 516
    _CONTROLLERTOREMOTECONTROL._serialized_end = 627
    _REMOTECONTROLTEAMSTATE._serialized_start = 630
    _REMOTECONTROLTEAMSTATE._serialized_end = 1077