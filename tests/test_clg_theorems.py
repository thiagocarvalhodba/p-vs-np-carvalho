"""
Suite de testes numéricos para os Teoremas 1 a 7B do framework CLG-R.

Executar a partir da raiz do repositório:
    venv\\Scripts\\python.exe -m pytest tests -q

Os testes são auto-contidos (NumPy + PyTorch) e usam implementações de
referência das três relaxações canônicas no hipercubo [-1, 1]^N:

    g_c(x)        = -1/2 (1 + sigma^(c) . x)
    Phi_quad(x)   = sum_c max(0, g_c)^2
    Phi_mult(x)   = sum_c prod_{j in c} (1 - sigma_j x_j)/2
    Phi_soft(x)   = sum_c (1/beta) log(1 + exp(beta g_c))

Cada teste referencia o teorema que verifica. Os testes marcados como
"documenta lacuna" registram comportamentos que CONTRADIZEM a prova escrita
(não o enunciado) e devem ser mantidos até a prova ser corrigida.
"""
import itertools
import math
import os
import sys

import numpy as np
import pytest
import torch

torch.set_default_dtype(torch.float64)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "Fontes"))


# --------------------------------------------------------------------------
# Implementações de referência
# --------------------------------------------------------------------------
def random_3sat_sigma(n, m, rng):
    """Matriz de polaridades S (M x N) com exatamente 3 entradas +-1 por linha (H1)."""
    S = np.zeros((m, n))
    for c in range(m):
        vs = rng.choice(n, 3, replace=False)
        S[c, vs] = rng.choice([-1.0, 1.0], 3)
    return S


def g(S, x):
    return -0.5 * (1.0 + S @ x)


def phi_quad(S, x):
    return float(np.sum(np.maximum(0.0, g(S, x)) ** 2))


def grad_quad(S, x):
    gc = g(S, x)
    act = gc > 0
    return (2.0 * gc[act]) @ (-0.5 * S[act])


def phi_mult(S, x):
    rows, cols = np.nonzero(S)
    if len(rows) == 3 * S.shape[0]:
        V = cols.reshape(-1, 3)
        signs = S[rows, cols].reshape(-1, 3)
        t0 = 0.5 * (1.0 - signs[:, 0] * x[V[:, 0]])
        t1 = 0.5 * (1.0 - signs[:, 1] * x[V[:, 1]])
        t2 = 0.5 * (1.0 - signs[:, 2] * x[V[:, 2]])
        return float(np.sum(t0 * t1 * t2))
    return float(np.sum(np.prod(np.where(S != 0, (1.0 - S * x) / 2.0, 1.0), axis=1)))


def grad_mult(S, x):
    rows, cols = np.nonzero(S)
    if len(rows) == 3 * S.shape[0]:
        V = cols.reshape(-1, 3)
        signs = S[rows, cols].reshape(-1, 3)
        t0 = 0.5 * (1.0 - signs[:, 0] * x[V[:, 0]])
        t1 = 0.5 * (1.0 - signs[:, 1] * x[V[:, 1]])
        t2 = 0.5 * (1.0 - signs[:, 2] * x[V[:, 2]])
        g0 = -0.5 * signs[:, 0] * (t1 * t2)
        g1 = -0.5 * signs[:, 1] * (t0 * t2)
        g2 = -0.5 * signs[:, 2] * (t0 * t1)
        grad = np.zeros_like(x)
        np.add.at(grad, V[:, 0], g0)
        np.add.at(grad, V[:, 1], g1)
        np.add.at(grad, V[:, 2], g2)
        return grad
    out = np.zeros_like(x)
    for c in range(S.shape[0]):
        vs = np.nonzero(S[c])[0]
        for i in vs:
            others = [j for j in vs if j != i]
            out[i] += (-S[c, i] / 2.0) * np.prod([(1 - S[c, j] * x[j]) / 2 for j in others])
    return out


def phi_soft(S, x, beta):
    return float(np.sum(np.logaddexp(0.0, beta * g(S, x))) / beta)


def grad_soft(S, x, beta):
    s = 1.0 / (1.0 + np.exp(-beta * g(S, x)))
    return s @ (-0.5 * S)


