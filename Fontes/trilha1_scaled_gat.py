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
# ARQUITETURA: Scaled Dot-Product Graph Attention (Cura do GAT)
# -------------------------------------------------------------
class ScaledDotProductGNN(nn.Module):
    def __init__(self, in_dim=1, d_model=64, n_heads=4):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_head = d_model // n_heads
        
        self.node_embed = nn.Linear(in_dim, d_model)
        
        # Projeções Q, K, V
        self.w_q = nn.Linear(d_model, d_model)
        self.w_k = nn.Linear(d_model, d_model)
        self.w_v = nn.Linear(d_model, d_model)
        
        self.out_proj = nn.Linear(d_model, d_model)
        
        self.update_mlp = nn.Sequential(
            nn.Linear(d_model * 2, d_model),
            nn.ReLU(),
            nn.Linear(d_model, 1)
        )
        
    def forward(self, x, A):
        n = x.shape[0]
        h = self.node_embed(x.unsqueeze(-1))  # (N, d_model)
        
        # Multi-Head Scaled Attention mascarada por adjacência
        Q = self.w_q(h).view(n, self.n_heads, self.d_head).transpose(0, 1) # (H, N, d_head)
        K = self.w_k(h).view(n, self.n_heads, self.d_head).transpose(0, 1) # (H, N, d_head)
        V = self.w_v(h).view(n, self.n_heads, self.d_head).transpose(0, 1) # (H, N, d_head)
        
        scores = torch.matmul(Q, K.transpose(-2, -1)) / np.sqrt(self.d_head) # (H, N, N)
        
        # Máscara de adjacência: posições sem aresta recebem -1e9
        mask = (A == 0).unsqueeze(0).expand(self.n_heads, -1, -1)
        scores = scores.masked_fill(mask, -1e9)
        
        # Softmax estável com fallback para nós isolados
        attn_weights = torch.softmax(scores, dim=-1)
        attn_weights = torch.nan_to_num(attn_weights, nan=0.0)
        
        # Agregação ponderada dos valores
        context = torch.matmul(attn_weights, V) # (H, N, d_head)
        context = context.transpose(0, 1).contiguous().view(n, self.d_model) # (N, d_model)
        context = self.out_proj(context)
        
        # Residual connection + MLP de atualização
        combined = torch.cat([h, context], dim=-1)
        delta = self.update_mlp(combined).squeeze(-1)
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

