from PySide6.QtCore import QThread, Signal
import tomllib
import socket
import struct

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

UDP_PORT = config["udp"]["UDP_PORT"]
UDP_IP = config["udp"]["UDP_IP"]

class UDPListener(QThread):
    x_position = Signal(float)

    def __init__(self, port=UDP_PORT, parent=None):
        super().__init__(parent)
        self.port = port
        self.running = True

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, self.port))
        while self.running:
            data, _ = sock.recvfrom(6*8)  # Expecting a double (8 bytes)
            x = struct.unpack('dddddd', data)[0]  # Unpack double
            self.x_position.emit(x)

    # def stop(self):
    #     self.running = False
  