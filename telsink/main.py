from argparse import ArgumentParser
import time
import yaml

from logger.logger import Logger
from player.player import Player
from ether.signal_bus import SignalBus
from ether.drawty import Drawty


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

    ether_config = config["ether"]
    log_topic_list = [
        ether_config["s_signals_pub_url"] + ether_config["monitor_suffix"],
        ether_config["s_draw_pub_url"] + ether_config["monitor_suffix"],
        ether_config["s_telemetry_pub_url"] + ether_config["monitor_suffix"],
    ]

    logger = Logger(
        log_path=config["telsink"]["log_path"], socket_url_list=log_topic_list
    )

    player_url_mapping = {
        ether_config["s_signals_pub_url"]
        + ether_config["monitor_suffix"]: "ipc:///tmp/dev.null",
        ether_config["s_draw_pub_url"]
        + ether_config["monitor_suffix"]: config["ether"]["s_draw_sub_url"]
        + config["ether"]["phantom_suffix"],
        ether_config["s_telemetry_pub_url"]
        + ether_config["monitor_suffix"]: config["ether"]["s_telemetry_sub_url"]
        + config["ether"]["phantom_suffix"],
    }

    player = Player(socket_url_mapping=player_url_mapping)

    event_bus = SignalBus(
        "telsink",
        config["ether"]["s_signals_pub_url"],
        config["ether"]["s_signals_sub_url"],
    )

    drawty = Drawty(
        draw_out_url=config["ether"]["s_draw_sub_url"],
        telemetry_out_url=config["ether"]["s_telemetry_sub_url"],
    )
    phantom_drawty = Drawty(
        draw_out_url=config["ether"]["s_draw_sub_url"]
        + config["ether"]["phantom_suffix"],
        telemetry_out_url=config["ether"]["s_telemetry_sub_url"]
        + config["ether"]["phantom_suffix"],
    )

    event_bus.on("start_recording", lambda signal: logger.start_recording())
    event_bus.on("stop_recording", lambda signal: logger.stop_recording())
    event_bus.on(
        "start_playback", lambda signal: player.start_playback("logs/1755180879.log")
    )  # signal.data))
    event_bus.on("stop_playback", lambda signal: player.stop_playback())

    event_bus.start()

    print("Telsink online")

    # player.start_playback("logs/1755180879.log")

    while True:
        try:
            time.sleep(0.1)

            event_bus.s_signals_out.send_json(
                {
                    "serviz": "update_telsink_recording_status",
                    "data": logger.is_recording,
                }
            )

            drawty.telemetry(
                {"Telsink status": f"Real data: {logger.is_recording}, {time.time()}"}
            )
            phantom_drawty.telemetry(
                {
                    "Telsink status": f"Phantom data: {logger.is_recording}, {time.time()}"
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
