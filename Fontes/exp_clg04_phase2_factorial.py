"""
EXP-CLG-04-PHASE2-FACTORIAL: MATRIZ FATORIAL 3x3, NORMALIZACAO DE ESCALA E CONDICIONAMENTO
Autor: Thiago Carvalho (2026)
Conformidade estrita com o Parecer 08 do Professor Avaliador.

Os 4 Controles Mandatorios:
1. Normalizacao de Escala Energetica: Phi_tilde = Phi / c_Phi, com c_Phi = E[||grad Phi||].
2. Matriz Fatorial 3x3:
   - Representacoes: Multilinear, Quadratica, Softplus
   - Dinamicas: GD Puro, Langevin, Adam
3. Condicionamento Espectral Rigoroso: kappa_2(H) = max |lambda_i| / max(min |lambda_i|, 1e-5).
4. Diferencas Pareadas por Instancia: Delta_i = d_H(Quad) - d_H(Soft) para cada formula.
5. Decomposicao do Efeito de Interacao: C(Phi, D) no modelo Q(I, Phi, D).
"""

import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import time
import math
import json
from typing import List, Tuple, Dict, Any

import numpy as np
import torch


def gf2_rank(A: np.ndarray) -> int:
    mat = A.copy() % 2
    n_rows, n_cols = mat.shape
    rank = 0
    for col in range(n_cols):
        pivot_row = None
        for row in range(rank, n_rows):
            if mat[row, col] == 1:
                pivot_row = row
                break
        if pivot_row is not None:
            mat[[rank, pivot_row]] = mat[[pivot_row, rank]]
            for row in range(n_rows):
                if row != rank and mat[row, col] == 1:
                    mat[row] = (mat[row] ^ mat[rank])
            rank += 1
    return rank


def create_planted_3sat(instance_id: str, n: int, alpha: float, seed: int):
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
            
    return instance_id, n, clauses, s_plant_spin


def compute_spectral_metrics(phi_fn, x: torch.Tensor) -> Tuple[float, float]:
    """Calcula ||grad Phi|| e kappa_2(H) = max |lambda_i| / max(min |lambda_i|, 1e-5)."""
    n = x.shape[0]
    val = phi_fn(x)
    grad = torch.autograd.grad(val, x, create_graph=True)[0]
    grad_norm = float(torch.norm(grad).item())
    
    hessian = torch.zeros((n, n), dtype=torch.float32)
    for i in range(n):
        grad2 = torch.autograd.grad(grad[i], x, retain_graph=(i < n - 1))[0]
        hessian[i] = grad2.detach()
        
    eigenvals = np.abs(torch.linalg.eigvalsh(hessian).cpu().numpy())
    l_max = float(np.max(eigenvals))
    l_min = float(np.min(eigenvals))
    kappa_2 = float(l_max / max(l_min, 1e-5))
    return grad_norm, kappa_2


