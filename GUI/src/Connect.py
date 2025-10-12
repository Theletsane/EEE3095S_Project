import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QGraphicsOpacityEffect

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Responsive Button Animation")
        self.resize(600, 400)  # initial size

        # Button to animate
        self.button = QPushButton("Welcome", self)
        self.button.resize(150, 50)  # set fixed button size

        # Apply fade-in effect
        self.opacity_effect = QGraphicsOpacityEffect()
        self.button.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

        # Start animation
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(2000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

        # Position button initially
        self.update_button_position()

    def resizeEvent(self, event):
        """Triggered when window is resized."""
        self.update_button_position()
        super().resizeEvent(event)

    def update_button_position(self):
        """Position button based on window size."""
        w = self.width()
        h = self.height()

        btn_w = self.button.width()
        btn_h = self.button.height()

        if w > 950 or h > 900:
            # 25% down from top, centered horizontally
            x = (w - btn_w) // 2
            y = int(h * 0.35)
        elif w < 500 or h < 500:
            # Centered
            x = (w - btn_w) // 2
            y = (h - btn_h) // 2
        else:
            # Default: center
            x = (w - btn_w) // 2
            y = (h - btn_h) // 2

        self.button.move(x, y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())
