import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# Configuração de dispositivo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------------
# 1. Funções de Grafo (Max-Cut)
# -----------------------------
def generate_graph(n, p=0.5):
    A = (torch.rand(n, n, device=device) < p).float()
    A = torch.triu(A, 1)
    A = A + A.T
    return A

def get_cut_value(A, s_bin):
    # s_bin: (-1 ou 1)
    diff = (s_bin.unsqueeze(1) != s_bin.unsqueeze(0)).float()
    return torch.sum(A * diff) / 2

# -----------------------------
# 2. Solver Robusto (Grafo Protegido)
# -----------------------------
def solve_enhanced(A, lr, steps, restarts=3):
    n = A.shape[0]
    best_cut = 0.0
    
    for _ in range(restarts):
        # Usar nn.Parameter garante que o PyTorch trate x como variável de otimização
        x = nn.Parameter(torch.randn(n, device=device))
        opt = torch.optim.Adam([x], lr=lr)
        
        for t in range(steps):
            s = torch.tanh(x)
            
            # Cálculo da Loss (Vetorizado e explícito para o Autograd)
            # Loss = -0.25 * sum( A * (1 - s_i * s_j) )
            loss = -0.25 * torch.sum(A * (1 - torch.outer(s, s)))
            
            # Verificação de segurança: se a loss não exige gradiente, algo quebrou
            if not loss.requires_grad:
                continue

            opt.zero_grad()
            loss.backward()
            opt.step()
            
            # Injeção de ruído segura (Simulated Annealing)
            noise_scale = 0.01 * (1 - t/steps)
            with torch.no_grad():
                x.add_(noise_scale * torch.randn_like(x))
        
        # Resultado final da tentativa
        s_final = torch.sign(torch.tanh(x)).detach()
        cut = get_cut_value(A, s_final).item()
        best_cut = max(best_cut, cut)
    
    return best_cut

# -----------------------------
# 3. Métrica de Dificuldade Ψ(A)
# -----------------------------
def compute_difficulty(A, trials=6):
    results = []
    for _ in range(trials):
        results.append(solve_enhanced(A, lr=0.05, steps=50, restarts=2))
    
    results = np.array(results)
    mean = results.mean()
    std = results.std()
    
    max_possible = A.sum().item() / 2
    quality = mean / (max_possible + 1e-6)
    
    # Dificuldade combina instabilidade (std) com baixa performance (quality)
    difficulty = (std / (mean + 1e-6)) + (1 - quality)
    return np.clip(difficulty, 0, 1)

# -----------------------------
# 4. GNN Vetorizada (Alta Performance)
# -----------------------------
class GNN(nn.Module):
    def __init__(self, dim=16):
        super().__init__()
        self.dim = dim
        self.node_init = nn.Linear(1, dim)
        self.message_mlp = nn.Sequential(
            nn.Linear(dim * 2 + 1, 32),
            nn.ReLU(),
            nn.Linear(32, dim)
        )
        self.readout = nn.Sequential(
            nn.Linear(dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
    
    def forward(self, A):
        n = A.shape[0]
        # Inicializa estados dos nós
        h = self.node_init(torch.ones(n, 1, device=device))
        
        # 3 épocas de troca de mensagens (Totalmente vetorizado)
        for _ in range(3):
            # Prepara vizinhança: expande h para (N, N, Dim)
            h_left = h.unsqueeze(1).expand(-1, n, -1)
            h_right = h.unsqueeze(0).expand(n, -1, -1)
            A_ext = A.unsqueeze(-1)
            
            # Concatena [nó_i, nó_j, aresta_ij]
            combined = torch.cat([h_left, h_right, A_ext], dim=-1)
            
            # Processa todas as mensagens de uma vez
            messages = self.message_mlp(combined)
            
            # Agrega mensagens (soma por linha) e atualiza h
            h = h + messages.sum(dim=1)
            
        return self.readout(h.mean(dim=0))

# -----------------------------
# 5. Loop Principal
# -----------------------------
N_NODES = 10
model = GNN().to(device)
optimizer = optim.Adam(model.parameters(), lr=0.003)

print(f"Iniciando exploração em: {device}")

history = {"loss": [], "pred": [], "gain": []}

for epoch in range(101):
    # Gera problema
    A = generate_graph(N_NODES)
    
    # 1. Calcula dificuldade real
    d_true = compute_difficulty(A)
    d_true_t = torch.tensor([d_true], dtype=torch.float32, device=device)
    
    # 2. Treina predição
    d_pred = model(A)
    loss_train = nn.MSELoss()(d_pred, d_true_t)
    
    optimizer.zero_grad()
    loss_train.backward()
    optimizer.step()
    
    # 3. Diagnóstico
    if epoch % 20 == 0:
        with torch.no_grad():
            p_val = d_pred.item()
            
            # Testa eficácia da IA
            cut_base = solve_enhanced(A, lr=0.05, steps=50)
            
            # Ajuste adaptativo pela IA
            a_lr = 0.01 + (1 - p_val) * 0.07
            a_steps = int(40 + p_val * 100)
            cut_ai = solve_enhanced(A, lr=a_lr, steps=a_steps)
            
            gain = cut_ai - cut_base
            print(f"Época {epoch:3d} | Loss {loss_train.item():.4f} | Dif_Pred: {p_val:.2f} | Ganho_IA: {gain:.1f}")
            
            history["loss"].append(loss_train.item())
            history["pred"].append(p_val)
            history["gain"].append(gain)

print("\n--- RESULTADO FINAL ---")
print(f"Loss caiu: {history['loss'][-1] < history['loss'][0]}")
print(f"Variação de Predição: {np.std(history['pred']):.4f}")
print(f"Melhoria Média (Gain): {np.mean(history['gain']):.2f}")