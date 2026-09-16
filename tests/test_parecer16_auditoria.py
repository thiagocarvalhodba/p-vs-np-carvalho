"""
Suíte de Testes Matemáticos e Dinâmicos — Auditoria Cirúrgica Parecer nº 16.
Verifica programaticamente:
1. Sinal da matriz Jacobiana da Proposição 7A (J_{ij} <= 0, dinâmica competitiva).
2. Cota inferior analítica de dimensão finita do Teorema 8 (E[mu(Z)] >= (5/6)^{alpha N} > 0).
3. Classificação analítica de faces d=1 (arestas) no Teorema 10:
   - Se a != 0: sem ponto crítico no interior aberto (-1, 1).
   - Se a == 0: variedade crítica degenerada flat com energia constante.
4. Cota de primeiro momento do Lema 10.1: E[X] <= 9 alpha^2 = O(1).
"""
import pytest
import numpy as np
import sympy as sp

def test_prop7a_jacobian_competitive_sign():
    """
    Verifica que para cláusulas puramente negativas P_c(x) = (1+x_i)(1+x_j)(1+x_k)/8,
    a derivada cruzada d^2 P_c / dx_i dx_j = (1+x_k)/8 >= 0 em [-1, 1]^N.
    Consequentemente, o Jacobiano do campo gradiente f = -grad Phi é
    J_{ij} = -d^2 Phi / dx_i dx_j <= 0 (competitivo/inibitório), NUNCA cooperativo (J_{ij} >= 0).
    """
    xi, xj, xk = sp.symbols('xi xj xk')
    Pc = (1 + xi) * (1 + xj) * (1 + xk) / 8
    
    # Derivada cruzada
    d2_Pc = sp.diff(Pc, xi, xj)
    expected_d2 = (1 + xk) / 8
    assert sp.simplify(d2_Pc - expected_d2) == 0
    
    # Campo f_i = -dPc/dxi
    # Jacobiano J_ij = df_i/dxj = -d^2 Pc / (dxi dxj)
    J_ij = -d2_Pc
    
    # Avaliar para uma grade de pontos xk em [-1, 1]
    grid_xk = np.linspace(-1.0, 1.0, 21)
    for val_k in grid_xk:
        val_d2 = float(expected_d2.subs(xk, val_k))
        val_J = float(J_ij.subs(xk, val_k))
        assert val_d2 >= -1e-12, f"d^2 P_c / dx_i dx_j deve ser >= 0, obteve {val_d2}"
        assert val_J <= 1e-12, f"J_ij deve ser <= 0 (competitivo), obteve {val_J}"

def test_teorema8_finite_lower_bound():
    """
    Verifica que a cota de Jensen garante E[mu(Z)] >= (5/6)^{floor(alpha N)} > 0
    para qualquer N finito, mas a cota inferior em si decai exponencialmente para 0,
    o que NÃO prova que mu(Z) -> 0 sem uma cota superior independente.
    """
    alpha = 0.12
    for N in [5, 10, 20, 50, 100]:
        M = int(np.floor(alpha * N))
        lower_bound = (5.0 / 6.0) ** M
        assert lower_bound > 0.0, f"Cota inferior deve ser estritamente positiva para N={N}"
        assert lower_bound <= 1.0, f"Cota inferior deve ser <= 1"
    
    # Demonstração do contra-exemplo matemático apontado pelo Professor:
    # Se f(N) = 0.5 (constante), f(N) >= (5/6)^N para todo N >= 4, mas lim f(N) = 0.5 != 0.
    N_test = np.arange(4, 50)
    cota = (5.0 / 6.0) ** N_test
    assert np.all(0.5 >= cota), "Contra-exemplo: cota inferior decrescente não implica convergência a zero de f"

def test_teorema10_edge_classification():
    """
    Verifica a classificação analítica exata de uma face de dimensão d = 1 (aresta):
    Phi(t) = a * t + b para t em [-1, 1].
    - Caso 1: a != 0 => grad_F Phi = a != 0, nenhum ponto crítico em (-1, 1).
    - Caso 2: a == 0 => grad_F Phi == 0, toda a aresta é variedade crítica degenerada flat.
    """
    t = sp.symbols('t')
    a, b = sp.symbols('a b')
    phi_edge = a * t + b
    grad_edge = sp.diff(phi_edge, t)
    
    # Se a != 0
    assert grad_edge == a
    # A equação grad_edge == 0 não tem solução em t quando a != 0
    critical_pts_generic = sp.solve(grad_edge.subs(a, 2.5), t)
    assert len(critical_pts_generic) == 0, "Quando a != 0, não existem pontos críticos na aresta"
    
    # Se a == 0
    phi_flat = phi_edge.subs(a, 0)
    grad_flat = sp.diff(phi_flat, t)
    assert grad_flat == 0, "Quando a == 0, o gradiente tangencial é identicamente nulo"
    # A energia ao longo de toda a aresta é idêntica à energia nos vértices t = -1 e t = +1
    assert phi_flat.subs(t, -1) == phi_flat.subs(t, 0) == phi_flat.subs(t, 1) == b

def test_lema10_1_first_moment_bound():
    """
    Verifica que E[X] <= 9 * alpha^2 é O(1) e estritamente menor que 1/4 para alpha < 1/6.
    Para alpha = 0.12, E[X] <= 0.1296.
    Pela desigualdade de Markov: P(X >= 1) <= E[X] <= 0.1296, logo P(X = 0) >= 0.8704 > 0.
    """
    alpha = 0.12
    cota_E = 9.0 * (alpha ** 2)
    assert cota_E == pytest.approx(0.1296, rel=1e-5)
    assert cota_E < 0.25, "E[X] deve ser < 1/4 no regime subcrítico"
    
    # Pela desigualdade de Markov:
    prob_upper = cota_E
    prob_no_overlap = 1.0 - prob_upper
    assert prob_no_overlap >= 0.8704
    # Note que 0.8704 não tende a 1 quando N -> infty (é constante O(1)),
    # provando que a linearidade a.a.s. não decorre apenas da cota de primeiro momento.
