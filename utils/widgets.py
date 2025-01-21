from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
from utils.tts import invoke_tts


# CharLabel: Display a single Chinese character
class CharLabel(QLabel):
    char_clicked = Signal(str)  # Custom signal to emit the character text when clicked
    
    # Class variable to track the currently selected CharLabel
    current_selected = None
    default_style = """
            QLabel {
                background-color: #FF626262;  /* Background color */
                color: white;                   /* Text color */
                font-size: 80px;               /* Text size */
                font-family: "Microsoft YaHei";/* Font family */
                padding: 7px;                  /* Padding around text */
                text-align: center;            /* Center alignment */
            }
        """
    
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet(self.default_style)

    def mousePressEvent(self, event):
        # Emit the signal when the label is clicked
        self.char_clicked.emit(self.text())

        # Select the clicked label and remove the border from any previously selected one
        self.select()

    def select(self):
        # If there's a previously selected label, remove the border
        if CharLabel.current_selected:
            CharLabel.current_selected.setStyleSheet(self.default_style)

        # Now, select the current label and add the yellow border
        CharLabel.current_selected = self  # Update the currently selected label
        self.setStyleSheet("""
            QLabel {
                background-color: #FF626262;  /* Background color */
                color: white;                  /* Text color */
                font-size: 80px;               /* Text size */
                font-family: "Microsoft YaHei";/* Font family */
                padding: 0px;                  /* Padding around text */
                text-align: center;            /* Center alignment */
                border: 7px solid yellow;     /* Border for selected label */
            }
        """)


# TextBlock: Display the user inputs
class TextBlock(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setWordWrap(True)
        
        # Set the desired styling directly in the class
        self.setStyleSheet("""
            QLabel {
                background-color: white;  /* Background color */
                color: black;                   /* Text color */
                font-size: 64px;              /* Text size */
                font-family: "Microsoft YaHei";      /* Font family */
                padding: 1px;                /* Padding around text */
            }
        """)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)


# ControlButton: control buttons
class ControlButton(QLabel):
    clicked = Signal()
    
    def __init__(self, text):
        super().__init__(text)
        
        # Set the desired styling directly in the class
        self.setStyleSheet("""
            QLabel {
                background-color: #FFDDDDDD;  /* Background color */
                color: black;                   /* Text color */
                font-size: 48px;              /* Text size */
                font-family: "Microsoft YaHei";      /* Font family */
                padding: 0px;                /* Padding around text */
            }
        """)
        self.setAlignment(Qt.AlignCenter)
        
    def mousePressEvent(self, event):
        # Emit the clicked signal when the label is clicked
        self.clicked.emit()
