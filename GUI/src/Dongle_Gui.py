import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QGraphicsOpacityEffect,
    QGraphicsColorizeEffect, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsTextItem, QVBoxLayout
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

class AnimatedOpacity(QObject):
    def __init__(self, graphics_item):
        super().__init__()
        self.graphics_item = graphics_item
        self._opacity = graphics_item.opacity()
        
    def get_opacity(self):
        return self._opacity
    
    def set_opacity(self, value):
        self._opacity = value
        self.graphics_item.setOpacity(value)
    
    opacity = pyqtProperty(float, get_opacity, set_opacity)

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

        # Labels
        self.title_label = QLabel("⚠️ Connection Failed")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #ff6b6b; font-size: 28px; font-weight: bold;")
        layout.addWidget(self.title_label)

        self.instruction_label = QLabel("Please connect your STM board to the PC")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setStyleSheet("color: #4A706F; font-size: 16px;")
        layout.addWidget(self.instruction_label)

        # USB Animation
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

        # Countdown
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
        # Port
        self.port = QGraphicsRectItem(220, 45, 60, 30)
        self.port.setBrush(QBrush(QColor(45, 55, 72)))
        self.scene.addItem(self.port)
        port_slot = QGraphicsRectItem(228, 52, 44, 16)
        port_slot.setBrush(QBrush(Qt.black))
        self.scene.addItem(port_slot)

        # Cable
        self.cable_item = QGraphicsRectItem(-50, 57, 100, 6)
        self.cable_item.setBrush(QBrush(QColor(100,100,100)))
        self.scene.addItem(self.cable_item)
        self.cable = AnimatedPosX(self.cable_item)

        # Connector
        self.connector_item = QGraphicsRectItem(0, 0, 40, 20)
        self.connector_item.setBrush(QBrush(QColor(200,200,200)))
        self.connector_item.setPos(20, 50)
        self.scene.addItem(self.connector_item)
        self.connector = AnimatedUSB(self.connector_item)

        # USB Symbol
        self.usb_symbol_item = self.scene.addText("⚡")
        self.usb_symbol_item.setFont(QFont("Arial", 12, QFont.Bold))
        self.usb_symbol_item.setPos(28,48)
        self.usb_symbol = AnimatedItem(self.usb_symbol_item)

        # Dots
        self.dots = []
        self.dot_wrappers = []
        for i in range(3):
            dot = QGraphicsEllipseItem(0,0,8,8)
            dot.setBrush(QBrush(QColor(112,198,197)))
            dot.setPos(120+i*15,58)
            dot.setOpacity(0)
            self.scene.addItem(dot)
            self.dots.append(dot)
            self.dot_wrappers.append(AnimatedOpacity(dot))

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

        # Connector
        conn_anim = QPropertyAnimation(self.connector, b"pos_x")
        conn_anim.setDuration(2000)
        conn_anim.setStartValue(20)
        conn_anim.setEndValue(180)
        conn_anim.setEasingCurve(QEasingCurve.InOutQuad)
        conn_anim.setLoopCount(-1)
        conn_anim.start()
        self.animations.append(conn_anim)

        # Cable
        cable_anim = QPropertyAnimation(self.cable, b"pos_x")
        cable_anim.setDuration(2000)
        cable_anim.setStartValue(-50)
        cable_anim.setEndValue(110)
        cable_anim.setEasingCurve(QEasingCurve.InOutQuad)
        cable_anim.setLoopCount(-1)
        cable_anim.start()
        self.animations.append(cable_anim)

        # USB symbol
        symbol_anim = QPropertyAnimation(self.usb_symbol, b"pos")
        symbol_anim.setDuration(2000)
        symbol_anim.setStartValue(QPointF(28,48))
        symbol_anim.setEndValue(QPointF(188,48))
        symbol_anim.setEasingCurve(QEasingCurve.InOutQuad)
        symbol_anim.setLoopCount(-1)
        symbol_anim.start()
        self.animations.append(symbol_anim)

        # Dots
        for i, dot in enumerate(self.dot_wrappers):
            anim = QPropertyAnimation(dot, b"opacity")
            anim.setDuration(1000)
            anim.setStartValue(0)
            anim.setKeyValueAt(0.5,1)
            anim.setEndValue(0)
            anim.setLoopCount(-1)
            QTimer.singleShot(i*200, anim.start)
            self.animations.append(anim)

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
        self.setWindowTitle("USB Animation + Button Demo")
        self.resize(1000,850)
        self.setStyleSheet("background-color: white;")
        # Connect button
        self.connect_button = QPushButton("Connect", self)
        self.connect_button.setGeometry(350,700,300,80)
        self.connect_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #800080;
                border: 3px solid #800080;
                border-radius: 14px;
                font-size: 24px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: rgba(128,0,128,0.1);}
        """)
        self.connect_button.clicked.connect(self.simulate_connection_fail)
        self.failed_widget = None

    def simulate_connection_fail(self):
        self.connect_button.hide()
        self.show_connection_failed()

    def show_connection_failed(self):
        if self.failed_widget:
            self.failed_widget.deleteLater()
        w,h = self.width(), self.height()
        panel_w, panel_h = int(w*0.7), int(h*0.45)
        x = (w-panel_w)//2
        y = int(h*0.25)
        self.failed_widget = ConnectionFailedWidget(parent=self, return_callback=self.return_to_main)
        self.failed_widget.setGeometry(x,y,panel_w,panel_h)
        self.failed_widget.setStyleSheet("""
            background-color: #F5F5F5;
            border: 3px solid #ff6b6b;
            border-radius: 20px;
            padding: 20px;
        """)
        self.failed_widget.show()
        self.failed_widget.show_animation()

    def return_to_main(self):
        self.connect_button.show()
        if self.failed_widget:
            self.failed_widget.deleteLater()
            self.failed_widget = None
        print("Returned to main page.")

# ------------------------- Run -------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())
