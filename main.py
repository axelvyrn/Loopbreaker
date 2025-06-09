# Copyright (c) 2025 Axel Vyrn. All rights reserved.
# Unauthorized copying, modification, or distribution is strictly prohibited.

import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from utils.profile_manager import load_profile_menu

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Loopbreaker v3")

    profile = load_profile_menu()
    window = MainWindow(profile)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
