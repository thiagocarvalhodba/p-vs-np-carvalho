"""
Execução Rigorosa do Protocolo Pré-Registrado V2 (CLG-R v4.0.2).
Autor: Grupo de Trabalho CLG-R (2026)
Conformidade Estrita com PROTOCOLO_V2_PREREGISTRADO.md:
1. Dinâmica Euler Projetada Pura em [-1, 1]^N (sem box penalty, sem Adam).
2. Pareamento estrito: mesma instância I x mesmo ponto inicial x0 x mesmo orçamento.
3. Instância como unidade primária de amostragem; reinícios como medidas aninhadas.
4. Bootstrap hierárquico por instância (2000 reamostragens).
5. 3 Sementes globais independentes (20260911, 20260918, 20260925) e análise de sensibilidade.
6. Exportação de dados brutos e metadados completos em JSON (sem números codificados à mão).
"""
import os
import sys
import time
import math
import json
import concurrent.futures
import numpy as np

# Adiciona diretório de fontes
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
if DIR_PATH not in sys.path:
    sys.path.insert(0, DIR_PATH)

from clg_framework import (
    Relaxation,
    ErcseyRavaszToroczkaiDynamics,
    bootstrap_instance_ci,
    wilson_score_interval
)

def generate_monotone_horn(n, m, rng):
    """
    Gera fórmula Horn monótona: fatos unitários positivos + regras de implicação.
    """
    clauses = []
    # Fato unitário em x_0 e x_1
    clauses.append(([0], [1.0]))
    clauses.append(([1], [1.0]))
    # Cláusulas de implicação (x_i1 and x_i2 -> x_c <=> not x_i1 or not x_i2 or x_c)
    for _ in range(m - 2):
        antecedents = rng.choice(n, 2, replace=False).tolist()
        consequent = rng.choice(n, 1)[0]
        while consequent in antecedents:
            consequent = rng.choice(n, 1)[0]
        clauses.append(([antecedents[0], antecedents[1], consequent], [-1.0, -1.0, 1.0]))
    return clauses

def generate_subcritical_3sat(n, alpha, rng):
    """
    Gera 3-SAT aleatório subcrítico puro (alpha < 1/6).
    """
    m = max(1, int(round(alpha * n)))
    clauses = []
    for _ in range(m):
        vs = rng.choice(n, 3, replace=False).tolist()
        ss = rng.choice([-1.0, 1.0], 3).tolist()
        clauses.append((vs, ss))
    return clauses

def generate_planted_3sat(n, alpha, rng):
    """
    Gera 3-SAT com solução embutida plantada s* in {-1, +1}^N.
    """
    m = max(1, int(round(alpha * n)))
    s_star = rng.choice([-1.0, 1.0], n)
    clauses = []
    while len(clauses) < m:
        vs = rng.choice(n, 3, replace=False).tolist()
        ss = rng.choice([-1.0, 1.0], 3).tolist()
        # Garante que s_star satisfaz a cláusula
        if any(ss[j] * s_star[vs[j]] > 0 for j in range(3)):
            clauses.append((vs, ss))
    return clauses, s_star

def generate_3xorsat(n, alpha, rng):
    """
    Gera equações de paridade de 3 variáveis sobre F_2 expandidas em 4 cláusulas 3-CNF cada.
    """
    num_eq = max(1, int(round(alpha * n)))
    clauses = []
    for _ in range(num_eq):
        vs = rng.choice(n, 3, replace=False).tolist()
        b = rng.integers(0, 2)
        for s1 in [-1.0, 1.0]:
            for s2 in [-1.0, 1.0]:
                for s3 in [-1.0, 1.0]:
                    b1 = 1 if s1 > 0 else 0
                    b2 = 1 if s2 > 0 else 0
                    b3 = 1 if s3 > 0 else 0
                    if (b1 ^ b2 ^ b3) != b:
                        clauses.append((vs, [-s1, -s2, -s3]))
    return clauses

