import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------------
# 1. Grafo esparso
# -----------------------------
def generate_sparse_graph(n, p=0.01):
    A = (torch.rand(n, n, device=device) < p).float()
    A = torch.triu(A, 1)
    A = A + A.T
    return A


# -----------------------------
# 2. GNN Sparse (rápida)
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
        h = self.embed(x.unsqueeze(-1))   # (n, dim)
        
        # agregação eficiente (sparse-like)
        agg = torch.matmul(A, h)          # (n, dim)
        
        combined = torch.cat([h, agg], dim=-1)
        
        delta = self.update(combined).squeeze()
        
        return delta


# -----------------------------
# 3. Solver contínuo
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
    
    return cut


# -----------------------------
# 4. Treinamento com batch
# -----------------------------
N = 1000
BATCH = 4
EPOCHS = 200

model = SparseGNN().to(device)
optimizer = optim.Adam(model.parameters(), lr=1e-3)

print("\n--- TREINAMENTO SPARSE + BATCH ---\n")

for epoch in range(EPOCHS):
    
    cuts = []
    
    for _ in range(BATCH):
        A = generate_sparse_graph(N, p=0.01)
        cut = learned_solver(model, A, steps=20)
        cuts.append(cut)
    
    cuts_tensor = torch.stack(cuts)
    
    mean_cut = cuts_tensor.mean()
    
    # regularização leve (estabilidade)
    reg = 1e-4 * torch.mean(cuts_tensor**2)
    
    loss = -mean_cut + reg
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if epoch % 10 == 0:
        print(f"E{epoch:3d} | Mean Cut: {mean_cut.item():.2f}")


# -----------------------------
# 5. Avaliação final
# -----------------------------
def evaluate(model, n=1000):
    A = generate_sparse_graph(n, p=0.01)
    
    with torch.no_grad():
        x = torch.randn(n, device=device)
        
        for _ in range(20):
            delta = model(x, A)
            x = x + 0.1 * delta
            x = torch.clamp(x, -5, 5)
        
        s = torch.sign(torch.tanh(x))
        
        diff = (s.unsqueeze(1) != s.unsqueeze(0)).float()
        cut = torch.sum(A * diff) / 2
    
    return cut.item()


print("\n--- AVALIAÇÃO ---\n")

results = []
for i in range(3):
    c = evaluate(model)
    results.append(c)
    print(f"Grafo {i+1}: Cut = {c:.1f}")

print(f"\nMédia: {np.mean(results):.1f}")