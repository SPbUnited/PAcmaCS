"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*erforce/ssl_simulation_robot_control.proto"\x86\x01\n\x0cRobotCommand\x12\n\n\x02id\x18\x01 \x02(\r\x12\'\n\x0cmove_command\x18\x02 \x01(\x0b2\x11.RobotMoveCommand\x12\x12\n\nkick_speed\x18\x03 \x01(\x02\x12\x15\n\nkick_angle\x18\x04 \x01(\x02:\x010\x12\x16\n\x0edribbler_speed\x18\x05 \x01(\x02"\xa9\x01\n\x10RobotMoveCommand\x12,\n\x0ewheel_velocity\x18\x01 \x01(\x0b2\x12.MoveWheelVelocityH\x00\x12,\n\x0elocal_velocity\x18\x02 \x01(\x0b2\x12.MoveLocalVelocityH\x00\x12.\n\x0fglobal_velocity\x18\x03 \x01(\x0b2\x13.MoveGlobalVelocityH\x00B\t\n\x07command"c\n\x11MoveWheelVelocity\x12\x13\n\x0bfront_right\x18\x01 \x02(\x02\x12\x12\n\nback_right\x18\x02 \x02(\x02\x12\x11\n\tback_left\x18\x03 \x02(\x02\x12\x12\n\nfront_left\x18\x04 \x02(\x02"C\n\x11MoveLocalVelocity\x12\x0f\n\x07forward\x18\x01 \x02(\x02\x12\x0c\n\x04left\x18\x02 \x02(\x02\x12\x0f\n\x07angular\x18\x03 \x02(\x02";\n\x12MoveGlobalVelocity\x12\t\n\x01x\x18\x01 \x02(\x02\x12\t\n\x01y\x18\x02 \x02(\x02\x12\x0f\n\x07angular\x18\x03 \x02(\x02"5\n\x0cRobotControl\x12%\n\x0erobot_commands\x18\x01 \x03(\x0b2\r.RobotCommandB8Z6github.com/RoboCup-SSL/ssl-simulation-protocol/pkg/sim')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'erforce.ssl_simulation_robot_control_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z6github.com/RoboCup-SSL/ssl-simulation-protocol/pkg/sim'
    _ROBOTCOMMAND._serialized_start = 47
    _ROBOTCOMMAND._serialized_end = 181
    _ROBOTMOVECOMMAND._serialized_start = 184
    _ROBOTMOVECOMMAND._serialized_end = 353
    _MOVEWHEELVELOCITY._serialized_start = 355
    _MOVEWHEELVELOCITY._serialized_end = 454
    _MOVELOCALVELOCITY._serialized_start = 456
    _MOVELOCALVELOCITY._serialized_end = 523
    _MOVEGLOBALVELOCITY._serialized_start = 525
    _MOVEGLOBALVELOCITY._serialized_end = 584
    _ROBOTCONTROL._serialized_start = 586
    _ROBOTCONTROL._serialized_end = 639