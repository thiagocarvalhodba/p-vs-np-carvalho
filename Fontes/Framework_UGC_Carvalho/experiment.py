from generator import generate_unique_game
from solver import solve_ug
from evaluator import compute_value
from config import *

import numpy as np

def run_experiment():
    print("\n--- UNIQUE GAMES EXPERIMENT ---\n")

    noise_levels = np.linspace(0.01, 0.3, 10)

    correct = 0
    total = 0

    for noise in noise_levels:
        vals = []

        for _ in range(20):
            A, pi, x_true = generate_unique_game(N, P, K, noise)

            labels = solve_ug(A, pi, K)

            val = compute_value(A, pi, labels)
            vals.append(val)

            # decisão simples
            is_yes = noise < 0.1
            pred_yes = val >= THRESHOLD

            if is_yes == pred_yes:
                correct += 1
            total += 1

        print(f"Noise={noise:.3f} | Mean Val={np.mean(vals):.4f} | Std={np.std(vals):.4f}")

    print("\n--- RESULTADO FINAL ---")
    print(f"Accuracy: {correct / total:.3f}")


if __name__ == "__main__":
    run_experiment()