import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QGraphicsOpacityEffect, QGraphicsColorizeEffect, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import (
    QPropertyAnimation, QEasingCurve, QPoint, QTimer, pyqtProperty, QObject
)
from PyQt5.QtGui import QColor


# Helper class for animating button background
class ColorAnimator(QObject):
    def __init__(self, button):
        super().__init__()
        self._color = QColor("#EBE8EB")
        self.button = button

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color
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


# Helper class for animating text + border color after drop
class TextBorderAnimator(QObject):
    def __init__(self, button):
        super().__init__()
        self._color = QColor("#800080")
        self.button = button

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color
        # Animate text and border colors
        self.button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {color.name()};
                border: 3px solid {color.name()};
                border-radius: 14px;
                font-size: 24px;
                font-weight: bold;
                padding: 10px 20px;
            }}
        """)

    color = pyqtProperty(QColor, fget=getColor, fset=setColor)


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smooth Color Fade Button")
        self.resize(1000, 850)
        self.setStyleSheet("background-color: white;")

        # Button setup
        self.button = QPushButton("Welcome", self)
        self.button.setEnabled(False)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #EBE8EB;
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 25px;
                padding: 10px 20px;
            }
        """)

        # Effects
        self.opacity_effect = QGraphicsOpacityEffect()
        self.button.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

        self.color_animator = ColorAnimator(self.button)
        self.glow_effect = QGraphicsColorizeEffect()
        self.glow_effect.setColor(QColor(128, 0, 128))
        self.glow_effect.setStrength(0)

        # Place button
        self.update_button()

        # Start sequence with delay
        QTimer.singleShot(500, self.start_fade_in)

    def resizeEvent(self, event):
        self.update_button()
        super().resizeEvent(event)

    def update_button(self):
        w, h = self.width(), self.height()
        btn_w, btn_h = int(w * 0.3), int(h * 0.2)
        self.button.resize(btn_w, btn_h)
        self.button.move((w - btn_w) // 2, int(h * 0.25))

    def start_fade_in(self):
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(2000)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.finished.connect(self.start_color_fade)
        self.fade_animation.start()

    def start_color_fade(self):
        self.color_animation = QPropertyAnimation(self.color_animator, b"color")
        self.color_animation.setDuration(7000)
        self.color_animation.setKeyValueAt(0.0, QColor("#EBE8EB"))
        self.color_animation.setKeyValueAt(0.25, QColor("#DEB7EE"))
        self.color_animation.setKeyValueAt(0.5, QColor("#7497C4"))
        self.color_animation.setKeyValueAt(0.75, QColor("#70C6C5"))
        self.color_animation.setKeyValueAt(1.0, QColor("#4A706F"))
        self.color_animation.finished.connect(self.drop_button)
        self.color_animation.start()

    def drop_button(self):
        w, h = self.width(), self.height()
        btn_w, btn_h = self.button.width(), self.button.height()

        target_x = (w - btn_w) // 2
        target_y = int(h * 0.8) - btn_h // 2

        # Drop animation (position only)
        self.drop_animation = QPropertyAnimation(self.button, b"pos")
        self.drop_animation.setDuration(2400)
        self.drop_animation.setEndValue(QPoint(target_x, target_y))
        self.drop_animation.setEasingCurve(QEasingCurve.OutBounce)
        self.drop_animation.finished.connect(self.resize_after_drop)
        self.drop_animation.start()

    def resize_after_drop(self):
        # Resize the button after reaching bottom
        w, h = self.width(), self.height()
        new_w, new_h = int(w * 0.3), int(h * 0.1)
        self.size_animation = QPropertyAnimation(self.button, b"size")
        self.size_animation.setDuration(800)
        self.size_animation.setEndValue(self.button.size().expandedTo(self.button.size()))
        self.button.resize(new_w, new_h)
        QTimer.singleShot(300, self.start_post_drop_glow)

    def start_post_drop_glow(self):
        self.button.setText("Connect")
        self.button.setEnabled(True)
        self.button.setGraphicsEffect(self.glow_effect)

        # Glow effect
        self.glow_animation = QPropertyAnimation(self.glow_effect, b"strength")
        self.glow_animation.setDuration(2500)
        self.glow_animation.setStartValue(0)
        self.glow_animation.setEndValue(1)
        self.glow_animation.start()

        # Text + border animation
        self.text_border_animator = TextBorderAnimator(self.button)
        self.text_border_animation = QPropertyAnimation(self.text_border_animator, b"color")
        self.text_border_animation.setDuration(10000)
        self.text_border_animation.setKeyValueAt(0.0, QColor("#800080"))
        self.text_border_animation.setKeyValueAt(0.25, QColor("#DEB7EE"))
        self.text_border_animation.setKeyValueAt(0.5, QColor("#7497C4"))
        self.text_border_animation.setKeyValueAt(0.75, QColor("#70C6C5"))
        self.text_border_animation.setKeyValueAt(1.0, QColor("#800080"))
        self.text_border_animation.setLoopCount(-1)
        self.text_border_animation.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())
