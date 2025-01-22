from ui import MainWindow
from PySide6.QtWidgets import QApplication
import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

# App entry point
if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()

    if config["ui"]["full_screen"]:
        window.showFullScreen()
    else:
        window.show()

    app.exec()
