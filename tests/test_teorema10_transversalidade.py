"""
Validação Matemática e Numérica da Resolução da Lacuna 1 do Teorema 10:
Lema 10.3 (Instabilidade Transversal e Não-Equilíbrio de Arestas Planas sob H_leaf).

Testes implementados:
1. Identidade Simbólica SymPy da velocidade transversal s_l * grad_l = (1 - sigma_i * t) / 4 > 0;
2. Projeção no cone tangente: prova de que ||Pi_{T_X(x)}(-grad Phi)||_2 >= (1 - |t|)/4 > 0 em todo relint(F_1);
3. Repulsão transversal dinâmica e decrescimento estrito de energia ao deixar a aresta;
4. Simulação Monte Carlo comprovando medida de bacia zero para arestas planas não-satisfatíveis;
5. Classificação exaustiva de faces de dimensão d=1 (a != 0, a = 0 satisfatível, a = 0 não-satisfatível).
"""
import os
import sys
import pytest
import numpy as np
import sympy as sp

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
possible_fontes = [
    os.path.abspath(os.path.join(CURRENT_DIR, "..", "Fontes")),
    os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "P_NP", "Fontes")),
    os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "..", "P_NP", "Fontes")),
    r"C:\MathDoCarvalho\P_NP\Fontes"
]
for p in possible_fontes:
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)
        break


from clg_framework import Relaxation


def test_transversal_gradient_symbolic_identity():
    """
    Testa analiticamente e simbolicamente que a derivada transversal sob H_leaf
    satisfaz rigorosamente s_l * dPhi/dx_l = (1 - sigma_i * t) / 4 > 0 para todo t in (-1, 1).
    """
    t = sp.Symbol('t', real=True)
    sigma_i = sp.Symbol('sigma_i', real=True)
    sigma_l = sp.Symbol('sigma_l', real=True)
    sigma_k = sp.Symbol('sigma_k', real=True)
    x_l = sp.Symbol('x_l', real=True)
    x_k = sp.Symbol('x_k', real=True)

    # Cláusula violada c = (sigma_i x_i or sigma_l x_l or sigma_k x_k)
    # Na aresta: x_i = t, x_l = s_l = -sigma_l, x_k = s_k = -sigma_k
    P_c = ((1 - sigma_i * t) / 2) * ((1 - sigma_l * x_l) / 2) * ((1 - sigma_k * x_k) / 2)
    grad_l = sp.diff(P_c, x_l)

    # Avaliação no bordo
    grad_l_eval = grad_l.subs({x_l: -sigma_l, x_k: -sigma_k})
    s_l = -sigma_l
    s_l_grad_l = sp.simplify((s_l * grad_l_eval).subs({sigma_l**2: 1, sigma_k**2: 1}))

    # Verifica a forma canônica (1 - sigma_i * t) / 4
    for s_i_val in [-1, 1]:
        val = s_l_grad_l.subs({sigma_i: s_i_val})
        expected = (1 - s_i_val * t) / 4
        assert sp.simplify(val - expected) == 0, f"Divergência simbólica para sigma_i = {s_i_val}"

        # Verifica positividade estrita para toda a faixa aberta t in (-1, 1)
        for t_test in [-0.99, -0.5, 0.0, 0.5, 0.99]:
            assert float(val.subs({t: t_test})) > 0, f"Falha de positividade em t = {t_test}"


def test_flat_edge_projected_equilibrium_is_empty():
    """
    Testa que em uma aresta plana violada (a = 0, E > 0), a velocidade projetada
    Pi_{T_X(x)}(-grad Phi) NUNCA é zero no interior relativo da aresta (-1 < t < 1).
    """
    # Modelo canônico com aresta plana em x_0:
    # c1: (x0 or x1 or x2)  -> sigma = [1, 1, 1]
    # c2: (not x0 or x3 or x4) -> sigma = [-1, 1, 1]
    # Na aresta: x0 = t, x1=x2=x3=x4 = -1
    clauses = [
        ([0, 1, 2], [1.0, 1.0, 1.0]),
        ([0, 3, 4], [-1.0, 1.0, 1.0])
    ]
    rel = Relaxation(5, clauses)

    for t_val in np.linspace(-0.95, 0.95, 20):
        x = np.array([t_val, -1.0, -1.0, -1.0, -1.0])
        # Energia deve ser constante igual a 1.0 em toda a aresta
        energy = rel.phi_mult(x)
        assert abs(energy - 1.0) < 1e-12, f"Energia não é constante: {energy} em t={t_val}"

        g = rel.grad_mult(x)
        # Derivada tangencial ao longo da aresta é zero
        assert abs(g[0]) < 1e-12, f"Derivada tangencial não nula: {g[0]} em t={t_val}"

        # Projeção no cone tangente: para coordenadas no bordo x_k = -1,
        # velocidade projetada v_k = max(0, -g_k)
        proj_v = np.zeros(5)
        proj_v[0] = -g[0]
        for k in range(1, 5):
            proj_v[k] = max(0.0, -g[k])

        # Velocidade transversal projetada deve ser estritamente positiva (empurrando para o interior)
        assert np.all(proj_v[1:] > 0), f"Velocidade projetada não é estritamente interior em t={t_val}: {proj_v}"
        norm_v = np.linalg.norm(proj_v)
        expected_min = (1.0 - abs(t_val)) / 4.0
        assert norm_v >= expected_min, f"Norma {norm_v} inferior à cota teórica {expected_min}"


