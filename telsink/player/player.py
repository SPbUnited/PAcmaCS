import multiprocessing
from ctypes import c_bool, c_float
import zmq
from attrs import define, field
import time


@define
class Player:
    socket_url_mapping: dict = field()

    playback_file_name: str = field(init=False)
    playback_thread: multiprocessing.Process = field(init=False)

    is_playing: bool = field(init=False)
    is_paused: bool = field(init=False)
    playback_speed: float = field(init=False)
    forward_override: float = field(init=False)

    duration: float = field(init=False, default=0.0)
    current_time: float = field(init=False)

    def __attrs_post_init__(self):
        self.is_playing = multiprocessing.Value(c_bool, False)
        self.is_paused = multiprocessing.Value(c_bool, False)
        self.playback_speed = multiprocessing.Value(c_float, 1.0)
        self.forward_override = multiprocessing.Value(c_float, 0.0)
        self.current_time = multiprocessing.Value(c_float, 0.0)

    def start_playback(self, playback_file_name):
        if self.is_playing.value:
            print("Already playing")
            return
        self.playback_file_name = playback_file_name

        with open(self.playback_file_name, "rb") as f:
            first_line = f.readline()
            if not first_line:
                print("Empty log file")
                return

            first_ts = float(first_line.decode().split(" ", 1)[0])
            last_ts = first_ts

            for line in f:
                last_ts = float(line.decode().split(" ", 1)[0])

        self.duration = max(0.0, last_ts - first_ts)

        self.is_playing.value = True
        self.is_paused.value = False
        self.current_time.value = 0.0
        self.forward_override.value = 0.0

        self.playback_thread = multiprocessing.Process(
            target=self._playback_loop,
            args=(
                self.playback_file_name,
                self.is_playing,
                self.is_paused,
                self.socket_url_mapping,
                self.playback_speed,
                self.current_time,
                self.forward_override,
            ),
        )
        self.playback_thread.start()

        print("Started playback from ", self.playback_file_name)

    def stop_playback(self):
        if not self.is_playing.value:
            print("Not playing")
            return
        self.is_playing.value = False
        self.is_paused.value = False
        self.playback_thread.terminate()
        self.playback_thread.join()
        print("Stopped playback from ", self.playback_file_name)

    def toggle_pause(self):
        self.is_paused.value = not self.is_paused.value

    def set_playback_speed(self, speed):
        if speed < 0 or speed > 10:
            print("Invalid speed")
            return
        print("Set playback speed to ", speed)
        self.playback_speed.value = speed

    def move_forward(self, time_to_move: float):
        self.forward_override.value += time_to_move

    def _playback_loop(
        self,
        playback_file_name,
        is_playing,
        is_paused,
        socket_url_mapping,
        playback_speed,
        current_time,
        forward_override,
    ):
        playback_file = open(playback_file_name, "rb")
        context = zmq.Context()
        sockets = {}

        for src, dst in socket_url_mapping.items():
            s = context.socket(zmq.PUB)
            s.connect(dst)
            sockets[src] = s

        current_time.value = 0.0
        dtime = 0.0
        first_timestamp = None

        while is_playing.value:
            line = playback_file.readline()
            if not line:
                break

            ts_str, source_endpoint, message = line.decode().split(" ", 2)
            timestamp = float(ts_str)

            if first_timestamp is None:
                first_timestamp = timestamp
                last_update = time.time()
                continue

            target_time = timestamp - first_timestamp

            while True:
                if dtime >= target_time:
                    break

                if not is_playing.value:
                    break


                if is_paused.value:
                    time.sleep(0.01)
                    last_update = time.time()
                    continue

                time.sleep(0.001)

                # apply seek
                if forward_override.value != 0.0:
                    dtime += forward_override.value
                    forward_override.value = 0.0

                dtime += (time.time() - last_update) * playback_speed.value
                current_time.value = dtime
                last_update = time.time()


            sockets[source_endpoint].send(message.encode())



        playback_file.close()
        context.destroy()
        is_playing.value = False
        current_time.value = 0.0

