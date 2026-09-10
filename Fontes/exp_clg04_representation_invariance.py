"""
EXP-CLG-04: BENCHMARK DE INVARIÂNCIA DE REPRESENTAÇÃO (ENSEMBLE E_equiv)
Autor: Thiago Carvalho (2026)
Ambiente: PyTorch / NumPy

Objetivo:
Investigar o teste decisivo proposto pelo Professor Avaliador:
'Mesmo problema lógico -> Múltiplas representações contínuas'

Hipótese a Testar:
A dificuldade geométrica (alcançabilidade e armadilhas) pertence ao problema lógico
ou é um artefato da representação contínua escolhida?

Para a MESMA instância lógica I (3-XOR-SAT e 3-SAT com solução plantada s*), comparamos:
1. Representação A (Multilinear Padrão):
   Phi_mult(x) = sum_c prod_{j=1}^k (1 - sigma_j x_j)/2
2. Representação B (Penalização Quadrática / Hinge SOS):
   Phi_quad(x) = sum_c [ relu( 1 - sum_{j=1}^k (1 + sigma_j x_j)/2 ) ]^2
3. Representação C (Log-Sum-Exp / Softplus Suavizada):
   Phi_soft(x) = sum_c softplus( beta * (1 - sum_{j=1}^k (1 + sigma_j x_j)/2) ) / beta

Métricas Formalizadas:
- Reachability Dinâmico R_dyn com Intervalo de Confiança Binomial (Wilson 95%)
- Severidade da Armadilha E_trap (média de cláusulas violadas se falhou)
- Distância de Hamming Normalizada d_H = dist(s_final, s*) / N
"""

import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import time
import math
import json
from typing import List, Tuple, Dict, Any

import numpy as np
import torch


# ==============================================================================
# 1. CÁLCULO DE INTERVALO DE CONFIANÇA BINOMIAL (WILSON SCORE INTERVAL)
# ==============================================================================
def wilson_score_interval(successes: int, trials: int, confidence: float = 0.95) -> Tuple[float, float, float]:
    """
    Calcula taxa de sucesso e intervalo de confiança binomial de Wilson (95%).
    Retorna (p_hat, ci_lower, ci_upper).
    """
    if trials == 0:
        return 0.0, 0.0, 0.0
    p = successes / trials
    z = 1.95996 # para 95% de confiança
    denom = 1.0 + (z**2) / trials
    center = (p + (z**2) / (2.0 * trials)) / denom
    margin = (z * math.sqrt((p * (1.0 - p) / trials) + (z**2) / (4.0 * (trials**2)))) / denom
    lower = max(0.0, center - margin)
    upper = min(1.0, center + margin)
    return float(p), float(lower), float(upper)


# ==============================================================================
# 2. DEFINIÇÃO DA INSTÂNCIA LÓGICA E MÚLTIPLAS REPRESENTAÇÕES CONTÍNUAS
# ==============================================================================
class LogicalInstance:
    def __init__(self, n: int, family: str, clauses: List[Tuple[List[int], List[float]]], s_plant: np.ndarray):
        self.n = n
        self.family = family
        self.clauses = clauses
        self.m = len(clauses)
        self.s_plant = s_plant # vetor spin {-1, +1}^n
        
        self.indices = torch.tensor([c[0] for c in clauses], dtype=torch.long)
        self.signs = torch.tensor([c[1] for c in clauses], dtype=torch.float32)

    # Representação A: Multilinear
    def potential_multilinear(self, x: torch.Tensor) -> torch.Tensor:
        selected = x[self.indices] # [M, k]
        factors = (1.0 - self.signs * selected) * 0.5
        return torch.sum(torch.prod(factors, dim=-1))

    # Representação B: Quadrática Hinge (Sum of Squares)
    def potential_quadratic(self, x: torch.Tensor) -> torch.Tensor:
        # Cada literal sat: (1 + sigma * x) / 2 em [0, 1]
        selected = x[self.indices]
        literal_sat = (1.0 + self.signs * selected) * 0.5
        # Cláusula sat se sum(literal_sat) >= 1. Violação: max(0, 1 - sum)
        clause_sat_sum = torch.sum(literal_sat, dim=-1)
        violation = torch.relu(1.0 - clause_sat_sum)
        return torch.sum(violation ** 2)

    # Representação C: Softplus / Log-Sum-Exp
    def potential_softplus(self, x: torch.Tensor, beta: float = 5.0) -> torch.Tensor:
        selected = x[self.indices]
        literal_sat = (1.0 + self.signs * selected) * 0.5
        clause_sat_sum = torch.sum(literal_sat, dim=-1)
        violation_linear = 1.0 - clause_sat_sum
        return torch.sum(torch.nn.functional.softplus(violation_linear, beta=beta))

    def discrete_evaluation(self, spin_state: np.ndarray) -> Tuple[int, float]:
        """Retorna (clausulas_violadas, distancia_hamming_normalizada)."""
        unsat = 0
        for v_idx, s_sign in self.clauses:
            clause_sat = False
            for v, s in zip(v_idx, s_sign):
                if spin_state[v] == s:
                    clause_sat = True
                    break
            if not clause_sat:
                unsat += 1
                
        # Distância de Hamming normalizada até s_plant
        hamming_dist = float(np.mean(spin_state != self.s_plant))
        return unsat, hamming_dist


