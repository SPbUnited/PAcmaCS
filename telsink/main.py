from argparse import ArgumentParser
import time
import yaml

from logger.logger import Logger
from signal_bus.signal_bus import SignalBus


def main():

    parser = ArgumentParser()
    parser.add_argument("--config", default="config.yml")
    parser.add_argument("--log-path", default="")
    args = parser.parse_args()

    config = yaml.safe_load(open(args.config))

    if args.log_path != "":
        config["telsink"]["log_path"] = args.log_path

    if config["telsink"]["log_format_version"] != 1:
        raise Exception("Only log format version 1 is supported")

    ether_topics = config["ether"]
    log_topic_list = [
        ether_topics["s_signals_pub_url"],
        ether_topics["s_draw_pub_url"],
        ether_topics["s_telemetry_pub_url"],
    ]

    logger = Logger(
        log_path=config["telsink"]["log_path"], socket_url_list=log_topic_list
    )

    event_bus = SignalBus(
        "telsink",
        config["ether"]["s_signals_pub_url"],
        config["ether"]["s_signals_sub_url"],
    )

    event_bus.on("start_recording", lambda signal: logger.start_recording())
    event_bus.on("stop_recording", lambda signal: logger.stop_recording())

    event_bus.start()

    print("Telsink online")

    while True:
        try:
            time.sleep(0.1)

            event_bus.s_signals_out.send_json(
                {
                    "serviz": "update_telsink_recording_status",
                    "data": logger.is_recording,
                }
            )
            # print(
            #     "Sent: ",
            #     {
            #         "serviz": "update_telsink_recording_status",
            #         "data": logger.is_recording,
            #     },
            # )
        except KeyboardInterrupt:
            # event_bus.stop()
            break


if __name__ == "__main__":
    main()
