# Спецификация интерфейса рисования для Serviz

## Пример рисования всех доступных объектов

```python
import zmq
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("ipc:///tmp/ether.draw.xsub")

draw_test_data = {
    "draw_test": {
        "data": [
            {
                "type": "robot_yel",
                "robot_id": 3,
                "x": -1000,
                "y": 100,
                "rotation": 0
            },
            {
                "type": "robot_blu",
                "robot_id": 4,
                "x": 1400,
                "y": 100,
                "rotation": 3.14
            },
            {
                "type": "ball",
                "x": 200,
                "y": 400
            },
            {
                "type": "line",
                "x_list": [1000, 100, 220],
                "y_list": [0, 100, 1000],
                "color": "#FF0000",
                "width": 20,
            },
            {
                "type": "arrow",
                "x": 220,
                "y": 1000,
                "dx": 800,
                "dy": -400,
                "color": "#FF0000",
                "width": 20,
            },
            {
                "type": "polygon",
                "x_list": [0, 100, 200, 100],
                "y_list": [0, 100, 100, 0],
                "color": "#00FF00",
                "width": 10,
            },
            {
                "type": "rect",
                "x": -300,
                "y": -350,
                "width": 100,
                "height": 100,
                "color": "#0000FF",
            },
            {
                "type": "circle",
                "x": 1500,
                "y": 1400,
                "radius": 50,
                "color": "#FFFF00",
            },
            {
                "type": "text",
                "text": "Hello World!",
                "x": -500,
                "y": -500,
                "color": "#EEFF00",
                "modifiers": "bold 100px",
                "align": "center",
            }
        ],
        "is_visible": True,
    }
}

import time
time.sleep(1)

socket.send_json(draw_test_data)
```

## Поддерживаемые объекты

```
/**
 * Drawing API Reference
 *
 * sprite.type
 * - robot_yel
 * - robot_blu
 * - ball
 * - line
 * - polygon
 * - rect
 *
 * expected fields:
 * # robot_yel
 *      - robot_id
 *      - x
 *      - y
 *      - rotation
 *      -* vx
 *      -* vy
 * # robot_blu
 *      - robot_id
 *      - x
 *      - y
 *      - rotation
 *      -* vx
 *      -* vy
 *
 * # ball
 *      - x
 *      - y
 *      -* vx
 *      -* vy
 *
 * # line
 *      - x_list
 *      - y_list
 *      - color
 *      - width
 *
 * # arrow
 *      - x
 *      - y
 *      - dx
 *      - dy
 *      - color
 *      - width
 *
 * # polygon
 *      - x_list
 *      - y_list
 *      - color
 *      - width
 *
 * # rect
 *      - x
 *      - y
 *      - width
 *      - height
 *      - color
 *
 * # circle
 *      - x
 *      - y
 *      - radius
 *      - color
 * # text
 *      - text
 *      - x
 *      - y
 *      - color [black, white, etc.]
 *      - modifiers [bold, italic, etc., size: 42px, 100px, etc.]
 *      - align [left, center, right]
 */
```