def hess_soft(S, x, beta):
    s = 1.0 / (1.0 + np.exp(-beta * g(S, x)))
    W = beta * s * (1 - s)
    V = -0.5 * S
    return V.T @ (W[:, None] * V), V, W


def e_disc(S, s):
    """Número de cláusulas violadas no vértice s in {-1,+1}^N."""
    viol = 0
    for c in range(S.shape[0]):
        vs = np.nonzero(S[c])[0]
        if np.all(S[c, vs] * s[vs] < 0):
            viol += 1
    return viol


def fd_grad(f, x, h=1e-6):
    gr = np.zeros_like(x)
    for i in range(len(x)):
        e = np.zeros_like(x)
        e[i] = h
        gr[i] = (f(x + e) - f(x - e)) / (2 * h)
    return gr


def torch_hessian(f, x):
    return torch.autograd.functional.hessian(f, torch.tensor(x)).numpy()


def all_negative_family(N):
    """Família F_N do Teorema 7A: todas as C(N,3) cláusulas puramente negativas."""
    triples = list(itertools.combinations(range(N), 3))
    S = np.zeros((len(triples), N))
    for c, t in enumerate(triples):
        S[c, list(t)] = -1.0
    return S


def gradient_flow_quad(S, x0, dt=1e-3, T=40.0):
    """Fluxo exato dx/dt = -grad Phi_quad (Euler explícito com passo pequeno, clamp no cubo)."""
    x = x0.copy()
    t = 0.0
    left_A_N = None
    while t < T:
        gr = grad_quad(S, x)
        if np.linalg.norm(gr) < 1e-12:
            break
        x = np.clip(x - dt * gr, -1.0, 1.0)
        t += dt
        if left_A_N is None and np.any(x <= 1.0 / 3.0):
            left_A_N = t
    return x, left_A_N


@pytest.fixture(scope="module")
def rng():
    return np.random.default_rng(20260911)


@pytest.fixture(scope="module")
def formula(rng):
    n, m = 12, 51
    return n, m, random_3sat_sigma(n, m, rng)


# --------------------------------------------------------------------------
# Verificação de gradientes / Hessianas (Seção 3 da auditoria)
# --------------------------------------------------------------------------
def test_gradients_match_finite_differences(formula, rng):
    n, m, S = formula
    for _ in range(10):
        x = rng.uniform(-1, 1, n)
        assert np.max(np.abs(grad_mult(S, x) - fd_grad(lambda y: phi_mult(S, y), x))) < 1e-6
        assert np.max(np.abs(grad_soft(S, x, 5.0) - fd_grad(lambda y: phi_soft(S, y, 5.0), x))) < 1e-6
        # Hinge é C^1 mas não C^2: o erro de DF é O(h) apenas se um vínculo estiver a < h de g_c = 0
        if np.min(np.abs(g(S, x))) > 1e-4:
            assert np.max(np.abs(grad_quad(S, x) - fd_grad(lambda y: phi_quad(S, y), x))) < 1e-6


def test_clg_framework_multilinear_matches_reference(rng):
    """Integração com Fontes/clg_framework.py: potencial, gradiente e Hessiana."""
    from clg_framework import CNFInstance
    n = 10
    clauses = []
    for _ in range(40):
        vs = rng.choice(n, 3, replace=False).tolist()
        ss = rng.choice([-1.0, 1.0], 3).tolist()
        clauses.append((vs, ss))
    inst = CNFInstance(n, 3, clauses, "Random-3-SAT", "NP-Complete")
    S = np.zeros((40, n))
    for c, (vs, ss) in enumerate(clauses):
        S[c, vs] = ss
    x = rng.uniform(-1, 1, n)
    xt = torch.tensor(x, dtype=torch.float32)
    assert abs(inst.potential(xt).item() - phi_mult(S, x)) < 1e-4
    assert np.max(np.abs(inst.gradient(xt).numpy() - grad_mult(S, x))) < 1e-4
    H = inst.compute_hessian(xt).numpy()
    assert abs(np.trace(H)) < 1e-4  # Teorema 3 via o código do repositório
    assert np.max(np.abs(np.diag(H))) < 1e-5
    # energia discreta coincide com Phi_mult nos vértices
    s = rng.choice([-1.0, 1.0], n)
    assert inst.discrete_energy(s) == e_disc(S, s) == round(phi_mult(S, s))


