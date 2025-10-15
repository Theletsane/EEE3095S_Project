# HomePage.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QGraphicsOpacityEffect,
    QGraphicsColorizeEffect, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QVBoxLayout
)
from PyQt5.QtCore import (
    QPropertyAnimation, QEasingCurve, QPoint, QTimer, pyqtProperty,
    QObject, QPointF, Qt
)
from PyQt5.QtGui import QColor, QBrush, QPen, QFont, QPainter

# ------------------------- Button Animators -------------------------
class ColorAnimator(QObject):
    def __init__(self, button):
        super().__init__()
        self._color = QColor("#87A19E")
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

class TextBorderAnimator(QObject):
    def __init__(self, button):
        super().__init__()
        self._color = QColor("#87A19E")
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

class PanelColorAnimator(QObject):
    def __init__(self, panel):
        super().__init__()
        self._color = QColor("#AFDDCE")
        self.panel = panel

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color
        self.panel.setStyleSheet(f"background-color: {color.name()}; border-radius: 15px;")

    color = pyqtProperty(QColor, fget=getColor, fset=setColor)

# ------------------------- USB Animators -------------------------
class AnimatedUSB(QObject):
    def __init__(self, graphics_item):
        super().__init__()
        self.graphics_item = graphics_item
        self._pos_x = graphics_item.x()
        
    def get_pos_x(self):
        return self._pos_x
    
    def set_pos_x(self, x):
        self._pos_x = x
        self.graphics_item.setX(x)
    
    pos_x = pyqtProperty(float, get_pos_x, set_pos_x)

class AnimatedItem(QObject):
    def __init__(self, graphics_item):
        super().__init__()
        self.graphics_item = graphics_item
        self._pos = graphics_item.pos()
        
    def get_pos(self):
        return self._pos
    
    def set_pos(self, pos):
        self._pos = pos
        self.graphics_item.setPos(pos)
    
    pos = pyqtProperty(QPointF, get_pos, set_pos)

class AnimatedPosX(QObject):
    def __init__(self, graphics_item):
        super().__init__()
        self.graphics_item = graphics_item
        self._pos_x = graphics_item.x()
        self._pos_y = graphics_item.y()
        
    def get_pos_x(self):
        return self._pos_x
    
    def set_pos_x(self, x):
        self._pos_x = x
        self.graphics_item.setPos(x, self._pos_y)
    
    pos_x = pyqtProperty(float, get_pos_x, set_pos_x)

