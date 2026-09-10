import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import time
import json

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def generate_graph(n, p):
    A = (torch.rand(n, n, device=device) < p).float()
    A = torch.triu(A, 1)
    A = A + A.T
    return A

def count_edges(A):
    return (A.sum().item()) / 2

def get_cut_value(A, s_bin):
    diff = (s_bin.unsqueeze(1) != s_bin.unsqueeze(0)).float()
    return (torch.sum(A * diff) / 2).item()

# 1. Random Solver
def random_solver(A):
    n = A.shape[0]
    s = torch.randint(0, 2, (n,), device=device) * 2 - 1
    return get_cut_value(A, s)

# 2. Greedy Solver
def greedy_solver(A, steps=5):
    n = A.shape[0]
    s = torch.randint(0, 2, (n,), device=device) * 2 - 1
    for _ in range(steps):
        for i in range(n):
            gain = torch.sum(A[i] * s[i] * s)
            if gain > 0:
                s[i] *= -1
    return get_cut_value(A, s)

# 3. Continuous Laplacian Solver
def solve_continuous(A, lr, steps, noise_level):
    n = A.shape[0]
    D = torch.diag(A.sum(dim=1))
    L = D - A
    
    with torch.enable_grad():
        x = torch.randn(n, device=device).detach().requires_grad_(True)
        optimizer = torch.optim.Adam([x], lr=lr)
        for t in range(steps):
            s = torch.tanh(x)
            cut_cont = 0.25 * torch.dot(s, torch.mv(L, s))
            loss = -cut_cont
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            with torch.no_grad():
                x.data.add_(noise_level * (1 - t/steps) * torch.randn_like(x))
        
        s_final = torch.sign(torch.tanh(x)).detach()
        return get_cut_value(A, s_final)

# 4. MetaGNN
class MetaGNN(nn.Module):
    def __init__(self, dim=64):
        super().__init__()
        self.node_init = nn.Linear(1, dim)
        self.message_mlp = nn.Sequential(
            nn.Linear(dim*2+1, dim), nn.ReLU(), nn.Linear(dim, dim)
        )
        self.strategy_head = nn.Sequential(
            nn.Linear(dim, 32),
            nn.ReLU(),
            nn.Linear(32, 3),
            nn.Sigmoid()
        )
    
    def forward(self, A):
        n = A.shape[0]
        h = self.node_init(torch.ones(n, 1, device=device))
        for _ in range(3):
            h_i = h.unsqueeze(1).expand(-1, n, -1)
            h_j = h.unsqueeze(0).expand(n, -1, -1)
            combined = torch.cat([h_i, h_j, A.unsqueeze(-1)], dim=-1)
            h = h + self.message_mlp(combined).mean(dim=1)
        return self.strategy_head(h.mean(dim=0))

