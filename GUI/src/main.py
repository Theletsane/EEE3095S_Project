"""
main.py - Application entry point
"""
import sys
from PyQt5.QtWidgets import QApplication
from home_page import HomePage


def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()