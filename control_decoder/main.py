import time
from argparse import ArgumentParser

import decoder.control_decoder_command_model as cdcm
import yaml
import zmq
from cattrs import structure

from control_models import base_model, footbot2, footbot4, simulator

parser = ArgumentParser()
parser.add_argument("--config", default="config.yml")
parser.add_argument("--ctrl", default="SIM")
args = parser.parse_args()

config = yaml.safe_load(open(args.config))
control_mode = args.ctrl

if config["ether"]["api_version"] != 3:
    raise Exception("Only Ether v3 is supported")

if config["control_decoder"]["api_version"] != 2:
    raise Exception("Only Control_Decoder v2 is supported")

#########

context = zmq.Context()

telemetry_socket = context.socket(zmq.PUB)
telemetry_socket.connect("ipc:///tmp/ether.telemetry.xsub")

inbound = config["control_decoder"]["s_control_sink_url"]
signals_inbound = config["ether"]["s_signals_pub_url"]

s_inbound = context.socket(zmq.SUB)
s_inbound.bind(inbound)
s_inbound.setsockopt_string(zmq.SUBSCRIBE, "{'control':")
s_inbound.setsockopt_string(zmq.SUBSCRIBE, '{"control":')
# s_inbound.setsockopt(zmq.CONFLATE, 1)

s_signals = context.socket(zmq.SUB)
s_signals.connect(signals_inbound)
s_signals.setsockopt_string(zmq.SUBSCRIBE, '{"control":')
s_signals.setsockopt_string(zmq.SUBSCRIBE, "{'control':")

poller = zmq.Poller()
poller.register(s_inbound, zmq.POLLIN)
poller.register(s_signals, zmq.POLLIN)

#########

def telemetry_sender(topic_name: str, message:str):
    telemetry_socket.send_json({topic_name: message})

Decoder: base_model.ControlModel

match control_mode:
    case "SIM":
        Decoder = simulator.SimDecoder(config, telemetry_sender)
    case "FB4":
        Decoder = footbot4.FB4Decoder(config, telemetry_sender)
    case _:
        Decoder = footbot2.FB2Decoder(config, telemetry_sender)

print(f"Control decoder ready in mode {control_mode}")

telemetry_text = ""

while True:
    socks = dict(poller.poll(timeout=0))
    # print(socks.values())
    if socks == {}:
        time.sleep(0.01)
    else:
        if s_inbound in socks:
            try:
                signal = s_inbound.recv_json()
                signal_data = structure(signal["data"], cdcm.DecoderTeamCommand)
                Decoder.process(signal_data)

            except OverflowError:
                print(
                    "\033[31mAn invalid control command was received.\033[0m Are you sure the SIM/REAL mode of control is correct?"
                )
                time.sleep(0.1)
            except Exception as e:
                print("Unknown exception while processing inbound: ", e)
                time.sleep(0.1)
            

        if s_signals in socks:
            try:
                signal = s_signals.recv_json()
                if signal["control"] == "send_udpie":
                    raw = signal.get("data")
                    Decoder.process_signal(raw)

            except Exception as e:
                print("Unknown exception while processing inbound: ", e)
                time.sleep(0.1)

    Decoder.send_telemetry()

