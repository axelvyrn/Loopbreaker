# logic/game_logic.py

import random

def generate_pattern(difficulty_level: int):
    """
    Generates a number sequence based on the current difficulty level.
    Difficulty increases sequence complexity:
    1: Arithmetic
    2: Geometric
    3: Squares
    4: Cubes
    5+: Fibonacci variants or mixes
    """
    length = min(5 + difficulty_level, 10)
    
    if difficulty_level == 1:
        base = random.randint(1, 5)
        return [base * i for i in range(1, length + 1)]
    
    elif difficulty_level == 2:
        base = random.randint(2, 4)
        return [base ** i for i in range(1, length + 1)]
    
    elif difficulty_level == 3:
        start = random.randint(1, 4)
        return [i ** 2 for i in range(start, start + length)]
    
    elif difficulty_level == 4:
        start = random.randint(1, 3)
        return [i ** 3 for i in range(start, start + length)]
    
    else:
        # Fibonacci-style pattern
        a, b = random.randint(1, 5), random.randint(1, 5)
        seq = [a, b]
        while len(seq) < length:
            seq.append(seq[-1] + seq[-2])
        return seq


def generate_noise(length: int):
    """Generate a non-patterned, random sequence."""
    return [random.randint(1, 100) for _ in range(length)]


def generate_sequence(difficulty_level: int):
    """
    Returns a tuple (sequence, is_pattern)
    """
    if random.random() > 0.5:
        return generate_pattern(difficulty_level), True
    else:
        length = min(5 + difficulty_level, 10)
        return generate_noise(length), False
