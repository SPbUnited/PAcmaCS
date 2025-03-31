# Описание связи между модулями через zmq

## Используемые сокеты

### Serviz

#### `ipc:///tmp/serviz.sock :: PULL`

Принимает данные о слоях для отрисовки. Пример данных:

```json
{
  "test_vision": {
    "data": [
      {
        "type": "robot_yel",
        "x": -1000,
        "y": 100,
        "rotation": 0
      },
      {
        "type": "robot_blu",
        "x": 1400,
        "y": 100,
        "rotation": 3.14
      },
      {
        "type": "robot_blu",
        "x": -1400,
        "y": -100,
        "rotation": 0
      },
      {
        "type": "ball",
        "x": 200,
        "y": 400
      }
    ],
    "is_visible": true // Read only on first update
  }
}
```

Пример работы:

```python
socket = context.socket(zmq.PUSH)
socket.connect("ipc:///tmp/serviz.sock")

data = {
    "test_vision": {
        "data": [{"type": "robot_yel", "x": 100, "y": 100, "rotation": 0}],
        "is_visible": True,
    }
}
socket.send_json(data)
```

При обновлении данных о слое все данные заменяются на новые. Таким образом отрисовывается всегда самые последние данные.

#### `ipc:///tmp/serviz.pub.sock :: PUB`

Публикует сигналы для других модулей. Сигналы имеют следующий формат:

```json
{
    "<recipient>": "<signal_name>",
    "data": { /* ... */ } // optional
}
```

Первый ключ в словаре определяет получателя сигнала, второй - название сигнала. Сигналы публикуются с помощью метода `socket.send_json`.

Пример работы:

```python
signal_socket = context.socket(zmq.SUB)
signal_socket.connect("ipc:///tmp/serviz.pub.sock")
# Требуется дважды подписаться, т.к. кавычки могут быть любыми
signal_socket.setsockopt_string(zmq.SUBSCRIBE, '{"larcmacs":')
signal_socket.setsockopt_string(zmq.SUBSCRIBE, "{'larcmacs':")

poller = zmq.Poller()
poller.register(signal_socket, zmq.POLLIN)

while True:
    socks = dict(poller.poll(timeout=1))
    if signal_socket in socks:
        signal = signal_socket.recv_json()
        print(signal)
```
