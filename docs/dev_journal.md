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
