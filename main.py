# main.py

import sys
from PyQt6.QtWidgets import QApplication
from ui.welcome_screen import WelcomeScreen

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Loopbreaker v3")

    welcome = WelcomeScreen()
    welcome.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
