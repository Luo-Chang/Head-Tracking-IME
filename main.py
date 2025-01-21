from ui import MainWindow
from PySide6.QtWidgets import QApplication


# App entry point
if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()

    app.exec()
