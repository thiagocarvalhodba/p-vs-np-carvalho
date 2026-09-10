import torch
import random
from config import DEVICE

def generate_graph(n, p):
    A = (torch.rand(n, n, device=DEVICE) < p).float()
    A = torch.triu(A, 1)
    A = A + A.T
    return A

def random_permutation(k):
    perm = list(range(k))
    random.shuffle(perm)
    return perm

def generate_unique_game(n, p, k, noise):
    A = generate_graph(n, p)

    # solução verdadeira (ground truth)
    x_true = torch.randint(0, k, (n,), device=DEVICE)

    pi = {}

    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j] == 1:

                if random.random() < noise:
                    # permutação aleatória
                    perm = random_permutation(k)
                else:
                    # permutação consistente com solução
                    shift = (x_true[j].item() - x_true[i].item()) % k
                    perm = [(x + shift) % k for x in range(k)]

                # 🔥 IMPORTANTE: já salvar como tensor (evita bugs no solver)
                pi[(i, j)] = torch.tensor(perm, device=DEVICE)

    return A, pi, x_true