import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import QSize

class MainWindow(QMainWindow):
    def __init__(self, parent = ..., flags = ...):
        super().__init__()
        self.setWindowTitle("My APP")
        self.setMinimumSize(QSize(1366, 768))

        layout1 = QVBoxLayout()
        layout1.addWidget(Color("white"))

        layout2 = QHBoxLayout()
        layout21 = QHBoxLayout()
        layout22 = QVBoxLayout()

        layout1.addLayout(layout2)
        layout2.addLayout(layout21)
        layout2.addLayout(layout22)

        layout21.addWidget(Color("red"))
        layout21.addWidget(Color("blue"))
        layout22.addWidget(Color("yellow"))
        layout22.addWidget(Color("green"))
        
        self.widget = QWidget()
        self.widget.setLayout(layout1)
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