# ------------------------- Connection Failed Widget -------------------------
class ConnectionFailedWidget(QWidget):
    def __init__(self, parent=None, return_callback=None):
        super().__init__(parent)
        self.return_callback = return_callback
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.title_label = QLabel("Device Not Found!")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #ff6b6b; font-size: 28px; font-weight: bold;")
        layout.addWidget(self.title_label)

        self.instruction_label = QLabel("Please connect your STM board to the PC")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setStyleSheet("color: #4A706F; font-size: 16px;")
        layout.addWidget(self.instruction_label)

        self.animation_container = QWidget()
        self.animation_container.setFixedHeight(150)
        layout.addWidget(self.animation_container)
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 300, 120)
        self.view = QGraphicsView(self.scene, self.animation_container)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setStyleSheet("border:none; background:transparent;")
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setGeometry(0, 0, 300, 150)

        self.setup_usb_animation()

        self.countdown_label = QLabel("Returning in 15 seconds...")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet("color: #8892b0; font-size: 14px;")
        layout.addWidget(self.countdown_label)

        self.hint_label = QLabel("💡 Check USB cable connection and try again")
        self.hint_label.setAlignment(Qt.AlignCenter)
        self.hint_label.setStyleSheet("color: #70C6C5; font-size: 13px; font-style: italic;")
        layout.addWidget(self.hint_label)

        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

        self.countdown_seconds = 15
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)

    def setup_usb_animation(self):
        self.port = QGraphicsRectItem(220, 45, 60, 30)
        self.port.setBrush(QBrush(QColor(45, 55, 72)))
        self.scene.addItem(self.port)
        port_slot = QGraphicsRectItem(228, 52, 44, 16)
        port_slot.setBrush(QBrush(Qt.black))
        self.scene.addItem(port_slot)

        self.cable_item = QGraphicsRectItem(0, 57, 70, 6)
        self.cable_item.setBrush(QBrush(QColor(100,100,100)))
        self.scene.addItem(self.cable_item)
        self.cable = AnimatedPosX(self.cable_item)

        self.connector_item = QGraphicsRectItem(0, 0, 40, 20)
        self.connector_item.setBrush(QBrush(QColor(200,200,200)))
        self.connector_item.setPen(QPen(QColor(150, 150, 150), 2))
        self.connector_item.setPos(20, 50)
        self.scene.addItem(self.connector_item)
        self.connector = AnimatedUSB(self.connector_item)

        self.usb_symbol_item = self.scene.addText("⚡")
        self.usb_symbol_item.setFont(QFont("Arial", 12, QFont.Bold))
        self.usb_symbol_item.setDefaultTextColor(QColor(80, 80, 80))
        self.usb_symbol_item.setPos(28,48)
        self.usb_symbol = AnimatedItem(self.usb_symbol_item)

        arrow = self.scene.addText("→")
        arrow.setPos(140, 40)
        arrow.setDefaultTextColor(QColor(255, 107, 107))
        arrow.setFont(QFont("Arial", 40, QFont.Bold))

    def show_animation(self):
        fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        fade_in.setDuration(500)
        fade_in.setStartValue(0)
        fade_in.setEndValue(1)
        fade_in.start()
        self.fade_in_anim = fade_in

        QTimer.singleShot(300, self.start_usb_loop)
        self.countdown_timer.start(1000)

    def start_usb_loop(self):
        self.animations = []

        conn_anim = QPropertyAnimation(self.connector, b"pos_x")
        conn_anim.setDuration(2000)
        conn_anim.setStartValue(20)
        conn_anim.setEndValue(180)
        conn_anim.setEasingCurve(QEasingCurve.InOutQuad)
        conn_anim.setLoopCount(-1)
        conn_anim.start()
        self.animations.append(conn_anim)

        cable_anim = QPropertyAnimation(self.cable, b"pos_x")
        cable_anim.setDuration(2000)
        cable_anim.setStartValue(-50)
        cable_anim.setEndValue(110)
        cable_anim.setEasingCurve(QEasingCurve.InOutQuad)
        cable_anim.setLoopCount(-1)
        cable_anim.start()
        self.animations.append(cable_anim)

        symbol_anim = QPropertyAnimation(self.usb_symbol, b"pos")
        symbol_anim.setDuration(2000)
        symbol_anim.setStartValue(QPointF(28,48))
        symbol_anim.setEndValue(QPointF(188,48))
        symbol_anim.setEasingCurve(QEasingCurve.InOutQuad)
        symbol_anim.setLoopCount(-1)
        symbol_anim.start()
        self.animations.append(symbol_anim)

    def update_countdown(self):
        self.countdown_seconds -= 1
        if self.countdown_seconds>0:
            self.countdown_label.setText(f"Returning in {self.countdown_seconds} seconds...")
        else:
            self.countdown_label.setText("Returning now...")
            self.countdown_timer.stop()
            QTimer.singleShot(500, self.hide_and_return)

    def hide_and_return(self):
        fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        fade_out.setDuration(500)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)
        fade_out.finished.connect(self.on_fade_out_complete)
        fade_out.start()
        self.fade_out_anim = fade_out

    def on_fade_out_complete(self):
        self.hide()
        if self.return_callback:
            self.return_callback()

