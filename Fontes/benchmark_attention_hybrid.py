import torch
import torch.nn as nn
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

def count_edges(A):
    return A.sum().item() / 2

def cut_value(A, s):
    diff = (s.unsqueeze(1) != s.unsqueeze(0)).float()
    return torch.sum(A * diff) / 2


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
            
            if len(neighbors) == 0:
                continue
            
            h_i = h[i].repeat(len(neighbors), 1)
            h_j = h[neighbors]
            
            pair = torch.cat([h_i, h_j], dim=1)
            
            e = self.attn(pair).squeeze()
            alpha = torch.softmax(e, dim=0)
            
            agg[i] = torch.sum(alpha.unsqueeze(-1) * h_j, dim=0)
        
        # residual connection
        h_new = h + agg
        
        delta = self.update(h_new).squeeze()
        
        return delta


# -----------------------------
# RANDOM
# -----------------------------
def random_solver(A):
    n = A.shape[0]
    s = torch.randint(0, 2, (n,), device=device) * 2 - 1
    return cut_value(A, s).item()


# -----------------------------
# GREEDY
# -----------------------------
def greedy_solver(A, steps=3):
    n = A.shape[0]
    s = torch.randint(0, 2, (n,), device=device) * 2 - 1
    
    for _ in range(steps):
        for i in range(n):
            gain = torch.sum(A[i] * s[i] * s)
            if gain > 0:
                s[i] *= -1
    
    return cut_value(A, s).item()


# -----------------------------
# ATTENTION SOLVER
# -----------------------------
def attention_solver(model, A, steps=30):
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
# HYBRID (ATTENTION + GREEDY)
# -----------------------------
def hybrid_solver(model, A, steps=30, greedy_steps=2):
    n = A.shape[0]
    
    with torch.no_grad():
        x = torch.randn(n, device=device)
        
        for _ in range(steps):
            delta = model(x, A)
            x = x + 0.1 * delta
            x = torch.clamp(x, -5, 5)
        
        s = torch.sign(torch.tanh(x))
    
    # refinamento greedy
    for _ in range(greedy_steps):
        for i in range(n):
            gain = torch.sum(A[i] * s[i] * s)
            if gain > 0:
                s[i] *= -1
    
    return cut_value(A, s).item()


# -----------------------------
# BENCHMARK
# -----------------------------
def run_benchmark(model, n=1000, ps=[0.005, 0.01, 0.02], graphs=3):
    
    print("\n=== BENCHMARK ATTENTION + HYBRID ===\n")
    
    for p in ps:
        results = {
            "random": [],
            "greedy": [],
            "attention": [],
            "hybrid": []
        }
        
        for _ in range(graphs):
            A = generate_sparse_graph(n, p)
            edges = count_edges(A)
            
            r = random_solver(A)
            g = greedy_solver(A)
            att = attention_solver(model, A)
            h = hybrid_solver(model, A)
            
            results["random"].append(r / edges)
            results["greedy"].append(g / edges)
            results["attention"].append(att / edges)
            results["hybrid"].append(h / edges)
        
        print(f"\n--- p = {p} ---")
        
        for k in results:
            mean = np.mean(results[k])
            std = np.std(results[k])
            print(f"{k.upper():10s} | mean: {mean:.4f} | std: {std:.4f}")


# -----------------------------
# EXECUÇÃO
# -----------------------------
if __name__ == "__main__":
    
    model = EdgeAttentionGNN().to(device)
    
    # ⚠️ IMPORTANTE:
    # Se você treinou outro modelo, esse NÃO vai carregar corretamente.                  benchmark_attention_hybrid
    # Esse arquivo serve para testar a nova arquitetura.
    
    print("\n⚠️ Rodando modelo NÃO treinado (baseline attention)\n")
    
    run_benchmark(model)