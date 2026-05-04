import math
import socket
import time

from decoder import control_decoder_command_model as cdcm
from control_models.base_model import ControlModel

class FB2Decoder(ControlModel):
    def __init__(self, config, telemetry_sender):
        super().__init__(config, telemetry_sender)
        self.fb2_ip_port_low: tuple[str, int] = (
            config["control_decoder"]["fb2_ip_low"],
            config["control_decoder"]["fb2_port"],
        )
        self.fb2_ip_port_high: tuple[str, int] = (
            config["control_decoder"]["fb2_ip_high"],
            config["control_decoder"]["fb2_port"],
        )
        self.s_outbound_real_low = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s_outbound_real_high = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.last_update = time.time()

    def process(self, signal_data: cdcm.DecoderTeamCommand) -> None:
        self.telemetry_text = 'SENDING COMMANDS IN "FB2" MODE\n \tr_id\tspeedX\tspeedY\tspeedW\tdribler\tvoltage\tkickUP\tkickDWN\tbeep\tdribEN\tcharEN\tautokck\n'
        packets_low, packets_high = self.decoder(signal_data)
        for packet in packets_low:
            self.s_outbound_real_low.sendto(packet, self.fb2_ip_port_low)
        for packet in packets_high:
            self.s_outbound_real_high.sendto(packet, self.fb2_ip_port_high)

        for cmd in packets_low + packets_high:
            self.telemetry_text += create_telemetry(cmd)
        self.last_update = time.time()

    def decoder(self, decoder_team_command: cdcm.DecoderTeamCommand) -> tuple[list[bytes], list[bytes]]:
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


def create_telemetry(data: bytes) -> str:
    """Create line for telemetry for single robot"""
    values = [
        data[1],
        int.from_bytes(data[2:3], "big", signed=True),
        int.from_bytes(data[3:4], "big", signed=True),
        int.from_bytes(data[4:5], "big", signed=True),
        data[5],
        data[6],
        data[7],
        data[8],
        data[9],
        data[10],
        data[11],
        data[12],
    ]
    values_str = [str(val) for val in values]
    return "\t" + "\t".join(values_str) + "\n"
