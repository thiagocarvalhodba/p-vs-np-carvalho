"""
Suíte de Testes Matemáticos e de Consistência — Auditoria Parecer nº 19.
Verifica programaticamente:
1. Contraexemplo numérico do Professor para Proposição 7A (N=4, x0=(0.334, 1, 1, 1)):
   demonstra que x_1 torna-se negativo sob o fluxo Hinge, falsificando a conservação de coordenadas positivas.
2. Sinal competitivo do Jacobiano J_ij <= 0 da Proposição 7A (núcleo preservado).
3. Formulação rigorosa do Teorema 7B com lim dist(x(t), Z) = 0 e projeção no cone tangente.
4. Relaxamento da condição de Jensen no Teorema 8 para t -> t^M convexa (M >= 1).
5. Sobriedade do título e da conclusão (eliminação de "Rigorous Dynamic Separations" e de "explain why").
6. Ausência completa do Item 2 da Proposição 7A nos manuscritos.
"""
import os
import re
import pytest
import numpy as np
import sympy as sp

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PUB_DIR = os.path.join(REPO_DIR, "Publicacoes")

def test_prop7a_counterexample_n4():
    """
    Reproduz o contraexemplo do Parecer 19:
    N=4, 4 cláusulas puramente negativas.
    x0 = (0.334, 1.0, 1.0, 1.0) in (1/3, 1)^4.
    Integração do fluxo Hinge:
    Mostra que x_1 cruza para valores estritamente negativos (x_1* ≈ -0.004 < 0),
    provando que o fluxo NÃO mantém coordenadas positivas e refutando a afirmação
    universal de arredondamento (+1, +1, +1, +1) em 100% das trajetórias.
    """
    clauses = [
        [0, 1, 2],
        [0, 1, 3],
        [0, 2, 3],
        [1, 2, 3]
    ]
    x = np.array([0.334, 1.0, 1.0, 1.0], dtype=float)
    dt = 0.001
    
    for _ in range(10000):
        grad_push = np.zeros(4)
        for cl in clauses:
            s = sum(x[i] for i in cl)
            gc = (s - 1.0) / 2.0
            if gc > 0:
                for i in cl:
                    grad_push[i] += gc * (-1.0)
        x_new = x + dt * grad_push
        x = np.clip(x_new, -1.0, 1.0)
    
    # x1 limite é estritamente negativo:
    assert x[0] < 0.0, f"x_1 deveria cruzar o zero e tornar-se negativo, mas obteve {x[0]}"
    assert np.isclose(x[0], -0.004186, atol=1e-3), f"x_1* ≈ -0.004 esperado, obteve {x[0]}"
    # As outras coordenadas convergem para 1/3:
    assert np.isclose(x[1], 1.0/3.0, atol=1e-2)
    assert np.isclose(x[2], 1.0/3.0, atol=1e-2)
    assert np.isclose(x[3], 1.0/3.0, atol=1e-2)

def test_prop7a_jacobian_competitive():
    """
    Verifica que para qualquer par de variáveis em cláusulas negativas,
    d^2 P_c / dx_i dx_j >= 0, logo J_ij = -d^2 Phi / dx_i dx_j <= 0.
    """
    x1, x2, x3 = sp.symbols('x1 x2 x3')
    # Cláusula negativa (neg x1 or neg x2 or neg x3)
    # Potencial de penalidade multilinear:
    P_c = ((1 + x1)/2) * ((1 + x2)/2) * ((1 + x3)/2)
    
    d2P_dx1dx2 = sp.diff(sp.diff(P_c, x1), x2)
    expected_cross = (1 + x3) / 8
    assert sp.simplify(d2P_dx1dx2 - expected_cross) == 0
    
    # Para x3 in [-1, 1], (1 + x3)/8 >= 0, logo J_12 = - d2P <= 0
    for val_x3 in [-1.0, -0.5, 0.0, 0.5, 1.0]:
        val = (1.0 + val_x3) / 8.0
        assert val >= 0.0
        assert -val <= 0.0