def run_experiment():
    print("==========================================================")
    print(" EXPERIMENTO 3: BENCHMARK ESTATÍSTICO COMPLETO DE SOLVERS")
    print(f" Dispositivo: {device} | Python / PyTorch")
    print("==========================================================")
    
    # Treina uma instância da MetaGNN para o benchmark
    print("\n[1/3] Treinamento rápido da MetaGNN (N=150, 20 épocas)...")
    model = MetaGNN().to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    for epoch in range(1, 21):
        A_train = generate_graph(150, np.random.uniform(0.03, 0.08))
        strat = model(A_train)
        ia_steps = int(80 + strat[0].item() * 150)
        ia_noise = 0.01 + strat[1].item() * 0.03
        ia_lr    = 0.01 + strat[2].item() * 0.04
        
        cb = solve_continuous(A_train, lr=0.04, steps=100, noise_level=0.03)
        cia = solve_continuous(A_train, lr=ia_lr, steps=ia_steps, noise_level=ia_noise)
        
        gain = cia - cb
        reward = gain / 150.0
        loss = -reward * torch.sum(torch.log(strat + 1e-6)) + 0.05 * torch.mean(strat**2)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print("  -> MetaGNN pronta para benchmark.")
    
    # Baterias de testes
    test_cases = [
        {"n": 100, "p": 0.05, "name": "N=100, p=0.05"},
        {"n": 200, "p": 0.03, "name": "N=200, p=0.03"},
        {"n": 300, "p": 0.02, "name": "N=300, p=0.02"}
    ]
    
    print("\n[2/3] Executando bateria estatística (6 grafos por escala)...")
    benchmark_data = {}
    
    for tc in test_cases:
        n = tc["n"]
        p = tc["p"]
        name = tc["name"]
        print(f"\n--- Bateria: {name} ---")
        
        records = {
            "random": [],
            "greedy": [],
            "base_laplacian": [],
            "metagnn_managed": [],
            "gains_ia": []
        }
        
        for g_idx in range(6):
            A = generate_graph(n, p)
            num_edges = count_edges(A)
            if num_edges == 0:
                continue
            
            c_rnd = random_solver(A)
            c_grd = greedy_solver(A, steps=4)
            c_base = solve_continuous(A, lr=0.04, steps=100, noise_level=0.03)
            
            with torch.no_grad():
                strat = model(A)
                ia_steps = int(80 + strat[0].item() * 150)
                ia_noise = 0.01 + strat[1].item() * 0.03
                ia_lr    = 0.01 + strat[2].item() * 0.04
            
            c_ia = solve_continuous(A, lr=ia_lr, steps=ia_steps, noise_level=ia_noise)
            gain = c_ia - c_base
            
            records["random"].append(c_rnd / num_edges)
            records["greedy"].append(c_grd / num_edges)
            records["base_laplacian"].append(c_base / num_edges)
            records["metagnn_managed"].append(c_ia / num_edges)
            records["gains_ia"].append(gain)
            
            print(f"  Instância {g_idx+1} (|E|={num_edges:.0f}): Random={c_rnd/num_edges:.3f} | Greedy={c_grd/num_edges:.3f} | Base={c_base/num_edges:.3f} | MetaGNN={c_ia/num_edges:.3f} | Ganho={gain:+5.1f}")
            
        benchmark_data[name] = {
            "random_mean_ratio": float(np.mean(records["random"])),
            "greedy_mean_ratio": float(np.mean(records["greedy"])),
            "base_mean_ratio": float(np.mean(records["base_laplacian"])),
            "metagnn_mean_ratio": float(np.mean(records["metagnn_managed"])),
            "metagnn_mean_gain": float(np.mean(records["gains_ia"])),
            "metagnn_win_rate": float(np.mean([1 if g > 0 else 0 for g in records["gains_ia"]])) * 100
        }
        
    print("\n[3/3] Relatório Consolidado do Benchmark:")
    report_lines = [
        "=== RESULTADOS: EXPERIMENTO 3 (BENCHMARK ESTATÍSTICO) ===",
        f"Data/Hora: {time.ctime()}\n"
    ]
    for tc_name, metrics in benchmark_data.items():
        summary = (
            f"Cenário: {tc_name}\n"
            f"  - Random:            {metrics['random_mean_ratio']*100:.2f}%\n"
            f"  - Greedy:            {metrics['greedy_mean_ratio']*100:.2f}%\n"
            f"  - Base Laplaciano:   {metrics['base_mean_ratio']*100:.2f}%\n"
            f"  - MetaGNN Carvalho:  {metrics['metagnn_mean_ratio']*100:.2f}%\n"
            f"  - Ganho Médio da IA: {metrics['metagnn_mean_gain']:+.2f} arestas\n"
            f"  - Taxa de Vitória IA vs Base: {metrics['metagnn_win_rate']:.1f}%\n"
        )
        print(summary)
        report_lines.append(summary)
        
    with open("exp3_benchmark_solvers_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
        
    with open("exp3_benchmark_solvers_results.json", "w", encoding="utf-8") as f:
        json.dump(benchmark_data, f, indent=2)
        
    print("Resultados salvos em exp3_benchmark_solvers_report.txt e exp3_benchmark_solvers_results.json")

if __name__ == "__main__":
    run_experiment()
