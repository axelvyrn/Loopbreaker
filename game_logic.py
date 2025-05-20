import random

def generate_sequence(level):
    if level == 1:
        base = random.randint(1, 5)
        pattern = [base * i for i in range(1, 5)]
    elif level == 2:
        pattern = [i ** 2 for i in range(1, 5)]
    elif level == 3:
        pattern = [i ** 3 for i in range(1, 5)]
    elif level == 4:
        pattern = [1, 1]
        for _ in range(2, 4):
            pattern.append(pattern[-1] + pattern[-2])
    elif level == 5:
        pattern = [int(i*(i+1)/2) for i in range(1, 5)]
    else:
        pattern = [random.randint(1, 50) for _ in range(4)]

    noise = [random.randint(1, 50) for _ in range(4)]

    if random.random() > 0.5:
        return pattern, True
    else:
        return noise, False
