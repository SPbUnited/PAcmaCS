from attrs import define, field
import zmq
from common.sockets import SocketReader
import multiprocessing


@define
class GameControllerRelay:
    game_controller_fan_url: str

    multicast_ip: str = field(default="224.5.23.1")
    multicast_port: int = field(default=10003)

    _reader: multiprocessing.Process = field(init=False)

    def __attrs_post_init__(self):
        pass
        self._reader = multiprocessing.Process(
            target=self._read_loop,
        )

    def init(self):
        self._reader.start()

    def _read_loop(self):
        reader = SocketReader(ip=self.multicast_ip, port=self.multicast_port)

        context = zmq.Context()
        relay = context.socket(zmq.PUB)
        relay.bind(self.game_controller_fan_url)
        print("Game controller relay init")
        while True:
            data = reader.read_package()
            relay.send(data)
