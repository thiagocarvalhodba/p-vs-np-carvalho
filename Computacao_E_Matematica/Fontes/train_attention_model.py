import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------------
# GRAFO
# -----------------------------
def generate_sparse_graph(n, p):
    A = (torch.rand(n, n, device=device) < p).float()
    A = torch.triu(A, 1)
    A = A + A.T
    return A


# -----------------------------
# EDGE ATTENTION GNN (SPARSE REAL)
# -----------------------------
class EdgeAttentionGNN(nn.Module):
    def __init__(self, dim=64):
        super().__init__()
        
        self.embed = nn.Linear(1, dim)
        
        self.attn = nn.Sequential(
            nn.Linear(dim * 2, dim),
            nn.ReLU(),
            nn.Linear(dim, 1)
        )
        
        self.update = nn.Sequential(
            nn.Linear(dim, dim),
            nn.ReLU(),
            nn.Linear(dim, 1)
        )
    
    def forward(self, x, A):
        h = self.embed(x.unsqueeze(-1))
        
        n = h.shape[0]
        agg = torch.zeros_like(h)
        
        for i in range(n):
            neighbors = torch.where(A[i] > 0)[0]
            
            if neighbors.numel() == 0:
                continue
            
            h_i = h[i].repeat(neighbors.shape[0], 1)
            h_j = h[neighbors]
            
            pair = torch.cat([h_i, h_j], dim=1)
            
            e = self.attn(pair).squeeze()
            alpha = torch.softmax(e, dim=0)
            
            agg[i] = torch.sum(alpha.unsqueeze(-1) * h_j, dim=0)
        
        # residual
        h_new = h + agg
        
        delta = self.update(h_new).squeeze()
        
        return delta


# -----------------------------
# SOLVER (COM BALANCEAMENTO)
# -----------------------------
def learned_solver(model, A, steps=30):
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
# TREINAMENTO
# -----------------------------
def train():
    N = 1000
    BATCH = 2              # menor por custo maior
    EPOCHS = 120
    LR = 5e-4
    
    model = EdgeAttentionGNN().to(device)
    optimizer = optim.Adam(model.parameters(), lr=LR)
    
    print("\n--- TREINAMENTO EDGE ATTENTION (SPARSE REAL) ---\n")
    
    for epoch in range(EPOCHS):
        
        scores = []
        
        for _ in range(BATCH):
            p = np.random.choice([0.005, 0.01, 0.02])
            A = generate_sparse_graph(N, p)
            
            score = learned_solver(model, A)
            scores.append(score)
        
        scores = torch.stack(scores)
        
        mean_score = scores.mean()
        
        # regularização leve
        reg = 1e-4 * torch.mean(scores**2)
        
        loss = -mean_score + reg
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if epoch % 10 == 0:
            print(f"E{epoch:3d} | Score: {mean_score.item():.2f}")
    
    # salvar modelo
    torch.save(model.state_dict(), "model_maxcut_attention.pth")
    
    print("\nModelo salvo: model_maxcut_attention.pth")


# -----------------------------
# EXECUÇÃO
# -----------------------------
if __name__ == "__main__":
    train()