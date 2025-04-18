# Описание связи между модулями через zmq

## Serviz

- `ipc:///tmp/ether.draw :: PULL`
- `ipc:///tmp/ether.telemetry :: PULL`
- `ipc:///tmp/ether.signals :: PUB`

#### `ipc:///tmp/ether.draw :: PULL`

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
socket = context.socket(zmq.PUSH)
socket.connect("ipc:///tmp/ether.draw")

data = {
    "test_vision": {
        "data": [{"type": "robot_yel", "x": 100, "y": 100, "rotation": 0}],
        "is_visible": True,
    }
}
socket.send_json(data)
```

При обновлении данных о слое все данные заменяются на новые.

#### `ipc:///tmp/ether.telemetry :: PULL`

Принимает данные о телеметрии модуля. Пример данных:

```json
{
  "test_telemetry": "test telemetry value\nit is just a string"
}
```

Пример работы:

```python
socket = context.socket(zmq.PULL)
socket.connect("ipc:///tmp/ether.telemetry")

data = {"test_telemetry": "test telemetry value\nit is just a string"}
socket.send_json(data)
```

#### `ipc:///tmp/ether.signals :: PUB`

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
signal_socket.connect("ipc:///tmp/ether.signals")
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
