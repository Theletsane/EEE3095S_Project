# Connect.py
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout,
    QGraphicsOpacityEffect, QApplication
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer
from PyQt5.QtGui import QClipboard, QPainter, QColor, QTransform

# --------------------- Snackbar ---------------------
class Snackbar(QLabel):
    """Snackbar notification that fades in/out."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLabel {
                background-color: rgba(50, 50, 50, 180);
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }
        """)
        self.setAlignment(Qt.AlignCenter)
        self.setVisible(False)
        self.effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.effect)
        self.anim = QPropertyAnimation(self.effect, b"opacity", self)
        self.anim.setDuration(400)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)

    def show_message(self, text):
        self.setText(text)
        self.setVisible(True)
        self.raise_()
        self.anim.stop()
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()
        QTimer.singleShot(2000, self.fade_out)

    def fade_out(self):
        self.anim.stop()
        self.anim.setStartValue(1)
        self.anim.setEndValue(0)
        self.anim.start()
        self.anim.finished.connect(lambda: self.setVisible(False))

# --------------------- Paper Tab ---------------------
class PaperTab(QLabel):
    """Paper tab under the button, expands on hover, tilted."""
    def __init__(self, parent, button, textbox, snackbar):
        super().__init__(parent)
        self.button = button
        self.textbox = textbox
        self.snackbar = snackbar
        self.stick_offset = 5
        self.default_height = int(button.height() * 0.55)
        self.expanded_height = int(button.height() * 0.8)
        self.anim = None

        self.setStyleSheet("""
            background-color: #87A19E;
            border: 1px solid #FAFAF0;
            border-radius: 3px;
        """)
        self.setFixedHeight(self.default_height)
        self.hide()

    def enterEvent(self, event):
        self.animate_height(self.expanded_height)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animate_height(self.default_height)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        text_content = self.textbox.toPlainText().strip()
        if text_content:
            QApplication.clipboard().setText(text_content)
            self.snackbar.show_message("Code in clipboard")
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        transform = QTransform()
        transform.shear(0.05, 0)
        painter.setTransform(transform)
        painter.fillRect(self.rect(), QColor("#87A19E"))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

    def animate_height(self, target_height):
        anim = QPropertyAnimation(self, b"geometry")
        anim.setDuration(250)
        anim.setEasingCurve(QEasingCurve.InOutCubic)

        rect = self.geometry()
        btn_pos = self.button.mapTo(self.parent(), self.button.rect().topLeft())
        btn_w = self.button.width()
        new_y = btn_pos.y() - target_height + self.stick_offset
        new_h = target_height
        new_x = btn_pos.x() + int(btn_w * 0.1)
        new_w = int(btn_w * 0.8)

        anim.setStartValue(rect)
        anim.setEndValue(QRect(new_x, new_y, new_w, new_h))
        anim.start()
        self.anim = anim

    def update_position(self):
        btn_pos = self.button.mapTo(self.parent(), self.button.rect().topLeft())
        btn_w = self.button.width()
        tab_w = int(btn_w * 0.8)
        tab_x = btn_pos.x() + int(btn_w * 0.1)
        tab_y = btn_pos.y() - self.height() + self.stick_offset
        self.setGeometry(tab_x, tab_y, tab_w, self.height())

