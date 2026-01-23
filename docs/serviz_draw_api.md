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
                "width": 20
            },
            {
                "type": "arrow",
                "x": 220,
                "y": 1000,
                "dx": 800,
                "dy": -400,
                "color": "#FF0000",
                "width": 20
            },
            {
                "type": "polygon",
                "x_list": [0, 100, 200, 100],
                "y_list": [0, 100, 100, 0],
                "color": "#00FF00",
                "width": 10
            },
            {
                "type": "rect",
                "x": -300,
                "y": -350,
                "width": 100,
                "height": 100,
                "color": "#0000FF"
            },
            {
                "type": "circle",
                "x": 1500,
                "y": 1400,
                "radius": 50,
                "color": "#FFFF00"
            },
            {
                "type": "text",
                "text": "Hello World!",
                "x": -500,
                "y": -500,
                "font_size": 100,
                "color": "#EEFF00",
                "align": "middle"
            }
        ]
        "is_visible": True,
        "heigh": 10,
    }
}

import time
time.sleep(1)

socket.send_json(draw_test_data)
```
## Параметры слоя

Каждый слой в `FeedData` имеет параметры `heigh` и `is_visible`, которые управляют отображением объектов.

### `heigh`

* Определяет порядок отрисовки слоев (аналог z-index).
* Слои сортируются по убыванию `heigh`.
* Чем больше `heigh`, тем выше слой рисуется.
* Если значение отсутствует или некорректно, используется `1` (увеличивается на 0.001 пока не станет отличаться от высот других слоев).

### `is_visible`

* Управляет видимостью слоя.
* Если `false`, слой полностью не отрисовывается.
* Данные слоя при этом могут продолжать приходить.

### Управление из интерфейса

* `is_visible` можно менять прямо в интерфейсе.
* Порядок слоев также можно менять в интерфейсе (через изменение `heigh`).
* Это позволяет управлять видимостью и приоритетом слоев без изменения данных на бэкенде.

## Поддерживаемые объекты

```
/**
 * Drawing API Reference
 *
 * sprite.type:
 * - robot_yel
 * - robot_blu
 * - ball
 * - line
 * - arrow
 * - polygon
 * - rect
 * - circle
 * - text
 * - svg
 *
 * expected fields:
 *
 * # robot_yel / robot_blu
 *      - type: "robot_yel" | "robot_blu"
 *      - robot_id: number
 *      - x: number
 *      - y: number
 *      - rotation?: number        // radians
 *      - vx?: number
 *      - vy?: number
 *
 * # ball
 *      - type: "ball"
 *      - x: number
 *      - y: number
 *      - vx?: number
 *      - vy?: number
 *
 * # line
 *      - type: "line"
 *      - x_list: number[]
 *      - y_list: number[]
 *      - color: string            // hex or css color
 *      - width: number
 *
 * # arrow
 *      - type: "arrow"
 *      - x: number
 *      - y: number
 *      - dx: number
 *      - dy: number
 *      - color: string
 *      - width: number
 *
 * # polygon
 *      - type: "polygon"
 *      - x_list: number[]
 *      - y_list: number[]
 *      - color: string
 *      - width: number
 *
 * # rect
 *      - type: "rect"
 *      - x: number
 *      - y: number
 *      - width: number
 *      - height: number
 *      - color: string
 *
 * # circle
 *      - type: "circle"
 *      - x: number
 *      - y: number
 *      - radius: number
 *      - color: string
 *
 * # text
 *      - type: "text"
 *      - text: string
 *      - x: number
 *      - y: number
 *      - font_size: number
 *      - color: string
 *      - modifiers?: string       // CSS style string
 *      - align?: "left" | "middle" | "right"
 *
 * # svg
 *      - type: "svg"
 *      - svg: string              // raw SVG text
 *      - x: number                // center X
 *      - y: number                // center Y
 *      - scale?: number
 *      - rotation?: number        // radians
 */
```
