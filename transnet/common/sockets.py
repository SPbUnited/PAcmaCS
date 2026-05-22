import socket
import struct
import sys
import time
from typing import Optional

import attr


@attr.s(auto_attribs=True, kw_only=True)
class SocketReader:
    ip: str = "224.5.23.2"
    port: int = 10020
    timeout: Optional[float] = 1.0
    sock: socket.socket = attr.ib(init=False)
    msg_size: int = attr.ib(default=65536, init=False)

    error_flag: bool = False

    def __attrs_post_init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))

        mreq = struct.pack("4sl", socket.inet_aton(self.ip), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        self.sock.settimeout(self.timeout)

    def read_package(self) -> bytes:
        error_counter = 0
        while True:
            try:
                ans = self.sock.recv(self.msg_size)
                if self.error_flag:
                    self.error_flag = False
                    print("  socket_reader info: ip ", self.ip, " port ", self.port)
                    print("\033[32m  reconnected...\033[0m\n")
                return ans
            except (socket.timeout, OSError) as e:
                if not self.error_flag:
                    self.error_flag = True
                    print(f"\033[31m  err in SocketReader: {e}\033[0m")
                    print("  socket_reader info: ip ", self.ip, " port ", self.port)
                time.sleep(0.25)
                error_counter += 1
                print(f"\033[33m  reconecting {error_counter}...\033[0m\n")

                if error_counter > 3:
                    print(f"\033[31m  err in SocketReader: {e}\n UNABLE TO RECONNECT\033[0m")
                    sys.exit(1)


@attr.s(auto_attribs=True, kw_only=True)
class SocketWriter:
    ip: str = "127.0.0.1"
    port: int = 20011
    sock: socket.socket = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    def send_package(self, msg: bytes) -> None:
        self.sock.sendto(msg, (self.ip, self.port))
