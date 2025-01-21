from PySide6.QtWidgets import *
from PySide6.QtCore import QSize, QTimer
from PySide6.QtGui import QIcon, QScreen
from utils.widgets import CharLabel, TextBlock, ControlButton
from utils.helper import load_vocab
from utils.tts import invoke_tts
from utils.udp import UDPListener
import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Head Tracking IME")
        self.setMinimumSize(QSize(1366, 768))

        # status
        self.ALLOW_INPUT = False
        self.FIRST_RUN = True
        self.current_page = 0 # Current page (index of characters)
        self.current_index = 0  # Single index to track the current selection

        # config
        self.page_rows = config["page_size"]["rows"]
        self.page_columns = config["page_size"]["columns"]
        self.page_size = self.page_rows*self.page_columns  # Number of characters per page
        self.vocab = load_vocab()
        self.movement_delay = config["timer"]["movement_delay"]
        
        # Set up UI
        self.init_ui()

        # Set icon
        my_icon = QIcon()
        my_icon.addFile('misc/icon_small.png')
        self.setWindowIcon(my_icon)

        # UDP Listener
        self.udp_listener = UDPListener()
        self.udp_listener.x_position.connect(self.handle_udp_input)
        self.udp_listener.start()

        # Timer to handle debounce
        self.allow_move = True  # Flag to allow movement
        self.movement_timer = QTimer(self)
        self.movement_timer.setSingleShot(True)  # Ensures it only fires once
        self.movement_timer.timeout.connect(self.allow_movement)  # When timer ends, we allow movement

    def init_ui(self):
        layout = QVBoxLayout()

        # TextBlock section
        layout1 = QHBoxLayout()
        self.text_block = TextBlock("输入的文字将在这里显示...")
        layout1.addWidget(self.text_block)  # Text display area

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
        self.char_label_list = [] # flat version
        for i in range(self.page_rows):
            row = []
            for j in range(self.page_columns):
                char_label = CharLabel("字")
                char_label.char_clicked.connect(self.add_to_text_block)  # Connect the signal to the handler
                layout21.addWidget(char_label, i, j)
                row.append(char_label)
                self.char_label_list.append(char_label)
            self.char_labels.append(row)
        
        layout221 = QHBoxLayout()
        layout222 = QGridLayout()

        self.start_stop_button = ControlButton("开始输入▶️")
        layout221.addWidget(self.start_stop_button)

        self.prev_button = ControlButton("上页")
        layout222.addWidget(self.prev_button, 0, 0)
        self.next_button = ControlButton("下页")
        layout222.addWidget(self.next_button, 0, 1)
        self.read_button = ControlButton("读📣")
        layout222.addWidget(self.read_button, 1, 0)
        self.delete_button = ControlButton("删除")
        layout222.addWidget(self.delete_button, 1, 1)

        self.control_button_list = [self.start_stop_button, self.prev_button, self.next_button, self.read_button, self.delete_button]
        self.full_widget_list = self.char_label_list + self.control_button_list

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
        self.start_stop_button.clicked.connect(self.start_stop_input)
        self.read_button.clicked.connect(self.read_loundly)
        self.delete_button.clicked.connect(self.delete)

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

    def add_to_text_block(self, char):
        """Add the clicked character to the TextBlock."""
        current_text = self.text_block.text()
        self.text_block.setText(current_text + char)
        # invoke_tts(char)

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

    def start_stop_input(self):
        # if self.FIRST_RUN:
        #     self.text_block.setText("")
        #     self.FIRST_RUN = False
        
        self.text_block.setText("") # clear each time
        if not self.ALLOW_INPUT:
            invoke_tts("开始输入")
            self.char_labels[0][0].select() # select the first char
            self.ALLOW_INPUT = True
            self.start_stop_button.setText("结束输入🛑")

        else:
            invoke_tts("输入完毕")
            self.ALLOW_INPUT = False
            self.start_stop_button.setText("开始输入▶️")

    def read_loundly(self):
        if self.ALLOW_INPUT:
            invoke_tts("输入完毕")
            self.ALLOW_INPUT = False
            self.start_stop_button.setText("开始输入▶️")

        # time
        invoke_tts(self.text_block.text())
    
    def delete(self):
        if self.ALLOW_INPUT:
            current_text = self.text_block.text()
            if len(current_text)>0:
                self.text_block.setText(current_text[:-1])
    
    def handle_udp_input(self, x):
        print(f"x: {x}")
        
        if x < -15:  # Move right
            if self.allow_move:
                self.move_right()
                self.allow_move = False
                self.movement_timer.start(self.movement_delay)  # Start the timer for some delay
        elif x > 15:  # Move left
            if self.allow_move:
                self.move_left()
                self.allow_move = False
                self.movement_timer.start(self.movement_delay)  # Start the timer for some delay
        else:
            self.movement_timer.stop()  # Stop timer if no movement is detected
            self.allow_move = True  # Allow movement again if no movement

    def allow_movement(self):
        self.allow_move = True

    def move_right(self):
        """Move selection to the right in the combined widget list."""
        self.current_index += 1
        if self.current_index >= len(self.full_widget_list):  # Wrap around
            self.current_index = 0
        self.full_widget_list[self.current_index].select()

    def move_left(self):
        """Move selection to the left in the combined widget list."""
        self.current_index -= 1
        if self.current_index < 0:  # Wrap around
            self.current_index = len(self.full_widget_list) - 1
        self.full_widget_list[self.current_index].select()
