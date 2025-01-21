from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal

# CharLabel: Display a single Chinese character
class CharLabel(QLabel):
    char_clicked = Signal(str) # Custom signal to emit the character text when clicked

    def __init__(self, text):
        super().__init__(text)
        
        # Set the desired styling directly in the class
        self.setStyleSheet("""
            QLabel {
                background-color: #FF626262;  /* Background color */
                color: white;                   /* Text color */
                font-size: 80px;              /* Text size */
                font-family: "Microsoft YaHei";      /* Font family */
                padding: 5px;                /* Padding around text */
                text-align: center;           /* Center alignment */
            }
        """)

    def mousePressEvent(self, event):
        # Emit the signal when the label is clicked
        self.char_clicked.emit(self.text())


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