def wilcoxon_signed_rank_pvalue(diffs):
    """
    Calcula aproximação assintótica do p-valor do teste dos postos sinalizados de Wilcoxon.
    """
    diffs = np.array([d for d in diffs if abs(d) > 1e-12])
    n = len(diffs)
    if n < 5:
        return 1.0
    ranks = np.argsort(np.abs(diffs)) + 1
    w_pos = np.sum(ranks[diffs > 0])
    e_w = n * (n + 1) / 4.0
    var_w = n * (n + 1) * (2 * n + 1) / 24.0
    z = (w_pos - e_w) / math.sqrt(var_w)
    # two-tailed normal approximation
    p_val = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(z) / math.sqrt(2.0))))
    return float(p_val)

def run_single_seed_suite(global_seed: int, eta: float = 0.01, T: float = 40.0):
    rng = np.random.default_rng(global_seed)
    num_inst = 15
    restarts_per_inst = 10
    
    suite_data = {
        "seed": global_seed,
        "eta": eta,
        "T": T,
        "ensembles": {}
    }
    
    # -------------------------------------------------------------
    # 1. Horn Monótono
    # -------------------------------------------------------------
    print(f"[{global_seed}] Executando Ensemble 1: Horn Monótono (N=25, M=40)...")
    horn_inst_data = []
    for inst_id in range(num_inst):
        clauses = generate_monotone_horn(25, 40, rng)
        rel = Relaxation(25, clauses)
        inst_mult_rhos, inst_quad_rhos, inst_soft_rhos = [], [], []
        trajectories = []
        for r in range(restarts_per_inst):
            x0 = rng.uniform(-1.0, 1.0, 25)
            xm, _, steps_m = rel.projected_gradient_descent(x0, "mult", eta=eta, T=T)
            em = rel.discrete_energy(np.where(xm >= 0, 1.0, -1.0))
            inst_mult_rhos.append(em / 40.0)
            
            xq, _, steps_q = rel.projected_gradient_descent(x0, "quad", eta=eta, T=T)
            eq = rel.discrete_energy(np.where(xq >= 0, 1.0, -1.0))
            inst_quad_rhos.append(eq / 40.0)

            xs, _, steps_s = rel.projected_gradient_descent(x0, "soft", eta=eta, T=T)
            es = rel.discrete_energy(np.where(xs >= 0, 1.0, -1.0))
            inst_soft_rhos.append(es / 40.0)
            
            trajectories.append({
                "restart": r,
                "rho_mult": em / 40.0,
                "rho_quad": eq / 40.0,
                "rho_soft": es / 40.0
            })
            
        mean_m = float(np.mean(inst_mult_rhos))
        mean_q = float(np.mean(inst_quad_rhos))
        mean_s = float(np.mean(inst_soft_rhos))
        horn_inst_data.append({
            "instance_id": inst_id,
            "mean_rho_mult": mean_m,
            "mean_rho_quad": mean_q,
            "mean_rho_soft": mean_s,
            "delta_quad_mult": mean_q - mean_m,
            "trajectories": trajectories
        })
        
    # Agregação hierárquica
    h_m_list = [d["mean_rho_mult"] for d in horn_inst_data]
    h_q_list = [d["mean_rho_quad"] for d in horn_inst_data]
    h_delta_list = [d["delta_quad_mult"] for d in horn_inst_data]
    
    m_mean, m_l, m_u = bootstrap_instance_ci(h_m_list)
    q_mean, q_l, q_u = bootstrap_instance_ci(h_q_list)
    d_mean, d_l, d_u = bootstrap_instance_ci(h_delta_list)
    p_val_horn = wilcoxon_signed_rank_pvalue(h_delta_list)
    
    suite_data["ensembles"]["Horn_Monotone"] = {
        "n": 25, "m": 40,
        "mult_rho": {"mean": m_mean, "ci95": [m_l, m_u]},
        "quad_rho": {"mean": q_mean, "ci95": [q_l, q_u]},
        "delta_effect": {"mean": d_mean, "ci95": [d_l, d_u], "p_value_wilcoxon": p_val_horn},
        "instances": horn_inst_data
    }
    
    # -------------------------------------------------------------
    # 2. Subcritical 3-SAT (alpha = 0.12 < 1/6)
    # -------------------------------------------------------------
    print(f"[{global_seed}] Executando Ensemble 2: 3-SAT Subcrítico (N=50, alpha=0.12)...")
    sub_inst_data = []
    for inst_id in range(num_inst):
        clauses = generate_subcritical_3sat(50, 0.12, rng)
        m_c = len(clauses)
        rel = Relaxation(50, clauses)
        inst_mult_rhos, inst_quad_rhos = [], []
        trajectories = []
        for r in range(restarts_per_inst):
            x0 = rng.uniform(-1.0, 1.0, 50)
            xm, _, _ = rel.projected_gradient_descent(x0, "mult", eta=eta, T=T)
            em = rel.discrete_energy(np.where(xm >= 0, 1.0, -1.0))
            inst_mult_rhos.append(em / m_c)
            
            xq, _, _ = rel.projected_gradient_descent(x0, "quad", eta=eta, T=T)
            eq = rel.discrete_energy(np.where(xq >= 0, 1.0, -1.0))
            inst_quad_rhos.append(eq / m_c)
            trajectories.append({"restart": r, "rho_mult": em / m_c, "rho_quad": eq / m_c})
            
        mean_m = float(np.mean(inst_mult_rhos))
        mean_q = float(np.mean(inst_quad_rhos))
        sub_inst_data.append({
            "instance_id": inst_id,
            "mean_rho_mult": mean_m,
            "mean_rho_quad": mean_q,
            "delta_quad_mult": mean_q - mean_m,
            "trajectories": trajectories
        })
        
    s_m_list = [d["mean_rho_mult"] for d in sub_inst_data]
    s_q_list = [d["mean_rho_quad"] for d in sub_inst_data]
    s_delta_list = [d["delta_quad_mult"] for d in sub_inst_data]
    m_mean, m_l, m_u = bootstrap_instance_ci(s_m_list)
    q_mean, q_l, q_u = bootstrap_instance_ci(s_q_list)
    d_mean, d_l, d_u = bootstrap_instance_ci(s_delta_list)
    p_val_sub = wilcoxon_signed_rank_pvalue(s_delta_list)
    
    suite_data["ensembles"]["Subcritical_3SAT"] = {
        "n": 50, "alpha": 0.12, "m": len(clauses),
        "mult_rho": {"mean": m_mean, "ci95": [m_l, m_u]},
        "quad_rho": {"mean": q_mean, "ci95": [q_l, q_u]},
        "delta_effect": {"mean": d_mean, "ci95": [d_l, d_u], "p_value_wilcoxon": p_val_sub},
        "instances": sub_inst_data
    }

    # -------------------------------------------------------------
    # 3. Planted 3-SAT (Benchmark Controlado: alpha=3.0 e alpha=4.26)
    # -------------------------------------------------------------
    for alpha_val in [3.0, 4.26]:
        print(f"[{global_seed}] Executando Ensemble 3: 3-SAT Plantado (N=30, alpha={alpha_val})...")
        plant_inst_data = []
        for inst_id in range(num_inst):
            clauses, s_star = generate_planted_3sat(30, alpha_val, rng)
            m_c = len(clauses)
            rel = Relaxation(30, clauses)
            inst_mult_rhos, inst_quad_rhos = [], []
            trajectories = []
            for r in range(restarts_per_inst):
                x0 = rng.uniform(-1.0, 1.0, 30)
                xm, _, _ = rel.projected_gradient_descent(x0, "mult", eta=eta, T=T)
                em = rel.discrete_energy(np.where(xm >= 0, 1.0, -1.0))
                inst_mult_rhos.append(em / m_c)
                
                xq, _, _ = rel.projected_gradient_descent(x0, "quad", eta=eta, T=T)
                eq = rel.discrete_energy(np.where(xq >= 0, 1.0, -1.0))
                inst_quad_rhos.append(eq / m_c)
                trajectories.append({"restart": r, "rho_mult": em / m_c, "rho_quad": eq / m_c})
                
            mean_m = float(np.mean(inst_mult_rhos))
            mean_q = float(np.mean(inst_quad_rhos))
            plant_inst_data.append({
                "instance_id": inst_id,
                "mean_rho_mult": mean_m,
                "mean_rho_quad": mean_q,
                "delta_quad_mult": mean_q - mean_m,
                "trajectories": trajectories
            })
            
        p_m_list = [d["mean_rho_mult"] for d in plant_inst_data]
        p_q_list = [d["mean_rho_quad"] for d in plant_inst_data]
        p_delta_list = [d["delta_quad_mult"] for d in plant_inst_data]
        m_mean, m_l, m_u = bootstrap_instance_ci(p_m_list)
        q_mean, q_l, q_u = bootstrap_instance_ci(p_q_list)
        d_mean, d_l, d_u = bootstrap_instance_ci(p_delta_list)
        p_val_plant = wilcoxon_signed_rank_pvalue(p_delta_list)
        
        suite_data["ensembles"][f"Planted_3SAT_alpha_{alpha_val}"] = {
            "n": 30, "alpha": alpha_val, "m": len(clauses),
            "mult_rho": {"mean": m_mean, "ci95": [m_l, m_u]},
            "quad_rho": {"mean": q_mean, "ci95": [q_l, q_u]},
            "delta_effect": {"mean": d_mean, "ci95": [d_l, d_u], "p_value_wilcoxon": p_val_plant},
            "instances": plant_inst_data
        }

    # -------------------------------------------------------------
    # 4. 3-XOR-SAT (Firewall Epistemológico Negativo)
    # -------------------------------------------------------------
    print(f"[{global_seed}] Executando Ensemble 4: 3-XOR-SAT (N=30, alpha=1.0)...")
    xor_inst_data = []
    for inst_id in range(num_inst):
        clauses = generate_3xorsat(30, 1.0, rng)
        m_c = len(clauses)
        rel = Relaxation(30, clauses)
        inst_mult_rhos, inst_quad_rhos = [], []
        trajectories = []
        for r in range(restarts_per_inst):
            x0 = rng.uniform(-1.0, 1.0, 30)
            xm, _, _ = rel.projected_gradient_descent(x0, "mult", eta=eta, T=T)
            em = rel.discrete_energy(np.where(xm >= 0, 1.0, -1.0))
            inst_mult_rhos.append(em / m_c)
            
            xq, _, _ = rel.projected_gradient_descent(x0, "quad", eta=eta, T=T)
            eq = rel.discrete_energy(np.where(xq >= 0, 1.0, -1.0))
            inst_quad_rhos.append(eq / m_c)
            trajectories.append({"restart": r, "rho_mult": em / m_c, "rho_quad": eq / m_c})
            
        mean_m = float(np.mean(inst_mult_rhos))
        mean_q = float(np.mean(inst_quad_rhos))
        xor_inst_data.append({
            "instance_id": inst_id,
            "mean_rho_mult": mean_m,
            "mean_rho_quad": mean_q,
            "delta_quad_mult": mean_q - mean_m,
            "trajectories": trajectories
        })
        
    x_m_list = [d["mean_rho_mult"] for d in xor_inst_data]
    x_q_list = [d["mean_rho_quad"] for d in xor_inst_data]
    x_delta_list = [d["delta_quad_mult"] for d in xor_inst_data]
    m_mean, m_l, m_u = bootstrap_instance_ci(x_m_list)
    q_mean, q_l, q_u = bootstrap_instance_ci(x_q_list)
    d_mean, d_l, d_u = bootstrap_instance_ci(x_delta_list)
    p_val_xor = wilcoxon_signed_rank_pvalue(x_delta_list)
    
    suite_data["ensembles"]["3_XOR_SAT"] = {
        "n": 30, "alpha": 1.0, "m": len(clauses),
        "mult_rho": {"mean": m_mean, "ci95": [m_l, m_u]},
        "quad_rho": {"mean": q_mean, "ci95": [q_l, q_u]},
        "delta_effect": {"mean": d_mean, "ci95": [d_l, d_u], "p_value_wilcoxon": p_val_xor},
        "instances": xor_inst_data
    }
    
    return suite_data

