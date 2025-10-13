import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QTimer, pyqtProperty, QObject
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtGui import QColor

# Helper class to animate button text and border color
class TextBorderAnimator(QObject):
    def __init__(self, button):
        super().__init__()
        self._color = QColor("#ffffff")
        self.button = button

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color
        # Apply text color and border color with 4px thickness
        self.button.setStyleSheet(
            f"background-color: none; "
            f"color: {color.name()}; "
            f"border: 4px solid {color.name()}; "
            f"border-radius: 12px; "
            f"font-size: 24px;"
        )

    color = pyqtProperty(QColor, fget=getColor, fset=setColor)


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smooth Color Fade Button")
        self.resize(1000, 850)

        # Button
        self.button = QPushButton("Welcome", self)
        self.button.setEnabled(False)

        # Fade-in effect
        self.opacity_effect = QGraphicsOpacityEffect()
        self.button.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

        # Pre-drop color animator for background
        self.color_animator = ColorAnimator(self.button)

        # Post-drop animator for text + border
        self.text_border_animator = TextBorderAnimator(self.button)

        # Wait 0.4 seconds before starting fade-in
        QTimer.singleShot(400, self.start_fade_in)

        self.update_button()

    def resizeEvent(self, event):
        self.update_button()
        super().resizeEvent(event)

    def update_button(self):
        w = self.width()
        h = self.height()
        btn_w = int(w * 0.2)
        btn_h = int(h * 0.1)
        self.button.resize(btn_w, btn_h)

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

    def start_fade_in(self):
        # Fade-in
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(3000)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.finished.connect(self.start_color_fade)
        self.fade_animation.start()

    def start_color_fade(self):
        # Animate background color smoothly
        self.color_animation = QPropertyAnimation(self.color_animator, b"color")
        self.color_animation.setDuration(7000)
        self.color_animation.setKeyValueAt(0.0, QColor("#EBE8EB"))  # purple
        self.color_animation.setKeyValueAt(0.25, QColor("#DEB7EE"))  # pink
        self.color_animation.setKeyValueAt(0.5, QColor("#7497C4"))   # light blue
        self.color_animation.setKeyValueAt(0.75, QColor("#70C6C5"))  # light green
        self.color_animation.setKeyValueAt(1.0, QColor("#4A706F"))   # back to purple
        self.color_animation.finished.connect(self.drop_button)
        self.color_animation.start()

    def drop_button(self):
        w = self.width()
        h = self.height()
        btn_w = self.button.width()
        btn_h = self.button.height()
        target_x = (w - btn_w) // 2
        target_y = int(h * 0.8) - btn_h // 2

        self.drop_animation = QPropertyAnimation(self.button, b"pos")
        self.drop_animation.setDuration(2400)
        self.drop_animation.setEndValue(QPoint(target_x, target_y))
        self.drop_animation.setEasingCurve(QEasingCurve.OutBounce)
        self.drop_animation.finished.connect(self.start_post_drop_animation)
        self.drop_animation.start()

    def start_post_drop_animation(self):
        # Change text and enable button
        self.button.setText("Connect")
        self.button.setEnabled(True)

        # Start text + border color fading
        self.text_border_animation = QPropertyAnimation(self.text_border_animator, b"color")
        self.text_border_animation.setDuration(10000)  # 10 seconds
        self.text_border_animation.setKeyValueAt(0.0, QColor("#800080"))  # purple
        self.text_border_animation.setKeyValueAt(0.25, QColor("#DEB7EE"))  # pink
        self.text_border_animation.setKeyValueAt(0.5, QColor("#7497C4"))   # light blue
        self.text_border_animation.setKeyValueAt(0.75, QColor("#70C6C5"))  # light green
        self.text_border_animation.setKeyValueAt(1.0, QColor("#800080"))   # back to purple
        self.text_border_animation.start()


# Pre-drop background color animator
class ColorAnimator(QObject):
    def __init__(self, button):
        super().__init__()
        self._color = QColor("#EBE8EB")
        self.button = button

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color
        self.button.setStyleSheet(f"background-color: {color.name()}; color: white; font-size: 24px;")

    color = pyqtProperty(QColor, fget=getColor, fset=setColor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())
