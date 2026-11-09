from attrs import define, field
import socket
import threading

from common.sockets import join_multicast_group


@define
class MulticastListener:
    multicast_group: str = field()
    port: int = field()
    callback: callable = field()
    sock = field(init=False)
    running = field(init=False)
    thread = field(init=False)

    def start(self):

        print("Starting multicast listener...")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("", self.port))

        join_multicast_group(self.sock, self.multicast_group)

        self.running = True
        self.thread = threading.Thread(target=self._listen)
        self.thread.start()

        print("Multicast listener started.")

    def _listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(
                    65535
                )  # Buffer size for SSL Vision packets
                self.callback(data, addr)
            except Exception as e:
                if self.running:
                    print(f"Error receiving data: {e}")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        if self.sock:
            self.sock.close()
