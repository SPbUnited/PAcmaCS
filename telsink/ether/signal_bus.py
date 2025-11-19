import threading
from attrs import define, field
import zmq

@define
class SignalBus:
    recipient_name: str = field()
    signal_in_url: str = field()
    signal_out_url: str = field()

    poller: zmq.Poller = field(init=False)
    subscribtions: dict = field(init=False)
    poller_thread: threading.Thread = field(init=False)

    context: zmq.Context = field(init=False)
    s_signals_out: zmq.Socket = field(init=False)

    def __attrs_post_init__(self):
        self.subscribtions = {}

        self.context = zmq.Context()
        self.s_signals_out = self.context.socket(zmq.PUB)
        self.s_signals_out.connect(self.signal_out_url)

    def on(self, signal, callback):
        self.subscribtions[signal] = callback

    def start(self):
        self.poller_thread = threading.Thread(target=self.__poll_loop)
        self.poller_thread.start()

    def stop(self):
        self.poller_thread.join()

    def __poll_loop(self):
        context = zmq.Context()
        s_signals_in = context.socket(zmq.SUB)
        s_signals_in.connect(self.signal_in_url)
        s_signals_in.setsockopt_string(zmq.SUBSCRIBE, '{"' + self.recipient_name + '":')
        s_signals_in.setsockopt_string(zmq.SUBSCRIBE, "{'" + self.recipient_name + "':")

        self.poller = zmq.Poller()
        self.poller.register(s_signals_in, zmq.POLLIN)

        while True:
            try:
                socks = dict(self.poller.poll(timeout=0))
            except KeyboardInterrupt:
                break

            if socks == {}:
                continue

            for socket in socks:
                signal = socket.recv_json()
                signal_type = next(iter(signal.values()))
                if signal_type in self.subscribtions:
                    self.subscribtions[signal_type](signal)
                    print("Signal received: ", signal_type)

        context.destroy()