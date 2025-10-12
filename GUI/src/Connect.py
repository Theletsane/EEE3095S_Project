import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import QPropertyAnimation, QRect

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home Page Animation")
        self.resize(400, 200)

        # Button to animate
        self.button = QPushButton("Connect", self)
        self.button.setGeometry(20, 80, 100, 40)
        self.button.clicked.connect(self.start_animation)

    def start_animation(self):
        # Create an animation object targeting the button's geometry
        self.anim = QPropertyAnimation(self.button, b"geometry")
        self.anim.setDuration(2000)  # duration in ms
        self.anim.setStartValue(QRect(20, 80, 100, 40))
        self.anim.setEndValue(QRect(260, 80, 100, 40))
        self.anim.start()