import attr

from common.vision_client import VisionClient
from common.vision_model import Team
from common.sockets import SocketWriter
from grsim.model import ActionCommand, BallReplacement, RobotReplacement

from grsim.pb.grsim_commands_pb2 import grSim_Robot_Command as GrSimRobotCommand
from grsim.pb.grsim_packet_pb2 import grSim_Packet as GrSimPacket
from grsim.pb.grsim_replacement_pb2 import grSim_RobotReplacement as GrSimRobotReplacement


# TODO: Refactor this class
@attr.s(auto_attribs=True, kw_only=True)
class GrSimClient(VisionClient):

    grsim_listen_ip: str = '127.0.0.1'
    grsim_listen_port: int = 20011

    _socket_writer: SocketWriter = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        super(GrSimClient, self).__attrs_post_init__()
        self._socket_writer = SocketWriter(ip=self.grsim_listen_ip, port=self.grsim_listen_port)

    def send_action_command(self, command: ActionCommand) -> None:
        packet = GrSimPacket()
        packet.commands.isteamyellow = command.team.value == Team.YELLOW.value
        packet.commands.timestamp = command.timestamp
        robot_command = GrSimRobotCommand()
        robot_command.id = command.robot_id
        robot_command.wheelsspeed = command.wheelsspeed
        robot_command.velnormal = command.velnormal
        robot_command.kickspeedx = command.kickspeedx
        robot_command.kickspeedz = command.kickspeedz
        robot_command.veltangent = command.veltangent
        robot_command.velangular = command.velangular
        robot_command.spinner = command.spinner
        if command.wheel1:
            robot_command.wheel1 = command.wheel1
        if command.wheel2:
            robot_command.wheel2 = command.wheel2
        if command.wheel3:
            robot_command.wheel3 = command.wheel3
        if command.wheel4:
            robot_command.wheel4 = command.wheel4
        packet.commands.robot_commands.append(robot_command)
        self._socket_writer.send_package(packet.SerializeToString())

    def send_robot_replacement(self, command: RobotReplacement) -> None:
        packet = GrSimPacket()
        robot_replacement = GrSimRobotReplacement()
        robot_replacement.x = command.x
        robot_replacement.y = command.y
        robot_replacement.dir = command.direction
        robot_replacement.id = command.robot_id
        robot_replacement.yellowteam = command.team.value == Team.YELLOW.value
        packet.replacement.robots.append(robot_replacement)
        self._socket_writer.send_package(packet.SerializeToString())

    def send_ball_replacement(self, command: BallReplacement) -> None:
        packet = GrSimPacket()
        packet.replacement.ball.x = command.x
        packet.replacement.ball.y = command.y
        packet.replacement.ball.vx = command.vx
        packet.replacement.ball.vy = command.vy
        self._socket_writer.send_package(packet.SerializeToString())
