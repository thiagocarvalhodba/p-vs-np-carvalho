import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
N = 200                # número de nós
P = 0.05               # probabilidade de aresta
K = 5                  # número de rótulos
NOISE = 0.1            # nível de ruído nas permutações

EPOCHS = 100
LR = 0.05
STEPS = 100
ROUNDS = 20

THRESHOLD = 0.9        # τ para decisão YES/NO