from datetime import datetime
import multiprocessing
from ctypes import c_bool
import time
from typing import List
from attrs import define, field
import os

import zmq


@define
class Logger:
    log_path: str = field()
    socket_url_list: List[str] = field()

    log_file_name: str = field(init=False)
    log_file_handler = field(init=False, default=None)
    log_thread: multiprocessing.Process = field(init=False)

    is_recording: multiprocessing.Value = field(init=False)

    def __attrs_post_init__(self):
        if not os.path.isdir(self.log_path):
            raise Exception(
                f"Log path {self.log_path} does not exist. Please create it"
            )
        self.is_recording = multiprocessing.Value(c_bool, False)

    def start_recording(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        self.log_file_name = f"{self.log_path}{timestamp}.log"

        self.is_recording.value = True


        self.log_thread = multiprocessing.Process(
            target=self._log_loop,
            args=(
                self.log_file_name,
                self.is_recording,
                self.socket_url_list,
            ),
        )
        self.log_thread.start()
        print("Started recording to ", self.log_file_name)

    def stop_recording(self):
        if not self.is_recording.value:
            print("Not recording")
            return

        self.is_recording.value = False
        self.log_thread.join()
        print("Stopped recording to ", self.log_file_name)


    def _log_loop(self, log_file_name, is_recording, socket_url_list):
        log_file_handler = open(log_file_name, "wb")

        context = zmq.Context()
        poller = zmq.Poller()

        sockets = []
        for socket_url in socket_url_list:
            socket = context.socket(zmq.SUB)
            socket.connect(socket_url)
            socket.setsockopt_string(zmq.SUBSCRIBE, "")
            poller.register(socket, zmq.POLLIN)
            sockets.append(socket)

        while is_recording.value:
            socks = dict(poller.poll(timeout=10))
            if not socks:
                continue

            for socket in socks:
                signal = socket.recv()
                endpoint = socket.getsockopt(zmq.LAST_ENDPOINT).decode("utf-8")

                log_file_handler.write(
                    f"{time.time()} {endpoint} ".encode() + signal + b"\n"
                )
                

        log_file_handler.close()
        context.destroy()

    def __get_unix_timestamp(self):
        return float(time.time())
