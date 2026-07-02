"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13robot/control.proto\x12\rrobot.control"\xb6\x02\n\tOldFormat\x12\r\n\x05vel_x\x18\x01 \x02(\x11\x12\r\n\x05vel_y\x18\x02 \x02(\x11\x12\'\n\x1fangular_velocity_or_delta_angle\x18\x03 \x02(\x11\x12\x16\n\x0ekicker_setting\x18\x04 \x02(\r\x12\x18\n\x10dribbler_setting\x18\x05 \x02(\r\x12\x19\n\x11autokick_straight\x18\x07 \x02(\x08\x12\x15\n\rautokick_high\x18\x08 \x02(\x08\x12\x15\n\rkick_straight\x18\t \x02(\x08\x12\x11\n\tkick_high\x18\n \x02(\x08\x12\x1b\n\x13angvel_angle_toggle\x18\x0b \x02(\x08\x12\x1b\n\x13dribbler_is_enabled\x18\x0c \x02(\x08\x12\x14\n\x0chigh_voltage\x18\r \x02(\x08J\x04\x08\x06\x10\x07"u\n\x11KickerAndDribbler\x12.\n\x0bkicker_mode\x18\x01 \x02(\x0e2\x19.robot.control.KickerMode\x12\x16\n\x0ekicker_setting\x18\x02 \x02(\r\x12\x18\n\x10dribbler_setting\x18\x03 \x02(\r"|\n\x0cSpeedControl\x12\r\n\x05vel_x\x18\x01 \x02(\x02\x12\r\n\x05vel_y\x18\x02 \x02(\x02\x12\x1a\n\x10angular_velocity\x18\x03 \x01(\x02H\x00\x12\x15\n\x0bdelta_angle\x18\x04 \x01(\x02H\x00B\x1b\n\x19angular_velocity_or_angle"Q\n\x06Target\x12\n\n\x02id\x18\x01 \x02(\r\x12\t\n\x01x\x18\x02 \x02(\x02\x12\t\n\x01y\x18\x03 \x02(\x02\x12\n\n\x02vx\x18\x04 \x02(\x02\x12\n\n\x02vy\x18\x05 \x02(\x02\x12\r\n\x05angle\x18\x06 \x02(\x02";\n\x11CoordinateControl\x12&\n\x07targets\x18\x01 \x03(\x0b2\x15.robot.control.Target"8\n\x11GlobalCoordinates\x12\t\n\x01x\x18\x01 \x02(\x02\x12\t\n\x01y\x18\x02 \x02(\x02\x12\r\n\x05angle\x18\x03 \x02(\x02"4\n\x0eCapVelAndAccel\x12\x0f\n\x07max_vel\x18\x01 \x02(\x02\x12\x11\n\tmax_accel\x18\x02 \x02(\x02"\x8e\x03\n\x0cRobotCommand\x12\x10\n\x08robot_id\x18\x01 \x02(\r\x12.\n\nold_format\x18\x02 \x01(\x0b2\x18.robot.control.OldFormatH\x00\x12?\n\x13kicker_and_dribbler\x18\x03 \x01(\x0b2 .robot.control.KickerAndDribblerH\x00\x124\n\rspeed_control\x18\x04 \x01(\x0b2\x1b.robot.control.SpeedControlH\x00\x12>\n\x12coordinate_control\x18\x05 \x01(\x0b2 .robot.control.CoordinateControlH\x00\x12>\n\x12global_coordinates\x18\x06 \x01(\x0b2 .robot.control.GlobalCoordinatesH\x00\x12:\n\x11cap_vel_and_accel\x18\x07 \x01(\x0b2\x1d.robot.control.CapVelAndAccelH\x00B\t\n\x07control*\x95\x01\n\x10RobotControlType\x12\x0e\n\nOLD_FORMAT\x10\x00\x12\x17\n\x13KICKER_AND_DRIBBLER\x10\x01\x12\x11\n\rSPEED_CONTROL\x10\x02\x12\x16\n\x12COORDINATE_CONTROL\x10\x03\x12\x16\n\x12GLOBAL_COORDINATES\x10\x04\x12\x15\n\x11CAP_VEL_AND_ACCEL\x10\x05*b\n\nKickerMode\x12\x08\n\x04IDLE\x10\x00\x12\x11\n\rKICK_STRAIGHT\x10\x01\x12\r\n\tKICK_HIGH\x10\x02\x12\x15\n\x11AUTOKICK_STRAIGHT\x10\x03\x12\x11\n\rAUTOKICK_HIGH\x10\x04')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'robot.control_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _ROBOTCONTROLTYPE._serialized_start = 1254
    _ROBOTCONTROLTYPE._serialized_end = 1403
    _KICKERMODE._serialized_start = 1405
    _KICKERMODE._serialized_end = 1503
    _OLDFORMAT._serialized_start = 39
    _OLDFORMAT._serialized_end = 349
    _KICKERANDDRIBBLER._serialized_start = 351
    _KICKERANDDRIBBLER._serialized_end = 468
    _SPEEDCONTROL._serialized_start = 470
    _SPEEDCONTROL._serialized_end = 594
    _TARGET._serialized_start = 596
    _TARGET._serialized_end = 677
    _COORDINATECONTROL._serialized_start = 679
    _COORDINATECONTROL._serialized_end = 738
    _GLOBALCOORDINATES._serialized_start = 740
    _GLOBALCOORDINATES._serialized_end = 796
    _CAPVELANDACCEL._serialized_start = 798
    _CAPVELANDACCEL._serialized_end = 850
    _ROBOTCOMMAND._serialized_start = 853
    _ROBOTCOMMAND._serialized_end = 1251