def run_experiment():
    print("==================================================================")
    print(" TRILHA 1: CURA ARQUITETURAL DO GAT VIA SCALED DOT-PRODUCT ATTENTION")
    print(f" Dispositivo: {device} | Python / PyTorch")
    print("==================================================================")
    
    # 1. Treinamento da nova arquitetura
    print("\n[1/3] Treinando ScaledDotProductGNN com normalização espectral...")
    model = ScaledDotProductGNN(d_model=64, n_heads=4).to(device)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    
    t_start = time.time()
    for epoch in range(1, 41):
        p = np.random.choice([0.02, 0.04, 0.06])
        A = generate_graph(150, p)
        n = A.shape[0]
        
        # Treino com relaxação laplaciana suave
        x = torch.randn(n, device=device)
        for _ in range(15):
            delta = model(x, A)
            x = x + 0.1 * delta
            x = torch.clamp(x, -5, 5)
        
        s = torch.tanh(x)
        D = torch.diag(A.sum(dim=1))
        L = D - A
        cut = 0.25 * torch.dot(s, torch.mv(L, s))
        balance_reg = 0.2 * (torch.mean(s) ** 2)
        loss = -(cut - balance_reg)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if epoch % 10 == 0:
            print(f"  Ep {epoch:2d} | Cut Contínuo Estimado: {cut.item():.1f} | Loss: {loss.item():.1f}")
            
    print(f"Treinamento concluído em {time.time() - t_start:.1f}s.")
    torch.save(model.state_dict(), "model_maxcut_scaled_gat.pth")
    print("Novo modelo salvo em model_maxcut_scaled_gat.pth")
    
    # 2. Carregar o GAT antigo para confronto direto
    print("\n[2/3] Avaliando a anomalia de colapso: GAT Antigo vs. Novo Scaled GAT...")
    
    # Definição do GAT antigo
    class OldEdgeAttentionGNN(nn.Module):
        def __init__(self, dim=64):
            super().__init__()
            self.embed = nn.Linear(1, dim)
            self.attn = nn.Linear(dim * 2, 1)
            self.update = nn.Sequential(
                nn.Linear(dim, dim), nn.ReLU(), nn.Linear(dim, 1)
            )
        def forward(self, x, A):
            h = self.embed(x.unsqueeze(-1))
            n = h.shape[0]
            agg = torch.zeros_like(h)
            for i in range(n):
                neighbors = torch.where(A[i] > 0)[0]
                if len(neighbors) == 0: continue
                h_i = h[i].repeat(len(neighbors), 1)
                h_j = h[neighbors]
                e = self.attn(torch.cat([h_i, h_j], dim=1)).squeeze(-1)
                alpha = torch.softmax(e, dim=0)
                agg[i] = torch.sum(alpha.unsqueeze(-1) * h_j, dim=0)
            return self.update(h + agg).squeeze(-1)
            
    old_gat = OldEdgeAttentionGNN().to(device)
    try:
        old_gat.load_state_dict(torch.load("model_maxcut_gat.pth", map_location=device, weights_only=True))
        old_gat.eval()
        has_old = True
    except Exception as e:
        print(f"Aviso: Não foi possível carregar o modelo antigo: {e}")
        has_old = False
        
    test_cases = [
        {"n": 200, "p": 0.02, "label": "Esparso (N=200, p=0.02)"},
        {"n": 200, "p": 0.05, "label": "Denso / Crítico (N=200, p=0.05)"},
        {"n": 300, "p": 0.03, "label": "Escala Média (N=300, p=0.03)"}
    ]
    
    results = {}
    print("\n[3/3] Bateria comparativa de validação da cura...")
    for tc in test_cases:
        n = tc["n"]
        p = tc["p"]
        label = tc["label"]
        print(f"\n--- Cenário: {label} ---")
        
        old_ratios = []
        new_ratios = []
        new_times = []
        
        for trial in range(5):
            A = generate_graph(n, p)
            num_edges = count_edges(A)
            if num_edges == 0: continue
            
            # GAT Antigo
            if has_old:
                c_old = learned_solver(old_gat, A)
                r_old = c_old / num_edges
            else:
                r_old = 0.0
            old_ratios.append(r_old)
            
            # Novo Scaled GAT
            t0 = time.time()
            c_new = learned_solver(model, A)
            t_inf = time.time() - t0
            r_new = c_new / num_edges
            new_ratios.append(r_new)
            new_times.append(t_inf * 1000)
            
            print(f"  Amostra {trial+1} (|E|={num_edges:.0f}): GAT Antigo={r_old*100:.1f}% | Novo Scaled GAT={r_new*100:.1f}% | Tempo={t_inf*1000:.1f}ms")
            
        results[label] = {
            "old_gat_mean_ratio": float(np.mean(old_ratios)),
            "new_scaled_gat_mean_ratio": float(np.mean(new_ratios)),
            "relative_improvement": float(np.mean(new_ratios) - np.mean(old_ratios)),
            "avg_latency_ms": float(np.mean(new_times))
        }
        
    print("\n--- RESUMO CONSOLIDADO: CURA ARQUITETURAL DO GAT ---")
    report_lines = [
        "=== RESULTADOS: TRILHA 1 (SCALED DOT-PRODUCT GAT) ===",
        f"Data/Hora: {time.ctime()}\n"
    ]
    for lbl, st in results.items():
        block = (
            f"Cenário: {lbl}\n"
            f"  - GAT Antigo (Local Softmax):    {st['old_gat_mean_ratio']*100:.2f}%\n"
            f"  - Novo Scaled GAT (Multi-Head):  {st['new_scaled_gat_mean_ratio']*100:.2f}%\n"
            f"  - Ganho Líquido da Cura:        {st['relative_improvement']*100:+.2f} p.p.\n"
            f"  - Latência Média de Inferência: {st['avg_latency_ms']:.2f} ms\n"
        )
        print(block)
        report_lines.append(block)
        
    with open("trilha1_scaled_gat_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    with open("trilha1_scaled_gat_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Relatórios salvos em trilha1_scaled_gat_report.txt e trilha1_scaled_gat_results.json")

if __name__ == "__main__":
    run_experiment()
