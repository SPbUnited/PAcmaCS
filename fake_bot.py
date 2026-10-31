import socket
from ssl_packet_package.protopy.spbunited.robot import telemetry_pb2
import time
def telemetry_tranciever():    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        proto_package = telemetry_pb2.RobotTelemetry()
        proto_package.robot_id = 2
        proto_package.strategy_telemetry.ball_deep = True
        proto_package.strategy_telemetry.ball_in = False
        proto_package.strategy_telemetry.kicker_voltage = 10
        proto_package.strategy_telemetry.ball_position.x = 200
        proto_package.strategy_telemetry.ball_position.y = 1000
        sock.sendto(proto_package.SerializeToString(), ("<broadcast>", 5556))
        time.sleep(0.1)
telemetry_tranciever()