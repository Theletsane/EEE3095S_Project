import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.QtWidgets import QGraphicsOpacityEffect

class FadeInDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fade-In Animation Demo")
        self.setGeometry(100, 100, 400, 200)

        # Create a label
        self.label = QLabel("Hello, Fade In!", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 24px;")

        # Apply opacity effect
        self.opacity_effect = QGraphicsOpacityEffect()
        self.label.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)  # start fully transparent

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Create animation
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(2000)  # 2 seconds
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()  # start animation

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FadeInDemo()
    window.show()
    sys.exit(app.exec_())
