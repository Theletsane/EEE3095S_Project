import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QGraphicsOpacityEffect, QGraphicsColorizeEffect, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import (
    QPropertyAnimation, QEasingCurve, QPoint, QTimer, pyqtProperty, QObject
)
from PyQt5.QtGui import QColor


# Helper class for animating the button’s background color
class ColorAnimator(QObject):
    def __init__(self, button):
        super().__init__()
        self._color = QColor("#EBE8EB")  # start color
        self.button = button

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color
        # update button background color only
        self.button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color.name()};
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 20px;
                padding: 10px 20px;
            }}
        """)

    color = pyqtProperty(QColor, fget=getColor, fset=setColor)


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smooth Color Fade Button")
        self.resize(1000, 850)
        self.setStyleSheet("background-color: white;")  # page background

        # Button
        self.button = QPushButton("Welcome", self)
        self.button.setEnabled(False)

        # Initial button style
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #EBE8EB;
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 20px;
                padding: 10px 20px;
            }
        """)

        # Fade-in effect
        self.opacity_effect = QGraphicsOpacityEffect()
        self.button.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

        # Color animator for background
        self.color_animator = ColorAnimator(self.button)

        # Shadow effect (instead of box-shadow)
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(0)
        self.shadow_effect.setOffset(0, 0)
        self.shadow_effect.setColor(QColor(180, 180, 180))

        # Glow effect for later (post-drop)
        self.glow_effect = QGraphicsColorizeEffect()
        self.glow_effect.setColor(QColor(128, 0, 128))
        self.glow_effect.setStrength(0)

        # Position button
        self.update_button()

        # Start animation after short delay
        QTimer.singleShot(500, self.start_fade_in)

    def resizeEvent(self, event):
        self.update_button()
        super().resizeEvent(event)

    def update_button(self):
        """Update button size and initial position"""
        w = self.width()
        h = self.height()
        btn_w = int(w * 0.2)
        btn_h = int(h * 0.1)
        self.button.resize(btn_w, btn_h)

        # Initial position (25% down)
        x = (w - btn_w) // 2
        y = int(h * 0.25)
        self.button.move(x, y)

    def start_fade_in(self):
        """Fade in the button"""
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(2000)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.finished.connect(self.start_color_fade)
        self.fade_animation.start()

    def start_color_fade(self):
        """Animate the button background color (before drop)"""
        self.button.setGraphicsEffect(self.shadow_effect)

        self.color_animation = QPropertyAnimation(self.color_animator, b"color")
        self.color_animation.setDuration(7000)
        self.color_animation.setKeyValueAt(0.0, QColor("#EBE8EB"))  # soft white
        self.color_animation.setKeyValueAt(0.25, QColor("#DEB7EE"))  # pink
        self.color_animation.setKeyValueAt(0.5, QColor("#7497C4"))   # light blue
        self.color_animation.setKeyValueAt(0.75, QColor("#70C6C5"))  # light green
        self.color_animation.setKeyValueAt(1.0, QColor("#4A706F"))   # bluish green
        self.color_animation.finished.connect(self.drop_button)
        self.color_animation.start()

    def drop_button(self):
        """Animate button drop to 80% of the screen height"""
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
        self.drop_animation.finished.connect(self.start_post_drop_glow)
        self.drop_animation.start()

    def start_post_drop_glow(self):
        """After drop: enable button, change text, start glow color fade"""
        self.button.setText("Connect")
        self.button.setEnabled(True)

        # Apply glow effect
        self.button.setGraphicsEffect(self.glow_effect)

        # Animate glow (text + border color fade)
        self.glow_color_animation = QPropertyAnimation(self.glow_effect, b"strength")
        self.glow_color_animation.setDuration(2500)
        self.glow_color_animation.setStartValue(0)
        self.glow_color_animation.setEndValue(1)
        self.glow_color_animation.start()

        # Start color animation for border + text
        self.text_border_animation = QPropertyAnimation(self.text_border_animator, b"color")
        self.text_border_animation.setDuration(10000)
        self.text_border_animation.setKeyValueAt(0.0, QColor("#800080"))  # purple
        self.text_border_animation.setKeyValueAt(0.25, QColor("#DEB7EE")) # pink
        self.text_border_animation.setKeyValueAt(0.5, QColor("#7497C4"))  # light blue
        self.text_border_animation.setKeyValueAt(0.75, QColor("#70C6C5")) # light green
        self.text_border_animation.setKeyValueAt(1.0, QColor("#800080"))  # purple again
        self.text_border_animation.setLoopCount(-1)  # loop forever
        self.text_border_animation.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())
