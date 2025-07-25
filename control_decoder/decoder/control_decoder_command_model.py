from attrs import define, field
from typing import List, Optional

@define
class DecoderCommand:
    robot_id: int = field()

    forward_vel: float = field() # [m/s]
    left_vel: float = field() # [m/s]
    angular_vel: Optional[float] = field() # [rad/s]
    angle: Optional[float] = field() # [rad]

    kick_up: bool = field()
    kick_forward: bool = field()
    auto_kick_up: bool = field()
    auto_kick_forward: bool = field()

    kicker_setting: int = field() # 0-15 [popugi]
    dribbler_setting: float = field() # 0-15 [popugi]

@define
class DecoderTeamCommand:
    robot_commands: List[DecoderCommand] = field(factory=list)
    isteamyellow: bool = field(default=False)
