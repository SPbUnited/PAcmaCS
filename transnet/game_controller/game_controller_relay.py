from enum import Enum
import time
from attrs import define, field
import zmq
from common.sockets import SocketReader
import multiprocessing
from protopy.state.ssl_gc_referee_message_pb2 import Referee


class TeamColour(Enum):
    NEUTRAL = 0
    BLUETEAM = 1
    YELLOWTEAM = 2


class State(Enum):
    HALT = 0
    STOP = 1
    RUNNING = 2
    TIMEOUT = 3
    POST_GAME = 4
    PREPARE_KICKOFF = 5
    KICKOFF = 6
    PREPARE_PENALTY = 7
    PENALTY = 8
    DIRECT_FREE = 9
    INDIRECT_FREE = 10
    BALL_PLACEMENT = 11


@define
class GameControllerRelay:
    game_controller_fan_url: str

    multicast_ip: str = field(default="224.5.23.1")
    multicast_port: int = field(default=10003)

    zmq_send_period: float = field(default=0.1)

    _socket_reader: SocketReader = field(init=False)
    _ssl_converter: Referee = field(default=Referee(), init=False)

    _reader: multiprocessing.Process = field(init=False)

    def __attrs_post_init__(self):
        self._socket_reader = SocketReader(
            ip=self.multicast_ip, port=self.multicast_port
        )
        self._reader = multiprocessing.Process(
            target=self._read_loop,
        )

    def init(self):
        self._reader.start()

    def _read_loop(self):
        context = zmq.Context()
        relay = context.socket(zmq.PUB)
        relay.bind(self.game_controller_fan_url)

        prev_state = Referee.HALT

        timer = time.time()

        print("Game controller relay init")
        while True:
            data = None

            while time.time() - timer < self.zmq_send_period:
                data = self._socket_reader.read_package()
            timer = time.time()

            package = self._ssl_converter.FromString(data)
            # print(package)

            mState, mForTeam = self.update_game_state(package, prev_state=prev_state)

            relay_data = {
                "state": mState.value,
                "team": mForTeam.value,
                "is_left": False,
            }

            if mState != prev_state:
                print(relay_data)

            relay.send_json(relay_data)

            prev_state = mState

    def update_game_state(
        self, message: Referee, prev_state: Referee.Command
    ) -> tuple[State, TeamColour]:
        command = message.command

        st = State
        tc = TeamColour
        ref = Referee

        mState = ref.HALT
        mForTeam = tc.NEUTRAL

        if command == ref.HALT:
            mState = st.HALT
            mForTeam = tc.NEUTRAL
        elif command == ref.STOP:
            mState = st.STOP
            mForTeam = tc.NEUTRAL
        elif command == ref.NORMAL_START:
            if prev_state == st.PREPARE_KICKOFF or prev_state == st.KICKOFF:
                mState = st.KICKOFF
            if prev_state == st.PREPARE_PENALTY or prev_state == st.PENALTY:
                mState = st.PENALTY
        elif command == ref.FORCE_START:
            mState = st.RUNNING
            mForTeam = tc.NEUTRAL
        elif command == ref.PREPARE_KICKOFF_YELLOW:
            mState = st.PREPARE_KICKOFF
            mForTeam = tc.YELLOWTEAM
        elif command == ref.PREPARE_KICKOFF_BLUE:
            mState = st.PREPARE_KICKOFF
            mForTeam = tc.BLUETEAM
        elif command == ref.PREPARE_PENALTY_YELLOW:
            mState = st.PREPARE_PENALTY
            mForTeam = tc.YELLOWTEAM
        elif command == ref.PREPARE_PENALTY_BLUE:
            mState = st.PREPARE_PENALTY
            mForTeam = tc.BLUETEAM
        elif command == ref.DIRECT_FREE_YELLOW:
            mState = st.DIRECT_FREE
            mForTeam = tc.YELLOWTEAM
        elif command == ref.DIRECT_FREE_BLUE:
            mState = st.DIRECT_FREE
            mForTeam = tc.BLUETEAM
        elif command == ref.INDIRECT_FREE_YELLOW:
            mState = st.INDIRECT_FREE
            mForTeam = tc.YELLOWTEAM
        elif command == ref.INDIRECT_FREE_BLUE:
            mState = st.INDIRECT_FREE
            mForTeam = tc.BLUETEAM
        elif command == ref.TIMEOUT_YELLOW:
            mState = st.TIMEOUT
            mForTeam = tc.YELLOWTEAM
        elif command == ref.TIMEOUT_BLUE:
            mState = st.TIMEOUT
            mForTeam = tc.BLUETEAM
        elif command == ref.GOAL_YELLOW:
            mState = st.STOP
            mForTeam = tc.NEUTRAL
        elif command == ref.GOAL_BLUE:
            mState = st.STOP
            mForTeam = tc.NEUTRAL
        elif command == ref.BALL_PLACEMENT_YELLOW:
            mState = st.BALL_PLACEMENT
            mForTeam = tc.YELLOWTEAM
        elif command == ref.BALL_PLACEMENT_BLUE:
            mState = st.BALL_PLACEMENT
            mForTeam = tc.BLUETEAM

        if message.stage == Referee.POST_GAME:
            mState = st.POST_GAME
            mForTeam = tc.NEUTRAL

        return mState, mForTeam
