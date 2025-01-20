# run the opentrack first
# draw the window
# read the corpus to fill in the characters
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QRect, QSize

class RectangleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_index = 0  # Default active index
        self.rows = 4
        self.cols = 4
        self.rectangles = [
            QRect(col * 100 + 10, row * 100 + 10, 80, 80)
            for row in range(self.rows)
            for col in range(self.cols)
        ]
        self.setFixedSize(420, 420)

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

    def mousePressEvent(self, event):
        for index, rect in enumerate(self.rectangles):
            if rect.contains(event.pos()):
                self.active_index = index
                self.update()  # Repaint the widget
                break

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
        self.update()  # Repaint the widget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selectable Rectangles")
        self.setFixedSize(QSize(420, 420))

        self.central_widget = RectangleWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setFocusPolicy(Qt.StrongFocus)  # Enable focus for key events

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()