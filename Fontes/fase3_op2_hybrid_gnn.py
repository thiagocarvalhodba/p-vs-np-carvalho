import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

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

# -------------------------------------------------------------
# ARQUITETURA HÍBRIDA: CONVOLUÇÃO ESPECTRAL + ATENÇÃO ESCALADA GATED
# -------------------------------------------------------------
class HybridSpectralAttentionGNN(nn.Module):
    def __init__(self, in_dim=1, d_model=64, n_heads=4):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_head = d_model // n_heads
        
        self.node_embed = nn.Linear(in_dim, d_model)
        
        # 1. Ramo Espectral (Sparse Global Diffusion)
        self.spectral_update = nn.Sequential(
            nn.Linear(d_model * 2, d_model),
            nn.ReLU(),
            nn.Linear(d_model, d_model)
        )
        
        # 2. Ramo de Atenção Relacional (Scaled Dot-Product Multi-Head)
        self.w_q = nn.Linear(d_model, d_model)
        self.w_k = nn.Linear(d_model, d_model)
        self.w_v = nn.Linear(d_model, d_model)
        self.attn_out = nn.Linear(d_model, d_model)
        
        # 3. Gated Fusion Unit (Portão de Decisão Adaptativa)
        self.gate = nn.Sequential(
            nn.Linear(d_model * 2, d_model),
            nn.Sigmoid()
        )
        
        # 4. Readout Final
        self.final_mlp = nn.Sequential(
            nn.Linear(d_model, d_model // 2),
            nn.ReLU(),
            nn.Linear(d_model // 2, 1)
        )
        
    def forward(self, x, A):
        n = x.shape[0]
        h = self.node_embed(x.unsqueeze(-1)) # (N, d_model)
        
        # Ramo 1: Difusão Espectral Global
        agg = torch.matmul(A, h)
        h_spec = self.spectral_update(torch.cat([h, agg], dim=-1))
        
        # Ramo 2: Atenção Escalada Seletiva Mascarada
        Q = self.w_q(h).view(n, self.n_heads, self.d_head).transpose(0, 1)
        K = self.w_k(h).view(n, self.n_heads, self.d_head).transpose(0, 1)
        V = self.w_v(h).view(n, self.n_heads, self.d_head).transpose(0, 1)
        
        scores = torch.matmul(Q, K.transpose(-2, -1)) / np.sqrt(self.d_head)
        mask = (A == 0).unsqueeze(0).expand(self.n_heads, -1, -1)
        scores = scores.masked_fill(mask, -1e9)
        attn_weights = torch.softmax(scores, dim=-1)
        attn_weights = torch.nan_to_num(attn_weights, nan=0.0)
        
        context = torch.matmul(attn_weights, V).transpose(0, 1).contiguous().view(n, self.d_model)
        h_attn = self.attn_out(context)
        
        # Ramo 3: Fusão Dinâmica com Portão Sigmoide
        g = self.gate(torch.cat([h_spec, h_attn], dim=-1))
        h_fused = g * h_spec + (1.0 - g) * h_attn
        
        delta = self.final_mlp(h_fused).squeeze(-1)
        return delta

def learned_solver(model, A, steps=25):
    n = A.shape[0]
    with torch.no_grad():
        x = torch.randn(n, device=device)
        for _ in range(steps):
            delta = model(x, A)
            x = x + 0.1 * delta
            x = torch.clamp(x, -5, 5)
        s = torch.sign(torch.tanh(x))
    return get_cut_value(A, s)

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
    print(" OPÇÃO 2: HIBRIDIZAÇÃO NEURO-SIMBÓLICA (SPECTRAL + SCALED ATTENTION)")
    print(" Arquitetura: HybridSpectralAttentionGNN | Dispositivo: cpu | PyTorch")
    print("==================================================================")
    
    # 1. Treinamento do Modelo Híbrido
    print("\n[1/3] Treinando HybridSpectralAttentionGNN (40 épocas)...")
    model = HybridSpectralAttentionGNN().to(device)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    
    t_start = time.time()
    for epoch in range(1, 41):
        p = np.random.choice([0.015, 0.03, 0.05])
        A = generate_graph(150, p)
        n = A.shape[0]
        
        x = torch.randn(n, device=device)
        for _ in range(15):
            delta = model(x, A)
            x = x + 0.1 * delta
            x = torch.clamp(x, -5, 5)
            
        s = torch.tanh(x)
        D = torch.diag(A.sum(dim=1))
        L = D - A
        cut = 0.25 * torch.dot(s, torch.mv(L, s))
        balance_penalty = 0.2 * (torch.mean(s) ** 2)
        loss = -(cut - balance_penalty)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if epoch % 10 == 0:
            print(f"  Ep {epoch:2d} | Cut Contínuo: {cut.item():.1f} | Loss: {loss.item():.1f}")
            
    print(f"Treinamento concluído em {time.time() - t_start:.1f}s.")
    torch.save(model.state_dict(), "model_maxcut_hybrid.pth")
    print("Modelo salvo em model_maxcut_hybrid.pth")
    
    # 2. Carregar modelos para confronto: SparseGNN vs Scaled GAT vs Modelo Híbrido
    print("\n[2/3] Carregando modelos especialistas para confronto de fronteira...")
    
    # SparseGNN
    class SparseGNN(nn.Module):
        def __init__(self, dim=64):
            super().__init__()
            self.embed = nn.Linear(1, dim)
            self.update = nn.Sequential(nn.Linear(dim * 2, dim), nn.ReLU(), nn.Linear(dim, 1))
        def forward(self, x, A):
            h = self.embed(x.unsqueeze(-1))
            return self.update(torch.cat([h, torch.matmul(A, h)], dim=-1)).squeeze(-1)
            
    sparse_model = SparseGNN().to(device)
    has_sparse = False
    try:
        sparse_model.load_state_dict(torch.load("model_maxcut.pth", map_location=device, weights_only=True))
        sparse_model.eval()
        has_sparse = True
    except Exception as e:
        print(f"Aviso SparseGNN: {e}")
        
    test_scales = [
        {"n": 200, "p": 0.02, "label": "N=200, p=0.02 (Esparso)"},
        {"n": 200, "p": 0.05, "label": "N=200, p=0.05 (Intermediário)"},
        {"n": 400, "p": 0.015, "label": "N=400, p=0.015 (Alta Escala)"}
    ]
    
    results = {}
    print("\n[3/3] Bateria comparativa de quebra de barreira (5 instâncias por cenário)...")
    
    for sc in test_scales:
        n = sc["n"]
        p = sc["p"]
        label = sc["label"]
        print(f"\n--- Cenário: {label} ---")
        
        hybrid_ratios = []
        sparse_ratios = []
        greedy_ratios = []
        hybrid_times  = []
        
        for trial in range(5):
            A = generate_graph(n, p)
            num_edges = count_edges(A)
            if num_edges == 0: continue
            
            # Modelo Híbrido
            t0 = time.time()
            c_hyb = learned_solver(model, A, steps=25)
            t_hyb = (time.time() - t0) * 1000
            r_hyb = c_hyb / num_edges
            hybrid_ratios.append(r_hyb)
            hybrid_times.append(t_hyb)
            
            # SparseGNN
            if has_sparse:
                c_sp = learned_solver(sparse_model, A, steps=20)
                r_sp = c_sp / num_edges
            else:
                r_sp = 0.0
            sparse_ratios.append(r_sp)
            
            # Greedy
            c_grd = greedy_solver(A, steps=4)
            r_grd = c_grd / num_edges
            greedy_ratios.append(r_grd)
            
            print(f"  Instância {trial+1} (|E|={num_edges:.0f}): Greedy={r_grd*100:.1f}% | SparseGNN={r_sp*100:.1f}% | Híbrido Carvalho={r_hyb*100:.1f}% ({t_hyb:.1f}ms)")
            
        mean_hyb = float(np.mean(hybrid_ratios))
        mean_sp  = float(np.mean(sparse_ratios))
        mean_grd = float(np.mean(greedy_ratios))
        
        results[label] = {
            "mean_hybrid_ratio": mean_hyb,
            "mean_sparse_ratio": mean_sp,
            "mean_greedy_ratio": mean_grd,
            "hybrid_vs_sparse_gain": float(mean_hyb - mean_sp),
            "hybrid_vs_greedy_gain": float(mean_hyb - mean_grd),
            "avg_latency_ms": float(np.mean(hybrid_times)),
            "surpassed_80_percent": bool(mean_hyb >= 0.80)
        }
        
    print("\n--- RESUMO CONSOLIDADO: HIBRIDIZAÇÃO NEURO-SIMBÓLICA ---")
    report_lines = [
        "=== RESULTADOS: OPÇÃO 2 (HIBRIDIZAÇÃO ESPECTRAL + ATENÇÃO) ===",
        f"Data/Hora: {time.ctime()}\n"
    ]
    for lbl, dat in results.items():
        block = (
            f"Cenário: {lbl}\n"
            f"  - Modelo Híbrido Carvalho:     {dat['mean_hybrid_ratio']*100:.2f}% (Latência: {dat['avg_latency_ms']:.1f} ms)\n"
            f"  - SparseGNN Pura:              {dat['mean_sparse_ratio']*100:.2f}%\n"
            f"  - Heurística Greedy:           {dat['mean_greedy_ratio']*100:.2f}%\n"
            f"  - Ganho Líquido vs Greedy:     {dat['hybrid_vs_greedy_gain']*100:+.2f} p.p.\n"
            f"  - Rompeu a barreira dos 80%?:   {'SIM! 🎉' if dat['surpassed_80_percent'] else 'Em consolidação'}\n"
        )
        print(block)
        report_lines.append(block)
        
    with open("fase3_op2_hybrid_gnn_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    with open("fase3_op2_hybrid_gnn_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Resultados salvos em fase3_op2_hybrid_gnn_report.txt e fase3_op2_hybrid_gnn_results.json")

if __name__ == "__main__":
    run_experiment()