# ------------------------- Home Page -------------------------
class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dongle Lock - Welcome")
        self.resize(1000, 850)
        self.setStyleSheet("background-color: white;")

        self.button = QPushButton("Welcome", self)
        self.button.setEnabled(False)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #E4EEF0;
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 25px;
                padding: 10px 20px;
            }
        """)

        self.opacity_effect = QGraphicsOpacityEffect()
        self.button.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

        self.color_animator = ColorAnimator(self.button)
        self.glow_effect = QGraphicsColorizeEffect()
        self.glow_effect.setColor(QColor(128,0,128))
        self.glow_effect.setStrength(0)

        self.update_button()

        self.failed_widget = None
        self.panel = None
        self.connect_page = None

        QTimer.singleShot(500, self.start_fade_in)

    def resizeEvent(self, event):
        self.update_button()
        super().resizeEvent(event)

    def update_button(self):
        w, h = self.width(), self.height()
        btn_w, btn_h = int(w*0.3), int(h*0.2)
        self.button.resize(btn_w, btn_h)
        self.button.move((w-btn_w)//2, int(h*0.25))

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
        anim.setKeyValueAt(0.0, QColor("#640F64"))
        anim.setKeyValueAt(0.25, QColor("#4C1661"))
        anim.setKeyValueAt(0.5, QColor("#1D3D67"))
        anim.setKeyValueAt(0.75, QColor("#14605F"))
        anim.setKeyValueAt(1.0, QColor("#0D4240"))
        anim.finished.connect(self.drop_button)
        anim.start()
        self.color_animation = anim

    def drop_button(self):
        w,h = self.width(), self.height()
        btn_w, btn_h = self.button.width(), self.button.height()
        target_x = (w-btn_w)//2
        target_y = int(h*0.8) - btn_h//2

        anim = QPropertyAnimation(self.button, b"pos")
        anim.setDuration(1500)
        anim.setEndValue(QPoint(target_x, target_y))
        anim.finished.connect(self.on_button_dropped)
        anim.start()
        self.drop_animation = anim

    def on_button_dropped(self):
        self.button.setText("Connect")
        self.button.setEnabled(True)
        w = self.width()
        h = self.height()
        btn_w = int(w * 0.3)
        btn_h = int(h * 0.1)
        self.button.resize(btn_w, btn_h)
        
        self.button.clicked.connect(self.on_connect_clicked)
        
        self.button.setGraphicsEffect(self.glow_effect)
        glow_anim = QPropertyAnimation(self.glow_effect, b"strength")
        glow_anim.setDuration(2500)
        glow_anim.setStartValue(0)
        glow_anim.setEndValue(1)
        glow_anim.start()
        self.glow_animation = glow_anim

        self.text_border_animator = TextBorderAnimator(self.button)
        border_anim = QPropertyAnimation(self.text_border_animator, b"color")
        border_anim.setDuration(8000)
        border_anim.setKeyValueAt(0.0, QColor("#87A19E"))
        border_anim.setKeyValueAt(0.25, QColor("#496767"))
        border_anim.setKeyValueAt(0.5, QColor("#0F3538"))
        border_anim.setKeyValueAt(0.75, QColor("#0F2021"))
        border_anim.setKeyValueAt(1.0, QColor("#87A19E"))
        border_anim.setLoopCount(-1)
        border_anim.start()
        self.text_border_animation = border_anim

        self.show_dropping_panel()

    def show_dropping_panel(self):
        w,h = self.width(), self.height()
        panel_w, panel_h = int(w*0.6), int(h*0.2)
        start_x = (w-panel_w)//2
        start_y = int(h*0.25)

        self.panel = QWidget(self)
        self.panel.resize(panel_w, panel_h)
        self.panel.setStyleSheet("background-color: #70C6C5; border-radius: 15px;")

        self.panel_label = QLabel("Connect Dongle", self.panel)
        self.panel_label.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
            background: transparent;
        """)
        self.panel_label.adjustSize()
        self.panel_label.move((panel_w - self.panel_label.width())//2,
                              (panel_h - self.panel_label.height())//2)

        self.panel.move(start_x, -panel_h)
        self.panel.show()

        anim = QPropertyAnimation(self.panel, b"pos")
        anim.setDuration(1800)
        anim.setStartValue(QPoint(start_x, -panel_h))
        anim.setEndValue(QPoint(start_x, start_y))
        anim.finished.connect(self.start_panel_color_loop)
        anim.start()
        self.panel_drop_animation = anim

    def start_panel_color_loop(self):
        self.panel_color_animator = PanelColorAnimator(self.panel)
        anim = QPropertyAnimation(self.panel_color_animator, b"color")
        anim.setDuration(7000)
        anim.setKeyValueAt(0.0, QColor("#87A19E"))
        anim.setKeyValueAt(0.25, QColor("#7497C4"))
        anim.setKeyValueAt(0.5, QColor("#70C6C5"))
        anim.setKeyValueAt(0.75, QColor("#4A706F"))
        anim.setKeyValueAt(1.0, QColor("#0F2021"))
        anim.start()
        self.panel_color_animation = anim

    def on_connect_clicked(self):
        # TODO: Add actual serial connection logic here
        connection_success = True  # Change to actual connection check
        
        if connection_success:
            self.show_connected_state()
        else:
            self.show_connection_failed()

    def show_connected_state(self):
        """Transition to ConnectPage (main interface)"""
        from Connect import ConnectPage
        self.connect_page = ConnectPage()
        self.connect_page.home_page = self  # Pass reference for back navigation
        self.connect_page.show()
        self.hide()

    def show_connection_failed(self):
        if self.panel:
            self.panel.hide()
        self.button.hide()
        
        if self.failed_widget:
            self.failed_widget.deleteLater()
        
        w, h = self.width(), self.height()
        panel_w, panel_h = int(w * 0.85), int(h * 0.8)
        x = (w - panel_w) // 2
        y = (h - panel_h) // 2
        
        self.failed_widget = ConnectionFailedWidget(
            parent=self, 
            return_callback=self.return_to_connect
        )
        self.failed_widget.setGeometry(x, y, panel_w, panel_h)
        self.failed_widget.setStyleSheet("""
            background-color: #F5F5F5;
            border: 4px solid #ff6b6b;
            border-radius: 27px;
            padding: 30px;
        """)
        self.failed_widget.show()
        self.failed_widget.show_animation()

    def return_to_connect(self):
        self.button.show()
        if self.panel:
            self.panel.show()
            
        if self.failed_widget:
            self.failed_widget.deleteLater()
            self.failed_widget = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())