# --------------------- SlideBox ---------------------
class SlideBox(QWidget):
    def __init__(self, label, snackbar):
        super().__init__()
        self.visible = False

        self.button = QPushButton(label)
        self.button.setFixedSize(200, 50)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #0F2021;
                color: white;
                font-size: 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #243037;
            }
        """)

        self.textbox = QTextEdit()
        self.textbox.setStyleSheet("""
            background-color: #87A19E;
            font-size: 14px;
            border-radius: 5px;
        """)
        self.textbox.setFixedHeight(50)
        self.textbox.setFixedWidth(0)
        self.textbox.hide()

        self.paper_tab = PaperTab(self, self.button, self.textbox, snackbar)

        container = QWidget()
        container.setFixedHeight(60)
        hbox_container = QHBoxLayout(container)
        hbox_container.setContentsMargins(0,0,0,0)
        hbox_container.setSpacing(20)
        hbox_container.addWidget(self.button, alignment=Qt.AlignCenter)
        hbox_container.addWidget(self.textbox, alignment=Qt.AlignLeft)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(container)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        self.button.clicked.connect(self.toggle_textbox)

    def resizeEvent(self, event):
        self.paper_tab.update_position()
        super().resizeEvent(event)

    def toggle_textbox(self):
        self.textbox.show()
        anim = QPropertyAnimation(self.textbox, b"maximumWidth")
        anim.setDuration(500)
        anim.setEasingCurve(QEasingCurve.InOutCubic)

        if not self.visible:
            self.paper_tab.hide()
            anim.setStartValue(0)
            anim.setEndValue(300)
        else:
            anim.setStartValue(300)
            anim.setEndValue(0)
            def after_close():
                if self.textbox.toPlainText().strip():
                    self.paper_tab.setFixedHeight(self.paper_tab.default_height)
                    self.paper_tab.show()
                    self.paper_tab.update_position()
                else:
                    self.paper_tab.hide()
            anim.finished.connect(after_close)

        anim.start()
        self.anim = anim
        self.visible = not self.visible

# --------------------- Connect Page ---------------------
class ConnectPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connect Page")
        self.setFixedSize(1000, 850)
        self.setStyleSheet("background-color: #E4EEF0;")
        
        self.home_page = None  # Reference to HomePage for back navigation
        self.disconnect_page = None

        self.snackbar = Snackbar(self)
        self.snackbar.setFixedWidth(250)
        self.snackbar.move((self.width() - 250)//2, self.height() - 100)

        # SlideBoxes
        self.box1 = SlideBox("Button 1", self.snackbar)
        self.box2 = SlideBox("Button 2", self.snackbar)
        self.box3 = SlideBox("Button 3", self.snackbar)

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.box1)
        vbox.addWidget(self.box2)
        vbox.addWidget(self.box3)
        vbox.addStretch()
        vbox.setSpacing(40)
        vbox.setAlignment(Qt.AlignCenter)
        self.setLayout(vbox)

        # Disconnect button (top-left) - goes back to HomePage
        self.disconnect_btn = QPushButton("Disconnect", self)
        self.disconnect_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6B6B;
                color: white;
                font-size: 14px;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover { background-color: #FF4C4C; }
        """)
        self.disconnect_btn.adjustSize()
        margin = 10
        self.disconnect_btn.move(margin, margin)
        self.disconnect_btn.clicked.connect(self.go_to_homepage)

        # Disconnect and Exit button (top-right) - goes to DisconnectPage
        self.exit_btn = QPushButton("Disconnect and Exit", self)
        self.exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6B6B;
                color: white;
                font-size: 14px;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover { background-color: #FF4C4C; }
        """)
        self.exit_btn.adjustSize()
        self.exit_btn.move(self.width() - self.exit_btn.width() - margin, margin)
        self.exit_btn.clicked.connect(self.open_disconnect_page)

    def go_to_homepage(self):
        """Go back to HomePage (connection screen)"""
        if self.home_page:
            self.home_page.show()
            self.close()
        else:
            # If no reference, create new HomePage
            from HomePage import HomePage
            home = HomePage()
            home.show()
            self.close()

    def open_disconnect_page(self):
        """Open DisconnectPage (exit sequence)"""
        from Disconnect import DisconnectPage
        self.disconnect_page = DisconnectPage()
        self.disconnect_page.connect_page = self  # Pass reference
        self.disconnect_page.show()
        self.close()

# Standalone run
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ConnectPage()
    window.show()
    sys.exit(app.exec_())