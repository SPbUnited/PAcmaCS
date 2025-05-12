# Описание связи между модулями через zmq

> v3

## Ether

- `ipc:///tmp/ether.draw.xsub :: XSUB`
- `ipc:///tmp/ether.draw.xpub :: XPUB`
- `ipc:///tmp/ether.telemetry.xsub :: XSUB`
- `ipc:///tmp/ether.telemetry.xpub :: XPUB`
- `ipc:///tmp/ether.signals.xsub :: XSUB`
- `ipc:///tmp/ether.signals.xpub :: XPUB`

#### `ipc:///tmp/ether.draw.xsub :: XSUB`

Принимает данные о слое для отрисовки. Пример данных:

```json
{
  "test_vision": {
    "data": [
      <objects to draw>
    ],
    "is_visible": true // Read only on first update
  }
}
```

Пример со всеми возможными объектами можно посмотреть в [спецификации](serviz_draw_api.md).

Пример работы:

```python
import time

socket = context.socket(zmq.PUB)
socket.connect("ipc:///tmp/ether.draw.xsub")

time.sleep(0.1)

data = {
    "test_vision": {
        "data": [{"type": "robot_yel", "x": 100, "y": 100, "rotation": 0}],
        "is_visible": True,
    }
}
socket.send_json(data)
```

При обновлении данных о слое все данные заменяются на новые.

#### `ipc:///tmp/ether.telemetry.xsub :: XSUB`

Принимает данные о телеметрии модуля. Пример данных:

```json
{
  "test_telemetry": "test telemetry value\nit is just a string"
}
```

Справку об опциях форматирования можно посмотреть в [спецификации](serviz_telemetry_api.md).

Пример работы:

```python
import time

socket = context.socket(zmq.PUB)
socket.connect("ipc:///tmp/ether.telemetry.xsub")

time.sleep(0.1)

data = {"test_telemetry": "test telemetry value\nit is just a string"}
socket.send_json(data)
```

#### `ipc:///tmp/ether.signals.xpub :: XPUB`

Публикует сигналы для других модулей. Сигналы имеют следующий формат:

```json
{
  "<recipient>": "<signal_name>",
  "data": {
    /* ... */
  } // optional
}
```

Первый ключ в словаре определяет получателя сигнала, второй - название сигнала. Сигналы публикуются с помощью метода `socket.send_json`.

Пример работы:

```python
signal_socket = context.socket(zmq.SUB)
signal_socket.connect("ipc:///tmp/ether.signals.xpub")
# Требуется дважды подписаться, т.к. кавычки могут быть любыми
signal_socket.setsockopt_string(zmq.SUBSCRIBE, '{"transnet":')
signal_socket.setsockopt_string(zmq.SUBSCRIBE, "{'transnet':")

poller = zmq.Poller()
poller.register(signal_socket, zmq.POLLIN)

while True:
    socks = dict(poller.poll(timeout=1))
    if signal_socket in socks:
        signal = signal_socket.recv_json()
        print(signal)
```

#### `ipc:///tmp/ether.signals.xsub :: XSUB`

Принимает сигналы для других модулей.

Пример отправки сигналов в Transnet можно посмотреть в [спецификации](transnet_signal_api.md).
