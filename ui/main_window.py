import time
import random
from reset import delete_directory_contents, reset_game
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import Qt

from logic.game_logic import generate_sequence
from utils.profile_manager import load_profile, update_stats, load_profile
from config import VINTAGE_THEME, DEFAULT_ROUNDS, SOUNDS_DIR
import pygame
from PyQt6.QtWidgets import QMessageBox
from config import PROFILE_DIR, DATA_DIR
import shutil

pygame.mixer.init()

def play_sound(name):
    try:
        pygame.mixer.Sound(str(SOUNDS_DIR / f"{name}.wav")).play()
    except:
        pass

class MainWindow(QMainWindow):
    def __init__(self, profile):
        super().__init__()
        self.profile = profile
        self.setWindowTitle(f"Loopbreaker v2 - {self.profile['username']}")
        self.setFixedSize(600, 400)

        self.reaction_times = []
        self.score = 0
        self.streak = 0
        self.round = 0

        self.setup_ui()
        self.next_round()

    def setup_ui(self):
        self.setWindowTitle("🌀 Loopbreaker v3")

        # Set palette
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(VINTAGE_THEME["bg_color"]))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(VINTAGE_THEME["text_color"]))
        self.setPalette(palette)

        # Set font
        font = QFont(VINTAGE_THEME["font"], VINTAGE_THEME["font_size"])
        self.setFont(font)

        # Create a central widget and layout
        central_widget = QWidget()
        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Add widgets
        self.title = QLabel(f"🎮 LOOPBREAKER ID: {self.profile['username']}")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)

        self.seq_label = QLabel("Sequence will appear here.")
        self.seq_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.seq_label)

        self.yes_button = QPushButton("YES (Pattern)")
        self.no_button = QPushButton("NO (Noise)")

        self.yes_button.clicked.connect(lambda: self.evaluate_answer("yes"))
        self.no_button.clicked.connect(lambda: self.evaluate_answer("no"))

        self.layout.addWidget(self.yes_button)
        self.layout.addWidget(self.no_button)
        self.reset_button = QPushButton("Reset Game")
        self.reset_button.clicked.connect(lambda: reset_game())
        self.layout.addWidget(self.reset_button)
        self.close()


        #spacing
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(40, 40, 40, 40)


    def next_round(self):
        if self.round >= DEFAULT_ROUNDS:
            self.end_game()
            return

        self.round += 1
        self.seq, self.is_pattern = generate_sequence(self.round)
        self.seq_label.setText(f"Pattern {self.round}: {self.seq}")
        self.start_time = time.time()

    def evaluate_answer(self, answer):
        end_time = time.time()
        reaction = round(end_time - self.start_time, 3)
        self.reaction_times.append(reaction)

        correct = ((answer == "yes" and self.is_pattern) or
                   (answer == "no" and not self.is_pattern))

        if correct:
            play_sound("correct")
            self.score += 1
            self.streak += 1
        else:
            play_sound("wrong")
            self.streak = 0

        self.next_round()

    def end_game(self):
        if self.reaction_times:
            avg_reaction_time = sum(self.reaction_times) / len(self.reaction_times)
        else:
            avg_reaction_time = 0.0

        update_stats(self.profile, self.score, avg_reaction_time, self.streak)

        msg = QMessageBox()
        msg.setWindowTitle("Game Over")
        msg.setText(
            f"🎯 Score: {self.score}\n🔥 Streak: {self.streak}\n⚡ Avg Reaction: {avg_reaction_time:.2f} s"
        )
        msg.exec()
        self.close()
