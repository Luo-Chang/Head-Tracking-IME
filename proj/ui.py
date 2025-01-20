import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QTextEdit, QGroupBox

class IMEWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("Chinese IME")
        self.setGeometry(100, 100, 800, 600)

        # Set the window background color to dark grey
        self.setStyleSheet("background-color: #FF5F5F5F;")

        # Main layout
        main_layout = QVBoxLayout(self)

        # Text Display Area
        self.text_display = QTextEdit(self)
        self.text_display.setReadOnly(True)
        self.text_display.setPlaceholderText("文字显示区域...")
        self.text_display.setStyleSheet("background-color: white;")
        main_layout.addWidget(self.text_display)

        # Bottom layout (Grid + Control Buttons)
        bottom_layout = QHBoxLayout()

        # Grid layout for word selection buttons
        grid_layout = QGridLayout()
        for i in range(3):  # 3 rows
            for j in range(6):  # 6 columns
                button = QPushButton("字", self)
                grid_layout.addWidget(button, i, j)

        # Group box for word grid with dark green background
        word_grid_group = QGroupBox(self)
        word_grid_group.setLayout(grid_layout)
        word_grid_group.setStyleSheet("background-color: #FF6DAB7C;")
        bottom_layout.addWidget(word_grid_group)

        # Control Buttons layout with dark blue background
        control_layout = QVBoxLayout()
        btn_start_input = QPushButton("开始输入", self)
        btn_prev_page = QPushButton("上页", self)
        btn_next_page = QPushButton("下页", self)
        btn_read = QPushButton("朗读", self)
        btn_delete = QPushButton("删除", self)

        control_layout.addWidget(btn_start_input)
        control_layout.addWidget(btn_prev_page)
        control_layout.addWidget(btn_next_page)
        control_layout.addWidget(btn_read)
        control_layout.addWidget(btn_delete)

        # Group box for control buttons
        control_group = QGroupBox(self)
        control_group.setLayout(control_layout)
        control_group.setStyleSheet("background-color: #FF39658C;")
        bottom_layout.addWidget(control_group)

        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IMEWindow()
    window.show()
    sys.exit(app.exec())
