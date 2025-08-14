import threading
from attrs import define, field
import zmq


@define
class Drawty:
    draw_out_url: str = field()
    telemetry_out_url: str = field()

    context: zmq.Context = field(init=False)
    s_draw_out: zmq.Socket = field(init=False)
    s_telemetry_out: zmq.Socket = field(init=False)

    def __attrs_post_init__(self):
        self.context = zmq.Context()
        self.s_draw_out = self.context.socket(zmq.PUB)
        self.s_draw_out.connect(self.draw_out_url)
        self.s_telemetry_out = self.context.socket(zmq.PUB)
        self.s_telemetry_out.connect(self.telemetry_out_url)

    def telemetry(self, data: dict):
        self.s_telemetry_out.send_json(data)

    def draw(self, data: dict):
        self.s_draw_out.send_json(data)
