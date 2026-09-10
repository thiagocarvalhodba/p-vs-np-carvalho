import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import torch
import torch.nn as nn
import numpy as np
import time
import json

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

ALPHA_GW_THEORETICAL = 0.87856

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

# -------------------------------------------------------------
# 1. SOLVER GOEMANS-WILLIAMSON (SDP + HIPERPLANO ALEATÓRIO)
# -------------------------------------------------------------
def goemans_williamson_sdp(A, d=16, steps=100, lr=0.05, num_hyperplanes=10):
    n = A.shape[0]
    D = torch.diag(A.sum(dim=1))
    L = D - A
    
    # Vetores unitários na esfera S^{d-1} (Fatoração Burer-Monteiro)
    V = torch.randn(n, d, device=device)
    V = V / torch.norm(V, dim=1, keepdim=True)
    V = nn.Parameter(V)
    
    optimizer = torch.optim.Adam([V], lr=lr)
    
    for _ in range(steps):
        # Normaliza na esfera
        V_norm = V / (torch.norm(V, dim=1, keepdim=True) + 1e-8)
        
        # Valor contínuo SDP: Tr(L * (V V^T)) = sum_k v_k^T L v_k
        # Cut_sdp = 0.25 * sum_{i,j} A_{ij} ||v_i - v_j||^2
        # Minimizar loss = -0.25 * Tr(V^T L V)
        loss = -0.25 * torch.trace(torch.matmul(V_norm.T, torch.matmul(L, V_norm)))
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
    with torch.no_grad():
        V_final = V / torch.norm(V, dim=1, keepdim=True)
        best_cut = 0.0
        # Arredondamento por múltiplos hiperplanos aleatórios
        for _ in range(num_hyperplanes):
            r = torch.randn(d, device=device)
            r = r / torch.norm(r)
            proj = torch.matmul(V_final, r)
            s_bin = torch.sign(proj)
            cut = get_cut_value(A, s_bin)
            if cut > best_cut:
                best_cut = cut
    return best_cut

