import errno
import socket
import struct
from typing import Optional

import attr


@attr.s(auto_attribs=True, kw_only=True)
class SocketReader:
    ip: str = "224.5.23.2"
    port: int = 10020
    timeout: Optional[float] = 0.5
    sock: socket.socket = attr.ib(init=False)
    msg_size: int = attr.ib(default=65536, init=False)

    error_flag: bool = False

    def __attrs_post_init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))

        mreq = struct.pack("=4s4s", socket.inet_aton(self.ip), socket.inet_aton("0.0.0.0"))
        try:
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            self.joined = True
        except OSError as e:
            if e.errno != errno.EADDRNOTAVAIL:
                raise

        self.sock.settimeout(self.timeout)

    def _reconnect(self) -> None:
        try:
            self.sock.close()
        except OSError:
            pass
        self.__attrs_post_init__()

    def read_package(self) -> bytes:
        while True:
            try:
                ans = self.sock.recv(self.msg_size)
                self.error_flag = False
                return ans
            except (socket.timeout, OSError) as e:
                if not self.error_flag:
                    self.error_flag = True
                    print("err in SocketReader: ", e)
                    print("socket_reader info: ip ", self.ip, " port ", self.port)
                    print("reconecting...\n")
                self._reconnect()


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
