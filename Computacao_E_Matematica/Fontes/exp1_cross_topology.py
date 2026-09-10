import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import networkx as nx
import time
import json

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def generate_er_graph(n, p=0.05):
    A = (torch.rand(n, n, device=device) < p).float()
    A = torch.triu(A, 1)
    A = A + A.T
    return A

def generate_ws_graph(n, k=10, p=0.1):
    G = nx.watts_strogatz_graph(n, k, p)
    adj = nx.to_numpy_array(G)
    return torch.tensor(adj, dtype=torch.float32, device=device)

def generate_ba_graph(n, m=5):
    G = nx.barabasi_albert_graph(n, m)
    adj = nx.to_numpy_array(G)
    return torch.tensor(adj, dtype=torch.float32, device=device)

def get_cut_value(A, s_bin):
    diff = (s_bin.unsqueeze(1) != s_bin.unsqueeze(0)).float()
    return (torch.sum(A * diff) / 2).item()

def solve_managed(A, lr, steps, noise_level, restarts=1):
    n = A.shape[0]
    D = torch.diag(A.sum(dim=1))
    L = D - A
    best_cut = 0.0
    
    with torch.enable_grad():
        for _ in range(restarts):
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
            best_cut = max(best_cut, get_cut_value(A, s_final))
    return best_cut

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
    print(" EXPERIMENTO 1: GENERALIZAÇÃO CROSS-TOPOLOGY (ZERO-SHOT)")
    print(f" Dispositivo: {device} | Python / PyTorch")
    print("==========================================================")
    
    N_NODES = 200
    model = MetaGNN().to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    print(f"\n[1/3] Treinando MetaGNN em Erdos-Renyi (N={N_NODES}, 25 épocas)...")
    start_train = time.time()
    for epoch in range(1, 26):
        p_train = np.random.uniform(0.03, 0.08)
        A = generate_er_graph(N_NODES, p_train)
        strategy = model(A)
        
        ia_steps = int(80 + strategy[0].item() * 150)
        ia_noise = 0.01 + strategy[1].item() * 0.03
        ia_lr    = 0.01 + strategy[2].item() * 0.04
        
        cut_base = solve_managed(A, lr=0.04, steps=100, noise_level=0.03)
        cut_ia   = solve_managed(A, lr=ia_lr, steps=ia_steps, noise_level=ia_noise)
        
        gain = cut_ia - cut_base
        reward = gain / N_NODES
        complexity_penalty = 0.05 * torch.mean(strategy**2)
        loss_meta = -reward * torch.sum(torch.log(strategy + 1e-6)) + complexity_penalty
        
        optimizer.zero_grad()
        loss_meta.backward()
        optimizer.step()
        
        if epoch % 5 == 0 or epoch == 25:
            print(f"  Ep {epoch:2d} | Gain: {gain:+6.1f} | Steps: {ia_steps:3d} | Noise: {ia_noise:.3f} | LR: {ia_lr:.3f}")
    
    print(f"Treinamento concluído em {time.time() - start_train:.1f}s.")
    
    print("\n[2/3] Avaliando Generalização Zero-Shot em 3 Famílias Topológicas...")
    topologies = {
        "Erdos-Renyi (Uniforme)": lambda: generate_er_graph(N_NODES, p=0.05),
        "Watts-Strogatz (Small-World)": lambda: generate_ws_graph(N_NODES, k=10, p=0.1),
        "Barabási-Albert (Scale-Free)": lambda: generate_ba_graph(N_NODES, m=5)
    }
    
    results = {}
    
    for name, gen_fn in topologies.items():
        print(f"\n--- Topologia: {name} ---")
        gains = []
        cuts_base = []
        cuts_ia = []
        cut_ratios_base = []
        cut_ratios_ia = []
        strategies = []
        
        for trial in range(5):
            A = gen_fn()
            num_edges = A.sum().item() / 2
            if num_edges == 0:
                continue
            
            with torch.no_grad():
                strat = model(A)
                ia_steps = int(80 + strat[0].item() * 150)
                ia_noise = 0.01 + strat[1].item() * 0.03
                ia_lr    = 0.01 + strat[2].item() * 0.04
            
            cb = solve_managed(A, lr=0.04, steps=100, noise_level=0.03)
            cia = solve_managed(A, lr=ia_lr, steps=ia_steps, noise_level=ia_noise)
            
            gain = cia - cb
            gains.append(gain)
            cuts_base.append(cb)
            cuts_ia.append(cia)
            cut_ratios_base.append(cb / num_edges)
            cut_ratios_ia.append(cia / num_edges)
            strategies.append({"steps": ia_steps, "noise": ia_noise, "lr": ia_lr})
            
            print(f"  Instância {trial+1}: Arestas={num_edges:.0f} | Base={cb:.1f} ({cb/num_edges:.3f}) | IA={cia:.1f} ({cia/num_edges:.3f}) | Ganho={gain:+5.1f} | Params: (S={ia_steps}, N={ia_noise:.3f}, LR={ia_lr:.3f})")
            
        results[name] = {
            "mean_gain": float(np.mean(gains)),
            "std_gain": float(np.std(gains)),
            "mean_cut_base": float(np.mean(cuts_base)),
            "mean_cut_ia": float(np.mean(cuts_ia)),
            "mean_ratio_base": float(np.mean(cut_ratios_base)),
            "mean_ratio_ia": float(np.mean(cut_ratios_ia)),
            "mean_steps": float(np.mean([s["steps"] for s in strategies])),
            "mean_noise": float(np.mean([s["noise"] for s in strategies])),
            "mean_lr": float(np.mean([s["lr"] for s in strategies]))
        }
        
    print("\n[3/3] Resumo Final de Generalização Cross-Topology:")
    report_lines = [
        "=== RESULTADOS: EXPERIMENTO 1 (CROSS-TOPOLOGY) ===",
        f"Data/Hora: {time.ctime()}",
        f"N={N_NODES} nós | Instâncias por Topologia: 5\n"
    ]
    for topo, stats in results.items():
        summary = (
            f"Topologia: {topo}\n"
            f"  - Ganho Médio IA vs Base: {stats['mean_gain']:+.2f} ± {stats['std_gain']:.2f}\n"
            f"  - Ratio Médio de Corte Base: {stats['mean_ratio_base']*100:.2f}%\n"
            f"  - Ratio Médio de Corte IA:   {stats['mean_ratio_ia']*100:.2f}%\n"
            f"  - Estratégia Média Predita: Steps={stats['mean_steps']:.1f}, Noise={stats['mean_noise']:.4f}, LR={stats['mean_lr']:.4f}\n"
        )
        print(summary)
        report_lines.append(summary)
        
    with open("exp1_cross_topology_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
        
    with open("exp1_cross_topology_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print("Relatório salvo em exp1_cross_topology_report.txt e exp1_cross_topology_results.json")

if __name__ == "__main__":
    run_experiment()
