from attrs import define, field

from .multicast_listener import MulticastListener

from .pb.messages_robocup_ssl_wrapper_tracked_pb2 import TrackerWrapperPacket
from .tracker_model import TrackerWrapperPacket as TrackerWrapperPacketModel


class TrackerClient:
    multicast_ip: str = field(default="224.5.23.2")
    multicast_port: int = field(default=10010)

    on_packet_callback: callable = field()

    multicast_listener: MulticastListener = field(init=False)

    def __attrs_post_init__(self) -> None:
        self.multicast_listener = MulticastListener(
            self.multicast_ip,
            self.multicast_port,
            self.process_packet,
        )
        self.multicast_listener.start()

    def start(self):
        # self.multicast_listener.start()
        pass

    def process_packet(self, data, addr):
        print(f"Received packet from {addr}, length: {len(data)}")
        # Add parsing logic here (e.g., SSL Vision protobuf parsing)
        tracking_data: TrackerWrapperPacketModel = TrackerWrapperPacket()
        tracking_data.ParseFromString(data)
        # print(tracking_data["tracked_frame"]["balls"])
        print(tracking_data.tracked_frame.balls)

    def close(self) -> None:
        self.multicast_listener.stop()
