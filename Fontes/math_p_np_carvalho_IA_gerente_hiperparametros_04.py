import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------------
# 1. Gerador de grafos
# -----------------------------
def generate_graph(n):
    p = np.random.uniform(0.2, 0.7)
    A = (torch.rand(n, n, device=device) < p).float()
    A = torch.triu(A, 1)
    A = A + A.T
    return A


# -----------------------------
# 2. Dynamic GNN
# -----------------------------
class DynamicGNN(nn.Module):
    def __init__(self, dim=64):
        super().__init__()
        
        self.node_embed = nn.Linear(1, dim)
        
        self.message = nn.Sequential(
            nn.Linear(dim*2 + 1, dim),
            nn.ReLU(),
            nn.Linear(dim, dim)
        )
        
        self.update = nn.Sequential(
            nn.Linear(dim, dim),
            nn.ReLU(),
            nn.Linear(dim, 1)
        )
    
    def forward(self, x, A):
        n = x.shape[0]
        
        h = self.node_embed(x.unsqueeze(-1))  # (n, dim)
        
        h_i = h.unsqueeze(1).expand(-1, n, -1)
        h_j = h.unsqueeze(0).expand(n, -1, -1)
        
        m = torch.cat([h_i, h_j, A.unsqueeze(-1)], dim=-1)
        
        agg = self.message(m).mean(dim=1)
        
        delta = self.update(agg).squeeze()
        
        return delta


# -----------------------------
# 3. Solver aprendido (diferenciável)
# -----------------------------
def learned_solver(model, A, steps=30):
    n = A.shape[0]
    
    x = torch.randn(n, device=device)
    
    for _ in range(steps):
        delta = model(x, A)
        x = x + 0.1 * delta
        
        # estabilidade numérica
        x = torch.clamp(x, -5, 5)
    
    # relaxação contínua
    s = torch.tanh(x)
    
    D = torch.diag(A.sum(dim=1))
    L = D - A
    
    cut_cont = 0.25 * torch.dot(s, torch.mv(L, s))
    
    return cut_cont


# -----------------------------
# 4. Treinamento
# -----------------------------
N = 100
EPOCHS = 200

model = DynamicGNN().to(device)
optimizer = optim.Adam(model.parameters(), lr=1e-3)

print("\n--- TREINAMENTO DYNAMIC GNN (VERSÃO FINAL) ---\n")

for epoch in range(EPOCHS):
    
    A = generate_graph(N)
    
    cut = learned_solver(model, A, steps=30)
    
    loss = -cut  # maximizar corte
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if epoch % 20 == 0:
        print(f"E{epoch:3d} | Cut (contínuo): {cut.item():.4f}")


# -----------------------------
# 5. Avaliação final (discreta)
# -----------------------------
def evaluate_discrete(model, A, steps=30):
    n = A.shape[0]
    
    x = torch.randn(n, device=device)
    
    for _ in range(steps):
        delta = model(x, A)
        x = x + 0.1 * delta
        x = torch.clamp(x, -5, 5)
    
    s = torch.sign(torch.tanh(x)).detach()
    
    diff = (s.unsqueeze(1) != s.unsqueeze(0)).float()
    cut = torch.sum(A * diff) / 2
    
    return cut.item()


print("\n--- AVALIAÇÃO FINAL ---\n")

test_graphs = 5
results = []

for i in range(test_graphs):
    A = generate_graph(N)
    cut = evaluate_discrete(model, A)
    results.append(cut)
    print(f"Grafo {i+1}: Cut = {cut:.1f}")

print(f"\nCut médio: {np.mean(results):.2f}")