import zmq
from attrs import define, field
import threading


@define
class ThreadProxySwitch:

    real_type: zmq.SocketType = field()
    phantom_type: zmq.SocketType = field()
    out_type: zmq.SocketType = field()
    monitor_type: zmq.SocketType = field()
    ctrl_type: zmq.SocketType = field()

    real: zmq.Socket = field(init=False)
    phantom: zmq.Socket = field(init=False)
    out: zmq.Socket = field(init=False)
    monitor: zmq.Socket = field(init=False)
    ctrl: zmq.Socket = field(init=False)

    context: zmq.Context = field(init=False)

    thread: threading.Thread = field(init=False)
    poller: zmq.Poller = field(init=False)

    def __attrs_post_init__(self):
        self.context = zmq.Context()
        self.real = self.context.socket(self.real_type)
        self.phantom = self.context.socket(self.phantom_type)
        self.out = self.context.socket(self.out_type)
        self.monitor = self.context.socket(self.monitor_type)
        self.ctrl = self.context.socket(self.ctrl_type)

        self.poller = zmq.Poller()
        self.poller.register(self.real, zmq.POLLIN)
        self.poller.register(self.phantom, zmq.POLLIN)
        self.poller.register(self.out, zmq.POLLIN)
        self.poller.register(self.monitor, zmq.POLLIN)
        self.poller.register(self.ctrl, zmq.POLLIN)

    def connect_real(self, url):
        self.real.connect(url)

    def connect_phantom(self, url):
        self.phantom.connect(url)

    def connect_out(self, url):
        self.out.connect(url)

    def connect_monitor(self, url):
        self.monitor.connect(url)

    def connect_ctrl(self, url):
        self.ctrl.connect(url)

    def bind_real(self, url):
        self.real.bind(url)

    def bind_phantom(self, url):
        self.phantom.bind(url)

    def bind_out(self, url):
        self.out.bind(url)

    def bind_monitor(self, url):
        self.monitor.bind(url)

    def bind_ctrl(self, url):
        self.ctrl.bind(url)

    def start(self):
        self.thread = threading.Thread(target=self._relay_loop)
        self.thread.start()

    def _relay_loop(self):
        mode = "ETHER"

        while True:
            socks = dict(self.poller.poll(timeout=0))

            if socks == {}:
                continue

            if self.ctrl in socks and socks[self.ctrl] == zmq.POLLIN:
                mode = self.ctrl.recv_string()
                print("Mode: ", mode)
                self.ctrl.send_string(mode)

            if self.real in socks and socks[self.real] == zmq.POLLIN:
                data = self.real.recv_multipart()
                self.monitor.send_multipart(data)

                if mode == "ETHER":
                    self.out.send_multipart(data)

            if self.phantom in socks and socks[self.phantom] == zmq.POLLIN:
                data = self.phantom.recv_multipart()

                if mode == "PHANTOM":
                    self.out.send_multipart(data)

            if self.out in socks and socks[self.out] == zmq.POLLIN:
                data = self.out.recv_multipart()
                self.real.send_multipart(data)
                self.phantom.send_multipart(data)

            if self.monitor in socks and socks[self.monitor] == zmq.POLLIN:
                data = self.monitor.recv_multipart()
                self.real.send_multipart(data)

            # if self.out.poll(0):
            #     print("polling out")
            #     data = self.out.recv_multipart()
            #     self.real.send_multipart(data)
            #     self.phantom.send_multipart(data)

            # if self.real.poll(0):
            #     print("polling")
            #     data = self.real.recv_multipart()
            #     self.monitor.send_multipart(data)
            #     self.out.send_multipart(data)