# --------------------------------------------------------------------------
# Teorema 1: caixa fracionária central
# --------------------------------------------------------------------------
def test_theorem1_plateau_zero_energy_and_gradient(formula, rng):
    n, m, S = formula
    for _ in range(500):
        x = rng.uniform(-1 / 3, 1 / 3, n)
        assert np.all(g(S, x) < 0)
        assert phi_quad(S, x) == 0.0
        assert np.all(grad_quad(S, x) == 0.0)
    # na fronteira |x_i| = 1/3 com polaridades adversas, g_c = 0 (justeza do 1/3)
    c = 0
    vs = np.nonzero(S[c])[0]
    x = np.zeros(n)
    x[vs] = -S[c, vs] / 3.0
    assert abs(g(S, x)[c]) < 1e-12


def test_theorem1_measure_bound_is_valid_but_loose(formula, rng):
    """Vol(Z) >= (2/3)^N é verdadeiro; Z é o politopo LP e é muito maior que U_N."""
    n, m, S = formula
    K = 20000
    z = sum(phi_quad(S, rng.uniform(-1, 1, n)) == 0.0 for _ in range(K)) / K
    assert z >= (1 / 3) ** n  # medida normalizada
    assert z > 100 * (1 / 3) ** n  # documenta a folga da cota


def test_theorem1_plateau_points_are_spurious_equilibria(formula, rng):
    """Todo ponto do platô em um ortante violador é um equilíbrio cujo arredondamento viola cláusulas.
    Isso já prova M_spur(Phi_quad) >= (1/3)^N (euclidiano) sem qualquer análise de EDO."""
    n, m, S = formula
    found = False
    for _ in range(200):
        x = rng.uniform(-1 / 3, 1 / 3, n)
        s = np.where(x >= 0, 1.0, -1.0)
        if e_disc(S, s) > 0:
            found = True
            assert np.all(grad_quad(S, x) == 0.0)
    assert found


# --------------------------------------------------------------------------
# Teorema 2: medida nula dos críticos de Phi_mult e Phi_soft
# --------------------------------------------------------------------------
def test_theorem2_random_points_are_never_critical(formula, rng):
    n, m, S = formula
    for _ in range(300):
        x = rng.uniform(-1, 1, n)
        assert np.linalg.norm(grad_mult(S, x)) > 1e-8
        assert np.linalg.norm(grad_soft(S, x, 5.0)) > 1e-8


def test_theorem2_h3prime_counterexample_is_constant():
    """Contraexemplo (H3'): as 8 cláusulas completas sobre 3 variáveis dão Phi_mult == 1."""
    S = np.array(list(itertools.product([-1.0, 1.0], repeat=3)))
    rng = np.random.default_rng(1)
    for _ in range(20):
        assert abs(phi_mult(S, rng.uniform(-1, 1, 3)) - 1.0) < 1e-12
    assert all(e_disc(S, np.array(b)) == 1 for b in itertools.product([-1.0, 1.0], repeat=3))


def test_theorem2_parseval_variance(formula):
    """Var(E_disc) > 0 <=> Phi_mult não constante (fórmula satisfatível ou não-balanceada)."""
    n, m, S = formula
    energies = np.array([e_disc(S, np.array(b)) for b in itertools.product([-1.0, 1.0], repeat=n)])
    assert energies.var() > 0


# --------------------------------------------------------------------------
# Teorema 3: harmonicidade e selas de Morse
# --------------------------------------------------------------------------
def test_theorem3_laplacian_vanishes(formula, rng):
    n, m, S = formula
    St = torch.tensor(S)
    f = lambda t: torch.sum(torch.prod(torch.where(St != 0, (1.0 - St * t) / 2.0, torch.ones_like(St)), dim=1))
    for _ in range(5):
        H = torch_hessian(f, rng.uniform(-1, 1, n))
        assert abs(np.trace(H)) < 1e-10
        assert np.max(np.abs(np.diag(H))) < 1e-12


