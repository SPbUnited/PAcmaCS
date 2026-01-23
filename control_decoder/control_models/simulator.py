import time
import zmq
from cattrs import unstructure

from decoder import robot_command_model as rcm
from decoder import control_decoder_command_model as cdcm
from control_models.base_model import ControlModel

class SimDecoder(ControlModel):
    def __init__(self, config, telemetry_sender):
        super().__init__(config, telemetry_sender)
        context = zmq.Context()

        outbound_sim = config["ether"]["s_signals_sub_url"]
        self.s_outbound_sim = context.socket(zmq.PUB)
        self.s_outbound_sim.connect(outbound_sim)


    def process(self, signal_data: cdcm.DecoderTeamCommand) -> None:
        self.telemetry_text = 'SENDING COMMANDS IN "SIM" MODE\n \tr_id\n'
        command: rcm.RobotControlExt = self.decoder(signal_data)
        self.s_outbound_sim.send_json({"transnet": "actuate_robot", "data": unstructure(command)})

        for cmd in signal_data.robot_commands:
            self.telemetry_text += f"\t{cmd.robot_id}\n"
        self.last_update = time.time()
        

    def decoder(self, decoder_team_command: cdcm.DecoderTeamCommand):
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
                        forward=decoder_command.forward_vel / 1000,
                        left=decoder_command.left_vel / 1000,
                        angular=angular_vel,
                    ),
                ),
                kick_speed=kick_speed,
                kick_angle=kick_angle,
                dribbler_speed=decoder_command.dribbler_setting,
            )

            robot_team_command.robot_commands.append(robot_command)

        return robot_team_command
    

