from attrs import define, field
from cattrs import Converter
from cattrs.strategies import configure_tagged_union
from typing import List, Optional, Union

@define
class DecoderCommand:
    robot_id: int = field()

    forward_vel: float = field() # [mm/s]
    left_vel: float = field() # [mm/s]
    angular_vel: Optional[float] = field(default=None) # [rad/s]
    angle: Optional[float] = field(default=None) # [rad]

    kick_up: bool = field(default=False)
    kick_forward: bool = field(default=False)
    auto_kick_up: bool = field(default=False)
    auto_kick_forward: bool = field(default=False)
    auto_kick_momentum: bool = field(default=False)

    kicker_setting: int = field(default=0) # 0-15 [popugi]
    dribbler_setting: float = field(default=0) # 0-15 [popugi]

    beep: bool = field(default=False)

@define
class DecoderRicochetCommand:
    """Drive to (x, y) holding angle; once the onboard camera sees the ball,
    shift sideways to meet it without turning"""
    robot_id: int = field()

    x: float = field() # [mm]
    y: float = field() # [mm]
    angle: float = field() # [rad]

    kick_up: bool = field(default=False)
    kick_forward: bool = field(default=False)
    auto_kick_up: bool = field(default=False)
    auto_kick_forward: bool = field(default=False)
    auto_kick_momentum: bool = field(default=False)

    kicker_setting: int = field(default=0)
    dribbler_setting: float = field(default=0)

    beep: bool = field(default=False)

@define
class DecoderCatchBallCommand:
    """Turn to angle and wait for the ball: no driving forward,
    shift sideways to meet the ball seen by the onboard camera"""
    robot_id: int = field()

    angle: float = field() # [rad]

    kick_up: bool = field(default=False)
    kick_forward: bool = field(default=False)
    auto_kick_up: bool = field(default=False)
    auto_kick_forward: bool = field(default=False)
    auto_kick_momentum: bool = field(default=False)

    kicker_setting: int = field(default=0)
    dribbler_setting: float = field(default=0)

    beep: bool = field(default=False)

@define
class DecoderCoefficientsCommand:
    """Controller coefficients (Coefficients in robot/control.proto), not a motion command: the robot keeps
    running the one it has. None: not sent, the robot keeps its value. Units as in the proto (m, m/s, s),
    not mm. FB4 over WiFi only"""
    robot_id: int = field()

    # STM32
    angle_k: Optional[float] = field(default=None)
    angle_b: Optional[float] = field(default=None)
    max_linear_vel: Optional[float] = field(default=None) # [m/s]
    max_linear_accel: Optional[float] = field(default=None) # [m/s^2]
    max_angular_vel: Optional[float] = field(default=None) # [rad/s]
    max_angular_accel: Optional[float] = field(default=None) # [rad/s^2]
    wheel_vel_p: Optional[float] = field(default=None)
    wheel_vel_i: Optional[float] = field(default=None)
    # fb4-runner
    position_kp: Optional[float] = field(default=None) # [1/s]
    position_max_vel: Optional[float] = field(default=None) # [m/s]
    ricochet_gain: Optional[float] = field(default=None) # [1/s]
    catch_gain: Optional[float] = field(default=None) # [1/s]
    onboard_max_vel: Optional[float] = field(default=None) # [m/s]
    kicker_face_x: Optional[float] = field(default=None) # [m]
    min_approach_vel: Optional[float] = field(default=None) # [m/s]
    freeze_s: Optional[float] = field(default=None) # [s]

AnyDecoderCommand = Union[
    DecoderCommand, DecoderRicochetCommand, DecoderCatchBallCommand, DecoderCoefficientsCommand
]

@define
class DecoderTeamCommand:
    robot_commands: List[AnyDecoderCommand] = field(factory=list)
    isteamyellow: bool = field(default=False)

# The command type is picked by the "control_type" key of each robot command
# (named after RobotControlType); commands without it are DecoderCommand
CONTROL_TYPES = {
    DecoderCommand: "NEW_FORMAT",
    DecoderRicochetCommand: "RICOCHET",
    DecoderCatchBallCommand: "CATCH_BALL",
    DecoderCoefficientsCommand: "SET_COEFFICIENTS",
}

converter = Converter()
configure_tagged_union(
    AnyDecoderCommand,
    converter,
    tag_generator=CONTROL_TYPES.__getitem__,
    tag_name="control_type",
    default=DecoderCommand,
)
    