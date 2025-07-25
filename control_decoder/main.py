import zmq

from argparse import ArgumentParser
import yaml
from cattrs import structure, unstructure

from decoder.decoder import Decoder
import decoder.control_decoder_command_model as cdcm

parser = ArgumentParser()
parser.add_argument("--config", default="config.yml")
args = parser.parse_args()

config = yaml.safe_load(open(args.config))

if config["ether"]["api_version"] != 3:
    raise Exception("Only Ether v3 is supported")


context = zmq.Context()

inbound = config["control_decoder"]["s_control_sink_url"]
outbound = config["ether"]["s_signals_sub_url"]

s_inbound = context.socket(zmq.SUB)
s_inbound.bind(inbound)
s_inbound.setsockopt_string(zmq.SUBSCRIBE, "{'control':")
s_inbound.setsockopt_string(zmq.SUBSCRIBE, '{"control":')

s_outbound = context.socket(zmq.PUB)
s_outbound.connect(outbound)

poller = zmq.Poller()
poller.register(s_inbound, zmq.POLLIN)

decoder = Decoder()

print("Control decoder ready")

while True:
    socks = dict(poller.poll(timeout=0))
    if socks == {}:
        continue
    if s_inbound in socks:
        signal = s_inbound.recv_json()
        signal_data = structure(signal["data"], cdcm.DecoderTeamCommand)

        # print(signal_data)

        if config["control_decoder"]["is_sim"]:
            command = decoder.decoder2sim(signal_data)
        else:
            command = decoder.decoder2robot(signal_data)

        # print(command)

        s_outbound.send_json(
            {"transnet": "actuate_robot", "data": unstructure(command)}
        )
