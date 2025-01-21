import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QScreen
from utils.widgets import CharLabel, TextBlock, ControlButton
from utils.helper import load_vocab
from utils.tts import invoke_tts

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Head Tracking IME")
        self.setMinimumSize(QSize(1366, 768))

        # status
        self.ALLOW_INPUT = False

        # Set icon
        my_icon = QIcon()
        my_icon.addFile('misc/icon_small.png')
        self.setWindowIcon(my_icon)

        # Current page (index of characters)
        self.current_page = 0
        self.page_size = 21  # Number of characters per page
        self.vocab = load_vocab()

        layout = QVBoxLayout()

        # TextBlock section
        layout1 = QHBoxLayout()
        layout1.addWidget(TextBlock("输入的文字将在这里显示..."))  # Text display area

        # Layout for other sections
        layout2 = QHBoxLayout()
        layout21_widget = QWidget()  # Create a QWidget to hold layout21
        layout21 = QGridLayout(layout21_widget)  # Assign layout21 to the QWidget

        layout22_widget = QWidget()
        layout22 = QVBoxLayout(layout22_widget)
        
        layout.addLayout(layout1, 1)
        layout.addLayout(layout2, 1)
        layout2.addWidget(layout21_widget)  # Add the layout21_widget to layout2
        layout2.addWidget(layout22_widget)

        # Adding CharLabels to the grid
        self.char_labels = []
        for i in range(3):
            row = []
            for j in range(7):
                char_label = CharLabel("字")
                layout21.addWidget(char_label, i, j)
                row.append(char_label)
            self.char_labels.append(row)
        
        layout221 = QHBoxLayout()
        layout222 = QGridLayout()

        self.start_stop_button = ControlButton("开始输入▶")
        layout221.addWidget(self.start_stop_button)

        self.prev_button = ControlButton("上页")
        layout222.addWidget(self.prev_button, 0, 0)
        self.next_button = ControlButton("下页")
        layout222.addWidget(self.next_button, 0, 1)
        self.read_button = ControlButton("朗读")
        layout222.addWidget(self.read_button, 1, 0)
        self.delete_button = ControlButton("删除")
        layout222.addWidget(self.delete_button, 1, 1)

        layout22.addLayout(layout221, 1)
        layout22.addLayout(layout222, 2)

        # Central widget setup
        self.window_widget = QWidget()
        self.window_widget.setLayout(layout)
        self.window_widget.setStyleSheet("background-color: #FF5F5F5F;")  # Set background for the entire window

        # Set background color for layout21 widget (grid layout)
        layout21_widget.setStyleSheet("background-color: #FF6DAB7C;")  # Color for the grid layout's parent widget
        layout22_widget.setStyleSheet("background-color: #FF5793C8;")  # Color for the grid layout's parent widget
        
        # Event handler
        # Connect the button click to the event handler
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)
        self.start_stop_button.clicked.connect(self.start_input)

        self.setCentralWidget(self.window_widget)  # Set central widget
        self.update_char_labels() # display vocab

    def update_char_labels(self):
        # Calculate the start and end index for the current page
        start_index = self.current_page * self.page_size
        end_index = start_index + self.page_size
        chars_to_display = self.vocab[start_index:end_index]

        # Flatten the 2D list of CharLabels to a 1D list
        char_label_list = [label for row in self.char_labels for label in row]

        # Update each CharLabel with the new character
        for i, char_label in enumerate(char_label_list):
            if i < len(chars_to_display):
                char_label.setText(chars_to_display[i])
            else:
                char_label.setText("")  # Clear any remaining labels if fewer characters

    def next_page(self):
        # Increment the page index and update the grid
        if self.current_page * self.page_size + self.page_size < len(self.vocab):
            self.current_page += 1
            self.update_char_labels()
    
    def prev_page(self):
        # Decrement the page index and update the grid
        if self.current_page > 0:
            self.current_page -= 1
            self.update_char_labels()

    def start_input(self):
        if not self.ALLOW_INPUT:
            invoke_tts("开始输入")
            self.ALLOW_INPUT = True
            self.start_stop_button.setText("停止输入🛑")
        else:
            invoke_tts("停止输入")
            self.ALLOW_INPUT = False
            self.start_stop_button.setText("开始输入▶")
        


app = QApplication()
window = MainWindow()
window.show()
app.exec()

# TODO
# 2. draw light yellow box and animation