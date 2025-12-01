import time
import zmq
import socket

from argparse import ArgumentParser
import yaml
from cattrs import structure, unstructure

from decoder.decoder import Decoder
import decoder.robot_command_model as rcm
import decoder.control_decoder_command_model as cdcm

parser = ArgumentParser()
parser.add_argument("--config", default="config.yml")
parser.add_argument("--ctrl", default="SIM")
args = parser.parse_args()

config = yaml.safe_load(open(args.config))
control_mode = args.ctrl

if config["ether"]["api_version"] != 3:
    raise Exception("Only Ether v3 is supported")


context = zmq.Context()

telemetry_socket = context.socket(zmq.PUB)
telemetry_socket.connect("ipc:///tmp/ether.telemetry.xsub")

inbound = config["control_decoder"]["s_control_sink_url"]
signals_inbound = config["ether"]["s_signals_pub_url"]
outbound_sim = config["ether"]["s_signals_sub_url"]

s_inbound = context.socket(zmq.SUB)
s_inbound.bind(inbound)
s_inbound.setsockopt_string(zmq.SUBSCRIBE, "{'control':")
s_inbound.setsockopt_string(zmq.SUBSCRIBE, '{"control":')
# s_inbound.setsockopt(zmq.CONFLATE, 1)

s_signals = context.socket(zmq.SUB)
s_signals.connect(signals_inbound)
s_signals.setsockopt_string(zmq.SUBSCRIBE, '{"control":')
s_signals.setsockopt_string(zmq.SUBSCRIBE, "{'control':")

s_outbound_sim = context.socket(zmq.PUB)
s_outbound_sim.connect(outbound_sim)

real_robots_ip_port_low: tuple[str, int] = (
    config["control_decoder"]["real_robots_ip_low"],
    config["control_decoder"]["real_robots_port"],
)
real_robots_ip_port_high: tuple[str, int] = (
    config["control_decoder"]["real_robots_ip_high"],
    config["control_decoder"]["real_robots_port"],
)
s_outbound_real_low = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_outbound_real_high = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

poller = zmq.Poller()
poller.register(s_inbound, zmq.POLLIN)
poller.register(s_signals, zmq.POLLIN)

decoder = Decoder()

print(f"Control decoder ready in mode {control_mode}")


def create_telemetry(data: bytes) -> str:
    """Create line for telemetry for single robot"""
    values = [
        data[1],
        int.from_bytes(data[2:3], "big", signed=True),
        int.from_bytes(data[3:4], "big", signed=True),
        int.from_bytes(data[4:5], "big", signed=True),
        data[5],
        data[6],
        data[7],
        data[8],
        data[9],
        data[10],
        data[11],
        data[12],
    ]
    values_str = [str(val) for val in values]
    return "\t" + "\t".join(values_str) + "\n"


last_update = 0.0
telemetry_text: str = "NO NEW MESSAGES"

while True:
    socks = dict(poller.poll(timeout=0))
    # print(socks.values())
    if socks == {}:
        time.sleep(0.01)
    else:
        try:
            if s_inbound in socks:
                signal = s_inbound.recv_json()
                signal_data = structure(signal["data"], cdcm.DecoderTeamCommand)

                telemetry_text = f'SENDING COMMANDS IN "{control_mode}" MODE\n \tr_id\tspeedX\tspeedY\tspeedW\tdribler\tvoltage\tkickUP\tkickDWN\tbeep\tdribEN\tcharEN\tautokck\n'

                if control_mode == "SIM":
                    command: rcm.RobotControlExt = decoder.decoder2sim(signal_data)
                    s_outbound_sim.send_json({"transnet": "actuate_robot", "data": unstructure(command)})
                else:
                    packets_low, packets_high = decoder.decoder2robot(signal_data)
                    for packet in packets_low:
                        s_outbound_real_low.sendto(packet, real_robots_ip_port_low)
                    for packet in packets_high:
                        s_outbound_real_high.sendto(packet, real_robots_ip_port_high)

                    for cmd in packets_low + packets_high:
                        telemetry_text += create_telemetry(cmd)
                    last_update = time.time()

            if s_signals in socks:
                signal = s_signals.recv_json()
                if signal["control"] == "send_udpie":
                    raw = signal.get("data")

                    try:
                        data = bytes(int(x) & 0xFF for x in raw)
                    except Exception as e:
                        print("send_udpie: cannot convert data to bytes:", e)
                        continue
                    
                    print("Get new udpie:", data)
                    robot_id = data[1] & 0x0F

                    if robot_id < 8:
                        s_outbound_real_low.sendto(data, real_robots_ip_port_low)
                    else:
                        s_outbound_real_high.sendto(data, real_robots_ip_port_high)
        except OverflowError:
            print("\033[31mAn invalid control command was received.\033[0m Are you sure the SIM/REAL mode of control is correct?")
            time.sleep(0.1)

    if time.time() - last_update < 2:
        telemetry_socket.send_json(
            {"COMMAND_DECODER": f"From previous message: {(time.time() - last_update)*1000:.2f}ms\n" + telemetry_text}
        )
    else:
        telemetry_socket.send_json({"COMMAND_DECODER": "NO NEW COMMANDS"})
