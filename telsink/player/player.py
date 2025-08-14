import multiprocessing
import zmq
from attrs import define, field
import time


@define
class Player:
    socket_url_mapping: dict = field()

    playback_file_name: str = field(init=False)
    playback_file_handler = field(init=False)
    playback_thread: multiprocessing.Process = field(init=False)

    is_playing: bool = field(init=False)
    playback_speed: float = field(init=False)

    def __attrs_post_init__(self):
        self.is_playing = False
        self.playback_speed = 1.0

    def start_playback(self, playback_file_name):
        self.playback_file_name = playback_file_name
        self.playback_file_handler = open(self.playback_file_name, "rb")
        self.is_playing = True
        self.playback_thread = multiprocessing.Process(
            target=self.__playback_loop,
            args=(
                lambda: self.is_playing,
                self.socket_url_mapping,
                lambda: self.playback_speed,
            ),
        )
        self.playback_thread.start()
        print("Started playback from ", self.playback_file_name)

    def stop_playback(self):
        if not self.is_playing:
            print("Not playing")
            return
        self.is_playing = False
        self.playback_thread.terminate()
        self.playback_thread.join()
        self.playback_file_handler.close()
        print("Stopped playback from ", self.playback_file_name)

    def __playback_loop(self, is_playing, socket_url_mapping, playback_speed):
        context = zmq.Context()

        sockets = {}
        for socket_src_url, socket_target_url in socket_url_mapping.items():
            sockets[socket_src_url] = context.socket(zmq.PUB)
            sockets[socket_src_url].connect(socket_target_url)

        start_time = time.time()
        dtime = 0
        offset_time = None

        while is_playing():
            line = self.playback_file_handler.readline()
            if line == b"":
                break
            # print(line[:100])
            timestamp, source_endpoint, message = line.decode().split(" ", maxsplit=2)
            timestamp = float(timestamp)

            if offset_time is None:
                offset_time = timestamp

            while timestamp - offset_time > dtime:
                dtime += (time.time() - start_time - dtime) * playback_speed()

            # print(offset_time, timestamp, timestamp - offset_time, dtime)

            sockets[source_endpoint].send(message.encode())