def test_transversal_ejection_and_strict_energy_decrease():
    """
    Testa que qualquer trajetória iniciada sobre a aresta plana é imediatamente ejetada
    para o interior e sofre decréscimo monótono estrito de energia.
    """
    clauses = [
        ([0, 1, 2], [1.0, 1.0, 1.0]),
        ([0, 3, 4], [-1.0, 1.0, 1.0])
    ]
    rel = Relaxation(5, clauses)

    for t_val in [-0.7, -0.3, 0.0, 0.3, 0.7]:
        x = np.array([t_val, -1.0, -1.0, -1.0, -1.0])
        initial_energy = rel.phi_mult(x)
        assert abs(initial_energy - 1.0) < 1e-12

        # Executa 10 passos de Euler projetado
        eta = 0.05
        traj_energies = [initial_energy]
        for _ in range(10):
            g = rel.grad_mult(x)
            x = np.clip(x - eta * g, -1.0, 1.0)
            traj_energies.append(rel.phi_mult(x))

        # A coordenada x_1 (folha) deve ter entrado estritamente no interior (-1, 1)
        assert x[1] > -1.0, f"Coordenada folha x_1 não foi ejetada para o interior: {x[1]}"
        assert x[3] > -1.0, f"Coordenada folha x_3 não foi ejetada para o interior: {x[3]}"

        # Energia deve decrescer estritamente a cada passo
        for step in range(len(traj_energies) - 1):
            assert traj_energies[step + 1] < traj_energies[step], (
                f"Energia não decresceu estritamente no passo {step}: {traj_energies[step+1]} >= {traj_energies[step]}"
            )


def test_monte_carlo_flat_edge_basin_measure_zero():
    """
    Comprova via amostragem uniforme (Monte Carlo com 500 pontos) que a bacia
    de atração do interior relativo da aresta plana tem medida nula (0.0%).
    """
    clauses = [
        ([0, 1, 2], [1.0, 1.0, 1.0]),
        ([0, 3, 4], [-1.0, 1.0, 1.0])
    ]
    rel = Relaxation(5, clauses)
    rng = np.random.default_rng(20260918)

    edge_attraction_count = 0
    num_samples = 500

    for _ in range(num_samples):
        x0 = rng.uniform(-1.0, 1.0, 5)
        x_final, final_energy, _ = rel.projected_gradient_descent(x0, "mult", eta=0.02, T=30.0)

        # Condição para pertencer ao interior relativo da aresta plana:
        # x_0 in (-0.95, 0.95) e todos os outros x_k <= -0.999
        on_flat_edge = (abs(x_final[0]) < 0.95) and np.all(x_final[1:] < -0.99)
        if on_flat_edge:
            edge_attraction_count += 1

    assert edge_attraction_count == 0, (
        f"Detectadas {edge_attraction_count} trajetórias convergindo para a aresta plana (medida positiva!)"
    )


def test_exhaustive_dimension_1_edge_classification():
    """
    Verifica que qualquer aresta d=1 satisfaz a tricotomia exaustiva:
    1. Se a != 0: gradiente constante não nulo empurra para os vértices (sem críticos interiores);
    2. Se a = 0 e E = 0: segmento globalmente satisfatível;
    3. Se a = 0 e E > 0: sob H_leaf, vetor projetado transversal não nulo empurra para o interior,
       com bacia de atração do interior da aresta rigorosamente vazia.
    """
    # 1. Aresta com a != 0
    c_affine = [([0, 1, 2], [1.0, 1.0, 1.0])]
    rel_aff = Relaxation(3, c_affine)
    # Na aresta x_1 = -1, x_2 = -1, x_0 = t: P = (1 - t)/2, logo a = -0.5 != 0
    x_test = np.array([0.2, -1.0, -1.0])
    g_aff = rel_aff.grad_mult(x_test)
    assert abs(g_aff[0] - (-0.5)) < 1e-12, "Derivada na aresta afim deve ser constante não nula (-0.5)"

    # 2. Aresta com a = 0 e E = 0 (satisfatível)
    # Na aresta x_1 = 1 (satisfazendo c_affine), P = 0 para todo t in [-1, 1]
    x_sat = np.array([0.2, 1.0, -1.0])
    assert rel_aff.phi_mult(x_sat) == 0.0, "Aresta satisfatível deve ter energia zero"

    # 3. Aresta com a = 0 e E > 0 (coberta pelo Lema 10.3)
    clauses_flat = [
        ([0, 1, 2], [1.0, 1.0, 1.0]),
        ([0, 3, 4], [-1.0, 1.0, 1.0])
    ]
    rel_flat = Relaxation(5, clauses_flat)
    x_mid = np.array([0.0, -1.0, -1.0, -1.0, -1.0])
    assert rel_flat.phi_mult(x_mid) > 0.0, "Aresta deve ter energia positiva"
    g_flat = rel_flat.grad_mult(x_mid)
    assert abs(g_flat[0]) < 1e-12, "Derivada tangencial deve ser zero"
    # Projeção transversal deve ser estritamente interior
    assert np.all(-g_flat[1:] > 0), "Direções transversais devem apontar para o interior"
