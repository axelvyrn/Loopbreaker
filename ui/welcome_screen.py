# ui/welcome_screen.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
)
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtCore import Qt
from config import VINTAGE_THEME
from utils.profile_manager import load_profile_menu
from utils.reset import reset_all_data


class WelcomeScreen(QWidget):
    def __init__(self, start_singleplayer_callback, create_room_callback, join_room_callback):
        super().__init__()
        self.start_singleplayer = start_singleplayer_callback
        self.create_room = create_room_callback
        self.join_room = join_room_callback
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("🌀 Loopbreaker v3 - Welcome")
        self.setFixedSize(500, 400)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(VINTAGE_THEME["bg_color"]))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(VINTAGE_THEME["text_color"]))
        self.setPalette(palette)

        font = QFont(VINTAGE_THEME["font"], VINTAGE_THEME["font_size"])
        self.setFont(font)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("🎮 LOOPBREAKER v3")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # Buttons
        btn_start = QPushButton("▶ Start Single Player")
        btn_start.clicked.connect(self.handle_start)
        layout.addWidget(btn_start)

        btn_create = QPushButton("🔗 Create Multiplayer Room")
        btn_create.clicked.connect(self.create_room)
        layout.addWidget(btn_create)

        btn_join = QPushButton("🔍 Join Multiplayer Room")
        btn_join.clicked.connect(self.join_room)
        layout.addWidget(btn_join)

        btn_reset = QPushButton("🧹 Reset Game")
        btn_reset.clicked.connect(self.handle_reset)
        layout.addWidget(btn_reset)

        btn_exit = QPushButton("🚪 Exit")
        btn_exit.clicked.connect(self.close)
        layout.addWidget(btn_exit)

        self.setLayout(layout)

    def handle_start(self):
        profile = load_profile_menu()
        self.start_singleplayer(profile)

    def handle_reset(self):
        confirm = QMessageBox.question(
            self,
            "Confirm Reset",
            "⚠️ This will delete all Loopbreaker IDs and logs. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            reset_all_data()
            QMessageBox.information(self, "Reset Complete", "✅ All profiles and logs deleted.")
