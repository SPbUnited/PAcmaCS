import time
from typing import Any, Callable
from abc import ABC, abstractmethod
from decoder import robot_command_model as rcm
from decoder import control_decoder_command_model as cdcm

UNSUPPORTED_WARNING_INTERVAL = 1.0 # [s]

class ControlModel(ABC):
    def __init__(self, _config: dict, telemetry_sender: Callable[[str, str], None]
):
        self.telemetry_sender = telemetry_sender
        self.telemetry_text = ""
        self.last_update = 0.0
        self.last_unsupported_warning = 0.0

    @abstractmethod
    def process(self, decoder_team_command: cdcm.DecoderTeamCommand) -> None:
        pass

    def send_telemetry(self):
        
        if time.time() - self.last_update < 2:
            self.telemetry_sender("COMMAND_DECODER", f"From previous message: {(time.time() - self.last_update)*1000:.2f}ms\n" + self.telemetry_text)
        else:
            self.telemetry_sender("COMMAND_DECODER", "NO NEW COMMANDS")
        

    def warn_unsupported(self, command: cdcm.AnyDecoderCommand) -> None:
        # Commands come at the strategy rate, so print at most once per interval
        if time.time() - self.last_unsupported_warning < UNSUPPORTED_WARNING_INTERVAL:
            return
        self.last_unsupported_warning = time.time()
        print(
            f"\033[33m{type(self).__name__}: {cdcm.CONTROL_TYPES[type(command)]} "
            f"is not supported, skipping command for robot {command.robot_id}\033[0m"
        )

    def process_signal(self, raw: Any):
        pass

    def broadcast_command(self, command: cdcm.AnyDecoderCommand) -> None:
        pass

    def process_telemetry(self) -> None:
        pass
