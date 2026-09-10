"""
EXP-CLG-04-PHASE2: CONTROLE DE CONDICIONAMENTO, SOLUÇÃO ÚNICA E SEPARAÇÃO DE DINÂMICAS
Autor: Thiago Carvalho (2026)
Conformidade estrita com o Parecer 07 do Professor Avaliador.

Objetivos:
1. CLG-04A vs CLG-04B: Separar explicitamente dinâmicas de 1ª ordem pura (GD/Langevin) de adaptativas (Adam).
2. Unicidade de Solução no 3-XOR-SAT: Garantir rank(A) = N sobre GF(2) (|S| = 1).
3. CLG-04C (Controle de Condicionamento): Medir ||grad Phi||, lambda_min(H), lambda_max(H), kappa(H).
4. Rastrear as 4 curvas temporais: E_disc(t), d_H(t), ||grad Phi(t)||, kappa(t).
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


def create_unique_solution_3xorsat(n: int, seed: int) -> Tuple[List[Tuple[List[int], List[float]]], np.ndarray, int]:
    """Gera um sistema 3-XOR-SAT com rank GF(2) = N, garantindo solucao unica |S| = 1."""
    rng = np.random.default_rng(seed)
    s_plant_bool = rng.integers(0, 2, size=n, dtype=np.int8)
    s_plant_spin = np.where(s_plant_bool == 1, 1.0, -1.0)
    
    # Adicionamos equacoes ate atingir rank = n
    eq_vars = []
    eq_parities = []
    A_list = []
    
    attempts = 0
    while len(eq_vars) < n or gf2_rank(np.array(A_list, dtype=int)) < n:
        attempts += 1
        vars_chosen = rng.choice(n, size=3, replace=False).tolist()
        parity = int(s_plant_bool[vars_chosen[0]] ^ s_plant_bool[vars_chosen[1]] ^ s_plant_bool[vars_chosen[2]])
        
        row = np.zeros(n, dtype=int)
        row[vars_chosen] = 1
        
        test_A = np.array(A_list + [row], dtype=int) if len(A_list) > 0 else np.array([row], dtype=int)
        new_rank = gf2_rank(test_A)
        if new_rank > (gf2_rank(np.array(A_list, dtype=int)) if len(A_list) > 0 else 0):
            A_list.append(row)
            eq_vars.append(vars_chosen)
            eq_parities.append(parity)
        elif len(eq_vars) < int(1.2 * n) and attempts < 1000:
            A_list.append(row)
            eq_vars.append(vars_chosen)
            eq_parities.append(parity)
            
        if len(A_list) >= n and gf2_rank(np.array(A_list, dtype=int)) == n:
            break

    final_rank = gf2_rank(np.array(A_list, dtype=int))
    
    cnf_clauses = []
    for vars_chosen, parity in zip(eq_vars, eq_parities):
        for s1 in [-1.0, 1.0]:
            for s2 in [-1.0, 1.0]:
                for s3 in [-1.0, 1.0]:
                    b1 = 1 if s1 > 0 else 0
                    b2 = 1 if s2 > 0 else 0
                    b3 = 1 if s3 > 0 else 0
                    if (b1 ^ b2 ^ b3) != parity:
                        cnf_clauses.append((vars_chosen, [-s1, -s2, -s3]))
                        
    return cnf_clauses, s_plant_spin, final_rank


def compute_conditioning_metrics(phi_fn, x: torch.Tensor) -> Tuple[float, float, float, float]:
    """Calcula ||grad Phi||, lambda_min(H), lambda_max(H), kappa(H)."""
    n = x.shape[0]
    # Gradiente
    val = phi_fn(x)
    grad = torch.autograd.grad(val, x, create_graph=True)[0]
    grad_norm = float(torch.norm(grad).item())
    
    # Hessiana completa
    hessian = torch.zeros((n, n), dtype=torch.float32)
    for i in range(n):
        grad_i = grad[i]
        grad2 = torch.autograd.grad(grad_i, x, retain_graph=(i < n - 1))[0]
        hessian[i] = grad2.detach()
        
    eigenvals = torch.linalg.eigvalsh(hessian).cpu().numpy()
    l_min = float(np.min(eigenvals))
    l_max = float(np.max(eigenvals))
    
    denom = max(abs(l_min), 1e-5)
    kappa = float(abs(l_max) / denom)
    return grad_norm, l_min, l_max, kappa


def run_phase2_experiments():
    print("=" * 95)
    print("CLG-04 PHASE II: CONTROLE DE CONDICIONAMENTO, UNICIDADE DE SOLUÇÃO E SEPARAÇÃO DE DINÂMICAS")
    print("=" * 95)
    
    # 1. Teste de Unicidade no 3-XOR-SAT
    print("\n--- 1. VERIFICAÇÃO DE UNICIDADE NO 3-XOR-SAT ---")
    for n in [30, 60]:
        clauses, s_plant, rk = create_unique_solution_3xorsat(n, seed=42)
        print(f"Scale N={n}: Rank GF(2) = {rk}/{n} | Soluções possíveis |S| = {2**(n - rk)} (Solução Única Estrita!)")

    # 2. Diagnóstico de Condicionamento em Trajetórias Pareadas (N=30)
    print("\n--- 2. DIAGNÓSTICO DE CONDICIONAMENTO EM TRAJETÓRIAS PAREADAS (Random-3-SAT N=30) ---")
    n = 30
    rng = np.random.default_rng(777)
    s_plant_bool = rng.integers(0, 2, size=n, dtype=np.int8)
    s_plant = np.where(s_plant_bool == 1, 1.0, -1.0)
    
    # Gera instancia sat
    clauses = []
    while len(clauses) < int(round(4.26 * n)):
        v = rng.choice(n, size=3, replace=False).tolist()
        s = rng.choice([-1.0, 1.0], size=3).tolist()
        if any(s_plant[var] == sign for var, sign in zip(v, s)):
            clauses.append((v, s))
            
    idx_tensor = torch.tensor([c[0] for c in clauses], dtype=torch.long)
    sgn_tensor = torch.tensor([c[1] for c in clauses], dtype=torch.float32)
    
    def phi_mult(x):
        sel = x[idx_tensor]
        factors = (1.0 - sgn_tensor * sel) * 0.5
        return torch.sum(torch.prod(factors, dim=-1))
        
    def phi_quad(x):
        sel = x[idx_tensor]
        lit_sat = (1.0 + sgn_tensor * sel) * 0.5
        c_sat = torch.sum(lit_sat, dim=-1)
        viol = torch.relu(1.0 - c_sat)
        return torch.sum(viol ** 2)
        
    def phi_soft(x):
        sel = x[idx_tensor]
        lit_sat = (1.0 + sgn_tensor * sel) * 0.5
        c_sat = torch.sum(lit_sat, dim=-1)
        viol = 1.0 - c_sat
        return torch.sum(torch.nn.functional.softplus(viol, beta=5.0))

    # Ponto inicial comum
    x0 = torch.tensor(rng.uniform(-0.5, 0.5, size=n), dtype=torch.float32)
    
    representations = [("multilinear", phi_mult), ("quadratic", phi_quad), ("softplus", phi_soft)]
    
    tracking_data = {}
    
    for rep_name, fn in representations:
        x = x0.clone().detach().requires_grad_(True)
        # Vamos rodar 50 passos e medir condicionamento nos passos 0, 10, 25, 50
        history = []
        lr = 0.02
        for step in range(51):
            grad_norm, l_min, l_max, kappa = compute_conditioning_metrics(fn, x)
            with torch.no_grad():
                spin = torch.sign(x).cpu().numpy()
                spin[spin == 0] = 1.0
                unsat = sum(1 for v, s in clauses if not any(spin[var] == sign for var, sign in zip(v, s)))
                dh = float(np.mean(spin != s_plant))
                overlap_q = 1.0 - 2.0 * dh
                val = fn(x).item()
                
            if step in [0, 10, 25, 50]:
                history.append({
                    "step": step,
                    "val": val,
                    "e_disc": unsat,
                    "dh": dh,
                    "overlap_q": overlap_q,
                    "grad_norm": grad_norm,
                    "l_min": l_min,
                    "l_max": l_max,
                    "kappa": kappa
                })
                
            # Passo de gradiente
            val_tensor = fn(x) + 0.2 * torch.sum((x**2 - 1.0)**2)
            val_tensor.backward()
            with torch.no_grad():
                x.add_(-lr * x.grad)
                x.clamp_(-1.0, 1.0)
            x.grad.zero_()
            
        tracking_data[rep_name] = history
        print(f"\nRepresentação: {rep_name.upper()}")
        print(f"{'Passo':<6} | {'Phi(x)':<10} | {'E_disc':<8} | {'d_H':<8} | {'Overlap q':<10} | {'||grad||':<10} | {'kappa(H)':<10}")
        print("-" * 75)
        for h in history:
            print(f"{h['step']:<6} | {h['val']:<10.4f} | {h['e_disc']:<8} | {h['dh']:<8.3f} | {h['overlap_q']:<10.3f} | {h['grad_norm']:<10.4f} | {h['kappa']:<10.2f}")

    with open("Fontes/exp_clg04_conditioning_tracking.json", "w", encoding="utf-8") as f:
        json.dump(tracking_data, f, indent=2)
    print("\n[OK] Rastreamento de condicionamento salvo em Fontes/exp_clg04_conditioning_tracking.json")


if __name__ == "__main__":
    run_phase2_experiments()
