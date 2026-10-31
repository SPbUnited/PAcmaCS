from attrs import define, field
from cattrs import Converter
from cattrs.strategies import configure_tagged_union
from typing import List, Optional, Union

@define
class DecoderCommand:
    robot_id: int = field()

    forward_vel: float = field() # [m/s]
    left_vel: float = field() # [m/s]
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

    x: float = field() # [m]
    y: float = field() # [m]
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

AnyDecoderCommand = Union[DecoderCommand, DecoderRicochetCommand, DecoderCatchBallCommand]

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
}

converter = Converter()
configure_tagged_union(
    AnyDecoderCommand,
    converter,
    tag_generator=CONTROL_TYPES.__getitem__,
    tag_name="control_type",
    default=DecoderCommand,
)
    