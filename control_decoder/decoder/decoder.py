import math
from attrs import define, field
from . import robot_command_model as rcm
from . import control_decoder_command_model as cdcm


@define
class Decoder:
    """Decoder for the control signals"""

    def decoder2sim(self, decoder_team_command: cdcm.DecoderTeamCommand):
        """Convert the decoder command to a sim robot command"""

        robot_team_command = rcm.RobotControlExt(
            isteamyellow=decoder_team_command.isteamyellow,
            robot_commands=[],
        )

        for decoder_command in decoder_team_command.robot_commands:

            is_kick = (
                decoder_command.kick_up
                or decoder_command.kick_forward
                or decoder_command.auto_kick_up
                or decoder_command.auto_kick_forward
            )
            is_upper_kick = decoder_command.kick_up or decoder_command.auto_kick_up

            # real robot hits the ball at about 6 m/s at maximum voltage
            kick_speed = decoder_command.kicker_setting * (6 / 15) if is_kick else 0
            kick_angle = 30 if is_upper_kick else 0

            angular_vel = decoder_command.angular_vel
            if angular_vel is None:
                angular_vel = 0

            robot_command = rcm.RobotCommand(
                id=decoder_command.robot_id,
                move_command=rcm.RobotMoveCommand(
                    local_velocity=rcm.MoveLocalVelocity(
                        forward=decoder_command.forward_vel,
                        left=decoder_command.left_vel,
                        angular=angular_vel,
                    ),
                ),
                kick_speed=kick_speed,
                kick_angle=kick_angle,
                dribbler_speed=decoder_command.dribbler_setting,
            )

            robot_team_command.robot_commands.append(robot_command)

        return robot_team_command

    def decoder2robot(self, decoder_team_command: cdcm.DecoderTeamCommand) -> tuple[list[bytes], list[bytes]]:
        """Convert the decoder command to a robot command"""
        commands_low: list[bytes] = []
        commands_high: list[bytes] = []
        for robot in decoder_team_command.robot_commands:
            angle: float
            angvel_flag: int
            if robot.angle is not None:
                angle = -robot.angle
                angvel_flag = 0
            elif robot.angular_vel is not None:
                angle = robot.angular_vel
                angvel_flag = 1
            else:
                raise RuntimeError

            angle_info = int(math.log(18 / math.pi * abs(angle) + 1) * math.copysign(1, angle) * (100 / math.log(18 + 1)))

            autokick = 0
            if robot.auto_kick_forward:
                autokick = 1
            elif robot.auto_kick_up:
                autokick = 2

            command_bytes = create_packet(
                bot_number=int(robot.robot_id),
                speed_x=int(-robot.left_vel / (1070 / 30)),
                speed_y=int(robot.forward_vel / (1300 / 30)),
                speed_w=int(angle_info),
                dribbler_speed=int(robot.dribbler_setting),
                kicker_voltage=int(robot.kicker_setting),
                kick_up=int(robot.kick_up),
                kick_down=int(robot.kick_forward),
                beep=int(angvel_flag),
                dribbler_en=int(robot.dribbler_setting > 0),
                charge_en=int(robot.kicker_setting > 0),
                autokick=autokick,
            )
            if robot.robot_id < 8:
                commands_low.append(command_bytes)
            else:
                commands_high.append(command_bytes)

        return commands_low, commands_high


def create_packet(
    bot_number: int,  # unsigned byte (0-255)
    speed_x: int,  # signed byte (-128 to 127)
    speed_y: int,  # signed byte
    speed_w: int,  # signed byte
    dribbler_speed: int,  # unsigned byte
    kicker_voltage: int,  # unsigned byte
    kick_up: int,  # boolean flag (bit 0)
    kick_down: int,  # boolean flag (bit 1)
    beep: int,  # boolean flag (bit 2)
    dribbler_en: int,  # boolean flag (bit 3)
    charge_en: int,  # boolean flag (bit 4)
    autokick: int,  # unsigned byte
) -> bytes:
    # Convert all values to bytes and pack into a list
    bytes_list = [
        0x01,  # Header
        bot_number,
        speed_x.to_bytes(1, "big", signed=True)[0],
        speed_y.to_bytes(1, "big", signed=True)[0],
        speed_w.to_bytes(1, "big", signed=True)[0],
        dribbler_speed,
        kicker_voltage,
        kick_up,
        kick_down,
        beep,
        dribbler_en,
        charge_en,
        autokick,
    ]

    return bytes(bytes_list)
