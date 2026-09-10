import torch
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------------
# 1. Grafo
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
# 2. RANDOM
# -----------------------------
def random_solver(A):
    n = A.shape[0]
    s = torch.randint(0, 2, (n,), device=device) * 2 - 1
    return cut_value(A, s).item()


# -----------------------------
# 3. GREEDY (local search)
# -----------------------------
def greedy_solver(A, steps=5):
    n = A.shape[0]
    s = torch.randint(0, 2, (n,), device=device) * 2 - 1
    
    for _ in range(steps):
        for i in range(n):
            gain = 0
            for j in range(n):
                if A[i, j] > 0:
                    gain += A[i, j] * s[i] * s[j]
            
            if gain > 0:
                s[i] *= -1
    
    return cut_value(A, s).item()


# -----------------------------
# 4. SEU MODELO
# -----------------------------
def neural_solver(model, A, steps=20):
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
# 5. BENCHMARK
# -----------------------------
def run_benchmark(model, n=1000, ps=[0.005, 0.01, 0.02], graphs_per_setting=5):
    
    print("\n=== BENCHMARK MAX-CUT ===\n")
    
    for p in ps:
        results = {
            "random": [],
            "greedy": [],
            "neural": []
        }
        
        for _ in range(graphs_per_setting):
            A = generate_sparse_graph(n, p)
            edges = count_edges(A)
            
            r = random_solver(A)
            g = greedy_solver(A)
            nn = neural_solver(model, A)
            
            results["random"].append(r / edges)
            results["greedy"].append(g / edges)
            results["neural"].append(nn / edges)
        
        print(f"\n--- p = {p} ---")
        
        for k in results:
            mean = np.mean(results[k])
            std = np.std(results[k])
            
            print(f"{k.upper():7s} | mean: {mean:.4f} | std: {std:.4f}")

run_benchmark(model)