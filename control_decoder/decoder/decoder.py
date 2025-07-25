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
            is_upper_kick = (
                decoder_command.kick_up
                or decoder_command.auto_kick_up
            )

            kick_speed = 1 if is_kick else 0
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
    
    def decoder2robot(self, decoder_command: cdcm.DecoderCommand):
        """Convert the decoder command to a robot command"""

        pass
