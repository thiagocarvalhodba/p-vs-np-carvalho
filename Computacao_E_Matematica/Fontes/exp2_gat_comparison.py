import torch
import torch.nn as nn
import numpy as np
import time
import json

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def generate_sparse_graph(n, p):
    A = (torch.rand(n, n, device=device) < p).float()
    A = torch.triu(A, 1)
    A = A + A.T
    return A

def count_edges(A):
    return (A.sum().item()) / 2

def cut_value(A, s):
    diff = (s.unsqueeze(1) != s.unsqueeze(0)).float()
    return (torch.sum(A * diff) / 2).item()

# 1. SparseGNN (Baseline neural sem atenção)
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
        return self.update(combined).squeeze(-1)

# 2. EdgeAttentionGNN (GAT com atenção por aresta)
class EdgeAttentionGNN(nn.Module):
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
            e = self.attn(pair).squeeze(-1)
            alpha = torch.softmax(e, dim=0)
            agg[i] = torch.sum(alpha.unsqueeze(-1) * h_j, dim=0)
        
        h_new = h + agg
        return self.update(h_new).squeeze(-1)

# Solvers
def random_solver(A):
    n = A.shape[0]
    s = torch.randint(0, 2, (n,), device=device) * 2 - 1
    return cut_value(A, s)

def greedy_solver(A, steps=3):
    n = A.shape[0]
    s = torch.randint(0, 2, (n,), device=device) * 2 - 1
    for _ in range(steps):
        for i in range(n):
            gain = torch.sum(A[i] * s[i] * s)
            if gain > 0:
                s[i] *= -1
    return cut_value(A, s)

def neural_solver(model, A, steps=20):
    n = A.shape[0]
    with torch.no_grad():
        x = torch.randn(n, device=device)
        for _ in range(steps):
            delta = model(x, A)
            x = x + 0.1 * delta
            x = torch.clamp(x, -5, 5)
        s = torch.sign(torch.tanh(x))
    return cut_value(A, s)

def run_experiment():
    print("==========================================================")
    print(" EXPERIMENTO 2: COMPARAÇÃO GAT (ATENÇÃO) VS SPARSE GNN")
    print(f" Dispositivo: {device} | Python / PyTorch")
    print("==========================================================")
    
    # Carregamento dos modelos pré-treinados
    print("\n[1/3] Carregando modelos pré-treinados...")
    sparse_model = SparseGNN().to(device)
    sparse_model.load_state_dict(torch.load("model_maxcut.pth", map_location=device, weights_only=True))
    sparse_model.eval()
    print("  -> SparseGNN (model_maxcut.pth) carregado com sucesso.")
    
    gat_model = EdgeAttentionGNN().to(device)
    gat_model.load_state_dict(torch.load("model_maxcut_gat.pth", map_location=device, weights_only=True))
    gat_model.eval()
    print("  -> EdgeAttentionGNN (model_maxcut_gat.pth) carregado com sucesso.")
    
    # Testes em diferentes escalas e densidades
    test_configs = [
        {"n": 200, "p": 0.02, "name": "N=200, p=0.02 (Esparso)"},
        {"n": 200, "p": 0.05, "name": "N=200, p=0.05 (Intermediário)"},
        {"n": 400, "p": 0.015, "name": "N=400, p=0.015 (Escala Alta)"}
    ]
    
    benchmark_results = {}
    print("\n[2/3] Executando testes comparativos com 5 grafos por configuração...")
    
    for cfg in test_configs:
        n = cfg["n"]
        p = cfg["p"]
        name = cfg["name"]
        print(f"\n--- Configuração: {name} ---")
        
        res = {
            "random": {"cuts": [], "ratios": [], "times": []},
            "greedy": {"cuts": [], "ratios": [], "times": []},
            "sparse_gnn": {"cuts": [], "ratios": [], "times": []},
            "gat_attention": {"cuts": [], "ratios": [], "times": []}
        }
        
        for g_idx in range(5):
            A = generate_sparse_graph(n, p)
            num_edges = count_edges(A)
            if num_edges == 0:
                continue
            
            # Random
            t0 = time.time()
            c_rand = random_solver(A)
            t_rand = time.time() - t0
            res["random"]["cuts"].append(c_rand)
            res["random"]["ratios"].append(c_rand / num_edges)
            res["random"]["times"].append(t_rand)
            
            # Greedy
            t0 = time.time()
            c_greedy = greedy_solver(A, steps=3)
            t_greedy = time.time() - t0
            res["greedy"]["cuts"].append(c_greedy)
            res["greedy"]["ratios"].append(c_greedy / num_edges)
            res["greedy"]["times"].append(t_greedy)
            
            # SparseGNN
            t0 = time.time()
            c_sparse = neural_solver(sparse_model, A, steps=20)
            t_sparse = time.time() - t0
            res["sparse_gnn"]["cuts"].append(c_sparse)
            res["sparse_gnn"]["ratios"].append(c_sparse / num_edges)
            res["sparse_gnn"]["times"].append(t_sparse)
            
            # GAT Attention
            t0 = time.time()
            c_gat = neural_solver(gat_model, A, steps=20)
            t_gat = time.time() - t0
            res["gat_attention"]["cuts"].append(c_gat)
            res["gat_attention"]["ratios"].append(c_gat / num_edges)
            res["gat_attention"]["times"].append(t_gat)
            
            print(f"  Grafo {g_idx+1} (|E|={num_edges:.0f}): Rand={c_rand/num_edges:.3f} | Greedy={c_greedy/num_edges:.3f} | SparseGNN={c_sparse/num_edges:.3f} | GAT={c_gat/num_edges:.3f}")
            
        summary_cfg = {}
        for solver_key, data in res.items():
            summary_cfg[solver_key] = {
                "mean_cut": float(np.mean(data["cuts"])),
                "mean_ratio": float(np.mean(data["ratios"])),
                "std_ratio": float(np.std(data["ratios"])),
                "avg_time_ms": float(np.mean(data["times"]) * 1000)
            }
        benchmark_results[name] = summary_cfg
        
    print("\n[3/3] Resumo Estatístico do Experimento 2:")
    report_lines = [
        "=== RESULTADOS: EXPERIMENTO 2 (GAT ATENÇÃO VS SPARSE GNN) ===",
        f"Data/Hora: {time.ctime()}\n"
    ]
    for cfg_name, stats in benchmark_results.items():
        block = f"Configuração: {cfg_name}\n"
        for s_name, s_vals in stats.items():
            block += f"  - {s_name.upper():14s} | Corte Ratio: {s_vals['mean_ratio']*100:.2f}% ± {s_vals['std_ratio']*100:.2f}% | Tempo Médio: {s_vals['avg_time_ms']:.2f} ms\n"
        print(block)
        report_lines.append(block)
        
    with open("exp2_gat_comparison_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
        
    with open("exp2_gat_comparison_results.json", "w", encoding="utf-8") as f:
        json.dump(benchmark_results, f, indent=2)
        
    print("Resultados salvos em exp2_gat_comparison_report.txt e exp2_gat_comparison_results.json")

if __name__ == "__main__":
    run_experiment()
