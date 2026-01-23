import time
from typing import Any, Callable
from abc import ABC, abstractmethod
from decoder import robot_command_model as rcm
from decoder import control_decoder_command_model as cdcm

class ControlModel(ABC):
    def __init__(self, _config: dict, telemetry_sender: Callable[[str, str], None]
):
        self.telemetry_sender = telemetry_sender
        self.telemetry_text = ""
        self.last_update = 0.0

    @abstractmethod
    def process(self, decoder_team_command: cdcm.DecoderTeamCommand) -> None:
        pass

    def send_telemetry(self):
        
        if time.time() - self.last_update < 2:
            self.telemetry_sender("COMMAND_DECODER", f"From previous message: {(time.time() - self.last_update)*1000:.2f}ms\n" + self.telemetry_text)
        else:
            self.telemetry_sender("COMMAND_DECODER", "NO NEW COMMANDS")
        

    def process_signal(self, raw: Any):
        pass
