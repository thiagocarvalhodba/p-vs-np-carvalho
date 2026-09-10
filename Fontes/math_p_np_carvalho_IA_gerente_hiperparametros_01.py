import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import time

# Configuração de dispositivo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 1. Gerador de Grafos (Escala N=1000)
def generate_graph(n):
    p = np.random.uniform(0.2, 0.7)
    A = (torch.rand(n, n, device=device) < p).float()
    A = torch.triu(A, 1)
    A = A + A.T
    return A

def get_cut_value(A, s_bin):
    diff = (s_bin.unsqueeze(1) != s_bin.unsqueeze(0)).float()
    return torch.sum(A * diff) / 2

# 2. Solver com Proteção de Estabilidade
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
                    # Ruído controlado e decrescente
                    x.data.add_(noise_level * (1 - t/steps) * torch.randn_like(x))
            
            s_final = torch.sign(torch.tanh(x)).detach()
            best_cut = max(best_cut, get_cut_value(A, s_final).item())
    return best_cut

# 3. Meta-GNN com Saída Estabilizada
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
            nn.Sigmoid() # Garante que os parâmetros fiquem entre 0 e 1
        )
    
    def forward(self, A):
        n = A.shape[0]
        h = self.node_init(torch.ones(n, 1, device=device))
        for _ in range(4):
            h_i = h.unsqueeze(1).expand(-1, n, -1)
            h_j = h.unsqueeze(0).expand(n, -1, -1)
            combined = torch.cat([h_i, h_j, A.unsqueeze(-1)], dim=-1)
            h = h + self.message_mlp(combined).mean(dim=1)
        return self.strategy_head(h.mean(dim=0))

# 4. Loop de Treino Meta-Estável
N_NODES = 1000
model = MetaGNN().to(device)
optimizer = optim.Adam(model.parameters(), lr=0.0005) # LR de treino mais lento para estabilidade

print(f"--- EXPERIMENTO FINAL: META-ESTABILIDADE P vs NP (N={N_NODES}) ---")

running_gain = 0.0

for epoch in range(61):
    A = generate_graph(N_NODES)
    
    # 1. IA gera a estratégia
    strategy = model(A)
    
    # Mapeamento para zonas de segurança (Freios aplicados)
    ia_steps = int(100 + strategy[0].item() * 250)   # Max 350 steps
    ia_noise = 0.01 + strategy[1].item() * 0.03       # Max 0.04 noise
    ia_lr    = 0.01 + strategy[2].item() * 0.04       # Max 0.05 LR (Zona segura)
    
    # 2. Duelo de Solvers
    cut_base = solve_managed(A, lr=0.04, steps=150, noise_level=0.03)
    cut_ia   = solve_managed(A, lr=ia_lr, steps=ia_steps, noise_level=ia_noise)
    
    # 3. Recompensa Normalizada
    gain = cut_ia - cut_base
    reward = gain / N_NODES
    
    # 4. Loss com Regularização (Penaliza parâmetros exagerados)
    # loss = -Recompensa * Ativação + Penalidade_de_Complexidade
    complexity_penalty = 0.05 * torch.mean(strategy**2)
    loss_meta = -reward * torch.sum(torch.log(strategy + 1e-6)) + complexity_penalty
    
    optimizer.zero_grad()
    loss_meta.backward()
    optimizer.step()
    
    running_gain = 0.9 * running_gain + 0.1 * gain
    
    if epoch % 5 == 0:
        status = "IA VENCENDO" if gain > 0 else "BASE VENCENDO"
        print(f"E{epoch:2d} | Gain: {gain:+.1f} (Média: {running_gain:+.1f}) | {status}")
        print(f"   > IA_LR: {ia_lr:.3f} | IA_Noise: {ia_noise:.3f} | IA_Steps: {ia_steps}")

print("\n--- PESQUISA CONCLUÍDA ---")