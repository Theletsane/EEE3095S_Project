# Disconnect.py
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGraphicsOpacityEffect, QApplication
from PyQt5.QtCore import QPropertyAnimation, QTimer, pyqtProperty, QObject, Qt
from PyQt5.QtGui import QColor

# ------------------------- Panel Border Animator -------------------------
class PanelBorderAnimator(QObject):
    def __init__(self, widget):
        super().__init__()
        self._color = QColor("#660000")  # initial dark red
        self.widget = widget

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color
        self.widget.setStyleSheet(f"""
            background-color: #E4EEF0;
            border: 4px solid {color.name()};
            border-radius: 15px;
        """)

    color = pyqtProperty(QColor, fget=getColor, fset=setColor)

# ------------------------- Disconnect Page -------------------------
class DisconnectPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Device Disconnected")
        self.resize(1000, 850)
        self.setStyleSheet("background-color: #0F2021;")  # dark background

        self.connect_page = None  # Reference to ConnectPage for reconnect

        # --- Panel ---
        self.panel = QWidget(self)
        self.panel.resize(int(self.width() * 0.6), int(self.height() * 0.3))
        self.panel.move((self.width() - self.panel.width()) // 2,
                        (self.height() - self.panel.height()) // 2)

        self.panel_opacity = QGraphicsOpacityEffect()
        self.panel.setGraphicsEffect(self.panel_opacity)
        self.panel_opacity.setOpacity(0)

        # Panel label
        self.panel_label = QLabel("Disconnected", self.panel)
        self.panel_label.setAlignment(Qt.AlignCenter)
        self.panel_label.setStyleSheet("color: #325D79; font-size: 32px; font-weight: bold;")
        self.panel_label.resize(self.panel.width(), self.panel.height())

        # Animator for glowing border
        self.border_animator = PanelBorderAnimator(self.panel)

        # Countdown label
        self.countdown_label = QLabel("", self)
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet("color: #CCCCCC; font-size: 18px;")
        self.countdown_label.setGeometry(0, self.panel.y() + self.panel.height() + 20,
                                         self.width(), 30)
        self.countdown_label.hide()

        # Reconnect button
        self.reconnect_button = QPushButton("Reconnect", self)
        self.reconnect_button.setStyleSheet("""
            QPushButton {
                background-color: #E4EEF0;
                color: #0F2021;
                border: 2px solid #FFFFFF;
                border-radius: 12px;
                font-size: 18px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #E7E7D8;
            }
        """)
        self.reconnect_button.resize(150, 40)
        self.reconnect_button.move((self.width() - self.reconnect_button.width()) // 2,
                                   self.countdown_label.y() + 50)
        self.reconnect_button.hide()
        self.reconnect_button.clicked.connect(self.on_reconnect)

        self.countdown_seconds = 10
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)

        self.start_disconnect_sequence()

    def start_disconnect_sequence(self):
        self.fade_in_anim = QPropertyAnimation(self.panel_opacity, b"opacity")
        self.fade_in_anim.setDuration(1000)
        self.fade_in_anim.setStartValue(0)
        self.fade_in_anim.setEndValue(1)
        self.fade_in_anim.finished.connect(self.start_border_glow_loop)
        self.fade_in_anim.start()

    def start_border_glow_loop(self):
        self.border_animation = QPropertyAnimation(self.border_animator, b"color")
        self.border_animation.setDuration(2000)
        self.border_animation.setStartValue(QColor("#660000"))
        self.border_animation.setKeyValueAt(0.5, QColor("#ff5b04"))
        self.border_animation.setEndValue(QColor("#660000"))
        self.border_animation.setLoopCount(-1)
        self.border_animation.start()
        QTimer.singleShot(5000, self.fade_panel_out)

    def fade_panel_out(self):
        self.fade_out_anim = QPropertyAnimation(self.panel_opacity, b"opacity")
        self.fade_out_anim.setDuration(800)
        self.fade_out_anim.setStartValue(1)
        self.fade_out_anim.setEndValue(0)
        self.fade_out_anim.finished.connect(self.show_countdown)
        self.fade_out_anim.start()

    def show_countdown(self):
        self.countdown_label.setText(f"Application closing in {self.countdown_seconds} seconds...")
        self.countdown_label.show()
        self.reconnect_button.show()
        self.countdown_timer.start(1000)

    def update_countdown(self):
        self.countdown_seconds -= 1
        if self.countdown_seconds > 0:
            self.countdown_label.setText(f"Application closing in {self.countdown_seconds} seconds...")
        else:
            self.countdown_label.setText("Closing now...")
            self.countdown_timer.stop()
            QTimer.singleShot(800, self.close_application)

    def close_application(self):
        """Close the entire application"""
        QApplication.instance().quit()

    def on_reconnect(self):
        """Go back to HomePage to reconnect"""
        self.countdown_timer.stop()
        
        # Go back to HomePage
        from HomePage import HomePage
        home = HomePage()
        home.show()
        self.close()

# Run standalone for testing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DisconnectPage()
    window.show()
    sys.exit(app.exec_())