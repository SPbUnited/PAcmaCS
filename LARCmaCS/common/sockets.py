import socket
import struct

import attr


@attr.s(auto_attribs=True, kw_only=True)
class SocketReader:
    ip: str = '224.5.23.2'
    port: int = 10020
    sock: socket.socket = attr.ib(init=False)
    msg_size: int = attr.ib(default=65536, init=False)

    def __attrs_post_init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))

        mreq = struct.pack("4sl", socket.inet_aton(self.ip), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def read_package(self) -> bytes:
        return self.sock.recv(self.msg_size)


@attr.s(auto_attribs=True, kw_only=True)
class SocketWriter:
    ip: str = '127.0.0.1'
    port: int = 20011
    sock: socket.socket = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    def send_package(self, msg: bytes) -> None:
        self.sock.sendto(msg, (self.ip, self.port))

