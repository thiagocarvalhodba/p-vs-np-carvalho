import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import time
import json

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -------------------------------------------------------------
# 1. GERADOR DE INSTÂNCIAS DE 3-SAT NO LIMIAR CRÍTICO
# -------------------------------------------------------------
def generate_3sat_instance(n_vars, ratio=4.26):
    # Limiar crítico de transição de fase: m/n ~ 4.267
    n_clauses = int(n_vars * ratio)
    clauses = []
    for _ in range(n_clauses):
        vars_chosen = np.random.choice(n_vars, 3, replace=False)
        signs = np.random.choice([-1, 1], 3)
        # Cada literal: (var_idx, sign) onde sign +1 = x_i, -1 = not x_i
        clause = [(v, s) for v, s in zip(vars_chosen, signs)]
        clauses.append(clause)
    return n_clauses, clauses

def count_satisfied_clauses(assignment, clauses):
    # assignment: array {-1, 1} de tamanho n_vars (+1 = True, -1 = False)
    satisfied = 0
    for clause in clauses:
        is_sat = False
        for var_idx, sign in clause:
            val = assignment[var_idx]
            if val == sign:
                is_sat = True
                break
        if is_sat:
            satisfied += 1
    return satisfied

# -------------------------------------------------------------
# 2. SOLVERS CLÁSSICOS (RANDOM & WALKSAT)
# -------------------------------------------------------------
def random_sat_solver(n_vars, clauses):
    assignment = np.random.choice([-1, 1], n_vars)
    return count_satisfied_clauses(assignment, clauses)

def walksat_solver(n_vars, clauses, max_flips=300, noise_prob=0.3):
    assignment = np.random.choice([-1, 1], n_vars)
    best_sat = count_satisfied_clauses(assignment, clauses)
    
    for _ in range(max_flips):
        # Encontra cláusulas insatisfeitas
        unsat_clauses = []
        for c_idx, clause in enumerate(clauses):
            if not any(assignment[v] == s for v, s in clause):
                unsat_clauses.append(c_idx)
                
        if not unsat_clauses:
            return len(clauses) # 100% satisfeito
            
        # Escolhe uma cláusula insatisfeita aleatória
        target_c = clauses[np.random.choice(unsat_clauses)]
        
        # Decide entre flip guloso ou ruído estocástico
        if np.random.rand() < noise_prob:
            flip_var, _ = target_c[np.random.randint(0, 3)]
        else:
            # Seleciona variável que maximiza o ganho líquido de cláusulas
            best_gain = -9999
            best_var = target_c[0][0]
            for var_idx, _ in target_c:
                assignment[var_idx] *= -1
                sat_count = count_satisfied_clauses(assignment, clauses)
                assignment[var_idx] *= -1
                gain = sat_count - (len(clauses) - len(unsat_clauses))
                if gain > best_gain:
                    best_gain = gain
                    best_var = var_idx
            flip_var = best_var
            
        assignment[flip_var] *= -1
        current_sat = count_satisfied_clauses(assignment, clauses)
        if current_sat > best_sat:
            best_sat = current_sat
            
    return best_sat

# -------------------------------------------------------------
# 3. SOLVER CONTÍNUO RELAXADO (GRADIENTE SUAVE + RECOZIMENTO)
# -------------------------------------------------------------
def continuous_sat_solver(n_vars, clauses, lr=0.05, steps=100, noise=0.02):
    n_clauses = len(clauses)
    v = torch.randn(n_vars, device=device, requires_grad=True)
    optimizer = torch.optim.Adam([v], lr=lr)
    
    # Construção de matrizes para cálculo contínuo
    for t in range(steps):
        # Probabilidade de cada variável ser verdadeira p_i in [0, 1]
        p = 0.5 * (torch.tanh(v) + 1.0)
        
        # Probabilidade contínua de falsidade por cláusula
        unsat_probs = []
        for clause in clauses:
            p_false_literals = []
            for var_idx, sign in clause:
                p_var = p[var_idx]
                p_lit_false = 1.0 - p_var if sign == 1 else p_var
                p_false_literals.append(p_lit_false)
            p_clause_unsat = p_false_literals[0] * p_false_literals[1] * p_false_literals[2]
            unsat_probs.append(p_clause_unsat)
            
        unsat_tensor = torch.stack(unsat_probs)
        loss = torch.sum(unsat_tensor) # minimizar probabilidade de insatisfação
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        with torch.no_grad():
            v.data.add_(noise * (1.0 - t/steps) * torch.randn_like(v))
            
    with torch.no_grad():
        discrete_assignment = np.where(torch.tanh(v).cpu().numpy() >= 0, 1, -1)
        # Refinamento rápido local WalkSAT com parâmetros quentes
        refined_sat = walksat_solver(n_vars, clauses, max_flips=100, noise_prob=0.15)
        raw_sat = count_satisfied_clauses(discrete_assignment, clauses)
        return max(raw_sat, refined_sat)

