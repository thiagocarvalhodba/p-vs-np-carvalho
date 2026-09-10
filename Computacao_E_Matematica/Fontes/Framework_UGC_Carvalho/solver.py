import torch
import torch.nn.functional as F
from config import DEVICE, STEPS, LR

def solve_ug(A, pi, k):
    n = A.shape[0]

    # logits de atribuição de rótulos
    X = torch.randn(n, k, device=DEVICE, requires_grad=True)

    optimizer = torch.optim.Adam([X], lr=LR)

    for _ in range(STEPS):
        probs = F.softmax(X, dim=1)

        loss = 0.0

        for (i, j), perm in pi.items():
            p_i = probs[i]
            p_j = probs[j]

            # 🔥 perm já é tensor agora
            p_j_perm = p_j[perm]

            loss -= torch.dot(p_i, p_j_perm)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    return torch.argmax(X, dim=1)