import torch
import torch.nn as nn
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------------
# GAT (mesma arquitetura)
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
        
        h = self.embed(x.unsqueeze(-1))
        
        h_i = h.unsqueeze(1).expand(-1, n, -1)
        h_j = h.unsqueeze(0).expand(n, -1, -1)
        
        pair = torch.cat([h_i, h_j], dim=-1)
        
        e = self.attn(pair).squeeze(-1)
        e = e.masked_fill(A == 0, -1e9)
        
        alpha = torch.softmax(e, dim=1)
        agg = torch.matmul(alpha, h)
        
        return self.update(agg).squeeze()


# -----------------------------
# UTIL
# -----------------------------
def generate_sparse_graph(n, p):
    A = (torch.rand(n, n, device=device) < p).float()
    A = torch.triu(A, 1)
    A = A + A.T
    return A

def cut_value(A, s):
    diff = (s.unsqueeze(1) != s.unsqueeze(0)).float()
    return torch.sum(A * diff) / 2

def count_edges(A):
    return A.sum().item() / 2


# -----------------------------
# SOLVER GAT
# -----------------------------
def gat_solver(model, A, steps=20):
    n = A.shape[0]
    
    with torch.no_grad():
        x = torch.randn(n, device=device)
        
        for _ in range(steps):
            delta = model(x, A)
            x = x + 0.1 * delta
            x = torch.clamp(x, -5, 5)
        
        s = torch.sign(torch.tanh(x))
    
    return cut_value(A, s).item()


# -----------------------------
# BENCHMARK
# -----------------------------
def run():
    model = SparseGAT().to(device)
    model.load_state_dict(torch.load("model_maxcut_gat.pth", map_location=device))
    model.eval()
    
    print("\n=== BENCHMARK GAT ===\n")
    
    for p in [0.005, 0.01, 0.02]:
        results = []
        
        for _ in range(5):
            A = generate_sparse_graph(1000, p)
            edges = count_edges(A)
            
            val = gat_solver(model, A)
            results.append(val / edges)
        
        print(f"p={p} | mean={np.mean(results):.4f} | std={np.std(results):.4f}")


run()