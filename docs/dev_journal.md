# Development journal

## Process IPC option considerations

To ease the development of the project it was decided to write application as separate modules, each of which would be responsible for a specific task. This approach allows us to split the application into smaller, more manageable pieces, making it easier to develop, test, and maintain. Also it would allow us to use different languages for different modules, would it be required.

However, this approach also introduces a new challenge of managing inter-module communication. So a number of requirements were formulated to address this issue:

1. Ideally, one IPC method should be used for all modules.
2. The IPC method should be reasonably easy to use and understand.
3. The IPC method should meet following requirements:
   - Low latency (sub-millisecond, 10-100μs)
   - High throughput
   - Cross-language support

Following IPC methods were considered:

1. Shared Memory
2. Unix Sockets
3. ZeroMQ (inproc, ipc, tcp)
4. TCP Sockets
5. In memory database (Redis)
6. Message Brokers (RabbitMQ, Kafka)

### **IPC Communication Options Comparison**
*(Speed estimates assume optimal local/loopback conditions; latency = round-trip time)*

| **IPC Method**            | **Latency (μs)** | **Throughput**       | **Ease of Use (1-5)** | **Cross-Lang Support (1-5)** | **Python Tools** | **Best Use Cases**                     | **Key Notes**                                  |
|---------------------------|------------------|----------------------|-----------------------|------------------------------|------------------|----------------------------------------|-----------------------------------------------|
| **Shared Memory**          | 0.1 – 1          | 10 – 20 GB/s         | 2                     | 2                            | `multiprocessing.shared_memory` | Real-time data sharing, high-frequency | Manual sync, data alignment critical          |
| **Unix Sockets**           | 5 – 50           | 2 – 5 GB/s           | 3                     | 4                            | `socket`         | Low-latency local IPC                  | Filesystem-based; no Windows support          |
| **ZeroMQ (inproc)**        | 1 – 10           | 5 – 10 GB/s          | 4                     | 3                            | `pyzmq`          | Thread-to-thread in same process       | No serialization/network overhead             |
| **ZeroMQ (ipc)**           | 10 – 100         | 1 – 5 GB/s           | 4                     | 4                            | `pyzmq`          | Process-to-process on same machine     | Uses OS-native IPC (e.g., Unix domain sockets)|
| **ZeroMQ (tcp)**           | 50 – 500         | 0.5 – 2 GB/s         | 4                     | 5                            | `pyzmq`          | Cross-machine communication            | Portable, but adds network stack overhead     |
| **TCP Sockets**            | 50 – 200         | 1 – 10 GB/s          | 3                     | 5                            | `socket`         | Networked or portable IPC              | OS networking stack overhead                  |
| **gRPC**                   | 200 – 1000       | 0.1 – 1 GB/s         | 3                     | 5                            | `grpcio`         | Strict APIs, RPC workflows             | Protobuf/HTTP2; codegen required              |
| **REST/HTTP**              | 1000 – 10,000   | 0.01 – 0.1 GB/s      | 5                     | 5                            | `requests`       | Web APIs, cross-platform compatibility | High overhead (text-based protocols)          |
| **Message Brokers**        | 500 – 5000       | 0.05 – 0.5 GB/s      | 3                     | 5                            | `pika`, `redis`  | Decoupled systems, async workflows     | Broker setup required (e.g., RabbitMQ/Redis)  |

---

### **ZeroMQ Transport-Specific Details**
| **ZeroMQ Transport** | **Scope**                | **Protocol**                 | **Key Constraints**                              |
|-----------------------|--------------------------|------------------------------|--------------------------------------------------|
| `inproc`              | Threads in same process  | In-process messaging          | Requires threads to share context; no cross-process. |
| `ipc`                | Processes on same host   | OS-native IPC (e.g., files)   | Platform-dependent (Unix-only for domain sockets).  |
| `tcp`                | Cross-network            | TCP/IP                        | Port management, network latency, and security.     |

---

### **Metric Definitions**
1. **Latency**: Round-trip time for a small message (lower = better).
2. **Throughput**: Maximum sustained data rate (higher = better).
3. **Ease of Use**:
   - `1` = Manual sync/boilerplate, `5` = Minimal setup (high-level API).
