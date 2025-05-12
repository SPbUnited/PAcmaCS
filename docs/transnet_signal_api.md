# Transnet signal API

Socket: `ipc:///tmp/ether.signals.xsub`

## Signals

### `set_formation`

Set the formation of the robots.

#### Example

```json
{
    "transnet": "set_formation",
    "data": {
        "BLUE": [ // Optional
            {"robot_id": 0, "x": -2000, "y": 0, "rotation": 0},
            {"robot_id": 1, "x": -700, "y": 600, "rotation": 0},
            {"robot_id": 2, "x": -700, "y": -600, "rotation": 0},
        ],
        "YELLOW": [ // Optional
            {"robot_id": 3, "x": 2000, "y": 0, "rotation": 180},
            {"robot_id": 4, "x": 700, "y": 600, "rotation": 180},
            {"robot_id": 5, "x": 700, "y": -600, "rotation": 180},
        ],
        "BALL": {"x": 1000, "y": 750, "vx": -2000, "vy": -2000}, // Optional
        "enable_graveyard": true, // Optional. Default: false
    }
}
```

#### Usage

```python
import time
import zmq

context = zmq.Context()

s_signals = context.socket(zmq.PUB)
s_signals.connect("ipc:///tmp/ether.signals.xsub")

time.sleep(0.1)

formation = {
    "BLUE": [
        {"robot_id": 0, "x": -2000, "y": 500, "rotation": 0},
        {"robot_id": 1, "x": -700, "y": 600, "rotation": 0},
        {"robot_id": 2, "x": -700, "y": -600, "rotation": 0},
    ],
    "YELLOW": [
        {"robot_id": 3, "x": 2000, "y": 500, "rotation": 180},
        {"robot_id": 4, "x": 700, "y": 600, "rotation": 180},
        {"robot_id": 5, "x": 700, "y": -600, "rotation": 180},
    ],
    "BALL": {"x": 1000, "y": 750, "vx": -2000, "vy": -2000},
    "enable_graveyard": True,
}

s_signals.send_json({"transnet": "set_formation", "data": formation})
```

### `set_ball`

Place ball at given position with given velocity.

#### Example

```json
{
    "transnet": "set_ball",
    "data": {
        "x": 1000,
        "y": 750,
        "vx": -2000,
        "vy": -2000
    }
}
```

### `actuate_robot`

Actuate robot with given commands.

#### Example

```json
{
    "transnet": "actuate_robot",
    "data": {
        "isteamyellow": true,
        "robot_commands": [
            {
                "id": 0,
                "move_command": { // one of following
                    "wheel_velocity": {
                        "front_left": 0.5,
                        "back_left": 0.5,
                        "back_right": 0.5,
                        "front_right": 0.5
                    },
                    "local_velocity": {
                        "left": 0.5,
                        "forward": 0.5,
                        "angular": 0.5
                    },
                    "global_velocity": {
                        "left": 0.5,
                        "forward": 0.5,
                        "angular": 0.5
                    }
                },
                "kick_speed": 0.0,
                "kick_angle": 0.0,
                "dribbler_speed": 0.0
            }
        ]
    }
}
```

#### Usage

```python
import time
import zmq

context = zmq.Context()

s_signals = context.socket(zmq.PUB)
s_signals.connect("ipc:///tmp/ether.signals.xsub")

time.sleep(0.1)

commands = [
    {
        "id": 0,
        "move_command": {
            "wheel_velocity": {
                "front_left": 0.5,
                "back_left": 0.5,
                "back_right": 0.5,
                "front_right": 0.5,
            },
            "local_velocity": {
                "left": 0.5,
                "forward": 0.5,
                "angular": 0.5,
            },
            "global_velocity": {
                "left": 0.5,
                "forward": 0.5,
                "angular": 0.5,
            },
        },
        "kick_speed": 0.0,
        "kick_angle": 0.0,
        "dribbler_speed": 0.0,
    }
]

s_signals.send_json({"transnet": "actuate_robot", "data": {"robot_commands": commands}})
```