def test_theorem3_interior_critical_point_is_saddle(formula, rng):
    """Constrói uma fórmula polaridade-balanceada F ∪ F̄ (cada cláusula e sua cópia com todas as
    polaridades invertidas). Em x = 0 o gradiente é -1/8 sum_{c∋i} sigma_i^(c) = 0, logo a origem é
    um ponto crítico interior; a Hessiana em 0 tem traço nulo e deve ter autovalores de ambos os sinais.
    Observação de auditoria: para fórmulas 3-SAT aleatórias (N=6,8,12) NÃO foram encontrados pontos
    críticos interiores por minimização de ||grad Phi||^2 (LBFGS, 30 partidas); o Teorema 3 é
    possivelmente vazio para instâncias típicas, cujos críticos vivem no bordo."""
    n, m, S = formula
    Sb = np.vstack([S, -S])
    assert np.linalg.norm(grad_mult(Sb, np.zeros(n))) < 1e-14
    St = torch.tensor(Sb)
    f = lambda t: torch.sum(torch.prod(torch.where(St != 0, (1.0 - St * t) / 2.0, torch.ones_like(St)), dim=1))
    ev = np.linalg.eigvalsh(torch_hessian(f, np.zeros(n)))
    assert abs(ev.sum()) < 1e-12          # harmonicidade
    assert ev[0] < -1e-8 and ev[-1] > 1e-8  # sela: índice de Morse entre 1 e N-1
    # e não é mínimo local: existe y arbitrariamente próximo com Phi(y) < Phi(0) (item 3 do Teorema 3)
    for eps in (1e-1, 1e-2, 1e-3):
        assert min(phi_mult(Sb, eps * v) for v in (np.linalg.eigh(torch_hessian(f, np.zeros(n)))[1][:, 0], -np.linalg.eigh(torch_hessian(f, np.zeros(n)))[1][:, 0])) < phi_mult(Sb, np.zeros(n))


# --------------------------------------------------------------------------
# Teorema 4A / Corolário 4B e a hipótese H4
# --------------------------------------------------------------------------
def test_h4_fails_on_random_3sat_and_on_F_N(rng):
    """DOCUMENTA LACUNA: H4 exige b_i(s_{-i}) != 0 em TODAS as N 2^{N-1} arestas, i.e.
    E_disc(s) != E_disc(s com x_i invertido). Isso falha em ~1/4 das arestas de 3-SAT
    aleatório e falha na própria família F_N do Teorema 7A. H4 NÃO é genérica."""
    n, m = 10, 43
    S = random_3sat_sigma(n, m, rng)
    flat, total = 0, 0
    for bits in itertools.product([-1.0, 1.0], repeat=n):
        s = np.array(bits)
        e = e_disc(S, s)
        for i in range(n):
            s2 = s.copy()
            s2[i] *= -1
            total += 1
            flat += e_disc(S, s2) == e
    assert flat / total > 0.05  # tipicamente ~0.2-0.25
    SF = all_negative_family(6)
    s = -np.ones(6)
    s2 = s.copy()
    s2[0] = 1.0
    assert e_disc(SF, s) == e_disc(SF, s2) == 0  # b_1(s_{-1}) = 0 em F_N


def test_theorem4_local_minima_value_equals_vertex_value(formula, rng):
    """Versão livre de H4: descida projetada em Phi_mult termina em um ponto x* cujo valor
    coincide com E_disc de todo vértice da face portadora (Phi_mult é afim por coordenada)."""
    n, m, S = formula
    for _ in range(10):
        x = rng.uniform(-1, 1, n)
        for _ in range(4000):
            x = np.clip(x - 0.05 * grad_mult(S, x), -1, 1)
        free = np.abs(x) < 1 - 1e-6
        val = phi_mult(S, x)
        # arredondando as coordenadas livres para qualquer vértice da face, o valor não muda
        for bits in itertools.product([-1.0, 1.0], repeat=min(int(free.sum()), 6)):
            v = x.copy()
            idx = np.nonzero(free)[0][: len(bits)]
            v[idx] = bits
            if np.all(np.abs(v) >= 1 - 1e-6):
                assert abs(phi_mult(S, v) - val) < 1e-6


