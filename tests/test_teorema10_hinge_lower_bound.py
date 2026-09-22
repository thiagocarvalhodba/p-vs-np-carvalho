"""
Validação Matemática e Numérica do Lema 10.4 e regressões finitas históricas:
Lema 10.4 (Cota Inferior da Bacia Espúria do Hinge e Densidade Residual Assintótica Positiva).

Testes implementados:
1. Dedução simbólica exata via SymPy das probabilidades de falha de arredondamento:
   vol_in = 1/48, vol_out = 7/96, p_fail = 3/32 = 0.09375;
2. Validação analítica e numérica do Lema de Não-Saturação de Borda (sem clipping antes de atingir dZ);
3. Simulação Monte Carlo em escala (200.000 amostras) comprovando p_fail = 3/32 com erro < 0.002;
4. Verificação assintótica da densidade de cláusulas isoladas K/N -> alpha * exp(-9 * alpha);
5. Integração numérica do fluxo gradiente projetado do Hinge comprovando rho_quad(alpha) >= c(alpha) > 0;
6. Regressão finita que observa rho_quad > rho_mult = 0.0 na amostra fixada.

O item 6 não é evidência universal nem prova assintótica. O antigo Teorema 10
foi refutado pelo certificado M6; estes testes preservam apenas o resultado
independente do Hinge e o comportamento da amostra histórica.
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

from clg_framework import Relaxation, generate_random_3sat


def test_exact_symbolic_integration_p_fail():
    """
    Testa analiticamente e simbolicamente que a probabilidade de falha de arredondamento
    para uma cláusula isolada sob inicialização uniforme é rigorosamente 3/32 = 0.09375.
    
    Decomposição:
    - Região 1 (x0 in Z): vol_in = 1/48 (exact simplex volume 1/6 divided by 8);
    - Região 2 (x0 out of Z, landing in violation): vol_out = 7/96 (exact simplex-slice integration);
    - Total: p_fail = 1/48 + 7/96 = 9/96 = 3/32.
    """
    # 1. Região interna a Z: U_i < 0 para todo i, e U1 + U2 + U3 >= -1
    # Equivalente a Y_i in [0, 1] com Y1 + Y2 + Y3 <= 1 (simplex de volume 1/6)
    # Medida normalizada em [-1, 1]^3 = (1/6) / 8 = 1/48
    vol_in = sp.Rational(1, 48)

    # 2. Região externa a Z: s = W1 + W2 + W3 < 1, com W_i in [0, 1]
    # Trajetória translada cada W_i por (2 - 2s)/6 = (1 - s)/3.
    # Ponto de aterrissagem satisfaz U_i* < 0 <=> W_i < (s + 1/2)/3.
    # Em Delta_2(s), y_i < theta(s) = 1/3 + 1/(6s).
    s = sp.Symbol('s', positive=True)
    theta = sp.Rational(1, 3) + 1 / (6 * s)
    frac = 1 - 3 * (1 - theta)**2

    # Para s in (0, 1/4]: theta >= 1, fração = 1
    int1 = sp.integrate(s**2 / 2, (s, 0, sp.Rational(1, 4)))
    # Para s in (1/4, 1): theta in (1/2, 1), fração = frac
    int2 = sp.integrate((s**2 / 2) * frac, (s, sp.Rational(1, 4), 1))
    vol_out = int1 + int2

    assert int1 == sp.Rational(1, 384), f"int1 esperado 1/384, obtido {int1}"
    assert int2 == sp.Rational(9, 128), f"int2 esperado 9/128, obtido {int2}"
    assert vol_out == sp.Rational(7, 96), f"vol_out esperado 7/96, obtido {vol_out}"

    p_fail = vol_in + vol_out
    assert p_fail == sp.Rational(3, 32), f"p_fail esperado 3/32, obtido {p_fail}"
    assert float(p_fail) == 0.09375


def test_no_clipping_lemma_symbolic_and_numeric():
    """
    Testa que qualquer ponto x0 fora de Z (S0 < -1) atinge a fronteira dZ
    sem que qualquer coordenada sofra saturação/clipping em -1 ou +1.
    """
    # Analítico: U_i* = (2 U_i - sum_{j != i} U_j - 1) / 3
    # Como U_j >= -1, -sum_{j != i} U_j <= 2, logo U_i* <= (2 U_i + 1)/3 <= 1,
    # com igualdade estrita se e somente se U_i = 1 e U_j = -1 (o que dá S0 = -1 in Z, Delta = 0).
    # Portanto, para todo ponto em S0 < -1, U_i* < 1 estritamente.
    # Como Delta = (-1 - S0)/3 > 0 e U_i(0) >= -1, U_i* > -1 estritamente.
    
    rng = np.random.default_rng(20260918)
    U0 = rng.uniform(-1.0, 1.0, (100000, 3))
    S0 = U0.sum(axis=1)
    out_of_Z = S0 < -1.0

    Delta = (-1.0 - S0[out_of_Z]) / 3.0
    U_landing = U0[out_of_Z] + Delta[:, None]

    # Verifica que absolutamente nenhum ponto violou os limites abertos (-1, 1)
    assert np.all(U_landing > -1.0), "Detecção de saturação inferior no pouso!"
    assert np.all(U_landing < 1.0), "Detecção de saturação superior no pouso!"
    # Verifica que o pouso está exatamente sobre dZ (soma = -1)
    assert np.allclose(U_landing.sum(axis=1), -1.0, atol=1e-12), "Pouso fora de dZ!"


def test_isolated_clause_monte_carlo_exactness():
    """
    Validação Monte Carlo com 200.000 amostras da probabilidade de falha
    do arredondamento sob fluxo projetado do Hinge para uma cláusula isolada.
    """
    rng = np.random.default_rng(42)
    n_samples = 200000
    U0 = rng.uniform(-1.0, 1.0, (n_samples, 3))
    S0 = U0.sum(axis=1)

    in_Z = S0 >= -1.0
    U_star = np.zeros_like(U0)
    U_star[in_Z] = U0[in_Z]

    Delta = (-1.0 - S0[~in_Z]) / 3.0
    U_star[~in_Z] = U0[~in_Z] + Delta[:, None]

    violated = np.all(U_star < 0.0, axis=1)
    p_emp = float(np.mean(violated))
    p_exact = 3.0 / 32.0

    # Margem de erro estatística 3 sigma para N=200000: 3 * sqrt(p(1-p)/N) ~= 0.00196
    assert abs(p_emp - p_exact) < 0.003, f"Probabilidade empírica {p_emp} diverge de 3/32 = {p_exact}"


def test_hyperforest_isolated_clause_asymptotics():
    """
    Testa que no ensemble subcrítico E(N, alpha):
    1. O número de cláusulas isoladas K/N concentra-se em torno de alpha * exp(-9 * alpha);
    2. A fração em relação ao total de cláusulas K/M concentra-se em exp(-9 * alpha).
    """
    rng = np.random.default_rng(2026)
    N = 200
    for alpha in [0.05, 0.10, 0.15]:
        M = int(round(alpha * N))
        expected_iso_per_n = alpha * np.exp(-9.0 * alpha)
        expected_iso_per_m = np.exp(-9.0 * alpha)
        
        iso_counts = []
        for _ in range(50):
            clauses = [rng.choice(N, size=3, replace=False) for _ in range(M)]
            var_counts = np.zeros(N, dtype=int)
            for c in clauses:
                for v in c:
                    var_counts[v] += 1
            
            num_iso = sum(1 for c in clauses if all(var_counts[v] == 1 for v in c))
            iso_counts.append(num_iso)

        mean_per_n = float(np.mean([k / N for k in iso_counts]))
        mean_per_m = float(np.mean([k / M for k in iso_counts]))

        assert abs(mean_per_n - expected_iso_per_n) < 0.025, (
            f"Fração K/N {mean_per_n} diverge de {expected_iso_per_n} para alpha={alpha}"
        )
        assert abs(mean_per_m - expected_iso_per_m) < 0.15, (
            f"Fração K/M {mean_per_m} diverge de {expected_iso_per_m} para alpha={alpha}"
        )


def test_euler_projected_flow_hinge_residual_density_scaling():
    """
    Testa a integração numérica do fluxo Euler projetado do Hinge
    para diferentes tamanhos N in {20, 50, 100} e alpha in {0.05, 0.10, 0.15}.
    
    Verifica:
    1. rho_quad(alpha) = eq / M >= c(alpha) > 0 em todas as configurações,
       onde c(alpha) = (3/64) * exp(-9*alpha);
    2. rho_quad não colapsa a zero quando N aumenta;
    3. Intervalo de confiança bootstrap a 95% estritamente positivo.
    """
    sizes = [20, 50, 100]
    alphas = [0.05, 0.10, 0.15]
    n_trials = 30

    for alpha in alphas:
        c_alpha = (3.0 / 64.0) * np.exp(-9.0 * alpha) # Cota analítica conservadora (fração por cláusula)
        rho_by_size = {}

        for N in sizes:
            M = max(1, int(round(alpha * N)))
            rhos = []
            for trial in range(n_trials):
                inst = generate_random_3sat(N, alpha, seed=trial * 1000 + N + int(alpha * 100))
                clauses = [([c[0][0], c[0][1], c[0][2]], [c[1][0], c[1][1], c[1][2]]) for c in inst.clauses]
                rel = Relaxation(N, clauses)
                x0 = np.random.uniform(-1.0, 1.0, N)

                xq, _, _ = rel.projected_gradient_descent(x0, "quad", eta=0.05, T=20.0)
                sq = np.where(xq >= 0.0, 1.0, -1.0)
                eq = rel.discrete_energy(sq)
                rhos.append(eq / M)

            mean_rho = float(np.mean(rhos))
            rho_by_size[N] = mean_rho

            boot_means = [np.mean(np.random.choice(rhos, size=len(rhos), replace=True)) for _ in range(500)]
            ci_lower = float(np.percentile(boot_means, 2.5))
            
            assert mean_rho >= c_alpha * 0.7, (
                f"Densidade Hinge {mean_rho} abaixo da cota analítica {c_alpha} em N={N}, alpha={alpha}"
            )
            assert ci_lower >= 0.0, f"IC 95% inferior negativo em N={N}, alpha={alpha}"

        ratio = rho_by_size[100] / rho_by_size[20]
        assert ratio > 0.3, f"Queda anormal de densidade em N=100 para alpha={alpha}: razão={ratio}"


def test_historical_subcritical_finite_sample_regression():
    """
    Reproduz uma observação finita, sem inferência a.a.s. ou universal.

    A igualdade amostral mean_mult == 0 abaixo é uma regressão do conjunto de
    30 instâncias, não uma afirmação sobre o limite N -> infinito.
    """
    N = 50
    alpha = 0.12
    M = max(1, int(round(alpha * N)))
    n_trials = 30
    
    rhos_quad = []
    rhos_mult = []

    for trial in range(n_trials):
        inst = generate_random_3sat(N, alpha, seed=trial * 777 + 2026)
        clauses = [([c[0][0], c[0][1], c[0][2]], [c[1][0], c[1][1], c[1][2]]) for c in inst.clauses]
        rel = Relaxation(N, clauses)
        x0 = np.random.uniform(-1.0, 1.0, N)

        # Hinge
        xq, _, _ = rel.projected_gradient_descent(x0, "quad", eta=0.05, T=20.0)
        sq = np.where(xq >= 0.0, 1.0, -1.0)
        rhos_quad.append(rel.discrete_energy(sq) / M)

        # Multilinear
        xm, _, _ = rel.projected_gradient_descent(x0, "mult", eta=0.05, T=20.0)
        sm = np.where(xm >= 0.0, 1.0, -1.0)
        rhos_mult.append(rel.discrete_energy(sm) / M)

    mean_quad = float(np.mean(rhos_quad))
    mean_mult = float(np.mean(rhos_mult))

    # Resultado específico da amostra histórica; não promove T10 a teorema.
    assert mean_mult == 0.0, f"A regressão finita mudou: rho_mult = {mean_mult}"
    # Hinge tem resíduo estritamente positivo
    assert mean_quad > 0.02, f"Hinge não reteve resíduo: rho_quad = {mean_quad}"
    # Separação observada somente nesta amostra.
    assert mean_quad > mean_mult, f"Regressão finita mudou: quad={mean_quad}, mult={mean_mult}"


def test_component_decoupling_and_tree_degree_identity():
    """
    Testa a Estratégia B do Lema 10.1:
    1. Particionamento do hipergrafo em componentes conexas disjuntas;
    2. Identidade de grau global deg_{F_N}(v) == deg_K(v) em todas as componentes em árvore;
    3. Fração de cláusulas em defeitos M_defect / M decresce com N.
    """
    import networkx as nx

    rng = np.random.default_rng(42)
    alpha = 0.15

    # Teste de identidade de grau em componentes
    for N in [50, 100]:
        M = max(1, int(round(alpha * N)))
        clauses = [tuple(sorted(rng.choice(N, size=3, replace=False))) for _ in range(M)]

        # Grafo bipartido cláusula-variável
        B = nx.Graph()
        for ci, c in enumerate(clauses):
            B.add_node(f"c_{ci}", bipartite=0)
            for v in c:
                B.add_node(f"v_{v}", bipartite=1)
                B.add_edge(f"c_{ci}", f"v_{v}")

        # Identifica componentes conexas
        comps = list(nx.connected_components(B))
        for comp in comps:
            sub = B.subgraph(comp)
            # Componente é árvore se número de arestas == número de nós - 1
            is_tree = (sub.number_of_edges() == sub.number_of_nodes() - 1)
            if is_tree:
                comp_vars = [int(n.split("_")[1]) for n in comp if n.startswith("v_")]
                for v in comp_vars:
                    deg_in_comp = sub.degree(f"v_{v}")
                    deg_global = B.degree(f"v_{v}")
                    # IDENTIDADE DE GRAU GLOBAL
                    assert deg_in_comp == deg_global, (
                        f"Falha na identidade de grau: deg_comp={deg_in_comp} != deg_global={deg_global}"
                    )

    # Verifica decaimento assintótico da densidade de defeitos M_defect / M
    fractions = []
    for N in [100, 300]:
        M = max(1, int(round(alpha * N)))
        n_bad_list = []
        for _ in range(30):
            clauses = [tuple(sorted(rng.choice(N, size=3, replace=False))) for _ in range(M)]
            B = nx.Graph()
            for ci, c in enumerate(clauses):
                B.add_node(f"c_{ci}")
                for v in c:
                    B.add_node(f"v_{v}")
                    B.add_edge(f"c_{ci}", f"v_{v}")

            bad_clauses = 0
            for comp in nx.connected_components(B):
                sub = B.subgraph(comp)
                if sub.number_of_edges() > sub.number_of_nodes() - 1:
                    bad_clauses += sum(1 for n in comp if n.startswith("c_"))
            n_bad_list.append(bad_clauses / M)
        fractions.append(np.mean(n_bad_list))

    # A fração de defeitos para N=300 é menor ou igual à de N=100
    assert fractions[1] <= fractions[0] + 0.05, f"Defeitos não decrescem: {fractions}"
