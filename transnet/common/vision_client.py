import multiprocessing
import time
import typing

import attr

from common.vision_model import (
    Detection,
    Team,
    BallDetection,
    RobotDetection,
    Geometry,
    FrameInfo,
)
from protopy.vision.ssl_vision_detection_pb2 import (
    SSL_DetectionFrame,
    SSL_DetectionRobot,
    SSL_DetectionBall,
)

from protopy.vision.ssl_vision_wrapper_pb2 import SSL_WrapperPacket

from common.sockets import SocketReader


# TODO: Refactor this class
@attr.s(auto_attribs=True, kw_only=True)
class VisionClient:
    multicast_ip: str = "224.5.23.2"
    multicast_port: int = 10006

    vision_timeout: float = 1

    zmq_relay_template: typing.Any = attr.ib(default=None, init=True)

    _socket_reader: SocketReader = attr.ib(init=False)
    _ssl_converter: SSL_WrapperPacket = attr.ib(default=SSL_WrapperPacket(), init=False)

    _packages: typing.List[bytes] = attr.ib(init=False)
    _detections: typing.List[Detection] = attr.ib(init=False)
    _reader: multiprocessing.Process = attr.ib(init=False)
    _robot_detection_time: dict = attr.ib(init=False)

    is_blue_on_positive_side: bool = True

    def __attrs_post_init__(self) -> None:
        self._socket_reader = SocketReader(
            ip=self.multicast_ip, port=self.multicast_port, timeout=self.vision_timeout
        )
        manager = multiprocessing.Manager()
        self._packages = manager.list()
        self._detections = manager.list()
        self._reader = multiprocessing.Process(target=self._read_loop)
        self._robot_detection_time = {}

    def init(self) -> None:
        self._reader.start()

    def close(self) -> None:
        self._reader.terminate()
        self._reader.join()

    def get_detection(self, use_async: bool = True) -> Detection:
        if use_async:
            return self._detections[0]
        return self._read_detection()

    def get_robot(
        self, team: Team, robot_id: int, use_async: bool = True
    ) -> typing.Optional[RobotDetection]:
        found = False
        robot = None
        while not found:
            robot = self.get_detection(use_async).get_robot(team, robot_id)
            found = robot or use_async
        return robot

    def get_ball(self, use_async: bool = True) -> typing.Optional[BallDetection]:
        found = False
        ball = None
        while not found:
            ball = self.get_detection(use_async).get_ball()
            found = ball or use_async
        return ball

    def _read_loop(self) -> None:
        self._packages.append(bytes())
        detection = Detection([], [], None)
        self._detections.append(detection)
        zmq_relay = self.zmq_relay_template()
        while True:
            try:
                new_package = self._socket_reader.read_package()
                new_detection = self._read_detection(new_package)
                detection = self._merge_detections(detection, new_detection)
                self._packages[0] = new_package
                zmq_relay.send(new_package)
            except TimeoutError:
                pass
            detection = self._filter_timed_out_robots(detection)
            self._detections[0] = detection

    def _robot2key(self, robot: RobotDetection) -> tuple:
        return (robot.robot_id, robot.team)

    def _filter_timed_out_robots(self, detection: Detection) -> Detection:
        for i, robot in enumerate(detection.robots):
            if self._robot2key(robot) not in self._robot_detection_time:
                self._robot_detection_time[self._robot2key(robot)] = (
                    time.time() - robot.frame_info.t_capture
                )

        detection.robots = [
            robot
            for robot in detection.robots
            if time.time()
            - (
                self._robot_detection_time[self._robot2key(robot)]
                + robot.frame_info.t_capture
            )
            < self.vision_timeout
        ]

        new_robot_detection_time = {
            rkey: det_time
            for rkey, det_time in self._robot_detection_time.items()
            if rkey in [self._robot2key(r) for r in detection.robots]
        }

        self._robot_detection_time = new_robot_detection_time

        return detection

    def read_last_package(self) -> bytes:
        return self._packages[0]

    def _read_detection(self, raw_package: bytes = None) -> Detection:
        if raw_package is None:
            raw_package = self._socket_reader.read_package()

        package = self._ssl_converter.FromString(raw_package)

        balls = []
        robots = []
        if package.HasField("detection"):
            detection = package.detection

            frame_info = self._convert_frame_info(detection)
            balls = [self._convert_ball(frame_info, ball) for ball in detection.balls]

            robots = [
                self._convert_robot(frame_info, robot, Team.BLUE)
                for robot in detection.robots_blue
            ] + [
                self._convert_robot(frame_info, robot, Team.YELLOW)
                for robot in detection.robots_yellow
            ]

        geometry = None
        if package.HasField("geometry"):
            raw_geometry = package.geometry
            field = raw_geometry.field

            penalty_area_width = 0
            penalty_area_depth = 0
            center_circle_radius = 0

            for line in field.field_lines:
                if "PenaltyStretch" in line.name:
                    depth = abs(line.p1.x - line.p2.x)
                    width = abs(line.p1.y - line.p2.y)
                    penalty_area_depth = max(penalty_area_depth, depth)
                    penalty_area_width = max(penalty_area_width, width)

            for arc in field.field_arcs:
                if arc.name == "CenterCircle":
                    center_circle_radius = arc.radius
                    break

            geometry = Geometry(
                width=raw_geometry.field.field_width,
                height=raw_geometry.field.field_length,
                goalWidth=raw_geometry.field.goal_width,
                goalDepth=raw_geometry.field.goal_depth,
                penaltyAreaWidth=penalty_area_width,
                penaltyAreaDepth=penalty_area_depth,
                centerCircleRadius=center_circle_radius,
                borderSize=raw_geometry.field.boundary_width
            )

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
    def _convert_robot(
        frame_info: FrameInfo, convert_from: SSL_DetectionRobot, team: Team
    ) -> RobotDetection:
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
    def _convert_ball(
        frame_info: FrameInfo, convert_from: SSL_DetectionFrame
    ) -> SSL_DetectionBall:
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
