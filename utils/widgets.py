from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QPainter, QPen, QColor, QBrush

# Global variable to track the currently selected CharLabel or ControlButton
current_selected = None

# CharLabel: Display a single Chinese character
class CharLabel(QLabel):
    char_clicked = Signal(str)  # Custom signal to emit the character text when clicked
    
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
    selected_style = """
            QLabel {
                background-color: #FF626262;  /* Background color */
                color: white;                  /* Text color */
                font-size: 80px;               /* Text size */
                font-family: "Microsoft YaHei";/* Font family */
                padding: 0px;                  /* Padding around text */
                text-align: center;            /* Center alignment */
                border: 7px solid #FFB140;     /* Border for selected label */
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
        global current_selected
        
        # Deselect the previously selected widget (if any)
        if current_selected:
            current_selected.deselect()
        
        # Mark this CharLabel as selected
        current_selected = self
        
        # Apply selected style to this widget
        self.setStyleSheet(self.selected_style)
    
    def deselect(self):
        """Reset the style of the CharLabel to default when deselected."""
        self.setStyleSheet(self.default_style)


# ControlButton: control buttons
class ControlButton(QLabel):
    clicked = Signal()
    default_style = """
            QLabel {
                background-color: #FFDDDDDD;  /* Background color */
                color: black;                   /* Text color */
                font-size: 48px;              /* Text size */
                font-family: "Microsoft YaHei";      /* Font family */
                padding: 7px;                /* Padding around text */
            }
        """
    selected_style = """
            QLabel {
                background-color: #FFDDDDDD;  /* Background color */
                color: black;                   /* Text color */
                font-size: 48px;              /* Text size */
                font-family: "Microsoft YaHei";      /* Font family */
                padding: 0px;                /* Padding around text */
                border: 7px solid #FFB140;     /* Border for selected label */
            }
    
        """
    
    def __init__(self, text):
        super().__init__(text)
        
        # Set the desired styling directly in the class
        self.setStyleSheet(self.default_style)
        self.setAlignment(Qt.AlignCenter)
        
    def mousePressEvent(self, event):
        # Emit the clicked signal when the label is clicked
        self.clicked.emit()
        # self.select()

    def select(self):
        global current_selected
        
        # Deselect the previously selected widget (if any)
        if current_selected:
            current_selected.deselect()
        
        # Mark this ControlButton as selected
        current_selected = self
        
        # Apply selected style to this widget
        self.setStyleSheet(self.selected_style)
    
    def deselect(self):
        """Reset the style of the ControlButton to default when deselected."""
        self.setStyleSheet(self.default_style)


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
