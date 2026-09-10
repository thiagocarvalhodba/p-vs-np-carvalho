import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import torch
import torch.nn as nn
import numpy as np
import time
import json
import gc

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -------------------------------------------------------------
# 1. GERADOR ESPARSO DE GRAFOS GIGANTES (LISTA DE ARESTAS)
# -------------------------------------------------------------
def generate_huge_sparse_graph(n, avg_degree=8):
    # Gera arestas sem alocar matriz N x N (Zero Memory Overhead)
    m_target = int((n * avg_degree) / 2)
    u = np.random.randint(0, n, size=m_target)
    v = np.random.randint(0, n, size=m_target)
    
    # Remove auto-laços
    mask = u != v
    u, v = u[mask], v[mask]
    
    # Torna não direcionado
    src = np.concatenate([u, v])
    dst = np.concatenate([v, u])
    
    # Remove arestas duplicadas
    edges = set()
    unique_src, unique_dst = [], []
    for s, d in zip(src, dst):
        if (s, d) not in edges:
            edges.add((s, d))
            unique_src.append(s)
            unique_dst.append(d)
            
    src_t = torch.tensor(unique_src, dtype=torch.long, device=device)
    dst_t = torch.tensor(unique_dst, dtype=torch.long, device=device)
    num_edges = len(unique_src) // 2
    return src_t, dst_t, num_edges

def compute_sparse_cut(s_bin, src, dst):
    # s_bin: vetor {-1, +1} de tamanho N
    diff = (s_bin[src] != s_bin[dst]).float()
    return (diff.sum() / 4.0).item() # dividido por 4 pois cada aresta aparece 2x (ida e volta)

# -------------------------------------------------------------
# 2. SOLVERS ESCALÁVEIS (RANDOM & GREEDY ESPARSO)
# -------------------------------------------------------------
def random_sparse_solver(n, src, dst):
    s = torch.randint(0, 2, (n,), device=device) * 2 - 1
    return compute_sparse_cut(s, src, dst)

def greedy_sparse_solver(n, src, dst, steps=2):
    s = torch.randint(0, 2, (n,), device=device) * 2 - 1
    # Grau por vértice
    degree = torch.zeros(n, device=device)
    degree.index_add_(0, src, torch.ones_like(src, dtype=torch.float32))
    
    for _ in range(steps):
        # Conexões com o mesmo sinal
        same_signal = (s[src] == s[dst]).float()
        internal_edges = torch.zeros(n, device=device)
        internal_edges.index_add_(0, src, same_signal)
        
        # Se mais da metade dos vizinhos têm o mesmo sinal, inverte
        flip_mask = internal_edges > (degree / 2.0)
        s[flip_mask] *= -1
        
    return compute_sparse_cut(s, src, dst)

# -------------------------------------------------------------
# 3. SOLVER CONTÍNUO LAPLACIANO ESPARSO (CARVALHO O(E))
# -------------------------------------------------------------
def solve_laplacian_sparse(n, src, dst, lr, steps, noise):
    x = torch.randn(n, device=device, requires_grad=True)
    optimizer = torch.optim.Adam([x], lr=lr)
    
    for t in range(steps):
        s = torch.tanh(x)
        # Perda de corte estritamente sobre arestas: -0.25 * sum (1 - s_u * s_v)
        # Minimizar: 0.25 * sum(s_u * s_v)
        loss = 0.25 * torch.sum(s[src] * s[dst]) / 2.0
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        with torch.no_grad():
            x.data.add_(noise * (1.0 - t/steps) * torch.randn_like(x))
            
    with torch.no_grad():
        s_final = torch.sign(torch.tanh(x))
        return compute_sparse_cut(s_final, src, dst)

# -------------------------------------------------------------
# 4. SparseMetaGNN COM INDEX_ADD NATIVO (O(V + E))
# -------------------------------------------------------------
class SparseMetaGNN(nn.Module):
    def __init__(self, d_model=32):
        super().__init__()
        self.node_embed = nn.Linear(1, d_model)
        self.msg_mlp = nn.Sequential(
            nn.Linear(d_model * 2, d_model),
            nn.ReLU(),
            nn.Linear(d_model, d_model)
        )
        self.head = nn.Sequential(
            nn.Linear(d_model, 16),
            nn.ReLU(),
            nn.Linear(16, 3),
            nn.Sigmoid()
        )
        
    def forward(self, n, src, dst):
        h = self.node_embed(torch.ones(n, 1, device=device))
        
        # 2 passagens de mensagem ultrarrápidas
        for _ in range(2):
            msg = self.msg_mlp(torch.cat([h[src], h[dst]], dim=-1))
            agg = torch.zeros_like(h)
            agg.index_add_(0, src, msg)
            h = h + agg
            
        pooled = h.mean(dim=0)
        return self.head(pooled)

