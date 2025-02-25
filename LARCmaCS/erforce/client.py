import multiprocessing
import typing

import attr

from common.sockets import SocketWriter
from common.vision_client import VisionClient
from erforce.model import RobotCommand, MoveWheelVelocity, MoveLocalVelocity, MoveGlobalVelocity
from erforce.pb import RobotControl as ProtoRobotCommand, RobotCommand as ProtoRobotCommand, \
    RobotControl as ProtoRobotControl


@attr.s(auto_attribs=True, kw_only=True)
class ErForceClient(VisionClient):

    should_loop_commands: bool = False

    er_force_listen_ip: str = '127.0.0.1'
    er_force_listen_port: int = 10301

    _socket_writer: SocketWriter = attr.ib(init=False)
    _loop_sender: multiprocessing.Process = attr.ib(init=False)
    _last_packages: typing.Dict[int, bytes] = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        super(ErForceClient, self).__attrs_post_init__()
        self._socket_writer = SocketWriter(ip=self.er_force_listen_ip, port=self.er_force_listen_port)
        if self.should_loop_commands:
            manager = multiprocessing.Manager()
            self._last_packages = manager.dict()
            self._loop_sender = multiprocessing.Process(target=self._send_loop)
            self._loop_sender.start()

    def send_action_command(self, command: RobotCommand) -> None:
        packet = ProtoRobotControl()

        pb_command = ProtoRobotCommand()
        pb_command.id = command.robot_id
        pb_command.kick_speed = command.kick_speed
        pb_command.kick_angle = command.kick_angle
        pb_command.dribbler_speed = command.dribbler_speed

        move_command = command.move_command
        pb_move_command = pb_command.move_command
        if isinstance(move_command, MoveWheelVelocity):
            pb_move_command.wheel_velocity.back_left = move_command.back_left
            pb_move_command.wheel_velocity.back_right = move_command.back_right
            pb_move_command.wheel_velocity.front_left = move_command.front_left
            pb_move_command.wheel_velocity.front_right = move_command.front_right
        elif isinstance(move_command, MoveLocalVelocity):
            pb_move_command.local_velocity.angular = move_command.angular
            pb_move_command.local_velocity.forward = move_command.forward
            pb_move_command.local_velocity.left = move_command.left
        elif isinstance(move_command, MoveGlobalVelocity):
            pb_move_command.global_velocity.angular = move_command.angular
            pb_move_command.global_velocity.x = move_command.x
            pb_move_command.global_velocity.y = move_command.y
        else:
            raise Exception(f"Unsupported command {move_command}")

        packet.robot_commands.append(pb_command)
        package = packet.SerializeToString()
        if self.should_loop_commands:
            self._last_packages[command.robot_id] = package
        else:
            self._send(package)

    def _send(self, package: bytes):
        self._socket_writer.send_package(package)

    def _send_loop(self):
        while True:
            for robot_id, last_package in self._last_packages.items():
                self._send(last_package)
