from PySide6.QtWidgets import QLabel, QApplication
from PySide6.QtCore import Qt

class ClickableLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

    def mousePressEvent(self, event):
        # Handle the click event here
        print("Label clicked!")
        # You can add more custom behavior, like emitting signals or triggering other actions.
        super().mousePressEvent(event)

if __name__ == "__main__":
    app = QApplication([])
    label = ClickableLabel("Click me!")
    label.show()
    app.exec()