def run_experiment():
    print("==================================================================")
    print(" OPÇÃO 3: ESCALAÇÃO EXTREMA PARA GRAFOS GIGANTES (N=2000 A 10000)")
    print(" Complexidade: Estritamente Linear O(|E|) | Zero Matrix Allocation")
    print(f" Dispositivo: {device} | Python / PyTorch")
    print("==================================================================")
    
    # Inicialização da SparseMetaGNN
    print("\n[1/3] Inicializando SparseMetaGNN para grafos massivos...")
    model = SparseMetaGNN(d_model=32).to(device)
    model.eval()
    
    test_scales = [
        {"n": 2000,  "deg": 8, "label": "N=2.000 nós (Espaço 10^602)"},
        {"n": 5000,  "deg": 8, "label": "N=5.000 nós (Espaço 10^1505)"},
        {"n": 10000, "deg": 8, "label": "N=10.000 nós (Espaço 10^3010)"}
    ]
    
    results = {}
    print("\n[2/3] Executando benchmark em escalas gigantes (3 instâncias por escala)...")
    
    for sc in test_scales:
        n = sc["n"]
        deg = sc["deg"]
        label = sc["label"]
        print(f"\n--- Escala: {label} ---")
        
        r_rands = []
        r_greedys = []
        r_carvalhos = []
        t_carvalhos = []
        memories_mb = []
        
        for trial in range(3):
            gc.collect()
            t0_gen = time.time()
            src, dst, num_edges = generate_huge_sparse_graph(n, avg_degree=deg)
            t_gen = time.time() - t0_gen
            
            # Estimativa de memória do grafo
            mem_bytes = (src.element_size() * src.nelement() * 2) + (n * 4)
            mem_mb = mem_bytes / (1024 * 1024)
            memories_mb.append(mem_mb)
            
            # 1. Random Solver
            c_rand = random_sparse_solver(n, src, dst)
            r_rand = c_rand / num_edges
            r_rands.append(r_rand)
            
            # 2. Greedy Solver Esparso
            c_grd = greedy_sparse_solver(n, src, dst, steps=2)
            r_grd = c_grd / num_edges
            r_greedys.append(r_grd)
            
            # 3. SparseMetaGNN Carvalho
            with torch.no_grad():
                strat = model(n, src, dst)
                ia_lr    = 0.02 + strat[0].item() * 0.04
                ia_steps = int(40 + strat[1].item() * 40)
                ia_noise = 0.01 + strat[2].item() * 0.02
                
            t0_solve = time.time()
            c_carv = solve_laplacian_sparse(n, src, dst, lr=ia_lr, steps=ia_steps, noise=ia_noise)
            t_solve = time.time() - t0_solve
            r_carv = c_carv / num_edges
            
            r_carvalhos.append(r_carv)
            t_carvalhos.append(t_solve)
            
            print(f"  Instância {trial+1} (|E|={num_edges}): Random={r_rand*100:.2f}% | Greedy={r_grd*100:.2f}% | Carvalho={r_carv*100:.2f}% (Tempo: {t_solve:.2f}s | Mem: {mem_mb:.2f}MB)")
            
        results[label] = {
            "num_nodes": n,
            "mean_edges": int(num_edges),
            "mean_random_ratio": float(np.mean(r_rands)),
            "mean_greedy_ratio": float(np.mean(r_greedys)),
            "mean_carvalho_ratio": float(np.mean(r_carvalhos)),
            "mean_solve_time_sec": float(np.mean(t_carvalhos)),
            "mean_memory_mb": float(np.mean(memories_mb)),
            "throughput_edges_per_sec": float(num_edges / np.mean(t_carvalhos))
        }
        
    print("\n[3/3] Resumo Final de Escalação Extrema:")
    report_lines = [
        "=== RESULTADOS: OPÇÃO 3 (ESCALAÇÃO EXTREMA N=2000 A 10000 NÓS) ===",
        f"Data/Hora: {time.ctime()}\n"
    ]
    for lbl, dat in results.items():
        block = (
            f"Escala: {lbl}\n"
            f"  - Vértices: {dat['num_nodes']} | Arestas Médias: {dat['mean_edges']}\n"
            f"  - Consumo de Memória RAM:           {dat['mean_memory_mb']:.2f} MB\n"
            f"  - Tempo Médio do Solver Carvalho:   {dat['mean_solve_time_sec']:.2f} s\n"
            f"  - Throughput de Arestas:            {dat['throughput_edges_per_sec']:.0f} arestas/s\n"
            f"  - Random Cut Ratio:                 {dat['mean_random_ratio']*100:.2f}%\n"
            f"  - Greedy Cut Ratio:                 {dat['mean_greedy_ratio']*100:.2f}%\n"
            f"  - Carvalho Cut Ratio:               {dat['mean_carvalho_ratio']*100:.2f}%\n"
        )
        print(block)
        report_lines.append(block)
        
    with open("fase3_op3_extreme_scale_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    with open("fase3_op3_extreme_scale_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Resultados salvos em fase3_op3_extreme_scale_report.txt e fase3_op3_extreme_scale_results.json")

if __name__ == "__main__":
    run_experiment()