# -------------------------------------------------------------
# 2. NEURO-META-HEURÍSTICA DE CARVALHO (CONTINUOUS LAPLACIAN + MetaGNN)
# -------------------------------------------------------------
class MetaGNN(nn.Module):
    def __init__(self, dim=64):
        super().__init__()
        self.node_init = nn.Linear(1, dim)
        self.message_mlp = nn.Sequential(
            nn.Linear(dim*2+1, dim), nn.ReLU(), nn.Linear(dim, dim)
        )
        self.strategy_head = nn.Sequential(
            nn.Linear(dim, 32), nn.ReLU(), nn.Linear(32, 3), nn.Sigmoid()
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

def carvalho_managed_solver(model, A):
    n = A.shape[0]
    D = torch.diag(A.sum(dim=1))
    L = D - A
    
    with torch.no_grad():
        strat = model(A)
        steps = int(80 + strat[0].item() * 150)
        noise = 0.01 + strat[1].item() * 0.03
        lr    = 0.01 + strat[2].item() * 0.04
        
    with torch.enable_grad():
        x = torch.randn(n, device=device).detach().requires_grad_(True)
        opt = torch.optim.Adam([x], lr=lr)
        for t in range(steps):
            s = torch.tanh(x)
            cut_cont = 0.25 * torch.dot(s, torch.mv(L, s))
            loss = -cut_cont
            opt.zero_grad()
            loss.backward()
            opt.step()
            with torch.no_grad():
                x.data.add_(noise * (1 - t/steps) * torch.randn_like(x))
        s_final = torch.sign(torch.tanh(x)).detach()
        return get_cut_value(A, s_final), {"steps": steps, "noise": noise, "lr": lr}

# -------------------------------------------------------------
# 3. GREEDY BASELINE
# -------------------------------------------------------------
def greedy_solver(A, steps=4):
    n = A.shape[0]
    s = torch.randint(0, 2, (n,), device=device) * 2 - 1
    for _ in range(steps):
        for i in range(n):
            gain = torch.sum(A[i] * s[i] * s)
            if gain > 0:
                s[i] *= -1
    return get_cut_value(A, s)

def run_experiment():
    print("==================================================================")
    print(" TRILHA 2: CONFRONTO CONTRA O LIMIAR DE GOEMANS-WILLIAMSON (UGC)")
    print(f" Limite Teórico GW: α_GW = {ALPHA_GW_THEORETICAL} (87.856%)")
    print(f" Dispositivo: {device} | Python / PyTorch")
    print("==================================================================")
    
    # Instanciar e inicializar modelo MetaGNN Carvalho
    print("\n[1/3] Inicializando e aquecendo a MetaGNN...")
    model = MetaGNN().to(device)
    opt = torch.optim.Adam(model.parameters(), lr=0.001)
    for _ in range(15):
        A_warm = generate_graph(100, 0.05)
        strat = model(A_warm)
        loss = torch.mean(strat**2)
        opt.zero_grad()
        loss.backward()
        opt.step()
    model.eval()
    print("  -> MetaGNN pronta.")
    
    test_scales = [
        {"n": 100, "p": 0.06, "label": "N=100 (Denso p=0.06)"},
        {"n": 200, "p": 0.03, "label": "N=200 (Médio p=0.03)"},
        {"n": 300, "p": 0.02, "label": "N=300 (Esparso p=0.02)"}
    ]
    
    results = {}
    print("\n[2/3] Executando confronto estatístico (5 instâncias por escala)...")
    
    for sc in test_scales:
        n = sc["n"]
        p = sc["p"]
        label = sc["label"]
        print(f"\n--- Escala: {label} ---")
        
        gw_ratios = []
        carvalho_ratios = []
        greedy_ratios = []
        gw_times = []
        carvalho_times = []
        
        for g_idx in range(5):
            A = generate_graph(n, p)
            num_edges = count_edges(A)
            if num_edges == 0: continue
            
            # Goemans-Williamson SDP
            t0 = time.time()
            c_gw = goemans_williamson_sdp(A, d=16, steps=70, lr=0.05, num_hyperplanes=10)
            t_gw = time.time() - t0
            r_gw = c_gw / num_edges
            gw_ratios.append(r_gw)
            gw_times.append(t_gw * 1000)
            
            # Carvalho Meta-Heurística
            t0 = time.time()
            c_carv, meta_params = carvalho_managed_solver(model, A)
            t_carv = time.time() - t0
            r_carv = c_carv / num_edges
            carvalho_ratios.append(r_carv)
            carvalho_times.append(t_carv * 1000)
            
            # Greedy
            c_grd = greedy_solver(A, steps=3)
            r_grd = c_grd / num_edges
            greedy_ratios.append(r_grd)
            
            print(f"  Instância {g_idx+1} (|E|={num_edges:.0f}): GW-SDP={r_gw*100:.2f}% ({t_gw*1000:.0f}ms) | Carvalho={r_carv*100:.2f}% ({t_carv*1000:.0f}ms) | Greedy={r_grd*100:.2f}%")
            
        mean_gw = float(np.mean(gw_ratios))
        mean_carv = float(np.mean(carvalho_ratios))
        mean_grd = float(np.mean(greedy_ratios))
        
        # Distância em relação ao teto analítico de Goemans-Williamson (0.87856)
        gap_gw = float(ALPHA_GW_THEORETICAL - mean_gw)
        gap_carvalho = float(ALPHA_GW_THEORETICAL - mean_carv)
        
        results[label] = {
            "mean_gw_ratio": mean_gw,
            "mean_carvalho_ratio": mean_carv,
            "mean_greedy_ratio": mean_grd,
            "gap_gw_to_bound": gap_gw,
            "gap_carvalho_to_bound": gap_carvalho,
            "carvalho_efficiency_vs_gw": float(mean_carv / (mean_gw + 1e-8)) * 100,
            "avg_gw_time_ms": float(np.mean(gw_times)),
            "avg_carvalho_time_ms": float(np.mean(carvalho_times)),
            "speedup_carvalho_vs_gw": float(np.mean(gw_times) / (np.mean(carvalho_times) + 1e-8))
        }
        
    print("\n[3/3] Resumo do Confronto contra Goemans-Williamson:")
    report_lines = [
        "=== RESULTADOS: TRILHA 2 (GOEMANS-WILLIAMSON VS CARVALHO NCO) ===",
        f"Data/Hora: {time.ctime()}",
        f"Limite Teórico Ótimo UGC (α_GW): {ALPHA_GW_THEORETICAL*100:.3f}%\n"
    ]
    for lbl, dat in results.items():
        block = (
            f"Escala: {lbl}\n"
            f"  - Goemans-Williamson (SDP):        {dat['mean_gw_ratio']*100:.2f}% (Tempo: {dat['avg_gw_time_ms']:.1f} ms)\n"
            f"  - Meta-Heurística Carvalho (NCO):   {dat['mean_carvalho_ratio']*100:.2f}% (Tempo: {dat['avg_carvalho_time_ms']:.1f} ms)\n"
            f"  - Heurística Greedy:                {dat['mean_greedy_ratio']*100:.2f}%\n"
            f"  - Eficiência Carvalho em Relação ao GW: {dat['carvalho_efficiency_vs_gw']:.2f}%\n"
            f"  - Speedup de Tempo (Carvalho vs GW):    {dat['speedup_carvalho_vs_gw']:.2f}x mais rápido\n"
            f"  - Gap até o Limite Analítico UGC:       {dat['gap_carvalho_to_bound']*100:.2f} p.p.\n"
        )
        print(block)
        report_lines.append(block)
        
    with open("trilha2_gw_benchmark_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    with open("trilha2_gw_benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Resultados salvos em trilha2_gw_benchmark_report.txt e trilha2_gw_benchmark_results.json")

if __name__ == "__main__":
    run_experiment()
