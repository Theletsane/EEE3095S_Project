from PyQt5.QtCore import QObject, pyqtProperty, QPointF
from PyQt5.QtGui import QColor

# ------------------------- Button Animators -------------------------
class ColorAnimator(QObject):
    """Animates button background color"""
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
    """Animates button text and border color"""
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
    """Animates panel background color"""
    def __init__(self, panel):
        super().__init__()
        self._color = QColor("#D1EBE4")
        self.panel = panel

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color
        self.panel.setStyleSheet(f"background-color: {color.name()}; border-radius: 15px;")

    color = pyqtProperty(QColor, fget=getColor, fset=setColor)


# ------------------------- Graphics Item Animators -------------------------
class AnimatedUSB(QObject):
    """Animates USB item X position"""
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
    """Animates graphics item position (QPointF)"""
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
    """Animates graphics item X position while preserving Y"""
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