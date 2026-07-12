from attrs import define, field
from typing import List, Optional

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

@define
class DecoderTeamCommand:
    robot_commands: List[DecoderCommand] = field(factory=list)
    isteamyellow: bool = field(default=False)
