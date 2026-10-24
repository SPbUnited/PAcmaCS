import math

from decoder import control_decoder_command_model as cdcm


def build_nrf_packet(robot: cdcm.DecoderCommand) -> bytes:
    """Convert the decoder command to a 13-byte packet for the NRF bridge"""
    angle: float
    angvel_flag: int
    if robot.angle is not None:
        angle = -robot.angle
        angvel_flag = 1
    else:
        angle = robot.angular_vel or 0.0
        angvel_flag = 0

    autokick = 0
    if robot.auto_kick_forward:
        autokick = 1
    elif robot.auto_kick_up:
        autokick = 2
    elif robot.auto_kick_momentum:
        autokick = 3

    return create_packet(
        bot_number=int(robot.robot_id),
        speed_x=-robot.left_vel / (1100 / 100),
        speed_y=robot.forward_vel / (1100 / 100),
        speed_w=angle,
        dribbler_speed=int(robot.dribbler_setting),
        kicker_voltage=int(robot.kicker_setting),
        kick_up=int(robot.kick_up),
        kick_down=int(robot.kick_forward),
        beep=int(angvel_flag),
        dribbler_en=int(robot.dribbler_setting > 0),
        charge_en=int(robot.kicker_setting > 0),
        autokick=autokick,
    )


def create_packet(
    bot_number: int,      # unsigned byte (0-255)
    speed_x: float,       # signed byte (-128 to 127)
    speed_y: float,       # signed byte
    speed_w: float,       # angular velocity, or angle in rad if beep == 1
    dribbler_speed: int,  # unsigned byte
    kicker_voltage: int,  # unsigned byte
    kick_up: int,         # boolean flag (bit 0)
    kick_down: int,       # boolean flag (bit 1)
    beep: int,            # boolean flag (bit 2)
    dribbler_en: int,     # boolean flag (bit 3)
    charge_en: int,       # boolean flag (bit 4)
    autokick: int,        # unsigned byte
) -> bytes:
    encoded_w = angle_to_int8_pi128(speed_w) if beep == 1 else float_to_143(speed_w)

    bytes_list = [
        0x01,  # Header
        bot_number + 240,
        float_to_143(speed_x),
        float_to_143(speed_y),
        encoded_w,
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


def angle_to_int8_pi128(angle_rad: float) -> int:
    """
    Кодирует угол в int8_t с единицей измерения pi/128 rad.
    Возвращает значение в диапазоне 0..255 для упаковки в bytes().
    """
    raw = round(angle_rad * 128 / math.pi)

    # clamp to int8_t range
    raw = max(-128, min(127, raw))

    # convert signed int8_t to byte
    return raw & 0xFF


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

        if rounded_mantissa >= (1 << mantissa_bits) and not is_subnormal:
            stored_exponent += 1
            mantissa = 0
            if stored_exponent > max_exp:
                return (sign, max_exp, max_significand)
        else:
            mantissa = rounded_mantissa

        return (sign, stored_exponent, mantissa)


def float_to_143(x: float) -> int:
    sign, exp, mantissa = float_to_minifloat(x, 4, 3)
    out = sign << 7 | exp << 3 | mantissa
    return out
