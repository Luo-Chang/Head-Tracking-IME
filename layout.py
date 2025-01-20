import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import QSize

class MainWindow(QMainWindow):
    def __init__(self, parent = ..., flags = ...):
        super().__init__()
        self.setWindowTitle("My APP")
        self.setMinimumSize(QSize(368, 640))

        layout = QVBoxLayout()
        layout.addWidget(Color("red"))
        layout.addWidget(Color("blue"))
        layout.addWidget(Color("yellow"))
        layout.addWidget(Color("green"))
        
        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


app = QApplication()
window = MainWindow()
window.show()
app.exec()