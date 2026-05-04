import socket
import struct
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
        while True:
            try:
                ans = self.sock.recv(self.msg_size)
                self.error_flag = False
                return ans
            except (socket.timeout, OSError) as e:
                if not self.error_flag:
                    self.error_flag = True
                    print(f"\033[31m  err in SocketReader: {e}\033[0m")
                    print("  socket_reader info: ip ", self.ip, " port ", self.port)
                    print("\033[33m  reconecting...\033[0m\n")



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
