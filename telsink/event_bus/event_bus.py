import threading
from attrs import define, field
import zmq

@define
class EventBus:
    poller: zmq.Poller = field()

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
        self.poller_thread.terminate()
        self.poller_thread.join()

    def __poll_loop(self):
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