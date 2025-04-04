from attrs import define, field
import socket
import threading


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

        # Join the multicast group
        mreq = struct.pack(
            "4sl", socket.inet_aton(self.multicast_group), socket.INADDR_ANY
        )
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

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
