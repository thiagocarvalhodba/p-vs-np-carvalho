import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------------
# GRAFO
# -----------------------------
def generate_sparse_graph(n, p=0.01):
    A = (torch.rand(n, n, device=device) < p).float()
    A = torch.triu(A, 1)
    A = A + A.T
    return A


# -----------------------------
# MODELO
# -----------------------------
class SparseGNN(nn.Module):
    def __init__(self, dim=64):
        super().__init__()
        self.embed = nn.Linear(1, dim)
        self.update = nn.Sequential(
            nn.Linear(dim * 2, dim),
            nn.ReLU(),
            nn.Linear(dim, 1)
        )
    
    def forward(self, x, A):
        h = self.embed(x.unsqueeze(-1))
        agg = torch.matmul(A, h)
        combined = torch.cat([h, agg], dim=-1)
        return self.update(combined).squeeze()


# -----------------------------
# SOLVER (COM BALANCEAMENTO)
# -----------------------------
def learned_solver(model, A, steps=20):
    n = A.shape[0]
    x = torch.randn(n, device=device)
    
    for _ in range(steps):
        delta = model(x, A)
        x = x + 0.1 * delta
        x = torch.clamp(x, -5, 5)
    
    s = torch.tanh(x)
    
    D = torch.diag(A.sum(dim=1))
    L = D - A
    
    cut = 0.25 * torch.dot(s, torch.mv(L, s))
    
    # penalidade de balanceamento
    balance_penalty = torch.mean(s) ** 2
    
    return cut - 0.2 * balance_penalty


# -----------------------------
# TREINO
# -----------------------------
def train():
    N = 1000
    BATCH = 4
    EPOCHS = 200
    
    model = SparseGNN().to(device)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    
    print("\n--- TREINAMENTO ---\n")
    
    for epoch in range(EPOCHS):
        scores = []
        
        for _ in range(BATCH):
            p = np.random.choice([0.005, 0.01, 0.02])
            A = generate_sparse_graph(N, p)
            score = learned_solver(model, A)
            scores.append(score)
        
        scores = torch.stack(scores)
        
        loss = -scores.mean() + 1e-4 * torch.mean(scores**2)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if epoch % 10 == 0:
            print(f"E{epoch:3d} | Score: {scores.mean().item():.2f}")
    
    torch.save(model.state_dict(), "model_maxcut.pth")
    print("\nModelo salvo: model_maxcut.pth")


if __name__ == "__main__":
    train()