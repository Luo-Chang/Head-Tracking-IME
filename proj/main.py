from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QRect, QSize, QTimer, QThread, Signal
import math
import socket
import struct
import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

UDP_PORT = config["udp"]["UDP_PORT"]
ALLOW_MOVEMENT = config["timer"]["allow_movement"]
WAIT_CONFIRMATION = config["timer"]["wait_comfirmation"]

class UDPListener(QThread):
    x_position = Signal(float)

    def __init__(self, port=UDP_PORT, parent=None):
        super().__init__(parent)
        self.port = port
        self.running = True

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("127.0.0.1", self.port))
        while self.running:
            data, _ = sock.recvfrom(6*8)  # Expecting a double (8 bytes)
            x = struct.unpack('dddddd', data)[0]  # Unpack double
            self.x_position.emit(x)

    def stop(self):
        self.running = False


class RectangleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_index = 0  # Default active index
        self.rows = 4
        self.cols = 4
        self.rectangles = [
            QRect(col * 200 + 20, row * 200 + 20, 160, 160)  # Doubled size
            for row in range(self.rows)
            for col in range(self.cols)
        ]

        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.start_progress)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.progress = 0
        self.progress_active = False

        self.movement_timer = QTimer(self)
        self.movement_timer.timeout.connect(self.move_right)
        self.allow_move = True

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.black)  # Set background color to black

        for index, rect in enumerate(self.rectangles):
            if index == self.active_index:
                # Draw white border for active rectangle
                painter.setPen(QPen(Qt.white, 3))
            else:
                # Draw default border
                painter.setPen(QPen(Qt.gray, 1))
            painter.setBrush(QColor(50, 50, 50))  # Gray fill color
            painter.drawRect(rect)

        # Draw progress circle if active
        if self.progress_active:
            center = self.rectangles[self.active_index].center()
            radius = 60  # Adjusted for larger rectangle
            painter.setPen(QPen(Qt.white, 2))
            painter.setBrush(Qt.NoBrush)
            start_angle = 90 * 16
            span_angle = -math.floor((self.progress / 100) * 360) * 16
            painter.drawArc(center.x() - radius, center.y() - radius, radius * 2, radius * 2, start_angle, span_angle)

    def keyPressEvent(self, event):
        if self.active_index is None:
            return

        row = self.active_index // self.cols
        col = self.active_index % self.cols

        if event.key() == Qt.Key_Up:
            if row > 0:
                row -= 1
        elif event.key() == Qt.Key_Down:
            if row < self.rows - 1:
                row += 1
        elif event.key() == Qt.Key_Left:
            if col > 0:
                col -= 1
            else:
                # Move to the previous row if available
                if row > 0:
                    row -= 1
                    col = self.cols - 1
        elif event.key() == Qt.Key_Right:
            if col < self.cols - 1:
                col += 1
            else:
                # Move to the next row if available
                if row < self.rows - 1:
                    row += 1
                    col = 0

        self.active_index = row * self.cols + col
        self.start_initial_timer()
        self.update()  # Repaint the widget

    def start_initial_timer(self):
        self.progress_timer.start(WAIT_CONFIRMATION)  # Wait 1 second before starting progress
        self.timer.stop()  # Reset the progress timer
        self.progress = 0
        self.progress_active = False

    def start_progress(self):
        self.progress_timer.stop()  # Stop the initial delay timer
        self.timer.start(100)  # Timer ticks every 100ms
        self.progress = 0
        self.progress_active = True

    def update_progress(self):
        self.progress += 3.33  # Increment progress (100% in ~3 seconds)
        if self.progress >= 100:
            self.progress = 100
            self.timer.stop()
            self.progress_active = False
            print(f"Rectangle {self.active_index} confirmed!")
        self.update()

    def move_right(self):
        row = self.active_index // self.cols
        col = self.active_index % self.cols

        if col < self.cols - 1:
            col += 1
        else:
            if row < self.rows - 1:
                row += 1
                col = 0

        self.active_index = row * self.cols + col
        self.start_initial_timer()
        self.update()

    def move_left(self):
        row = self.active_index // self.cols
        col = self.active_index % self.cols

        if col > 0:
            col -= 1
        else:
            if row > 0:
                row -= 1
                col = self.cols - 1

        self.active_index = row * self.cols + col
        self.start_initial_timer()
        self.update()

    def handle_udp_input(self, x):
        if x < -15:
            if self.allow_move:
                self.move_right()
                self.allow_move = False
                self.movement_timer.timeout.disconnect()
                self.movement_timer.timeout.connect(self.move_right)
                self.movement_timer.start(ALLOW_MOVEMENT)  # Allow movement every 0.5 seconds
        elif x > 15:
            if self.allow_move:
                self.move_left()
                self.allow_move = False
                self.movement_timer.timeout.disconnect()
                self.movement_timer.timeout.connect(self.move_left)
                self.movement_timer.start(ALLOW_MOVEMENT)  # Allow movement every 0.5 seconds
        else:
            self.movement_timer.stop()
            self.allow_move = True

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selectable Rectangles")
        self.showFullScreen()  # Set the window to full screen

        self.central_widget = RectangleWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setFocusPolicy(Qt.StrongFocus)  # Enable focus for key events

        self.udp_listener = UDPListener()
        self.udp_listener.x_position.connect(self.central_widget.handle_udp_input)
        self.udp_listener.start()

    def closeEvent(self, event):
        self.udp_listener.stop()
        self.udp_listener.wait()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
