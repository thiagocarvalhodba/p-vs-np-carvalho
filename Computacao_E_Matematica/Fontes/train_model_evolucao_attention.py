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
# GRAPH ATTENTION (SPARSE)
# -----------------------------
class SparseGAT(nn.Module):
    def __init__(self, dim=64):
        super().__init__()
        
        self.embed = nn.Linear(1, dim)
        
        self.attn = nn.Linear(dim * 2, 1)
        self.update = nn.Sequential(
            nn.Linear(dim, dim),
            nn.ReLU(),
            nn.Linear(dim, 1)
        )
    
    def forward(self, x, A):
        n = x.shape[0]
        
        h = self.embed(x.unsqueeze(-1))  # (n, dim)
        
        # expandir pares
        h_i = h.unsqueeze(1).expand(-1, n, -1)
        h_j = h.unsqueeze(0).expand(n, -1, -1)
        
        # concatenação
        pair = torch.cat([h_i, h_j], dim=-1)
        
        # atenção bruta
        e = self.attn(pair).squeeze(-1)
        
        # mascarar onde não há aresta
        e = e.masked_fill(A == 0, -1e9)
        
        # softmax por linha
        alpha = torch.softmax(e, dim=1)
        
        # agregação ponderada
        agg = torch.matmul(alpha, h)
        
        # update
        delta = self.update(agg).squeeze()
        
        return delta


# -----------------------------
# SOLVER
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
    
    balance_penalty = torch.mean(s) ** 2
    
    return cut - 0.2 * balance_penalty


# -----------------------------
# TREINO
# -----------------------------
def train():
    N = 1000
    BATCH = 2   # ⚠️ menor por custo maior
    EPOCHS = 150
    
    model = SparseGAT().to(device)
    optimizer = optim.Adam(model.parameters(), lr=5e-4)
    
    print("\n--- TREINAMENTO GAT ---\n")
    
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
    
    torch.save(model.state_dict(), "model_maxcut_gat.pth")
    print("\nModelo salvo: model_maxcut_gat.pth")


if __name__ == "__main__":
    train()