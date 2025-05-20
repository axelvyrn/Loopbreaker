import tkinter as tk
from game_logic import generate_sequence
from config import TOTAL_ROUNDS, WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, TEXT_COLOR

class LoopBreakerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Loopbreaker")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BG_COLOR)

        self.score = 0
        self.round = 0
        self.total_rounds = TOTAL_ROUNDS
        self.current_sequence = []
        self.is_pattern = False

        self.create_widgets()
        self.next_round()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="LOOPBREAKER", font=("Helvetica", 20, "bold"), fg="#39ff14", bg=BG_COLOR)
        self.title_label.pack(pady=10)

        self.instruction = tk.Label(self.root, text="Can you spot the pattern before the loop closes?", fg=TEXT_COLOR, bg=BG_COLOR)
        self.instruction.pack()

        self.sequence_label = tk.Label(self.root, text="", font=("Courier", 20), fg="cyan", bg=BG_COLOR)
        self.sequence_label.pack(pady=20)

        self.result_label = tk.Label(self.root, text="", fg="orange", bg=BG_COLOR)
        self.result_label.pack()

        self.yes_button = tk.Button(self.root, text="Pattern (Yes)", command=lambda: self.check_answer("yes"), width=15, bg="#007acc", fg="white")
        self.yes_button.pack(pady=5)

        self.no_button = tk.Button(self.root, text="Noise (No)", command=lambda: self.check_answer("no"), width=15, bg="#ff5c5c", fg="white")
        self.no_button.pack(pady=5)

        self.score_label = tk.Label(self.root, text="", fg=TEXT_COLOR, bg=BG_COLOR)
        self.score_label.pack(pady=10)

        self.next_button = tk.Button(self.root, text="Next Round", command=self.next_round, state="disabled", bg="#444", fg="white")
        self.next_button.pack(pady=10)

        self.reset_button = tk.Button(self.root, text="Restart Game", command=self.reset_game, bg="#333", fg="white")
        self.reset_button.pack(pady=5)

    def next_round(self):
        if self.round >= self.total_rounds:
            self.end_game()
            return

        self.round += 1
        self.result_label.config(text="")
        self.current_sequence, self.is_pattern = generate_sequence(self.round)
        self.sequence_label.config(text=str(self.current_sequence))
        self.score_label.config(text=f"Round {self.round} — Score: {self.score}/{self.total_rounds}")
        self.next_button.config(state="disabled")
        self.yes_button.config(state="normal")
        self.no_button.config(state="normal")

    def check_answer(self, answer):
        correct = ((answer == "yes") and self.is_pattern) or ((answer == "no") and not self.is_pattern)
        if correct:
            self.score += 1
            self.result_label.config(text="✅ Correct. You've broken the loop.")
        else:
            self.result_label.config(text="❌ Wrong. The loop closes around you.")

        self.score_label.config(text=f"Round {self.round} — Score: {self.score}/{self.total_rounds}")
        self.yes_button.config(state="disabled")
        self.no_button.config(state="disabled")
        self.next_button.config(state="normal")

    def end_game(self):
        self.sequence_label.config(text="")
        self.yes_button.pack_forget()
        self.no_button.pack_forget()
        self.next_button.pack_forget()
        self.result_label.config(text="")

        if self.score == self.total_rounds:
            message = "🔓 You are the Loopbreaker. Nothing controls you."
        elif self.score >= 3:
            message = "😐 You're aware, but not awake. Keep training."
        else:
            message = "🔒 You live in patterns you cannot see."

        self.title_label.config(text="Final Results")
        self.instruction.config(text=message)

    def reset_game(self):
        self.score = 0
        self.round = 0
        self.yes_button.pack(pady=5)
        self.no_button.pack(pady=5)
        self.next_button.pack(pady=10)
        self.title_label.config(text="LOOPBREAKER")
        self.instruction.config(text="Can you spot the pattern before the loop closes?")
        self.next_round()