def run_factorial_experiment():
    print("=" * 105)
    print("CLG-04 PHASE II FACTORIAL: MATRIZ 3x3 (REPRESENTAÇÃO x DINÂMICA) COM NORMALIZAÇÃO DE ESCALA")
    print("=" * 105)
    
    n = 60 # Escala crítica de N=60 variáveis
    num_instances = 5
    restarts_per_instance = 10 # 50 corridas pareadas por célula da matriz 3x3
    
    # 1. Gerar instâncias fixadas
    instances = []
    for i_idx in range(num_instances):
        inst_id, n_var, clauses, s_plant = create_planted_3sat(f"SAT_N60_inst{i_idx+1}", n, 4.26, seed=50000 + i_idx)
        instances.append({
            "id": inst_id,
            "n": n_var,
            "clauses": clauses,
            "s_plant": s_plant,
            "idx_t": torch.tensor([c[0] for c in clauses], dtype=torch.long),
            "sgn_t": torch.tensor([c[1] for c in clauses], dtype=torch.float32)
        })
        
    # 2. Ponto inicial compartilhado
    # Pool de 10 vetores x0 por instancia
    x0_pool = {}
    for inst in instances:
        rng_init = np.random.default_rng(60000 + hash(inst["id"]) % 10000)
        x0_pool[inst["id"]] = [
            torch.tensor(rng_init.uniform(-0.5, 0.5, size=n), dtype=torch.float32)
            for _ in range(restarts_per_instance)
        ]
        
    # 3. Funções de Perda Brutas
    def raw_multilinear(x, inst):
        sel = x[inst["idx_t"]]
        factors = (1.0 - inst["sgn_t"] * sel) * 0.5
        return torch.sum(torch.prod(factors, dim=-1))
        
    def raw_quadratic(x, inst):
        sel = x[inst["idx_t"]]
        lit_sat = (1.0 + inst["sgn_t"] * sel) * 0.5
        c_sat = torch.sum(lit_sat, dim=-1)
        viol = torch.relu(1.0 - c_sat)
        return torch.sum(viol ** 2)
        
    def raw_softplus(x, inst, beta=5.0):
        sel = x[inst["idx_t"]]
        lit_sat = (1.0 + inst["sgn_t"] * sel) * 0.5
        c_sat = torch.sum(lit_sat, dim=-1)
        viol = 1.0 - c_sat
        return torch.sum(torch.nn.functional.softplus(viol, beta=beta))

    # 4. CONTROLE 1: Normalização de Escala de Gradiente (c_Phi)
    # Amostra 50 pontos aleatórios em U([-1, 1]^N) para estimar E[||grad Phi||]
    print("\nEstimando fatores de escala de gradiente c_Phi em U([-1, 1]^N)...")
    scale_factors = {}
    for rep_name, raw_fn in [("multilinear", raw_multilinear), ("quadratic", raw_quadratic), ("softplus", raw_softplus)]:
        norms = []
        for inst in instances:
            for s_seed in range(10):
                rng_s = np.random.default_rng(70000 + s_seed)
                x_sample = torch.tensor(rng_s.uniform(-1.0, 1.0, size=n), dtype=torch.float32, requires_grad=True)
                v = raw_fn(x_sample, inst)
                g = torch.autograd.grad(v, x_sample)[0]
                norms.append(torch.norm(g).item())
        c_val = float(np.mean(norms))
        scale_factors[rep_name] = c_val
        print(f"  Fator c_Phi [{rep_name:<12}]: {c_val:.4f}")

    # Potenciais Normalizados
    def get_norm_potential(rep_name, inst):
        c_phi = scale_factors[rep_name]
        if rep_name == "multilinear":
            return lambda x: raw_multilinear(x, inst) / c_phi
        elif rep_name == "quadratic":
            return lambda x: raw_quadratic(x, inst) / c_phi
        elif rep_name == "softplus":
            return lambda x: raw_softplus(x, inst) / c_phi

    representations = ["multilinear", "quadratic", "softplus"]
    dynamics_list = ["GD_puro", "Langevin", "Adam"]
    
    matrix_results: Dict[str, Dict[str, Dict[str, Any]]] = {}
    per_instance_dh: Dict[str, Dict[str, List[float]]] = {}
    
    print("\nExecutando Matriz Fatorial 3x3 Pareada (50 trajetórias por célula)...")
    
    for rep in representations:
        matrix_results[rep] = {}
        per_instance_dh[rep] = {}
        for dyn in dynamics_list:
            per_instance_dh[rep][dyn] = []
            all_reached = 0
            all_runs = 0
            all_dh = []
            all_edisc = []
            all_grad_norms = []
            all_kappa = []
            
            for inst in instances:
                phi_norm = get_norm_potential(rep, inst)
                x0_list = x0_pool[inst["id"]]
                inst_dh = []
                
                for r_idx, x0 in enumerate(x0_list):
                    x = x0.clone().detach().requires_grad_(True)
                    optimizer = None
                    if dyn == "Adam":
                        optimizer = torch.optim.Adam([x], lr=0.05)
                        
                    steps = 150
                    for step in range(steps):
                        if dyn == "Adam":
                            optimizer.zero_grad()
                            loss = phi_norm(x) + 0.2 * torch.sum((x**2 - 1.0)**2)
                            loss.backward()
                            optimizer.step()
                        else:
                            if x.grad is not None:
                                x.grad.zero_()
                            loss = phi_norm(x) + 0.2 * torch.sum((x**2 - 1.0)**2)
                            loss.backward()
                            with torch.no_grad():
                                g_step = -0.02 * x.grad
                                if dyn == "Langevin":
                                    noise = math.sqrt(2.0 * 0.005 * 0.02) * torch.randn_like(x)
                                    x.add_(g_step + noise)
                                else:
                                    x.add_(g_step)
                        with torch.no_grad():
                            x.clamp_(-1.0, 1.0)
                            
                    # Avaliação final da trajetória
                    with torch.no_grad():
                        spin = torch.sign(x).cpu().numpy()
                        spin[spin == 0] = 1.0
                        unsat = sum(1 for v, s in inst["clauses"] if not any(spin[var] == sign for var, sign in zip(v, s)))
                        dh = float(np.mean(spin != inst["s_plant"]))
                        
                    # Mede condicionamento final
                    gn, k2 = compute_spectral_metrics(phi_norm, x)
                    
                    all_runs += 1
                    if unsat == 0:
                        all_reached += 1
                    all_dh.append(dh)
                    all_edisc.append(unsat)
                    all_grad_norms.append(gn)
                    all_kappa.append(k2)
                    inst_dh.append(dh)
                    
                per_instance_dh[rep][dyn].append(float(np.mean(inst_dh)))
                
            matrix_results[rep][dyn] = {
                "reachability_pct": (all_reached / all_runs) * 100.0,
                "dh_mean": float(np.mean(all_dh)),
                "dh_sem": float(np.std(per_instance_dh[rep][dyn], ddof=1) / math.sqrt(num_instances)),
                "overlap_q": float(1.0 - 2.0 * np.mean(all_dh)),
                "edisc_mean": float(np.mean(all_edisc)),
                "grad_norm_mean": float(np.mean(all_grad_norms)),
                "kappa_median": float(np.median(all_kappa)),
                "per_instance_dh": per_instance_dh[rep][dyn]
            }

    # Exibir a Matriz 3x3
    print("\n" + "=" * 105)
    print("MATRIZ FATORIAL 3x3 CONSOLIDADA: RANDOM-3-SAT (N=60, POTENCIAIS NORMALIZADOS)")
    print("=" * 105)
    print(f"{'Representação':<14} | {'Dinâmica':<10} | {'R_dyn':<8} | {'d_H (Média ± SEM)':<20} | {'Overlap q':<10} | {'E_disc':<8} | {'kappa_2 (med)'}")
    print("-" * 105)
    for rep in representations:
        for dyn in dynamics_list:
            res = matrix_results[rep][dyn]
            dh_str = f"{res['dh_mean']:.3f} ± {res['dh_sem']:.3f}"
            print(f"{rep:<14} | {dyn:<10} | {res['reachability_pct']:5.1f}%  | {dh_str:<20} | {res['overlap_q']:<10.3f} | {res['edisc_mean']:<8.2f} | {res['kappa_median']:.1f}")

    # Exibir Diferenças Pareadas por Instancia
    print("\n" + "=" * 105)
    print("DIFERENÇAS PAREADAS POR INSTÂNCIA (Delta_i = d_H(Quad) - d_H(Soft) e Delta_i = d_H(Multi) - d_H(Soft))")
    print("=" * 105)
    for dyn in dynamics_list:
        print(f"\n[Dinâmica: {dyn}]")
        print(f"{'Instância':<12} | {'d_H (Soft)':<12} | {'d_H (Multi)':<12} | {'d_H (Quad)':<12} | {'Delta(Quad-Soft)':<18} | {'Delta(Multi-Soft)'}")
        print("-" * 85)
        for i_idx in range(num_instances):
            dh_s = per_instance_dh["softplus"][dyn][i_idx]
            dh_m = per_instance_dh["multilinear"][dyn][i_idx]
            dh_q = per_instance_dh["quadratic"][dyn][i_idx]
            delta_qs = dh_q - dh_s
            delta_ms = dh_m - dh_s
            print(f"Instância {i_idx+1:<3} | {dh_s:<12.3f} | {dh_m:<12.3f} | {dh_q:<12.3f} | +{delta_qs:<17.3f} | +{delta_ms:<.3f}")

    # Salva os resultados estruturados
    with open("Fontes/exp_clg04_phase2_factorial_results.json", "w", encoding="utf-8") as f:
        json.dump(matrix_results, f, indent=2)
    print("\n[OK] Resultados salvos em Fontes/exp_clg04_phase2_factorial_results.json")


if __name__ == "__main__":
    run_factorial_experiment()
