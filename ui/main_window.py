# ui/main_window.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtCore import Qt
from config import VINTAGE_THEME


class MainWindow(QWidget):
    def __init__(self, profile):
        super().__init__()
        self.profile = profile
        self.score = 0
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(f"🧠 Loopbreaker v3 - {self.profile['username']}")
        self.setFixedSize(600, 400)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(VINTAGE_THEME["bg_color"]))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(VINTAGE_THEME["text_color"]))
        self.setPalette(palette)

        font = QFont(VINTAGE_THEME["font"], VINTAGE_THEME["font_size"])
        self.setFont(font)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel(f"👤 Welcome, {self.profile['username']}")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        self.seq_label = QLabel("🔁 Pattern will appear here")
        self.seq_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.seq_label)

        self.btn_yes = QPushButton("YES")
        self.btn_no = QPushButton("NO")
        self.btn_yes.clicked.connect(lambda: self.evaluate_answer("yes"))
        self.btn_no.clicked.connect(lambda: self.evaluate_answer("no"))

        layout.addWidget(self.btn_yes)
        layout.addWidget(self.btn_no)

        self.setLayout(layout)

    def evaluate_answer(self, answer):
        print(f"{self.profile['username']} answered: {answer}")
        # Placeholder for actual evaluation

    def show_sequence(self, sequence):
        self.seq_label.setText("➤ " + " ".join(sequence))
