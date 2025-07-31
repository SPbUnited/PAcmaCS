import multiprocessing
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
    log_file_handler = field(init=False)
    log_thread: multiprocessing.Process = field(init=False)

    is_recording: bool = field(init=False)

    def __attrs_post_init__(self):
        if not os.path.isdir(self.log_path):
            raise Exception(
                f"Log path {self.log_path} does not exist. Please create it"
            )
        self.is_recording = False

    def start_recording(self):
        self.log_file_name = self.log_path + str(int(self.__get_unix_timestamp())) + ".log"
        self.log_file_handler = open(self.log_file_name, "w")
        self.is_recording = True
        self.log_thread = multiprocessing.Process(
            target=self.__log_loop, args=(lambda: self.is_recording, self.socket_url_list)
        )
        self.log_thread.start()
        print("Started recording to ", self.log_file_name)

    def stop_recording(self):
        if(not self.is_recording):
            print("Not recording")
            return
        self.is_recording = False
        self.log_thread.join()
        self.log_file_handler.close()
        print("Stopped recording to ", self.log_file_name)

    def __log_loop(self, is_recording, socket_url_list):
        context = zmq.Context()
        poller = zmq.Poller()
        for socket_url in socket_url_list:
            socket = context.socket(zmq.SUB)
            socket.connect(socket_url)
            socket.setsockopt_string(zmq.SUBSCRIBE, "")
            poller.register(socket, zmq.POLLIN)

        while is_recording():
            try:
                socks = dict(poller.poll(timeout=0))
            except KeyboardInterrupt:
                break

            if socks == {}:
                continue

            for socket in socks:
                signal = socket.recv()
                endpoint = socket.getsockopt(zmq.LAST_ENDPOINT).decode("utf-8")
                self.__log_message(endpoint, signal)

        context.destroy()

    def __log_message(self, endpoint, message):
        timestamp = self.__get_unix_timestamp()
        self.log_file_handler.write(f"{timestamp} {endpoint} {message}\n")

    def __get_unix_timestamp(self):
        return float(time.time())