4. **Cross-Language Support**:
   - `1` = Language-locked, `5` = Universal (native bindings in most languages).

---

### **When to Use ZeroMQ Transports**
- **`inproc`**: Ultra-fast thread communication (e.g., Python’s `threading` module).
- **`ipc`**: Low-latency process communication on Unix systems.
- **`tcp`**: Distributed systems or mixed-language environments.

---

### **Notes**
- **ZeroMQ `inproc`**: Avoids serialization if using raw bytes, but limited to single-process communication.
- **ZeroMQ `ipc`**: Faster than TCP but slower than `inproc`; uses filesystem sockets on Unix.
- **ZeroMQ `tcp`**: Adds ~10-50μs overhead over raw TCP due to framing and message envelopes.

## Conclusion

Based on the analysis, the ZeroMQ library was chosen as means of inter-process communication. The ZMQ `ipc` transport is fast and suitable for communication between processes on a same machine. It is a good compromise between speed and ease of use, and it is available on all major platforms.

The `tcp` transport is very versatile, but adds additional overhead with no benefits for our usecase at the moment. However, usage of ZeroMQ also allows very easy switch to `tcp` transport if it is nesessary, i.e. for long and compute intensive calculations on a separate machine (real-time game analyzis using ML algorithms and other techniques) with no additional tooling required.

## IPC communication specification

### Serviz draw interface

Serviz draw functionality is based on layers. Each layer is a list of primitives (e.g. robots, balls, arrows). Each layer is a named dictionary with the following structure:

```python
example_layer = {
"layer_name":
   {
      "data":[
         {"type": "robot_yel", "robot_id": 0, "x": 100, "y": 100, "rotation": 0},
         {"type": "robot_blu", "robot_id": 0, "x": 1400, "y": 100, "rotation": 3.14},
         {"type": "ball", "x": 200, "y": 400}
      ],
      "is_visible": True
   },
}
```

The `data` field contains a list of primitives. Each primitive is a dictionary with the structure, specific to the primitive type.

Implemented primitives:
- `robot_yel`
```python
{
   "type": "robot_yel",
   "robot_id": 0,
   "x": 100,
   "y": 100,
   "rotation": 0,
}
```
- `robot_blu`
```python
{
   "type": "robot_blu",
   "robot_id": 0,
   "x": 1400,
   "y": 100,
   "rotation": 3.14,
}
```
- `ball`
```python
{
   "type": "ball",
   "x": 200,
   "y": 400,
}
```

Other processes can broadcast layer data to the serviz draw interface by sending a zmq message using `PUSH` socket type to the `PULL` socket of a serviz as JSON string.

This approach were chosen to allow multiple processes to send layer data to the serviz while keeping the message fetch logic simple and straightforward.

All serviz does, is to check for all available messages and update the corresponding layer data accordingly. So, if serviz receives a message with a layer name that is not present in the layer data, it will create a new layer with the given name and add it to the layer data. If the message contains a layer name that is already present in the layer data, the new data will completely overwrite the old data.

### Signal broadcasting

Serviz also can be used to broadcast signals to all other processes (for example in response to a user action in web UI). This is done by sending a zmq message using `PUB` socket type with the following structure:

```python
example_signal = {
   "transnet": "set_ball",
   "data": {
      "x": 100,
      "y": 100,
      "vx": 0,
      "vy": 0,
   }
}
```

Recipient process is specified as first key in the dictionary, allowing to easily filter messages by recipient.

Value of the recepient key is a message type, which should be recognized by the recipient process.

Data field is a dictionary with the payload to be broadcasted.

Example recipient code:

```python
import zmq

signal_socket = context.socket(zmq.SUB)
signal_socket.connect("ipc:///tmp/serviz.pub.sock")
signal_socket.setsockopt_string(zmq.SUBSCRIBE, "{\"transnet\":")
signal_socket.setsockopt_string(zmq.SUBSCRIBE, "{\'transnet\':")

poller = zmq.Poller()
poller.register(signal_socket, zmq.POLLIN)

while True:
    socks = dict(poller.poll(timeout=1))
    if signal_socket in socks:
        signal = signal_socket.recv_json()
        print(signal)
        signal_handler(signal)
```
