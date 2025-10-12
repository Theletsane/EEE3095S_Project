import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtWidgets import QGraphicsOpacityEffect

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Responsive Button Animation")
        self.resize(800, 600)  # initial size

        # Button
        self.button = QPushButton("Welcome", self)

        # Fade-in effect
        self.opacity_effect = QGraphicsOpacityEffect()
        self.button.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

        # Start fade-in animation
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(2000)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.finished.connect(self.drop_button)
        self.fade_animation.start()

        time.sleep(5)  # wait 2 seconds
        # Initial button setup
        self.update_button()

    def resizeEvent(self, event):
        self.update_button()
        super().resizeEvent(event)

    def update_button(self):
        """Update button size and position based on window size."""
        w = self.width()
        h = self.height()

        # Scale button size proportionally
        btn_w = int(w * 0.2)
        btn_h = int(h * 0.1)
        self.button.resize(btn_w, btn_h)

        # Initial position (25% down or center)
        if w > 950 or h > 900:
            x = (w - btn_w) // 2
            y = int(h * 0.25)
        elif w < 500 or h < 500:
            x = (w - btn_w) // 2
            y = (h - btn_h) // 2
        else:
            x = (w - btn_w) // 2
            y = (h - btn_h) // 2

        self.button.move(x, y)

    def drop_button(self):
        """Animate the button down to 80% of the screen height."""
        w = self.width()
        h = self.height()
        btn_w = self.button.width()
        btn_h = self.button.height()

        # Target position: horizontally center, 80% down
        target_x = (w - btn_w) // 2
        target_y = int(h * 0.8) - btn_h // 2
        
        self.drop_animation = QPropertyAnimation(self.button, b"pos")
        self.drop_animation.setDuration(1500)  # 1.5 seconds
        self.drop_animation.setEndValue(QPoint(target_x, target_y))
        self.drop_animation.setEasingCurve(QEasingCurve.OutBounce) 
        self.drop_animation.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())
