import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------------
# 1. Grafo
# -----------------------------
def generate_graph(n):
    p = np.random.uniform(0.2, 0.7)
    A = (torch.rand(n, n, device=device) < p).float()
    A = torch.triu(A, 1)
    A = A + A.T
    return A

def get_cut_value(A, s_bin):
    diff = (s_bin.unsqueeze(1) != s_bin.unsqueeze(0)).float()
    return torch.sum(A * diff) / 2

# -----------------------------
# 2. Solver
# -----------------------------
def solve_managed(A, lr, steps, noise_level):
    n = A.shape[0]
    D = torch.diag(A.sum(dim=1))
    L = D - A
    
    x = torch.randn(n, device=device, requires_grad=True)
    opt = torch.optim.Adam([x], lr=lr)
    
    for t in range(steps):
        s = torch.tanh(x)
        cut_cont = 0.25 * torch.dot(s, torch.mv(L, s))
        loss = -cut_cont
        
        opt.zero_grad()
        loss.backward()
        opt.step()
        
        with torch.no_grad():
            x += noise_level * (1 - t/steps) * torch.randn_like(x)
    
    s_bin = torch.sign(torch.tanh(x)).detach()
    return get_cut_value(A, s_bin).item()

# -----------------------------
# 3. Política (Gaussian Policy)
# -----------------------------
class MetaPolicy(nn.Module):
    def __init__(self, dim=64):
        super().__init__()
        
        self.node_init = nn.Linear(1, dim)
        
        self.message = nn.Sequential(
            nn.Linear(dim*2+1, dim),
            nn.ReLU(),
            nn.Linear(dim, dim)
        )
        
        self.head = nn.Linear(dim, 3)  # mean
        self.log_std = nn.Parameter(torch.zeros(3))  # std learnável
    
    def forward(self, A):
        n = A.shape[0]
        h = self.node_init(torch.ones(n,1, device=device))
        
        for _ in range(3):
            h_i = h.unsqueeze(1).expand(-1, n, -1)
            h_j = h.unsqueeze(0).expand(n, -1, -1)
            m = torch.cat([h_i, h_j, A.unsqueeze(-1)], dim=-1)
            h = h + self.message(m).mean(dim=1)
        
        g = h.mean(dim=0)
        
        mean = self.head(g)
        std = torch.exp(self.log_std)
        
        return mean, std

# -----------------------------
# 4. Treinamento REINFORCE
# -----------------------------
N = 200   # 🔥 menor para aprender melhor
model = MetaPolicy().to(device)
optimizer = optim.Adam(model.parameters(), lr=1e-3)

baseline = 0.0

print("\n--- TREINAMENTO REINFORCE ---\n")

for epoch in range(101):
    A = generate_graph(N)
    
    mean, std = model(A)
    
    # amostra ação
    dist = torch.distributions.Normal(mean, std)
    action = dist.sample()
    log_prob = dist.log_prob(action).sum()
    
    # squash para [0,1]
    action = torch.sigmoid(action)
    
    # mapear para parâmetros
    lr    = 0.01 + action[0].item() * 0.04
    noise = 0.01 + action[1].item() * 0.03
    steps = int(100 + action[2].item() * 200)
    
    # baseline
    cut_base = solve_managed(A, lr=0.04, steps=150, noise_level=0.03)
    
    # IA
    cut_ia = solve_managed(A, lr=lr, steps=steps, noise_level=noise)
    
    gain = cut_ia - cut_base
    reward = gain / N
    
    # baseline móvel (reduz variância)
    baseline = 0.9 * baseline + 0.1 * reward
    
    advantage = reward - baseline
    
    # loss REINFORCE
    loss = -log_prob * advantage
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if epoch % 10 == 0:
        print(f"E{epoch:3d} | Gain: {gain:+.1f} | AvgBase: {baseline:+.4f}")
        print(f"   > lr={lr:.3f}, noise={noise:.3f}, steps={steps}")