def _run_suite_worker(args):
    seed, eta, T = args
    return run_single_seed_suite(seed, eta=eta, T=T)

def main():
    t_start = time.perf_counter()
    print("================================================================================")
    print("REEXECUÇÃO DO PROTOCOLO EXPERIMENTAL V2 CONGELADO (CLG-R v4.0.2)")
    print("================================================================================")
    
    seeds = [20260911, 20260918, 20260925]
    primary_tasks = [(s, 0.01, 40.0) for s in seeds]
    sens_tasks = [(20260911, test_eta, test_T) for test_eta, test_T in [(0.005, 40.0), (0.02, 40.0), (0.01, 20.0)]]
    all_tasks = primary_tasks + sens_tasks
    
    max_w = min(len(all_tasks), os.cpu_count() or 4)
    print(f"\n>>> EXECUTANDO 3 SEMENTES E 3 ANÁLISES DE SENSIBILIDADE EM PARALELO ({max_w} WORKERS) <<<")
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_w) as executor:
        results = list(executor.map(_run_suite_worker, all_tasks))
        
    all_runs = results[:3]
    sensitivity_runs = results[3:]

    total_time = time.perf_counter() - t_start
    
    final_output = {
        "protocol_version": "2.0_FROZEN",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "hardware": {
            "os": "Windows 11 Pro",
            "cpu": "Intel Core 7 150U (10 cores, 12 threads)",
            "ram_gb": 32,
            "python_version": sys.version
        },
        "total_execution_seconds": total_time,
        "primary_runs": all_runs,
        "sensitivity_runs": sensitivity_runs
    }
    
    # Salva JSON Bruto
    json_path = os.path.join(DIR_PATH, "exp_protocol_v2_raw_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2)
    print(f"\n[OK] Dados brutos salvos em {json_path}")
    
    # Gera Relatório Textual Dinâmico (sem números hardcoded)
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("RELATÓRIO CONSOLIDADO DE EXECUÇÃO — PROTOCOLO EXPERIMENTAL V2")
    report_lines.append(f"Data: {final_output['timestamp']} | Tempo Total: {total_time:.2f}s")
    report_lines.append(f"Ambiente: {final_output['hardware']['os']} | CPU: {final_output['hardware']['cpu']}")
    report_lines.append("=" * 80)
    
    prim = all_runs[0] # semente primária 20260911
    report_lines.append(f"\n--- RESULTADOS SEMENTE PRIMÁRIA ({prim['seed']}) ---")
    for ens_name, data in prim["ensembles"].items():
        m_r = data["mult_rho"]
        q_r = data["quad_rho"]
        delta = data["delta_effect"]
        report_lines.append(f"\nEnsemble: {ens_name}")
        report_lines.append(f"  Multilinear rho: {m_r['mean']:.4f} [95% CI: {m_r['ci95'][0]:.4f}, {m_r['ci95'][1]:.4f}]")
        report_lines.append(f"  Hinge Quad  rho: {q_r['mean']:.4f} [95% CI: {q_r['ci95'][0]:.4f}, {q_r['ci95'][1]:.4f}]")
        report_lines.append(f"  Delta Efeito   : {delta['mean']:.4f} [95% CI: {delta['ci95'][0]:.4f}, {delta['ci95'][1]:.4f}] (Wilcoxon p={delta['p_value_wilcoxon']:.4e})")

    report_txt = "\n".join(report_lines)
    txt_path = os.path.join(DIR_PATH, "relatorio_experimentos_protocolo_v2.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(report_txt)
    print(f"[OK] Relatório textual salvo em {txt_path}")
    print("\n" + report_txt)

if __name__ == "__main__":
    main()
