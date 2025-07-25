from attrs import define, field
from typing import Optional, List


@define
class MoveWheelVelocity:
    """Move robot with wheel velocities

    Attributes:
        front_right (float): Velocity [m/s] of front right wheel
        back_right (float): Velocity [m/s] of back right wheel
        back_left (float): Velocity [m/s] of back left wheel
        front_left (float): Velocity [m/s] of front left wheel
    """

    front_right: float = field()
    back_right: float = field()
    back_left: float = field()
    front_left: float = field()


@define
class MoveLocalVelocity:
    """Move robot with local velocity

    Attributes:
        forward (float): Velocity forward [m/s] (towards the dribbler)
        left (float): Velocity to the left [m/s]
        angular (float): Angular velocity counter-clockwise [rad/s]
    """

    forward: float = field()
    left: float = field()
    angular: float = field()


@define
class MoveGlobalVelocity:
    """Move robot with global velocity

    Attributes:
        x (float): Velocity on x-axis of the field [m/s]
        y (float): Velocity on y-axis of the field [m/s]
        angular (float): Angular velocity counter-clockwise [rad/s]
    """

    x: float = field()
    y: float = field()
    angular: float = field()


@define
class RobotMoveCommand:
    """Wrapper for different kinds of movement commands

    Attributes:
        wheel_velocity (Optional[MoveWheelVelocity]): Move with wheel velocities
        local_velocity (Optional[MoveLocalVelocity]): Move with local velocity
        global_velocity (Optional[MoveGlobalVelocity]): Move with global velocity

    Only one of velocity types can be set.
    """

    wheel_velocity: Optional[MoveWheelVelocity] = field(default=None)
    local_velocity: Optional[MoveLocalVelocity] = field(default=None)
    global_velocity: Optional[MoveGlobalVelocity] = field(default=None)

    def __attrs_post_init__(self):
        present = []
        if self.wheel_velocity is not None:
            present.append("wheel_velocity")
        if self.local_velocity is not None:
            present.append("local_velocity")
        if self.global_velocity is not None:
            present.append("global_velocity")
        if len(present) != 1:
            raise ValueError(f"Exactly one command must be set, found {present}")


@define
class RobotCommand:
    """Full command for a single robot

    Attributes:
        id (int): Id of the robot
        move_command (Optional[RobotMoveCommand]): Movement command
        kick_speed (Optional[float]): Absolute (3 dimensional) kick speed [m/s]
        kick_angle (float): Kick angle [degree] (defaults to 0 degrees for a straight kick)
        dribbler_speed (Optional[float]): Dribbler speed in rounds per minute [rpm]
    """

    id: int = field()  # Id of the robot
    move_command: Optional[RobotMoveCommand] = field(default=None)
    kick_speed: Optional[float] = field(default=None)
    kick_angle: float = field(default=0.0)
    dribbler_speed: Optional[float] = field(default=None)


@define
class RobotControl:
    """Command from the connected client to the simulator

    Attributes:
        robot_commands (List[RobotCommand]): Control the robots
    """

    robot_commands: List[RobotCommand] = field(factory=list)


@define
class RobotCommandExt(RobotCommand):
    """Full command for a single robot (including team color)

    Attributes:
        isteamyellow (bool): Team color of the robot
        id (int): Id of the robot
        move_command (Optional[RobotMoveCommand]): Movement command
        kick_speed (Optional[float]): Absolute (3 dimensional) kick speed [m/s]
        kick_angle (float): Kick angle [degree] (defaults to 0 degrees for a straight kick)
        dribbler_speed (Optional[float]): Dribbler speed in rounds per minute [rpm]
    """

    isteamyellow: bool = field(default=False)


@define
class RobotControlExt(RobotControl):
    """Command from the connected client to the simulator (including team color)

    Attributes:
        isteamyellow (bool): Team color of the robot
        robot_commands (List[RobotCommand]): Control the robots
    """

    isteamyellow: bool = field(default=False)
