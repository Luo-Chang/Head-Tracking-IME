from PySide6.QtWidgets import *
from PySide6.QtCore import QSize, Qt
from udp import UDPListener
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My APP")
        self.label = QLabel()

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def mousePressEvent(self, e):
        # self.label.setText("鼠标点按！")
        if e.button() == Qt.MouseButton.LeftButton:
            print("Left button Pressed!")
            self.label.setText("鼠标左键！")
        elif e.button() == Qt.MouseButton.RightButton:
            print("Right button pressed!")
            self.label.setText("鼠标右键！")

app = QApplication([])

window = MainWindow()
window.show()

app.exec()

print("End!")
