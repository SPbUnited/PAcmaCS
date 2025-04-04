import multiprocessing
from attrs import define, field

from common.sockets import SocketReader

from .pb.messages_robocup_ssl_wrapper_tracked_pb2 import TrackerWrapperPacket
from .tracker_model import TrackerWrapperPacket as TrackerWrapperPacketModel


@define
class TrackerClient:
    multicast_ip: str = field(default="224.5.23.2")
    multicast_port: int = field(default=10010)

    _socket_reader: SocketReader = field(init=False)
    _ssl_converter: TrackerWrapperPacket = field(
        default=TrackerWrapperPacket(), init=False
    )

    _tracking_data: TrackerWrapperPacketModel = field(init=False)
    _reader: multiprocessing.Process = field(init=False)

    def __attrs_post_init__(self) -> None:
        self._socket_reader = SocketReader(
            ip=self.multicast_ip, port=self.multicast_port
        )
        manager = multiprocessing.Manager()
        self._tracking_data = manager.Value(
            TrackerWrapperPacketModel,
            TrackerWrapperPacketModel(uuid="", source_name=None, tracked_frame=None),
        )
        self._reader = multiprocessing.Process(target=self._read_loop)

    def init(self) -> None:
        self._reader.start()

    def _read_loop(self) -> None:
        while True:
            new_package = self._socket_reader.read_package()
            self.process_packet(new_package)

    def process_packet(self, data):
        tracking_data_parser: TrackerWrapperPacketModel = TrackerWrapperPacket()
        tracking_data_parser.ParseFromString(data)
        tracking_data = TrackerWrapperPacketModel(
            uuid=tracking_data_parser.uuid,
            source_name=tracking_data_parser.source_name,
            tracked_frame=tracking_data_parser.tracked_frame,
        )
        self._tracking_data.value = tracking_data

    def get_detection(self) -> TrackerWrapperPacketModel:
        return self._tracking_data.value

    def close(self) -> None:
        self._reader.terminate()
        self._reader.join()
