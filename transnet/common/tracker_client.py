import multiprocessing
from typing import Any, Dict
from attrs import define, field
from cattrs import structure, unstructure

from common.sockets import SocketReader

from protopy.tracker.ssl_vision_wrapper_tracked_pb2 import (
    TrackerWrapperPacket as TrackerWrapperPacketProto,
)
from .tracker_model import TrackerWrapperPacket
from .tracker_model import proto_to_wrapper_packet
from . import tracker_model


@define
class TrackerClient:
    multicast_ip: str = field(default="224.5.23.2")
    multicast_port: int = field(default=10010)

    zmq_relay_template: Any = field(init=True, default=None)

    _socket_reader: SocketReader = field(init=False)
    _ssl_converter: TrackerWrapperPacketProto = field(
        default=TrackerWrapperPacketProto(), init=False
    )

    _tracking_data: Dict = field(init=False)
    _reader: multiprocessing.Process = field(init=False)

    def __attrs_post_init__(self) -> None:
        self._socket_reader = SocketReader(
            ip=self.multicast_ip, port=self.multicast_port
        )
        manager = multiprocessing.Manager()
        self._tracking_data = manager.dict()
        self._reader = multiprocessing.Process(target=self._read_loop)

    def init(self) -> None:
        self._reader.start()

    def _read_loop(self) -> None:
        zmq_relay = self.zmq_relay_template()

        start = 0
        while True:

            new_package = self._socket_reader.read_package()
            self._socket_reader.read_package()
            self._socket_reader.read_package()
            self._socket_reader.read_package()
            processed_packet = self.process_packet(new_package)
            if processed_packet is None:
                continue

            zmq_relay.send(unstructure(processed_packet))

    def process_packet(self, data) -> TrackerWrapperPacket:
        tracking_data_parser: TrackerWrapperPacket = TrackerWrapperPacketProto()
        tracking_data_parser.ParseFromString(data)
        if (
            tracking_data_parser.uuid in self._tracking_data.keys()
            and self._tracking_data[
                tracking_data_parser.uuid
            ].tracked_frame.frame_number
            >= tracking_data_parser.tracked_frame.frame_number
        ):
            return None

        tracking_data: TrackerWrapperPacket = proto_to_wrapper_packet(
            tracking_data_parser
        )
        self._tracking_data[tracking_data.uuid] = tracking_data
        return tracking_data

    def get_detections(self) -> TrackerWrapperPacket:
        return self._tracking_data.copy()

    def close(self) -> None:
        self._reader.terminate()
        self._reader.join()
