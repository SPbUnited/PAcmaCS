# FB4: управление роботами по ZMQ

Робот не знает IP управляющего компьютера. Он только открывает два TCP-порта,
а управляющие компьютеры сами подключаются к роботам.

Каждое сообщение состоит из двух ZMQ frames: UTF-8 topic и JSON payload.

## Команды

```text
PC PUB connect tcp://fb4-XX.local:5555
  -> Robot SUB bind tcp://*:5555
topic: cmd/<robot_id> или cmd/all
payload: JSON
```

Робот подписан на адресный `cmd/<robot_id>` и общий `cmd/all`. JSON строится из
существующего объекта команды центрального декодера; к его полям добавляются
`isteamyellow` и `timestamp`.

```text
PC A PUB -------> fb4-00 SUB :5555
PC A PUB -------> fb4-01 SUB :5555
PC B PUB -------> fb4-02 SUB :5555
```

## Телеметрия

```text
Robot PUB bind tcp://*:5556
  -> PC SUB connect tcp://fb4-XX.local:5556
topic: tel/<robot_id>
payload: JSON
```

JSON телеметрии содержит как минимум `robot_id`, `timestamp` и `seq`. Эмулятор
также отправляет `voltage`, `ball_sensor`, `status` и `get_timestamp` последней
полученной команды.

```text
PC A SUB <------- fb4-00 PUB :5556
PC A SUB <------- fb4-01 PUB :5556
PC A SUB <------- fb4-02 PUB :5556

PC B SUB <------- fb4-00 PUB :5556
PC B SUB <------- fb4-01 PUB :5556
PC B SUB <------- fb4-02 PUB :5556
```

Один робот может обслуживать несколько подключившихся компьютеров. Поэтому
несколько компьютеров могут одновременно получать его телеметрию, а разные
компьютеры могут отправлять команды разным роботам. Смена `robot_id` требует
только перезапуска сетевого процесса робота, а не перезагрузки одноплатника.

## Настройка управляющего компьютера

Центральный декодер генерирует hostname всех 16 роботов, от `fb4-00.local` до
`fb4-15.local`. В `config.yml` задаются только порты:

```yaml
control_decoder:
  fb4_port: 10000
  fb4_command_port: 5555
  fb4_telemetry_port: 5556
```

Пакеты UDPie остаются UDP-датаграммами. Номер робота читается из пакета; роботы
с WiFi получают его напрямую на `fb4-XX.local:10000` (например,
`fb4-09.local:10000`), остальные — через мост NRF (см. ниже).

## Разделение роботов по способу связи

Способ связи определяется номером робота:

| `robot_id` | Связь | Куда уходят команды и UDPie |
|---|---|---|
| `< fb4_wifi_min_robot_id` (0–7) | NRF | 13-байтовый пакет на мост `fb4_ip_low:fb4_port` |
| `>= fb4_wifi_min_robot_id` (8–15) | WiFi | `NewFormat` на `fb4-XX.local:5555`, UDPie на `fb4-XX.local:10000` |

```yaml
control_decoder:
  fb4_ip_low: "10.0.120.220"   # мост NRF
  fb4_wifi_min_robot_id: 8     # порог (по умолчанию 8)
```

Телеметрия и mDNS-discovery работают только для WiFi-роботов; у NRF-роботов
статуса в serviz нет. `broadcast_command` отправляется обеим группам.
Кодировщик пакета NRF — `control_decoder/control_models/footbot4_nrf.py`.
