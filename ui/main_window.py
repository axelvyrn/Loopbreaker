# ui/main_window.py

import time
import random
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt

from logic.game_logic import generate_sequence
from utils.profile_manager import load_profile, update_stats
from config import VINTAGE_THEME, DEFAULT_ROUNDS, SOUNDS_DIR
import pygame

pygame.mixer.init()

def play_sound(name):
    try:
        pygame.mixer.Sound(str(SOUNDS_DIR / f"{name}.wav")).play()
    except:
        pass

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" ️ Loopbreaker v2")
        self.setFixedSize(600, 400)

        self.profile = load_profile()
        self.reaction_times = []
        self.score = 0
        self.streak = 0
        self.round = 0

        self.setup_ui()
        self.next_round()

    def setup_ui(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(VINTAGE_THEME["bg_color"]))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(VINTAGE_THEME["text_color"]))
        self.setPalette(palette)

        font = QFont(VINTAGE_THEME["font"], VINTAGE_THEME["font_size"])
        self.setFont(font)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

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
        update_stats(self.profile, self.score, self.streak, self.reaction_times)
        play_sound("end")

        msg = QMessageBox()
        msg.setWindowTitle("Game Over")
        msg.setText(f"Final Score: {self.score}/{DEFAULT_ROUNDS}\n"
                    f"Longest Streak: {self.streak}\n"
                    f"Avg Reaction Time: {round(sum(self.reaction_times)/len(self.reaction_times), 2)}s")
        msg.exec()

        self.close()
