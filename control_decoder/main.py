import time
from argparse import ArgumentParser

import decoder.control_decoder_command_model as cdcm
import yaml
import zmq

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
s_signals.setsockopt_string(zmq.SUBSCRIBE, '{"transnet":')
s_signals.setsockopt_string(zmq.SUBSCRIBE, "{'transnet':")

poller = zmq.Poller()
poller.register(s_inbound, zmq.POLLIN)
poller.register(s_signals, zmq.POLLIN)

#########

def telemetry_sender(topic_name: str, message:str):
    telemetry_socket.send_json({topic_name: message})


def drain_inbound() -> list[cdcm.DecoderTeamCommand]:
    """All the strategy commands waiting in the queue, merged: per team the latest command of each robot.

    Only the latest command matters, and a slow tick (or a stall) must not leave a backlog of stale
    commands that the robots would replay long after the strategy has changed or stopped. A message
    may carry only some robots, so robots are merged rather than the last message taken. The latest
    SET_COEFFICIENTS of a robot is kept beside its latest motion command."""
    latest: dict[bool, dict[tuple[int, bool], cdcm.AnyDecoderCommand]] = {}
    while True:
        try:
            signal = s_inbound.recv_json(zmq.NOBLOCK)
        except zmq.Again:
            break
        try:
            team_command = cdcm.converter.structure(signal["data"], cdcm.DecoderTeamCommand)
        except Exception as e:
            print("Unknown exception while processing inbound: ", e)
            continue
        robots = latest.setdefault(team_command.isteamyellow, {})
        for robot in team_command.robot_commands:
            # SET_COEFFICIENTS is not a motion command: it doesn't replace the robot's one, nor the other way
            robots[(robot.robot_id, isinstance(robot, cdcm.DecoderCoefficientsCommand))] = robot
    return [
        cdcm.DecoderTeamCommand(robot_commands=list(robots.values()), isteamyellow=is_yellow)
        for is_yellow, robots in latest.items()
    ]

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
            for signal_data in drain_inbound():
                try:
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
                # transnet signals (e.g. our own SIM "actuate_robot") have no "control" key
                control = signal.get("control")
                if "transnet" in signal and signal["transnet"] == "set_formation" and isinstance(Decoder,footbot4.FB4Decoder):
                    formation = signal["data"]
                    Decoder.process_formation(formation)
                elif control == "send_udpie":
                    raw = signal.get("data")
                    Decoder.process_signal(raw)
                elif control == "robot_commands":
                    signal_data = cdcm.converter.structure(signal["data"], cdcm.DecoderTeamCommand)
                    Decoder.process(signal_data)
                elif control == "broadcast_command":
                    team_cmd = cdcm.converter.structure(signal["data"], cdcm.DecoderTeamCommand)
                    if team_cmd.robot_commands:
                        Decoder.broadcast_command(team_cmd.robot_commands[0])
                    
            except Exception as e:
                print("Unknown exception while processing signals: ", e)
                time.sleep(0.1)

    Decoder.process_telemetry()
    Decoder.send_telemetry()