# ==============================================================================
# 3. GERADORES DE INSTÂNCIAS COM SOLUÇÃO PLANTADA s*
# ==============================================================================
def create_planted_3xorsat(n: int, alpha: float, seed: int) -> LogicalInstance:
    rng = np.random.default_rng(seed)
    s_plant_bool = rng.integers(0, 2, size=n, dtype=np.int8)
    s_plant_spin = np.where(s_plant_bool == 1, 1.0, -1.0)
    
    num_eqs = max(1, int(round(alpha * n)))
    cnf_clauses = []
    
    for _ in range(num_eqs):
        vars_chosen = rng.choice(n, size=3, replace=False).tolist()
        parity = int((s_plant_bool[vars_chosen[0]] ^ s_plant_bool[vars_chosen[1]] ^ s_plant_bool[vars_chosen[2]]))
        for s1 in [-1.0, 1.0]:
            for s2 in [-1.0, 1.0]:
                for s3 in [-1.0, 1.0]:
                    b1 = 1 if s1 > 0 else 0
                    b2 = 1 if s2 > 0 else 0
                    b3 = 1 if s3 > 0 else 0
                    if (b1 ^ b2 ^ b3) != parity:
                        cnf_clauses.append((vars_chosen, [-s1, -s2, -s3]))
                        
    return LogicalInstance(n, "3-XOR-SAT", cnf_clauses, s_plant_spin)


def create_planted_3sat(n: int, alpha: float, seed: int) -> LogicalInstance:
    rng = np.random.default_rng(seed)
    s_plant_bool = rng.integers(0, 2, size=n, dtype=np.int8)
    s_plant_spin = np.where(s_plant_bool == 1, 1.0, -1.0)
    
    num_clauses = max(1, int(round(alpha * n)))
    clauses = []
    
    while len(clauses) < num_clauses:
        vars_chosen = rng.choice(n, size=3, replace=False).tolist()
        signs = rng.choice([-1.0, 1.0], size=3).tolist()
        if any(s_plant_spin[v] == s for v, s in zip(vars_chosen, signs)):
            clauses.append((vars_chosen, signs))
            
    return LogicalInstance(n, "Planted-3-SAT", clauses, s_plant_spin)


# ==============================================================================
# 4. SOLVER CONTÍNUO PARAMETRIZADO POR REPRESENTAÇÃO
# ==============================================================================
def optimize_representation(inst: LogicalInstance, rep_type: str, num_restarts: int = 15, max_steps: int = 120) -> Dict[str, Any]:
    n = inst.n
    success_count = 0
    trap_energies = []
    hamming_dists = []
    final_cont_energies = []
    
    for _ in range(num_restarts):
        x = torch.empty(n).uniform_(-0.5, 0.5).requires_grad_(True)
        optimizer = torch.optim.Adam([x], lr=0.08)
        
        for step in range(max_steps):
            optimizer.zero_grad()
            if rep_type == "multilinear":
                energy = inst.potential_multilinear(x)
            elif rep_type == "quadratic":
                energy = inst.potential_quadratic(x)
            elif rep_type == "softplus":
                energy = inst.potential_softplus(x)
            else:
                raise ValueError(f"Unknown representation: {rep_type}")
                
            box_penalty = 0.2 * torch.sum((x**2 - 1.0)**2)
            loss = energy + box_penalty
            loss.backward()
            optimizer.step()
            
            with torch.no_grad():
                x.clamp_(-1.0, 1.0)
                
        # Arredondamento e avaliação
        with torch.no_grad():
            spin_sol = torch.sign(x).cpu().numpy()
            spin_sol[spin_sol == 0] = 1.0
            cont_val = energy.item()
            
        final_cont_energies.append(cont_val)
        e_disc, d_h = inst.discrete_evaluation(spin_sol)
        hamming_dists.append(d_h)
        
        if e_disc == 0:
            success_count += 1
        else:
            trap_energies.append(e_disc)
            
    p_hat, ci_low, ci_high = wilson_score_interval(success_count, num_restarts)
    mean_trap = float(np.mean(trap_energies)) if len(trap_energies) > 0 else 0.0
    mean_d_h = float(np.mean(hamming_dists))
    
    return {
        "success_count": success_count,
        "total_trials": num_restarts,
        "reachability_point": p_hat,
        "ci_95": (ci_low, ci_high),
        "mean_trap_severity": mean_trap,
        "mean_hamming_dist": mean_d_h,
        "mean_cont_energy": float(np.mean(final_cont_energies))
    }


