"""13-byte packet for FB4 robots controlled over the radio box (NRF bridge).

The box forwards it to the robot as the NRF "new old format" packet, which the
firmware decodes in src/devices/nrfm_decoder/decoders/new_old_and_old_format.hpp:
  - velx/vely are fp8 (1-4-3 minifloat) in cm/s; the robot drives
    forward = vely, left = -velx;
  - angular_velocity_or_angle is fp8 in rad/s, or int8 in pi/128 rad when the
    angle flag is set; the robot negates both;
  - kicker_setting and dribbler_setting are 4-bit levels 0..15, the firmware maps
    kicker levels 1..15 to KICKER_MIN_VOLTAGE..KICKER_MAX_VOLTAGE.
"""
import math

from decoder import control_decoder_command_model as cdcm

PACKET_HEADER = 0x01
# High nibble of the robot byte is the NRF packet type: 0xF - "new old format"
NEW_OLD_FORMAT_TYPE = 0xF0

MAX_LEVEL = 15
KICKER_MIN_VOLTAGE = 100  # [V] level 1, devices/kicker/kicker.hpp MIN_SETTING_VOLTAGE
KICKER_MAX_VOLTAGE = 330  # [V] level 15, devices/kicker/kicker.hpp MAX_VOLTAGE


def voltage_to_level(voltage: float) -> int:
    """Kicker voltage [V] -> radio level 0..15 (0 - don't charge)"""
    if voltage <= 0:
        return 0
    level = 1 + (voltage - KICKER_MIN_VOLTAGE) * (MAX_LEVEL - 1) / (KICKER_MAX_VOLTAGE - KICKER_MIN_VOLTAGE)
    return max(1, min(MAX_LEVEL, round(level)))


def build_radio_packet(robot: cdcm.DecoderCommand) -> bytes:
    """Convert the decoder command (mm/s, rad/s, rad, volts) to the box packet"""
    # The firmware negates the turn, so send it negated to keep > 0 counterclockwise
    if robot.angle is not None:
        encoded_w = angle_to_int8_pi128(-robot.angle)
        angle_flag = 1
    else:
        encoded_w = float_to_143(-(robot.angular_vel or 0.0))  # [rad/s]
        angle_flag = 0

    if robot.auto_kick_forward:
        autokick = 1
    elif robot.auto_kick_up:
        autokick = 2
    elif robot.auto_kick_momentum:
        autokick = 3
    else:
        autokick = 0

    kicker_level = voltage_to_level(robot.kicker_setting)
    dribbler_level = max(0, min(MAX_LEVEL, round(robot.dribbler_setting)))

    return bytes([
        PACKET_HEADER,
        NEW_OLD_FORMAT_TYPE | (robot.robot_id & 0x0F),
        float_to_143(-robot.left_vel / 10),    # [mm/s] -> [cm/s], velx = -left
        float_to_143(robot.forward_vel / 10),  # [mm/s] -> [cm/s], vely = forward
        encoded_w,
        dribbler_level,
        kicker_level,
        int(robot.kick_up),
        int(robot.kick_forward),
        angle_flag,
        int(dribbler_level > 0),
        int(kicker_level > 0),
        autokick,
    ])


def angle_to_int8_pi128(angle_rad: float) -> int:
    """Encode an angle as int8 in pi/128 rad, returned as a byte 0..255"""
    raw = round(angle_rad * 128 / math.pi)
    raw = max(-128, min(127, raw))
    return raw & 0xFF


def float_to_minifloat(x: float, exponent_bits: int, mantissa_bits: int) -> tuple[int, int, int]:
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
    return sign << 7 | exp << 3 | mantissa
