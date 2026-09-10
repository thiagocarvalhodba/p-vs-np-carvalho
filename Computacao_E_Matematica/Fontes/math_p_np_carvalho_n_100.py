import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import time

# Configuração de dispositivo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 1. Gerador de Grafos Dinâmico (Escala N=100)
def generate_graph(n):
    p = np.random.uniform(0.15, 0.75) 
    A = (torch.rand(n, n, device=device) < p).float()
    A = torch.triu(A, 1)
    A = A + A.T
    return A

def get_cut_value(A, s_bin):
    diff = (s_bin.unsqueeze(1) != s_bin.unsqueeze(0)).float()
    return torch.sum(A * diff) / 2

# 2. Solver Laplaciano Refinado
def solve_enhanced(A, lr, steps, restarts=1):
    n = A.shape[0]
    D = torch.diag(A.sum(dim=1))
    L = D - A
    best_cut = 0.0
    
    with torch.enable_grad():
        for _ in range(restarts):
            # Inicialização blindada para N=100
            x = torch.randn(n, device=device).detach().requires_grad_(True)
            opt = torch.optim.Adam([x], lr=lr)
            
            for t in range(steps):
                s = torch.tanh(x)
                # Maximização do corte via álgebra linear direta
                cut_cont = 0.25 * torch.dot(s, torch.mv(L, s))
                loss = -cut_cont 
                
                opt.zero_grad()
                loss.backward()
                opt.step()
                
                # Ruído de Annealing proporcional ao progresso
                with torch.no_grad():
                    noise = 0.03 * (1 - t/steps)
                    x.add_(noise * torch.randn_like(x))
            
            s_final = torch.sign(torch.tanh(x)).detach()
            best_cut = max(best_cut, get_cut_value(A, s_final).item())
        
    return best_cut

# 3. Métrica de Dificuldade (Calibrada para N=100)
def compute_difficulty(A):
    # Diminuímos os trials para economizar tempo em N=100, mas aumentamos steps
    results = [solve_enhanced(A, 0.05, 150, restarts=1) for _ in range(2)]
    mean, std = np.mean(results), np.std(results)
    max_theoretical = (A.sum().item() / 2) + 1e-6
    quality = mean / max_theoretical
    
    # Sensibilidade aumentada para variações sutis em grafos grandes
    diff = (std / (mean + 1e-6)) + (1.2 * (1 - quality))
    return np.clip(diff, 0.1, 0.95)

# 4. GNN Robusta (64 dimensões para padrões complexos)
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
        for _ in range(4): # 4 passagens de mensagem para cobrir o grafo de 100 nós
            h_i = h.unsqueeze(1).expand(-1, n, -1)
            h_j = h.unsqueeze(0).expand(n, -1, -1)
            combined = torch.cat([h_i, h_j, A.unsqueeze(-1)], dim=-1)
            h = h + self.message_mlp(combined).mean(dim=1)
        return self.readout(h.mean(dim=0))

# 5. Experimento de Alta Escala
N_NODES = 100
model = GNN().to(device)
optimizer = optim.Adam(model.parameters(), lr=0.001)

print(f"--- DESAFIO P vs NP: ESCALA N={N_NODES} ---")
print(f"Busca em ~1.26 x 10^30 combinações\n")

start_global = time.time()

for epoch in range(31): # 30 épocas são suficientes para ver a tendência inicial em N=100
    A = generate_graph(N_NODES)
    
    # 1. Obter Rótulo (Verdade de dificuldade)
    d_val = compute_difficulty(A)
    d_true = torch.tensor([d_val], dtype=torch.float32, device=device)
    
    # 2. Treino GNN
    d_pred = model(A)
    loss_train = nn.MSELoss()(d_pred, d_true)
    
    optimizer.zero_grad()
    loss_train.backward()
    optimizer.step()
    
    if epoch % 5 == 0:
        with torch.no_grad():
            p = d_pred.item()
            # Base: Esforço fixo e limitado
            cut_base = solve_enhanced(A, 0.05, 120, restarts=1)
            
            # IA Adaptativa: Esforço proporcional à complexidade detectada
            restarts_ai = 3 if p > 0.7 else (2 if p > 0.4 else 1)
            steps_ai = int(120 + p * 200)
            cut_ai = solve_enhanced(A, 0.05, steps_ai, restarts=restarts_ai)
            
            gain = cut_ai - cut_base
            print(f"E{epoch:2d} | Loss {loss_train.item():.4f} | Pred IA Dif: {p:.2f} | Gain IA: {gain:+.1f}")

total_time = (time.time() - start_global) / 60
print(f"\n--- CONCLUÍDO EM {total_time:.2f} MINUTOS ---")