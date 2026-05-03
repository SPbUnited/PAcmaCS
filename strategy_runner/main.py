import time
from argparse import ArgumentParser
import subprocess
import os
import signal as sig
import psutil
import yaml
import zmq
from cattrs import structure

parser = ArgumentParser()
parser.add_argument("--config", default="config.yml")
args = parser.parse_args()

config = yaml.safe_load(open(args.config))
#########

context = zmq.Context()
signals_inbound = config["ether"]["s_signals_pub_url"]

s_signals = context.socket(zmq.SUB)
s_signals.connect(signals_inbound)
s_signals.setsockopt_string(zmq.SUBSCRIBE, '{"strategy":')
s_signals.setsockopt_string(zmq.SUBSCRIBE, "{'strategy':")

poller = zmq.Poller()
poller.register(s_signals, zmq.POLLIN)
process = None
while True:
    socks = dict(poller.poll(timeout=0))
    # print(socks.values())
    if socks == {}:
        time.sleep(0.01)
    else:
        if s_signals in socks:
            try:
                signal = s_signals.recv_json()
                if signal["strategy"] == "start_strategy" and process is None:
                    path = signal["path"]
                    process = subprocess.Popen(
                        ["/" + os.path.dirname(path) + "/venv/bin/python3", os.path.basename(path)],
                        cwd="/" + os.path.dirname(path),
                    )
                    print("Start strategy" + path)
                if signal["strategy"] == "stop_strategy" and not process is None:
                    path = signal["path"]

                    parent = psutil.Process(process.pid)
                    # Получаем всех "детей" стратегии
                    children = parent.children(recursive=True)

                    # 1. Сначала пытаемся мягко остановить всех
                    for child in children:
                        child.send_signal(sig.SIGINT)
                    parent.send_signal(sig.SIGINT)

                    # 2. Ждем немного и добиваем тех, кто не закрылся
                    gone, alive = psutil.wait_procs(children + [parent], timeout=3)

                    process = None
                    # process.terminate()
                    print("stop strategy" + path)

            except Exception as e:
                print("Unknown exception while processing signals: ", e)
                time.sleep(0.1)
