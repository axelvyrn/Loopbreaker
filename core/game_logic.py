import random
import time

class LoopbreakerGame:
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
        self.sequence = []
        self.patterns = []
        self.noise = []
        self.current_index = 0
        self.start_time = None
        self.reaction_times = []
        self.streak = 0
        self.score = 0

    def generate_sequence(self):
        length = self.get_sequence_length()
        self.sequence = []
        for _ in range(length):
            if random.random() > 0.5:
                item = self.generate_pattern()
                self.patterns.append(item)
            else:
                item = self.generate_noise()
                self.noise.append(item)
            self.sequence.append(item)
        self.current_index = 0
        return self.sequence

    def get_sequence_length(self):
        return {
            'easy': 5,
            'medium': 8,
            'hard': 12
        }.get(self.difficulty, 8)

    def generate_pattern(self):
        return ''.join(random.choices('ABCDEF', k=4))

    def generate_noise(self):
        return ''.join(random.choices('GHIJKL', k=4))

    def start_round(self):
        self.start_time = time.time()

    def evaluate_input(self, user_input):
        if self.start_time is None:
            return False, 0.0

        reaction_time = time.time() - self.start_time
        self.reaction_times.append(reaction_time)

        current_item = self.sequence[self.current_index]
        is_pattern = current_item in self.patterns
        is_correct = (user_input == 'yes' and is_pattern) or (user_input == 'no' and not is_pattern)

        if is_correct:
            self.score += 1
            self.streak += 1
        else:
            self.streak = 0

        self.current_index += 1
        return is_correct, reaction_time

    def is_game_over(self):
        return self.current_index >= len(self.sequence)

    def get_average_reaction_time(self):
        if not self.reaction_times:
            return 0.0
        return sum(self.reaction_times) / len(self.reaction_times)

    def reset(self):
        self.sequence = []
        self.patterns = []
        self.noise = []
        self.current_index = 0
        self.start_time = None
        self.reaction_times = []
        self.streak = 0
        self.score = 0