# --------------------------------------------------------------------------
# Teorema 5: fatoração V^T W V e condicionamento
# --------------------------------------------------------------------------
def test_theorem5_hessian_factorization_and_bounds(formula, rng):
    n, m, S = formula
    St = torch.tensor(S)
    f = lambda t: torch.sum(torch.nn.functional.softplus(-0.5 * (1.0 + St @ t), beta=5.0))
    for _ in range(5):
        x = rng.uniform(-1, 1, n)
        H, V, W = hess_soft(S, x, 5.0)
        assert np.max(np.abs(H - torch_hessian(f, x))) < 1e-10
        evH = np.linalg.eigvalsh(H)
        evVV = np.linalg.eigvalsh(V.T @ V)
        assert evH[0] > -1e-12  # PSD
        if np.linalg.matrix_rank(V) == n:
            assert evH[0] >= W.min() * evVV[0] - 1e-12
            assert evH[-1] <= W.max() * evVV[-1] + 1e-12
            assert evH[-1] / evH[0] <= (W.max() / W.min()) * (evVV[-1] / evVV[0]) * (1 + 1e-9)
        assert abs(np.trace(H) - 0.75 * W.sum()) < 1e-10  # Laplaciano = 3/4 sum w_c


def test_theorem5_kernel_equals_kernel_of_V(rng):
    """Com M < N o posto de V é deficiente e ker(H) = ker(V)."""
    n, m = 12, 6
    S = random_3sat_sigma(n, m, rng)
    H, V, W = hess_soft(S, rng.uniform(-1, 1, n), 5.0)
    assert np.linalg.matrix_rank(H) == np.linalg.matrix_rank(V) < n


# --------------------------------------------------------------------------
# Teorema 6: Lipschitz e underflow IEEE 754
# --------------------------------------------------------------------------
def test_theorem6_lipschitz_sandwich(formula, rng):
    n, m, S = formula
    beta = 7.0
    dmax = int(np.sum(S != 0, axis=0).max())
    best = 0.0
    for _ in range(500):
        H, _, _ = hess_soft(S, rng.uniform(-1, 1, n), beta)
        best = max(best, np.linalg.eigvalsh(H)[-1])
    for c in range(m):  # pontos sobre cada hiperplano ativo g_c = 0
        x = np.zeros(n)
        vs = np.nonzero(S[c])[0]
        x[vs] = -S[c, vs] / 3.0
        H, _, _ = hess_soft(S, x, beta)
        best = max(best, np.linalg.eigvalsh(H)[-1])
    assert 3 * beta / 16 <= best + 1e-9
    assert best <= 3 * dmax * beta / 16 + 1e-9


def test_theorem6_gradient_decay_in_contracted_box(formula, rng):
    n, m, S = formula
    beta, rho = 30.0, 0.2
    for _ in range(50):
        x = rng.uniform(-rho, rho, n)
        gr = grad_soft(S, x, beta)
        assert np.max(np.abs(gr)) <= (m / 2) * math.exp(-beta * (1 - 3 * rho) / 2)
        assert np.linalg.norm(gr) <= (math.sqrt(3) * m / 2) * math.exp(-beta * (1 - 3 * rho) / 2)


def test_theorem6_ieee754_underflow_thresholds():
    """Limiar em que exp(-beta/2) (fator do gradiente na origem) sai do intervalo normal/subnormal."""
    assert round(2 * 126 * math.log(2)) == 175
    assert round(2 * 149 * math.log(2)) == 207
    assert round(2 * 1022 * math.log(2)) == 1417
    assert round(2 * 1074 * math.log(2)) == 1489
    assert np.exp(np.float32(-174 / 2)) > np.finfo(np.float32).tiny
    assert 0 < np.exp(np.float32(-200 / 2)) < np.finfo(np.float32).tiny  # subnormal
    assert np.exp(np.float32(-210 / 2)) == 0.0  # flush-to-zero


# --------------------------------------------------------------------------
# Teorema 7B: contração centrípeta
# --------------------------------------------------------------------------
def test_theorem7b_centripetal_identity(formula, rng):
    n, m, S = formula
    for _ in range(500):
        x = rng.uniform(-1, 1, n)
        gc = g(S, x)
        act = gc > 0
        lhs = -grad_quad(S, x) @ x
        rhs = -np.sum(2 * gc[act] ** 2 + gc[act])
        assert abs(lhs - rhs) < 1e-12
        if act.any():
            assert lhs < -np.sum(gc[act]) < 0


