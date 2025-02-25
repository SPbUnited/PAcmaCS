import multiprocessing
import typing

import attr

from common.vision_model import Detection, Team, BallDetection, RobotDetection, Geometry, FrameInfo
from common.pb.messages_robocup_ssl_detection_pb2 import SSL_DetectionFrame, SSL_DetectionRobot, SSL_DetectionBall
from common.pb.messages_robocup_ssl_wrapper_pb2 import SSL_WrapperPacket

from common.sockets import SocketReader


# TODO: Refactor this class
@attr.s(auto_attribs=True, kw_only=True)
class VisionClient:
    multicast_ip: str = '224.5.23.2'
    multicast_port: int = 10020

    _socket_reader: SocketReader = attr.ib(init=False)
    _ssl_converter: SSL_WrapperPacket = attr.ib(default=SSL_WrapperPacket(), init=False)

    _detections: typing.List[Detection] = attr.ib(init=False)
    _reader: multiprocessing.Process = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        self._socket_reader = SocketReader(ip=self.multicast_ip, port=self.multicast_port)
        manager = multiprocessing.Manager()
        self._detections = manager.list()
        self._reader = multiprocessing.Process(target=self._read_loop)

    def init(self) -> None:
        self._reader.start()

    def close(self) -> None:
        self._reader.terminate()
        self._reader.join()

    def get_detection(self, use_async: bool = True) -> Detection:
        if use_async:
            return self._detections[0]
        return self._read_detection()

    def get_robot(self,  team: Team, robot_id: int, use_async: bool = True) -> typing.Optional[RobotDetection]:
        found = False
        robot = None
        while not found:
            robot = self.get_detection(use_async).get_robot(team, robot_id)
            found = robot or use_async
        return robot

    def get_ball(self,  use_async: bool = True) -> typing.Optional[BallDetection]:
        found = False
        ball = None
        while not found:
            ball = self.get_detection(use_async).get_ball()
            found = ball or use_async
        return ball

    def _read_loop(self) -> None:
        detection = Detection([], [], None)
        self._detections.append(detection)
        while True:
            new_detection = self._read_detection()
            detection = self._merge_detections(detection, new_detection)
            self._detections[0] = detection

    def _read_detection(self) -> Detection:
        raw_package = self._socket_reader.read_package()
        package = self._ssl_converter.FromString(raw_package)

        balls = []
        robots = []
        if package.HasField('detection'):
            detection = package.detection

            frame_info = self._convert_frame_info(detection)
            balls = [self._convert_ball(frame_info, ball) for ball in detection.balls]

            robots = [self._convert_robot(frame_info, robot, Team.BLUE) for robot in detection.robots_blue] + \
                     [self._convert_robot(frame_info, robot, Team.YELLOW) for robot in detection.robots_yellow]

        geometry = None
        if package.HasField('geometry'):
            raw_geometry = package.geometry
            # TODO: Implement
            geometry = Geometry()

        return Detection(balls, robots, geometry)

    @staticmethod
    def _convert_frame_info(convert_from: SSL_DetectionFrame) -> FrameInfo:
        return FrameInfo(
            convert_from.frame_number,
            convert_from.t_capture,
            convert_from.t_sent,
            convert_from.camera_id,
        )

    @staticmethod
    def _convert_robot(frame_info: FrameInfo, convert_from: SSL_DetectionRobot, team: Team) -> RobotDetection:
        return RobotDetection(
            frame_info,
            team,
            convert_from.confidence,
            convert_from.robot_id,
            convert_from.x,
            convert_from.y,
            convert_from.orientation,
            convert_from.pixel_x,
            convert_from.pixel_y,
        )

    @staticmethod
    def _convert_ball(frame_info: FrameInfo, convert_from: SSL_DetectionFrame) -> SSL_DetectionBall:
        return BallDetection(
            frame_info,
            convert_from.confidence,
            convert_from.x,
            convert_from.y,
            convert_from.z,
            convert_from.pixel_x,
            convert_from.pixel_y,
        )

    @staticmethod
    def _merge_detections(old: Detection, new: Detection) -> Detection:
        geometry = new.geometry or old.geometry
        balls = new.balls or old.balls
        robots = {(robot.robot_id, robot.team): robot for robot in old.robots}
        robots.update({(robot.robot_id, robot.team): robot for robot in new.robots})
        robots = list(robots.values())
        return Detection(balls, robots, geometry)
