import threading
from attrs import define, field
import zmq

@define
class SignalBus:
    recipient_name: str = field()
    signal_url: str = field()

    poller: zmq.Poller = field(init=False)
    subscribtions: dict = field(init=False)
    poller_thread: threading.Thread = field(init=False)

    def __attrs_post_init__(self):
        self.subscribtions = {}

    def on(self, signal, callback):
        self.subscribtions[signal] = callback

    def start(self):
        self.poller_thread = threading.Thread(target=self.__poll_loop)
        self.poller_thread.start()

    def stop(self):
        self.poller_thread.join()

    def __poll_loop(self):
        context = zmq.Context()
        s_signals = context.socket(zmq.SUB)
        s_signals.connect(self.signal_url)
        s_signals.setsockopt_string(zmq.SUBSCRIBE, '{"' + self.recipient_name + '":')
        s_signals.setsockopt_string(zmq.SUBSCRIBE, "{'" + self.recipient_name + "':")

        self.poller = zmq.Poller()
        self.poller.register(s_signals, zmq.POLLIN)

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