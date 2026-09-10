import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# -----------------------------
# Configuração
# -----------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------------
# 1. Grafo
# -----------------------------
def generate_sparse_graph(n, p=0.01):
    A = (torch.rand(n, n, device=device) < p).float()
    A = torch.triu(A, 1)
    A = A + A.T
    return A


# -----------------------------
# 2. GNN
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
        
        # agregação eficiente
        agg = torch.matmul(A, h)
        
        combined = torch.cat([h, agg], dim=-1)
        
        delta = self.update(combined).squeeze()
        
        return delta


# -----------------------------
# 3. Solver com regularização
# -----------------------------
def learned_solver(model, A, steps=20):
    n = A.shape[0]
    
    x = torch.randn(n, device=device)
    
    for _ in range(steps):
        delta = model(x, A)
        
        # dinâmica com amortecimento (evita explosão)
        x = x + 0.1 * delta
        
        # estabilidade
        x = torch.clamp(x, -5, 5)
    
    s = torch.tanh(x)
    
    # Laplaciano
    D = torch.diag(A.sum(dim=1))
    L = D - A
    
    cut = 0.25 * torch.dot(s, torch.mv(L, s))
    
    # 🔥 PENALIDADE DE BALANCEAMENTO (CRÍTICO)
    balance = torch.mean(s)
    balance_penalty = balance ** 2
    
    # 🔥 LOSS FINAL DO SOLVER
    score = cut - 0.2 * balance_penalty
    
    return score


# -----------------------------
# 4. Treinamento
# -----------------------------
def train():
    N = 1000
    BATCH = 4
    EPOCHS = 200
    
    model = SparseGNN().to(device)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    
    print("\n--- TREINAMENTO ESTÁVEL + BALANCEADO ---\n")
    
    for epoch in range(EPOCHS):
        
        scores = []
        
        for _ in range(BATCH):
            # 🔥 mistura de densidades (generalização melhor)
            p = np.random.choice([0.005, 0.01, 0.02])
            A = generate_sparse_graph(N, p)
            
            score = learned_solver(model, A, steps=20)
            scores.append(score)
        
        scores_tensor = torch.stack(scores)
        
        mean_score = scores_tensor.mean()
        
        # regularização leve
        reg = 1e-4 * torch.mean(scores_tensor**2)
        
        loss = -mean_score + reg
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if epoch % 10 == 0:
            print(f"E{epoch:3d} | Score: {mean_score.item():.2f}")
    
    # -----------------------------
    # Salvar modelo
    # -----------------------------
    torch.save(model.state_dict(), "model_maxcut.pth")
    
    print("\nModelo salvo como: model_maxcut.pth")


# -----------------------------
# Execução
# -----------------------------
if __name__ == "__main__":
    train()