def test_teorema7b_lasalle_distance_formulation():
    """
    Verifica que tanto no LaTeX quanto no estudo analítico:
    1. A formulação de LaSalle explicita dist(x(t), Z) -> 0.
    2. O operador Pi_{T_X(x)} é identificado como projeção ortogonal no cone tangente.
    """
    tex_path = os.path.join(PUB_DIR, "CLG_FOUNDATIONS_ARXIV.tex")
    md_path = os.path.join(PUB_DIR, "ESTUDO_ANALITICO_DO_CONJUNTO_CRITICO.md")
    
    with open(tex_path, "r", encoding="utf-8") as f:
        tex_content = f.read()
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
        
    assert r"\lim_{t \to \infty} \text{dist}(x(t), Z) = 0" in tex_content
    assert r"\Pi_{T_{\mathcal{X}}(x)}" in tex_content
    assert "orthogonal projection operator" in tex_content
    
    assert r"\lim_{t \to \infty} \text{dist}(x(t), Z) = 0" in md_content
    assert "projeção ortogonal no cone tangente" in md_content

def test_teorema8_jensen_convexity_relaxed():
    """
    Verifica que o Teorema 8 usa 'convex' / 'convexa' para M >= 1,
    sem a restrição 'estritamente convexa para M >= 2'.
    """
    tex_path = os.path.join(PUB_DIR, "CLG_FOUNDATIONS_ARXIV.tex")
    md_path = os.path.join(PUB_DIR, "ESTUDO_ANALITICO_DO_CONJUNTO_CRITICO.md")
    
    with open(tex_path, "r", encoding="utf-8") as f:
        tex_content = f.read()
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
        
    # Extrai a seção do Teorema 8 do LaTeX
    t8_tex = re.search(r"\\section\{Theorem 8.*?\}(.*?)\\section\{Theorems 9", tex_content, re.DOTALL)
    assert t8_tex is not None, "Seção do Teorema 8 deve existir no LaTeX"
    t8_tex_text = t8_tex.group(1)
    
    assert "convex function $t \\mapsto t^M$" in t8_tex_text or "convex" in t8_tex_text
    assert "strictly convex" not in t8_tex_text.lower(), "Teorema 8 não deve exigir 'strictly convex'"
    
    # Extrai o Teorema 8 do markdown
    t8_md = re.search(r"### Teorema 8.*?(.*?)(?=### Lema 9\.1|\Z)", md_content, re.DOTALL)
    assert t8_md is not None, "Seção do Teorema 8 deve existir no markdown"
    t8_md_text = t8_md.group(1)
    
    assert "convexa em $[0, 1]$" in t8_md_text
    assert "estritamente convexa" not in t8_md_text

def test_sobriety_title_and_conclusion_parecer19():
    """
    Verifica a sobriedade epistemológica exigida no Parecer 19:
    1. O título não promete 'Rigorous Dynamic Separations'.
    2. O título adota 'Rigorous Structural Results and Open Dynamical Problems'.
    3. A conclusão não usa 'explain why continuous relaxations exhibit divergent algorithmic accessibility'.
    4. A conclusão usa 'provide a rigorous framework for studying divergent dynamical accessibility'.
    5. O Item 2 da Proposição 7A foi completamente expurgado de ambos os documentos.
    """
    tex_path = os.path.join(PUB_DIR, "CLG_FOUNDATIONS_ARXIV.tex")
    md_path = os.path.join(PUB_DIR, "ESTUDO_ANALITICO_DO_CONJUNTO_CRITICO.md")
    
    with open(tex_path, "r", encoding="utf-8") as f:
        tex_content = f.read()
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
        
    # Título
    assert "Rigorous Dynamic Separations" not in tex_content
    assert "Rigorous Structural Results and Open Dynamical Problems" in tex_content
    
    # Conclusão
    assert "explain why continuous relaxations exhibit divergent algorithmic accessibility" not in tex_content
    assert "provide a rigorous framework for studying divergent dynamical accessibility" in tex_content
    
    # Ausência do Item 2 da Proposição 7A
    assert "maintaining positive coordinates" not in tex_content
    assert "producing rounding" not in tex_content
    assert "100% of trajectories" not in tex_content
    assert "mantendo coordenadas positivas" not in md_content
    assert "100% das trajetórias" not in md_content
