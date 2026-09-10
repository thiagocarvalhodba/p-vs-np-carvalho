import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import time

# Configuração de dispositivo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 1. Gerador de Grafos Dinâmico
def generate_graph(n):
    p = np.random.uniform(0.2, 0.8)
    A = (torch.rand(n, n, device=device) < p).float()
    A = torch.triu(A, 1)
    A = A + A.T
    return A

def get_cut_value(A, s_bin):
    diff = (s_bin.unsqueeze(1) != s_bin.unsqueeze(0)).float()
    return torch.sum(A * diff) / 2

# 2. Solver Laplaciano com "Escudo de Gradiente"
def solve_enhanced(A, lr, steps, restarts=1):
    n = A.shape[0]
    D = torch.diag(A.sum(dim=1))
    L = D - A
    best_cut = 0.0
    
    # O "Escudo": Garante que o solver tenha gradientes mesmo se chamado em no_grad
    with torch.enable_grad():
        for _ in range(restarts):
            x = torch.randn(n, device=device).detach().requires_grad_(True)
            opt = torch.optim.Adam([x], lr=lr)
            
            for t in range(steps):
                s = torch.tanh(x)
                # Cálculo do Corte: 0.25 * s^T * L * s
                # Usamos dot e mv para máxima estabilidade
                cut_cont = 0.25 * torch.dot(s, torch.mv(L, s))
                loss = -cut_cont 
                
                opt.zero_grad()
                loss.backward()
                opt.step()
                
                with torch.no_grad():
                    x.add_(0.02 * torch.randn_like(x))
            
            s_final = torch.sign(torch.tanh(x)).detach()
            best_cut = max(best_cut, get_cut_value(A, s_final).item())
        
    return best_cut

# 3. Métrica de Dificuldade
def compute_difficulty(A):
    # Roda o solver para medir o quão instável o grafo é
    results = [solve_enhanced(A, 0.05, 100, restarts=1) for _ in range(3)]
    mean, std = np.mean(results), np.std(results)
    max_possible = (A.sum().item() / 2) + 1e-6
    quality = mean / max_possible
    diff = (std / (mean + 1e-6)) + (1 - quality)
    return np.clip(diff * 1.5, 0.1, 0.9)

# 4. GNN Vetorizada
class GNN(nn.Module):
    def __init__(self, dim=64):
        super().__init__()
        self.node_init = nn.Linear(1, dim)
        self.message_mlp = nn.Sequential(
            nn.Linear(dim*2+1, dim), 
            nn.ReLU(), 
            nn.Linear(dim, dim)
        )
        self.readout = nn.Sequential(
            nn.Linear(dim, 1), 
            nn.Sigmoid()
        )
    
    def forward(self, A):
        n = A.shape[0]
        h = self.node_init(torch.ones(n, 1, device=device))
        for _ in range(4):
            h_i = h.unsqueeze(1).expand(-1, n, -1)
            h_j = h.unsqueeze(0).expand(n, -1, -1)
            combined = torch.cat([h_i, h_j, A.unsqueeze(-1)], dim=-1)
            h = h + self.message_mlp(combined).mean(dim=1)
        return self.readout(h.mean(dim=0))

# 5. Loop de Experimento
N_NODES = 30
model = GNN().to(device)
optimizer = optim.Adam(model.parameters(), lr=0.001)

print(f"--- EXPLORAÇÃO P vs NP (N={N_NODES}) ---")
print(f"Ambiente: Python {torch.sys.version.split()[0]} | Dispositivo: {device}\n")

for epoch in range(51):
    A = generate_graph(N_NODES)
    
    # 1. Rótulo: Calculamos a dificuldade real do grafo
    # Removemos o no_grad daqui para permitir que o solver funcione internamente
    d_val = compute_difficulty(A)
    d_true = torch.tensor([d_val], dtype=torch.float32, device=device)
    
    # 2. Treino da IA: A rede tenta prever essa dificuldade
    d_pred = model(A)
    loss_train = nn.MSELoss()(d_pred, d_true)
    
    optimizer.zero_grad()
    loss_train.backward()
    optimizer.step()
    
    if epoch % 10 == 0:
        with torch.no_grad():
            p = d_pred.item()
            cut_base = solve_enhanced(A, 0.05, 100, restarts=1)
            
            # IA decide a estratégia com base na intuição estrutural
            restarts_ai = 2 if p > 0.6 else 1
            steps_ai = int(100 + p * 150)
            cut_ai = solve_enhanced(A, 0.05, steps_ai, restarts=restarts_ai)
            
            gain = cut_ai - cut_base
            print(f"E{epoch:2d} | Loss {loss_train.item():.4f} | Pred IA: {p:.2f} | Gain: {gain:+.1f}")

print("\n--- EXPERIMENTO CONCLUÍDO ---")