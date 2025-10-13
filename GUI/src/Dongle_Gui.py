import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QGraphicsOpacityEffect, QGraphicsColorizeEffect
)
from PyQt5.QtCore import (
    QPropertyAnimation, QEasingCurve, QPoint, QTimer, pyqtProperty, QObject
)
from PyQt5.QtGui import QColor

# Animate button background
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

# Animate button text & border
class TextBorderAnimator(QObject):
    def __init__(self, button):
        super().__init__()
        self._color = QColor("#800080")
        self.button = button

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color
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

# Animate panel background color
class PanelColorAnimator(QObject):
    def __init__(self, panel):
        super().__init__()
        self._color = QColor("#F0E68C")
        self.panel = panel

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color
        self.panel.setStyleSheet(f"background-color: {color.name()}; border-radius: 15px;")

    color = pyqtProperty(QColor, fget=getColor, fset=setColor)

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Button Drop + Panel Animation")
        self.resize(1000, 850)
        self.setStyleSheet("background-color: white;")

        # --- Button ---
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
        self.glow_effect.setColor(QColor(128,0,128))
        self.glow_effect.setStrength(0)

        # Place button
        self.update_button()

        # Start animation sequence
        QTimer.singleShot(500, self.start_fade_in)

    def resizeEvent(self, event):
        self.update_button()
        super().resizeEvent(event)

    def update_button(self):
        w, h = self.width(), self.height()
        btn_w, btn_h = int(w*0.3), int(h*0.2)
        self.button.resize(btn_w, btn_h)
        self.button.move((w-btn_w)//2, int(h*0.25))

    # --- Animations ---
    def start_fade_in(self):
        anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        anim.setDuration(2000)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.finished.connect(self.start_color_fade)
        anim.start()
        self.fade_animation = anim

    def start_color_fade(self):
        anim = QPropertyAnimation(self.color_animator, b"color")
        anim.setDuration(4000)
        anim.setKeyValueAt(0.0, QColor("#EBE8EB"))
        anim.setKeyValueAt(0.25, QColor("#DEB7EE"))
        anim.setKeyValueAt(0.5, QColor("#7497C4"))
        anim.setKeyValueAt(0.75, QColor("#70C6C5"))
        anim.setKeyValueAt(1.0, QColor("#4A706F"))
        anim.finished.connect(self.drop_button)
        anim.start()
        self.color_animation = anim

    def drop_button(self):
        w,h = self.width(), self.height()
        btn_w, btn_h = self.button.width(), self.button.height()
        target_x = (w-btn_w)//2
        target_y = int(h*0.8) - btn_h//2

        anim = QPropertyAnimation(self.button, b"pos")
        anim.setDuration(2400)
        anim.setEndValue(QPoint(target_x, target_y))
        anim.setEasingCurve(QEasingCurve.OutBounce)
        anim.finished.connect(self.on_button_dropped)
        anim.start()
        self.drop_animation = anim

    def on_button_dropped(self):
        # Glow and text-border animation
        self.button.setText("Connect")
        self.button.setEnabled(True)
        w = self.width()
        h = self.height()
        btn_w = int(w * 0.3)
        btn_h = int(h * 0.1)
        self.button.resize(btn_w, btn_h)
        self.button.setGraphicsEffect(self.glow_effect)
        glow_anim = QPropertyAnimation(self.glow_effect, b"strength")
        glow_anim.setDuration(2500)
        glow_anim.setStartValue(0)
        glow_anim.setEndValue(1)
        glow_anim.start()
        self.glow_animation = glow_anim

        # Looping text+border color
        self.text_border_animator = TextBorderAnimator(self.button)
        border_anim = QPropertyAnimation(self.text_border_animator, b"color")
        border_anim.setDuration(8000)
        border_anim.setKeyValueAt(0.0, QColor("#800080"))
        border_anim.setKeyValueAt(0.25, QColor("#DEB7EE"))
        border_anim.setKeyValueAt(0.5, QColor("#7497C4"))
        border_anim.setKeyValueAt(0.75, QColor("#70C6C5"))
        border_anim.setKeyValueAt(1.0, QColor("#800080"))
        border_anim.setLoopCount(-1)
        border_anim.start()
        self.text_border_animation = border_anim

        # Show panel after button settled
        self.show_dropping_panel()

    def show_dropping_panel(self):
        w,h = self.width(), self.height()
        panel_w, panel_h = int(w*0.6), int(h*0.2)
        start_x = (w-panel_w)//2
        start_y = int(h*0.25)

        self.panel = QWidget(self)
        self.panel.resize(panel_w, panel_h)
        self.panel.setStyleSheet("background-color: #F0E68C; border-radius: 15px;")

        # Label inside panel
        self.panel_label = QLabel("Hello! I am a panel", self.panel)
        self.panel_label.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
            background: transparent;
        """)
        self.panel_label.adjustSize()
        self.panel_label.move((panel_w - self.panel_label.width())//2,
                              (panel_h - self.panel_label.height())//2)

        # Start above window
        self.panel.move(start_x, -panel_h)
        self.panel.show()

        # Drop animation
        anim = QPropertyAnimation(self.panel, b"pos")
        anim.setDuration(1800)
        anim.setStartValue(QPoint(start_x, -panel_h))
        anim.setEndValue(QPoint(start_x, start_y))
        anim.setEasingCurve(QEasingCurve.OutBounce)
        anim.finished.connect(self.animate_panel_color)
        anim.start()
        self.panel_drop_animation = anim

    def animate_panel_color(self):
        self.panel_color_animator = PanelColorAnimator(self.panel)
        anim = QPropertyAnimation(self.panel_color_animator, b"color")
        anim.setDuration(2000)
        anim.setStartValue(QColor("#F0E68C"))
        anim.setEndValue(QColor("#C0C0C0"))  # Silver
        anim.start()
        self.panel_color_animation = anim


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())
