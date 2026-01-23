import math
import zmq
import socket
import time

from decoder import control_decoder_command_model as cdcm
from control_models.base_model import ControlModel

class FB4Decoder(ControlModel):
    def __init__(self, config, telemetry_sender):
        super().__init__(config, telemetry_sender)

        self.fb4_ip_port_low: tuple[str, int] = (
            config["control_decoder"]["fb4_ip_low"],
            config["control_decoder"]["fb4_port"],
        )
        self.fb4_ip_port_high: tuple[str, int] = (
            config["control_decoder"]["fb4_ip_high"],
            config["control_decoder"]["fb4_port"],
        )
        self.s_outbound_real_low = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s_outbound_real_high = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        def robots_sender_low(data: bytes):
            self.s_outbound_real_low.sendto(data, self.fb4_ip_port_low)
        def robots_sender_high(data: bytes):
            self.s_outbound_real_high.sendto(data, self.fb4_ip_port_high)
        self.udpie_processor = UdPieProcessor(robots_sender_low,robots_sender_high, telemetry_sender)

    def process(self, signal_data: cdcm.DecoderTeamCommand) -> None:
        self.telemetry_text = 'SENDING COMMANDS IN "FB4" MODE\n \tr_id\tspeedX\tspeedY\tspeedW\tdribler\tvoltage\tkickUP\tkickDWN\tbeep\tdribEN\tcharEN\tautokck\n'
        packets_low, packets_high = self.decoder(signal_data)
        for packet in packets_low:
            self.s_outbound_real_low.sendto(packet, self.fb4_ip_port_low)
        for packet in packets_high:
            self.s_outbound_real_high.sendto(packet, self.fb4_ip_port_high)

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
                speed_x=-robot.left_vel / (435 / 15),
                speed_y=robot.forward_vel / (440 / 15),
                speed_w=angle_info,
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
    
    def process_signal(self, raw: Any):
        self.udpie_processor.process_udpie(raw)



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


def create_packet(
    bot_number: int,  # unsigned byte (0-255)
    speed_x: float,  # signed byte (-128 to 127)
    speed_y: float,  # signed byte
    speed_w: float,  # signed byte
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
        bot_number + 240,
        float_to_143(speed_x),
        float_to_143(speed_y),
        float_to_143(speed_w),
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

def float_to_minifloat(x, exponent_bits, mantissa_bits):
    if x == 0.0:
        return (0, 0, 0)
    sign = 0 if x > 0 else 1
    x = abs(x)
    m, e = math.frexp(x)
    significand = m * 2  # Now in [1.0, 2.0)
    exponent = e - 1
    fractional_part = significand - 1.0
    bias = (1 << (exponent_bits - 1)) - 1
    stored_exponent = exponent + bias
    max_exp = (1 << exponent_bits) - 1
    max_significand = (1 << mantissa_bits) - 1
    # print()
    # print("signif\texp\tfrac\tbias\ts_exp\tmax_exp")
    # print(
    #     significand, exponent, fractional_part, bias, stored_exponent, max_exp, sep="\t"
    # )

    is_subnormal = False

    if stored_exponent > max_exp:
        return (sign, max_exp, max_significand)
    elif stored_exponent < -mantissa_bits:
        return (sign, 0, 0)
    else:
        if stored_exponent <= 0:
            fractional_part = (fractional_part + 1) * 2**stored_exponent
            stored_exponent = 0
            is_subnormal = True

        scaled = fractional_part * (2**mantissa_bits)
        rounded_mantissa = round(scaled)
        # print("scaled\trounded")
        # print(scaled, rounded_mantissa, sep="\t")
        if rounded_mantissa >= (1 << mantissa_bits) and not is_subnormal:
            stored_exponent += 1
            mantissa = 0
            if stored_exponent > max_exp:
                return (sign, max_exp, max_significand)
        else:
            mantissa = rounded_mantissa
        # if stored_exponent == 0:
        #     mantissa +=
        return (sign, stored_exponent, mantissa)


def minifloat_to_float(sign, stored_exponent, mantissa, exponent_bits, mantissa_bits):
    bias = (1 << (exponent_bits - 1)) - 1
    exponent2 = 2 ** (stored_exponent - bias - mantissa_bits)
    normalizer = (stored_exponent != 0) * (2 ** (stored_exponent - bias))
    print(bias, exponent2, mantissa, normalizer)
    return (-1) ** sign * (exponent2 * mantissa + normalizer)

def minifloat_to_binary(
    sign, stored_exponent, mantissa, exponent_bits, mantissa_bits
):
    exponent_str = format(stored_exponent, f"0{exponent_bits}b")
    mantissa_str = format(mantissa, f"0{mantissa_bits}b")
    return (
        f"{sign} {stored_exponent} {mantissa}\t{sign}{exponent_str}{mantissa_str}"
    )

def float_to_143(x: float) -> int:
    sign, exp, mantissa = float_to_minifloat(x, 4, 3)
    out = sign << 7 | exp << 3 | mantissa
    # binary_1_4_3 = minifloat_to_binary(sign, exp, mantissa, 4, 3)

    return out

###################################################################################################

udpies_history: list[tuple[str, int, str]] = []

class UdPieProcessor:
    def __init__(self, robots_sender_low, robots_sender_high, telemetry_sender):
        self.robots_sender_low = robots_sender_low
        self.robots_sender_high = robots_sender_high
        self.telemetry_sender = telemetry_sender

    def process_udpie(self, raw_data):
        try:
            data = bytes(int(x) & 0xFF for x in raw_data)
        except Exception as e:
            print("send_udpie: cannot convert data to bytes:", e)
            return

        print("Get new udpie:", data)
        robot_id = data[1] & 0x0F

        try:
            if robot_id < 8:
                self.robots_sender_low(data)
            else:
                self.robots_sender_high(data)
            self.log_udpie_packet(data)
        except OSError as e:
            print("Can't send UDPie, no route to host:", e)
            self.telemetry_sender({"SENDED UDPIES": "Can't send UDPie, no route to host"})

    def log_udpie_packet(self, data: bytes) -> None:
        global udpies_history

        now_str = time.strftime("%H:%M:%S", time.localtime())
        hex_str = " ".join(f"{b:02X}" for b in data)

        if udpies_history and udpies_history[0][0] == hex_str:
            last_hex, last_count, first_time = udpies_history[0]
            udpies_history[0] = (last_hex, last_count + 1, first_time)
        else:
            udpies_history.insert(0, (hex_str, 1, now_str))
            if len(udpies_history) > 20:
                udpies_history = udpies_history[:20]
                udpies_history.append(("...", 1, ""))

        lines: list[str] = []
        for pkt_hex, count, time_str in udpies_history:
            if count == 1:
                line = f"{time_str}\t{pkt_hex}"
            else:
                line = f"{time_str}\t{pkt_hex}"
                line += " " * (40 - len(line)) + f"x{count}"
            lines.append(line)

        udpies_text = "\n".join(lines)

        self.telemetry_sender({"SENDED UDPIES": udpies_text})