# -------------------------------------------------------------
# 4. SATMetaGNN: REDE EM GRAFO BIPARTIDO DE FATORES
# -------------------------------------------------------------
class SATMetaGNN(nn.Module):
    def __init__(self, d_model=64):
        super().__init__()
        self.var_embed = nn.Linear(2, d_model) # features: grau de ocorrência positiva e negativa
        self.clause_mlp = nn.Sequential(
            nn.Linear(d_model * 3, d_model),
            nn.ReLU(),
            nn.Linear(d_model, d_model)
        )
        self.strategy_head = nn.Sequential(
            nn.Linear(d_model, 32),
            nn.ReLU(),
            nn.Linear(32, 3),
            nn.Sigmoid()
        )
        
    def forward(self, n_vars, clauses):
        # Extrai contagem de sinais por variável
        pos_counts = np.zeros(n_vars)
        neg_counts = np.zeros(n_vars)
        for c in clauses:
            for v, s in c:
                if s == 1: pos_counts[v] += 1
                else: neg_counts[v] += 1
                
        var_feats = np.stack([pos_counts, neg_counts], axis=-1)
        var_t = torch.tensor(var_feats, dtype=torch.float32, device=device)
        
        h_v = self.var_embed(var_t) # (N_vars, d_model)
        
        # Agregação pelas cláusulas
        clause_embs = []
        for c in clauses:
            c_vars = [h_v[v] for v, _ in c]
            c_rep = torch.cat(c_vars, dim=-1)
            clause_embs.append(c_rep)
            
        c_tensor = torch.stack(clause_embs)
        h_c = self.clause_mlp(c_tensor) # (N_clauses, d_model)
        
        pooled = h_c.mean(dim=0)
        return self.strategy_head(pooled)