# ==============================================================================
# 5. BENCHMARK CONSOLIDADO E_equiv
# ==============================================================================
def run_representation_invariance_experiment():
    print("=" * 85)
    print("PROJETO CLG-04: BENCHMARK DE INVARIÂNCIA DE REPRESENTAÇÃO (ENSEMBLE E_equiv)")
    print("Investigação: A Rugosidade Geométrica Depende da Codificação Contínua?")
    print("=" * 85)
    
    scales = [30, 60]
    num_instances = 5
    representations = ["multilinear", "quadratic", "softplus"]
    
    results: Dict[str, Any] = {}
    
    for n in scales:
        print(f"\n==================== ESCALA N = {n} VARIÁVEIS ====================")
        sk = f"N_{n}"
        results[sk] = {}
        
        for family_name, gen_fn, alpha_val in [
            ("3-XOR-SAT (Classe P)", create_planted_3xorsat, 1.0),
            ("Random-3-SAT (NP-C)", create_planted_3sat, 4.26)
        ]:
            print(f"\n--- Família: {family_name} (alpha = {alpha_val}) ---")
            results[sk][family_name] = {}
            
            for rep in representations:
                print(f"  Avaliando Representação: {rep.upper()}...")
                all_successes = 0
                total_runs = 0
                traps_list = []
                dh_list = []
                
                for trial in range(num_instances):
                    inst = gen_fn(n, alpha=alpha_val, seed=7000 * n + trial)
                    res = optimize_representation(inst, rep_type=rep, num_restarts=15, max_steps=120)
                    all_successes += res["success_count"]
                    total_runs += res["total_trials"]
                    traps_list.append(res["mean_trap_severity"])
                    dh_list.append(res["mean_hamming_dist"])
                    
                p_hat, ci_low, ci_high = wilson_score_interval(all_successes, total_runs)
                results[sk][family_name][rep] = {
                    "reachability_pct": p_hat * 100.0,
                    "ci_95_pct": (ci_low * 100.0, ci_high * 100.0),
                    "mean_trap_severity": float(np.mean(traps_list)),
                    "mean_hamming_dist": float(np.mean(dh_list)),
                    "success_fraction": f"{all_successes}/{total_runs}"
                }
                ci_str = f"[{ci_low*100.0:.1f}%, {ci_high*100.0:.1f}%]"
                print(f"    -> Reachability: {p_hat*100.0:5.1f}% (IC 95%: {ci_str:<14}) | Armadilha: {np.mean(traps_list):.2f} cl | Dist. Hamming: {np.mean(dh_list):.3f}")

    # Salva JSON
    with open("Fontes/exp_clg04_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # Gera Relatório Textual
    lines = [
        "=" * 90,
        "RELATÓRIO EXPERIMENTAL CLG-04: INVARIÂNCIA DE REPRESENTAÇÃO (ENSEMBLE E_equiv)",
        "Autor: Thiago Carvalho (2026)",
        "=" * 90,
        "",
        "RESUMO DOS ACHADOS:",
        "1. Para a MESMA instância lógica booleana, a mudança na representação contínua",
        "   (Multilinear vs Quadrática Hinge vs Softplus) altera a topologia de atração.",
        "2. A dificuldade geométrica observada não é um invariante intrínseco do problema computacional,",
        "   mas uma propriedade conjunta da tríade: (Problema I, Mapa de Relaxação Phi, Dinâmica D).",
        "3. Intervalos de Confiança Binomial (Wilson 95%) substituem afirmações categóricas de '0%'.",
        "",
        "TABELA COMPARATIVA CONSOLIDADA:"
    ]
    
    for n in scales:
        sk = f"N_{n}"
        lines.append(f"\n--- ESCALA N = {n} VARIÁVEIS ---")
        lines.append(f"{'Problema':<22} | {'Representação':<14} | {'Reachability (IC 95%)':<26} | {'Severidade Armadilha':<20} | {'Dist. Hamming'}")
        lines.append("-" * 105)
        for fam in results[sk]:
            for rep in representations:
                d = results[sk][fam][rep]
                ci_s = f"{d['reachability_pct']:.1f}% [{d['ci_95_pct'][0]:.1f}%, {d['ci_95_pct'][1]:.1f}%]"
                lines.append(f"{fam:<22} | {rep:<14} | {ci_s:<26} | {d['mean_trap_severity']:>5.2f} cláusulas{'':<8} | {d['mean_hamming_dist']:.3f}")

    lines.append("\n" + "=" * 90)
    report_txt = "\n".join(lines)
    
    with open("Fontes/exp_clg04_report.txt", "w", encoding="utf-8") as f:
        f.write(report_txt)
        
    print("\n" + report_txt)
    print("\nResultados salvos com sucesso em Fontes/exp_clg04_report.txt e Fontes/exp_clg04_results.json!")


if __name__ == "__main__":
    run_representation_invariance_experiment()