def test_theorem7b_no_projected_equilibrium_with_positive_energy(formula, rng):
    """Descida projetada em Phi_quad sempre termina no platô Z = {Phi_quad = 0}."""
    n, m, S = formula
    for _ in range(10):
        x = rng.uniform(-1, 1, n)
        for _ in range(20000):
            gr = grad_quad(S, x)
            if np.linalg.norm(gr) == 0:
                break
            x = np.clip(x - 0.02 * gr, -1, 1)
        assert phi_quad(S, x) < 1e-20


def test_theorem7b_unsat_spurious_mass_is_trivially_one_for_every_representation():
    """Para UNSAT, E_disc(sign(x)) >= 1 para TODO x: M_spur = 1 vale para Phi_quad, Phi_mult e Phi_soft.
    A 'separação 1 - 0 = 1' afirmada na Resposta ao Parecer 11 (item 3 do Teorema 7B) é falsa."""
    S = np.array(list(itertools.product([-1.0, 1.0], repeat=3)))  # UNSAT: toda atribuição viola 1 cláusula
    for b in itertools.product([-1.0, 1.0], repeat=3):
        assert e_disc(S, np.array(b)) >= 1
    rng = np.random.default_rng(3)
    for _ in range(20):
        x = rng.uniform(-1, 1, 3)
        for _ in range(3000):
            x = np.clip(x - 0.05 * grad_mult(S, x), -1, 1)
        assert e_disc(S, np.where(x >= 0, 1.0, -1.0)) >= 1


# --------------------------------------------------------------------------
# Teorema 7A: família F_N
# --------------------------------------------------------------------------
@pytest.mark.parametrize("N", [4, 6, 8])
def test_theorem7a_hessian_constant_and_eigenvalues(N, rng):
    S = all_negative_family(N)
    HN = np.full((N, N), 0.5 * (N - 2))
    np.fill_diagonal(HN, 0.5 * math.comb(N - 1, 2))
    x = rng.uniform(1 / 3 + 0.05, 0.95, N)
    St = torch.tensor(S)
    f = lambda t: torch.sum(torch.relu(-0.5 * (1.0 + St @ t)) ** 2)
    assert np.max(np.abs(torch_hessian(f, x) - HN)) < 1e-10
    ev = np.sort(np.linalg.eigvalsh(HN))
    assert abs(ev[0] - (N - 2) * (N - 3) / 4) < 1e-10
    assert abs(ev[-1] - 3 * (N - 1) * (N - 2) / 4) < 1e-10
    assert np.all(g(S, x) > 0)  # todas as cláusulas ativas em A_N
    assert np.linalg.norm(grad_quad(S, np.full(N, 1 / 3))) < 1e-12


@pytest.mark.parametrize("N", [4, 6, 8])
def test_theorem7a_conclusion_holds_but_linear_regime_does_not_persist(N, rng):
    """DOCUMENTA LACUNA: a prova escrita assume que u(t) = exp(-t H_N) u(0) descreve o fluxo
    para todo t e que lim x(t) = (1/3) 1. Numericamente, toda trajetória genérica SAI de A_N em
    tempo finito (coordenadas abaixo da média cruzam 1/3), o regime linear cessa e o limite
    NÃO é (1/3) 1. A conclusão A_N ⊆ B_spur permanece verdadeira nos casos testados."""
    S = all_negative_family(N)
    left, at_third, spurious, negative = 0, 0, 0, 0
    K = 30
    for _ in range(K):
        x0 = rng.uniform(1 / 3, 1, N)
        xf, t_left = gradient_flow_quad(S, x0, dt=2e-3, T=30.0)
        left += t_left is not None
        at_third += np.max(np.abs(xf - 1 / 3)) < 1e-3
        negative += np.any(xf < 0)
        spurious += e_disc(S, np.where(xf >= 0, 1.0, -1.0)) > 0
        assert phi_quad(S, xf) < 1e-12  # termina no platô Z
    assert spurious == K          # enunciado: A_N ⊆ B_spur (suportado numericamente)
    assert negative == 0          # nenhuma coordenada muda de sinal (ingrediente para uma prova correta)
    assert left == K              # prova escrita inválida: o fluxo abandona A_N
    assert at_third == 0          # prova escrita inválida: o limite não é (1/3) 1