def run_experiment():
    print("==================================================================")
    print(" OPÇÃO 1: O NÚCLEO DE COOK-LEVIN - MAX-3-SAT NO LIMIAR CRÍTICO")
    print(" Transição de Fase: m/n = 4.26 | Dispositivo: cpu | PyTorch")
    print("==================================================================")
    
    # 1. Treinamento da SATMetaGNN
    print("\n[1/3] Treinando SATMetaGNN em instâncias de transição de fase...")
    model = SATMetaGNN().to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    t_start = time.time()
    for ep in range(1, 21):
        m, clauses = generate_3sat_instance(n_vars=40, ratio=4.26)
        strat = model(40, clauses)
        
        ia_lr    = 0.01 + strat[0].item() * 0.05
        ia_steps = int(40 + strat[1].item() * 80)
        ia_noise = 0.01 + strat[2].item() * 0.03
        
        sat_base = continuous_sat_solver(40, clauses, lr=0.03, steps=50, noise=0.02)
        sat_ia   = continuous_sat_solver(40, clauses, lr=ia_lr, steps=ia_steps, noise=ia_noise)
        
        gain = sat_ia - sat_base
        reward = gain / m
        loss = -reward * torch.sum(torch.log(strat + 1e-6)) + 0.05 * torch.mean(strat**2)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
    print(f"Treinamento concluído em {time.time() - t_start:.1f}s.")
    torch.save(model.state_dict(), "model_sat_meta_manager.pth")
    print("Modelo salvo em model_sat_meta_manager.pth")
    
    # 2. Bateria de testes comparativos
    test_scales = [50, 100, 150]
    results = {}
    print("\n[2/3] Executando benchmark estatístico no limiar crítico (5 instâncias por escala)...")
    
    for n_vars in test_scales:
        label = f"N={n_vars} variáveis (m={int(n_vars*4.26)} cláusulas)"
        print(f"\n--- Escala: {label} ---")
        
        rand_ratios = []
        walk_ratios = []
        base_ratios = []
        ia_ratios   = []
        gains = []
        
        for trial in range(5):
            m, clauses = generate_3sat_instance(n_vars, ratio=4.26)
            
            # 1. Random Assignment (teórico: 87.5%)
            c_rand = random_sat_solver(n_vars, clauses)
            r_rand = c_rand / m
            rand_ratios.append(r_rand)
            
            # 2. WalkSAT Clássico
            c_walk = walksat_solver(n_vars, clauses, max_flips=200, noise_prob=0.3)
            r_walk = c_walk / m
            walk_ratios.append(r_walk)
            
            # 3. Solver Contínuo Base (fixo)
            c_base = continuous_sat_solver(n_vars, clauses, lr=0.03, steps=60, noise=0.02)
            r_base = c_base / m
            base_ratios.append(r_base)
            
            # 4. SATMetaGNN Carvalho (IA Adaptativa)
            with torch.no_grad():
                strat = model(n_vars, clauses)
                ia_lr    = 0.01 + strat[0].item() * 0.05
                ia_steps = int(40 + strat[1].item() * 80)
                ia_noise = 0.01 + strat[2].item() * 0.03
                
            c_ia = continuous_sat_solver(n_vars, clauses, lr=ia_lr, steps=ia_steps, noise=ia_noise)
            r_ia = c_ia / m
            ia_ratios.append(r_ia)
            
            gain = c_ia - c_base
            gains.append(gain)
            
            print(f"  Instância {trial+1} (m={m}): Random={r_rand*100:.1f}% | WalkSAT={r_walk*100:.1f}% | Base={r_base*100:.1f}% | IA Carvalho={r_ia*100:.1f}% | Ganho={gain:+2.0f} cláusulas")
            
        results[label] = {
            "mean_random_ratio": float(np.mean(rand_ratios)),
            "mean_walksat_ratio": float(np.mean(walk_ratios)),
            "mean_base_ratio": float(np.mean(base_ratios)),
            "mean_ia_ratio": float(np.mean(ia_ratios)),
            "mean_gain_clauses": float(np.mean(gains)),
            "ia_win_rate_vs_base": float(np.mean([1 if g > 0 else 0 for g in gains])) * 100,
            "ia_satisfaction_percent": float(np.mean(ia_ratios)) * 100
        }
        
    print("\n[3/3] Resumo Final do Experimento Max-3-SAT:")
    report_lines = [
        "=== RESULTADOS: OPÇÃO 1 (MAX-3-SAT NO LIMIAR CRÍTICO DE COOK-LEVIN) ===",
        f"Data/Hora: {time.ctime()}\n"
    ]
    for lbl, dat in results.items():
        block = (
            f"Cenário: {lbl}\n"
            f"  - Random Assignment (Teórico 87.5%):  {dat['mean_random_ratio']*100:.2f}%\n"
            f"  - WalkSAT Clássico:                   {dat['mean_walksat_ratio']*100:.2f}%\n"
            f"  - Solver Contínuo Base (Fixo):        {dat['mean_base_ratio']*100:.2f}%\n"
            f"  - SATMetaGNN Carvalho (IA):           {dat['mean_ia_ratio']*100:.2f}%\n"
            f"  - Ganho Líquido de Cláusulas (IA):    {dat['mean_gain_clauses']:+.2f} cláusulas\n"
            f"  - Taxa de Vitória IA vs Base:         {dat['ia_win_rate_vs_base']:.1f}%\n"
        )
        print(block)
        report_lines.append(block)
        
    with open("fase3_op1_max_sat_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    with open("fase3_op1_max_sat_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Resultados salvos em fase3_op1_max_sat_report.txt e fase3_op1_max_sat_results.json")

if __name__ == "__main__":
    run_experiment()
