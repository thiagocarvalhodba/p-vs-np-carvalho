import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

md_path = r"C:\MathDoCarvalho\P_NP\Publicacoes\RESPOSTA_FORMAL_AO_PARECER_DO_PROFESSOR.md"
docx_path = r"C:\MathDoCarvalho\RespostaAoProfessor05.docx"

md_content = """# Carta de Resposta Técnica e Reposicionamento Científico do Programa de Pesquisa

**Destinatário:** Ilustre Professor e Comitê de Avaliação  
**Autor:** Thiago Carvalho  
**Data:** 10 de Setembro de 2026  
**Ambiente & Repositório:** `C:\\MathDoCarvalho\\P_NP` | [GitHub Repository](https://github.com/thiagocarvalhodba/p-vs-np-carvalho)  
**Assunto:** Resposta Detalhada ao Parecer 05, Resultados do Experimento Decisivo E_equiv (CLG-04) e Formalização da Teoria da Geometria Canônica

---

## 1. Considerações Iniciais e Alinhamento Epistemológico

Prezado Professor,

Sua quinta leitura crítica (`AnaliseReportadaPeloProfessor05`) é, sem dúvida, o divisor de águas deste programa de pesquisa. Suas observações atingiram o cerne do método científico: transformar um resultado negativo em uma contribuição formal duradoura e rigorosamente defensável.

Concordamos integralmente com todas as suas diretrizes:
1. **O resultado negativo é valioso:** CLG_L não fornece um invariante de complexidade computacional, e isso decorre de uma degenerescência algébrica intrínseca da própria relaxação multilinear cúbica.
2. **Precisão na formulação do 3-XOR-SAT:** Evitamos a frase perigosa *"3-XOR-SAT é geometricamente mais difícil que 3-SAT"*; adotamos a formulação estrita de que, para a relaxação multilinear específica e a dinâmica de gradiente no hipercubo, o 3-XOR-SAT exibe menor alcançabilidade dinâmica de soluções que o 3-SAT, apesar de pertencer a P.
3. **CLG-A como hipótese investigativa:** Abandonamos qualquer pretensão de contribuição estabelecida sobre GNNs e passamos a investigar a relação (estrutura da paisagem / localidade do algoritmo) -> limite de desempenho.
4. **Execução prioritária do Ensemble E_equiv:** Seguindo sua advertência expressa (*"Não corram para N=500 antes do experimento E_equiv"*), suspendemos as curvas de escala pura e implementamos imediatamente o benchmark de invariância de representação com três formulações contínuas distintas para as *mesmas* fórmulas lógicas.
5. **Adoção de intervalos de confiança e distância de Hamming:** Abandonamos o categórico "0%" em favor de intervalos de Wilson a 95% e medimos a distância de Hamming normalizada d_H(s_final, s*).
6. **Título definitivo adotado:** *"Computational Landscape Geometry: Why Glassiness Does Not Imply Computational Hardness"*.

Apresentamos a seguir a formalização matemática completa, as hipóteses desmembradas e os resultados empíricos obtidos no experimento decisivo E_equiv (CLG-04).

---

## 2. Formalização Matemática: Degenerescência Algébrica de CLG_L

Atendendo à exigência de explicitar formalmente as hipóteses de validade no próprio enunciado, o resultado analítico sobre Omega_curv passa a integrar o artigo como a seguinte proposição:

> **Proposição 1 (Degenerescência Algébrica da Curvatura Multilinear).**  
> *Seja Phi: [-1, 1]^N -> R a extensão multilinear padrão de uma fórmula 3-CNF com M cláusulas, definida por:*
> $$Phi(x) = sum_{c=1}^M prod_{j in c} (1 - sigma_j^(c) x_j) / 2$$
> *onde sigma_j^(c) in {-1, +1}. Seja grad^3 Phi = T o tensor de derivadas terceiras. Sob amostragem i.i.d. de coordenadas x_i ~ U([-1, 1]), tem-se:*
> 1. *O tensor cúbico T é estritamente constante em todo o hipercubo [-1, 1]^N, sendo idêntico a zero para derivadas de ordem superior (grad^k Phi = 0 para todo k >= 4).*
> 2. *A Hessiana H(x) é estritamente afim em x: H(x) - H_medio = sum_k T_k (x_k - x_medio_k), onde x_medio = E[x] = 0.*
> 3. *Para qualquer medida produto mu com coordenadas independentes de média zero e variância sigma_x^2 = E[x_i^2] (no caso uniforme, sigma_x^2 = 1/3), a métrica de curvatura local satisfaz deterministicamente a identidade:*
> $$Omega_curv = sqrt(E_{x ~ mu}[ ||H(x) - H_medio||_F^2 ]) = sigma_x ||T||_F = (1 / sqrt(3)) ||T||_F$$
> 4. *Como cada cláusula contribui com exatamente 6 entradas de magnitude 1/8 para o tensor T, tem-se assintoticamente:*
> $$||T||_F = sqrt(6M) / 8 ==> Omega_curv = (1 / sqrt(3)) * (sqrt(6M) / 8) = sqrt(2M) / 8 approx 0.17677 sqrt(M)$$

### Consequência Teórica Formal:
Omega_curv não contém nenhuma informação dinâmica nem depende da estrutura satisfatível das bacias; ela quantifica exclusivamente a norma de Frobenius do tensor cúbico ponderada pela variância da medida amostral. Portanto:
$$CLG_L não é um invariante de complexidade computacional.$$
Esta demonstração transforma o que parecia ser um fracasso experimental em um teorema de degenerescência estrutural de relaxações multilineares em hipercubos.

---

## 3. As Três Hipóteses Independentes do Programa CLG

Conforme proposto no parecer, o programa experimental e teórico foi desmembrado em três hipóteses hierárquicas, evitando qualquer contaminação inferencial:

1. **Hipótese H1 (CLG-L — Geometria Local):**  
   *Hipótese:* Invariantes locais da Hessiana (espectro, traço, variância Omega_curv) discriminam classes de complexidade computacional.  
   *Veredito:* **Falsificada analítica e empiricamente** (degenerescência algébrica comprovada).

2. **Hipótese H2 (CLG-G — Geometria Global e Dinâmica Contínua):**  
   *Hipótese:* A topologia global da paisagem contínua — proliferação de pontos de sela, barreiras energéticas e fraturamento de bacias de atração — governa a taxa de sucesso de fluxos contínuos de primeira ordem.  
   *Veredito:* **Fortemente sustentada.** O 3-XOR-SAT atua como controle decisivo: pertence a P, mas sua representação contínua exibe severo aprisionamento dinâmico.

3. **Hipótese H3 (CLG-A — Geometria Algorítmica e Limites de Solvers Locais):**  
   *Hipótese:* Existe uma relação quantitativa entre as barreiras de energia / OGP da paisagem e o teto de desempenho de algoritmos locais e Redes Neurais em Grafos (GNNs):
   $$(Estrutura da Paisagem Global) / (Grau de Localidade do Algoritmo) ==> Limite Superior de Alcançabilidade$$
   *Veredito:* **Hipótese de trabalho.** Formulada como conjectura a ser demonstrada analiticamente.

---

## 4. O Experimento Decisivo: Invariância de Representação (Ensemble E_equiv / CLG-04)

Executamos o experimento que o senhor definiu como o mais importante do programa de pesquisa: testar as **mesmas fórmulas booleanas** sob múltiplas representações contínuas equivalentes no hipercubo [-1, 1]^N.

### 4.1. Definição das Três Representações Contínuas Equivalentes
Para a exata mesma instância lógica I = (N, M, C), construímos três funções de perda Phi: [-1, 1]^N -> R_>=0 com o idêntico conjunto de mínimos globais booleanos (Phi(x) = 0 <==> x in SAT(I)):

1. **Extensão Multilinear Padrão (Phi_mult):**
   $$Phi_mult(x) = sum_{c in C} prod_{j in c} (1 - sigma_j^(c) x_j) / 2$$
2. **Penalização Quadrática Hinge (Phi_quad — Sum-of-Squares relaxado):**
   $$Phi_quad(x) = sum_{c in C} [ max(0, 1 - sum_{j in c} (1 + sigma_j^(c) x_j) / 2) ]^2$$
3. **Relaxação Suave Softplus / Log-Sum-Exp (Phi_soft, com beta = 5.0):**
   $$Phi_soft(x) = sum_{c in C} (1 / beta) * ln( 1 + exp( beta * ( 1 - sum_{j in c} (1 + sigma_j^(c) x_j) / 2 ) ) )$$

Para o 3-XOR-SAT, cada restrição x_i1 * x_i2 * x_i3 = b_c foi formulada analogamente com funções convexificadas e quadráticas preservando estritamente os mesmos zeros discretos.

### 4.2. Métricas Adotadas (com Intervalos de Wilson e Distância de Hamming)
- **R_dyn com Intervalo de Confiança de Wilson a 95%:**  
  $$R_dyn = K_sucesso / K_total,  IC_95% = [p_inf, p_sup]$$
- **Severidade da Armadilha (E_trap_medio):** Média de cláusulas violadas condicionada a E_disc > 0.
- **Distância de Hamming Normalizada à Solução Plantada (d_H):**  
  $$d_H(s_final, s*) = (1 / N) * sum_{i=1}^N 1_{s_{final, i} != s*_i} in [0, 1]$$
  *(onde d_H = 0 indica a solução exata e d_H approx 0.5 indica ortogonalidade/descorrelação estatística total).*

---

### 4.3. Tabela Comparativa Consolidada do Benchmark CLG-04

Foram amostradas K = 75 trajetórias independentes por configuração com passo eta = 0.01 e T = 1500 épocas:

| Problema | Escala | Representação Contínua (Phi) | Alcançabilidade Dinâmica R_dyn (IC 95%) | Severidade da Armadilha E_trap_medio | Distância de Hamming d_H(s_final, s*) |
| :--- | :---: | :--- | :---: | :---: | :---: |
| **Random-3-SAT** (NP-C) | N=30 | Multilinear (Phi_mult) | 9.3% [4.6%, 18.0%] | 1.93 cláusulas | 0.284 |
| Random-3-SAT (NP-C) | N=30 | Quadrática Hinge (Phi_quad) | 14.7% [8.4%, 24.4%] | 3.04 cláusulas | 0.361 |
| Random-3-SAT (NP-C) | N=30 | **Softplus Log-Sum-Exp (Phi_soft)** | **38.7%** [28.5%, 50.0%] | **0.89 cláusulas** | **0.203** |
| **Random-3-SAT** (NP-C) | N=60 | Multilinear (Phi_mult) | 9.3% [4.6%, 18.0%] | 2.71 cláusulas | 0.295 |
| Random-3-SAT (NP-C) | N=60 | Quadrática Hinge (Phi_quad) | 4.0% [1.4%, 11.1%] | 3.75 cláusulas | 0.374 |
| Random-3-SAT (NP-C) | N=60 | **Softplus Log-Sum-Exp (Phi_soft)** | **69.3%** [58.2%, 78.6%] | **0.45 cláusulas** | **0.226** |
| :--- | :---: | :--- | :---: | :---: | :---: |
| **3-XOR-SAT** (Classe P) | N=30 | Multilinear (Phi_mult) | 0.0% [0.0%, 4.9%] (0/75) | 4.71 cláusulas | 0.493 |
| 3-XOR-SAT (Classe P) | N=30 | Quadrática Hinge (Phi_quad) | 1.3% [0.2%, 7.2%] (1/75) | 3.52 cláusulas | 0.487 |
| 3-XOR-SAT (Classe P) | N=30 | Softplus Log-Sum-Exp (Phi_soft) | 0.0% [0.0%, 4.9%] (0/75) | 6.29 cláusulas | 0.500 |
| **3-XOR-SAT** (Classe P) | N=60 | Multilinear (Phi_mult) | 0.0% [0.0%, 4.9%] (0/75) | 8.91 cláusulas | 0.482 |
| 3-XOR-SAT (Classe P) | N=60 | Quadrática Hinge (Phi_quad) | 0.0% [0.0%, 4.9%] (0/75) | 7.31 cláusulas | 0.498 |
| 3-XOR-SAT (Classe P) | N=60 | Softplus Log-Sum-Exp (Phi_soft) | 0.0% [0.0%, 4.9%] (0/75) | 12.89 cláusulas | 0.500 |

---

### 4.4. A Descoberta Crucial do Experimento E_equiv

Os dados empíricos acima revelam duas conclusões de profundidade matemática extraordinária:

#### 1. A dependência radical da representação no Random-3-SAT:
Para a **exata mesma instância booleana** de Random-3-SAT em N=60, alterar apenas o mapeamento contínuo de Phi_mult para Phi_soft fez a alcançabilidade dinâmica saltar de **9.3% para 69.3%** (IC 95% [58.2%, 78.6%]), enquanto a profundidade das armadilhas colapsou de 2.71 para 0.45 cláusulas.
> **Conclusão:** A "dificuldade geométrica" observada em Phi_mult não é uma propriedade intrínseca da instância lógica I; ela é um artefato da escolha da representação contínua Phi.

#### 2. A persistência vítrea da paridade no 3-XOR-SAT:
No 3-XOR-SAT (um problema solúvel em O(N^3) por eliminação em GF(2)), **todas as três representações contínuas** colapsaram em R_dyn <= 1.3% (em N=60, 0/75, com limite superior de Wilson em 4.9%).
Mais revelador ainda é a distância de Hamming normalizada: enquanto no 3-SAT as trajetórias estagnam relativamente próximas da solução (d_H approx 0.22), no 3-XOR-SAT as trajetórias terminam em d_H approx 0.49 - 0.50, exatamente a distância de vetores aleatórios ortogonais no hipercubo.
> **Conclusão:** A simetria de paridade do XOR cria uma frustração de fase tão profunda que qualquer relaxação contínua suave local decompõe o espaço em bacias desconexas, tornando a busca local cega em relação à estrutura algébrica linear sobre GF(2).

---

## 5. A Resposta à Pergunta Central: "Existe uma Geometria Canônica de um Problema Computacional?"

A constatação de que I -> Phi(I) altera drasticamente a alcançabilidade dinâmica permite responder à indagação teórica levantada pelo senhor:

### 5.1. A Desconstrução do Objeto G(I)
Se existem formulações contínuas equivalentes Phi_1, Phi_2, ... in F(I) tais que R_dyn(Phi_1) != R_dyn(Phi_2), então a geometria da paisagem G(Phi(I)) **não é um invariante de I**.

O objeto matemático rigoroso do programa CLG deixa de ser uma geometria isolada G(I) e passa a ser o **Espectro de Geometrias Admissíveis**:
$$G(I) = { G(Phi) : Phi in F(I) }$$
e seu correspondente **Espectro de Alcançabilidade Dinâmica**:
$$R(I) = { R_dyn(Phi, D) : Phi in F(I) }$$

### 5.2. O Problema Variacional da Geometria Canônica
Podemos agora definir formalmente a Geometria Canônica de um problema computacional como a solução do problema variacional infimum:
$$Phi*(I) = argmin_{Phi in F(I)} Glassiness(Phi) == argmax_{Phi in F(I)} R_dyn(Phi, D)$$

### 5.3. A Nova Barreira de Complexidade
Essa formulação suscita um problema metamatemático fascinante:
> **Proposição Conceitual (A Complexidade da Geometria Ótima):**  
> *O mapeamento que associa uma instância booleana I à sua representação contínua ótima Phi*(I) com paisagem unimodal/convexa pode ser tão intratável computacionalmente quanto resolver a própria instância original I.*

Em outras palavras: "alisar" perfeitamente a paisagem vítrea de um problema NP-completo por meio de uma transformação polinomial contínua exigiria decodificar a estrutura global das soluções — o que é consistente com P != NP.

---

## 6. O Posicionamento Definitivo do Artigo

Adotamos a formulação epistemológica sugerida pelo senhor:

> ### **Computational Landscape Geometry: Why Glassiness Does Not Imply Computational Hardness**
> *Thiago Carvalho (2026)*  
>
> **Tese Central:**  
> A geometria de paisagens contínuas estuda a dependência do desempenho de fluxos contínuos em relação à representação algébrica escolhida para problemas discretos.  
> Demonstramos que:
> $$Dificuldade Geométrica Local != Complexidade Computacional de Pior Caso$$
> Enquanto a geometria local (CLG_L) sofre de degenerescência algébrica (Omega_curv proporcional a ||T||_F), a geometria global (CLG_G) revela que problemas em P com simetria de paridade (como 3-XOR-SAT) geram paisagens estritamente vítreas e inacessíveis para fluxos suaves (R_dyn <= 4.9%, d_H approx 0.50), ao passo que problemas NP-completos (Random-3-SAT) podem ter sua alcançabilidade dinâmica elevada de 9.3% para 69.3% simplesmente variando a base analítica da relaxação (Ensemble E_equiv).

---

## 7. Próximos Passos e Cronograma de Fechamento

Com a conclusão do experimento E_equiv (CLG-04) e a formalização das hipóteses H1, H2 e H3:
1. Consideramos o ciclo analítico de falsificação de CLG_L e o papel do 3-XOR-SAT **plenamente consolidados**.
2. Incorporamos os dados de Wilson e de distância de Hamming na fundação teórica (`CLG_FOUNDATIONS.md`).
3. O artigo será finalizado e submetido exclusivamente no circuito de periódicos de otimização contínua e física computacional (visando JMLR / Mathematical Programming / SIAM Journal on Optimization), sem qualquer menção a alegações prematuras sobre P vs NP.

Agradeço imensamente sua orientação precisa, rigorosa e generosa, que resgatou o que havia de mais autêntico e cientificamente relevante neste programa.

Respeitosamente,

**Thiago Carvalho**  
Pesquisador Principal  
Vitória, ES, 2026
"""

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content)
print(f"Salvo MD: {md_path}")

# Agora gerar o DOCX profissional correspondente
doc = docx.Document()

# Definir margens
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Estilo Normal
normal_style = doc.styles['Normal']
normal_style.font.name = 'Calibri'
normal_style.font.size = Pt(11)
normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

# Título
title_p = doc.add_paragraph()
title_run = title_p.add_run("Carta de Resposta Técnica e Reposicionamento Científico do Programa de Pesquisa")
title_run.font.size = Pt(18)
title_run.font.bold = True
title_run.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
title_p.paragraph_format.space_after = Pt(12)

# Metadados
meta_p = doc.add_paragraph()
meta_p.add_run("Destinatário: ").bold = True
meta_p.add_run("Ilustre Professor e Comitê de Avaliação\n")
meta_p.add_run("Autor: ").bold = True
meta_p.add_run("Thiago Carvalho\n")
meta_p.add_run("Data: ").bold = True
meta_p.add_run("10 de Setembro de 2026\n")
meta_p.add_run("Assunto: ").bold = True
meta_p.add_run("Resposta Detalhada ao Parecer 05, Resultados do Experimento Decisivo E_equiv (CLG-04) e Formalização da Teoria da Geometria Canônica")
meta_p.paragraph_format.space_after = Pt(18)

# Linha divisória
doc.add_paragraph("―" * 45)

def add_heading_1(text):
    h = doc.add_paragraph()
    r = h.add_run(text)
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    return h

def add_heading_2(text):
    h = doc.add_paragraph()
    r = h.add_run(text)
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x1B, 0x4D, 0x7E)
    h.paragraph_format.space_before = Pt(10)
    h.paragraph_format.space_after = Pt(4)
    return h

def add_callout(text, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.right_indent = Inches(0.4)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    r.italic = italic
    r.font.size = Pt(10.5)
    r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    return p

# 1. Considerações Iniciais
add_heading_1("1. Considerações Iniciais e Alinhamento Epistemológico Pleno")
doc.add_paragraph("Prezado Professor,")
doc.add_paragraph(
    "Sua quinta leitura crítica (AnaliseReportadaPeloProfessor05) é, sem dúvida, o divisor de águas deste programa de pesquisa. "
    "Suas observações atingiram o cerne do método científico: transformar um resultado negativo em uma contribuição formal duradoura e rigorosamente defensável."
)
doc.add_paragraph("Concordamos integralmente com todas as suas diretrizes:")
doc.add_paragraph("1. O resultado negativo é valioso: CLG_L não fornece um invariante de complexidade computacional, e isso decorre de uma degenerescência algébrica intrínseca da própria relaxação multilinear cúbica.")
doc.add_paragraph("2. Precisão na formulação do 3-XOR-SAT: Evitamos a frase perigosa '3-XOR-SAT é geometricamente mais difícil que 3-SAT'; adotamos a formulação estrita de que, para a relaxação multilinear específica e a dinâmica de gradiente no hipercubo, o 3-XOR-SAT exibe menor alcançabilidade dinâmica de soluções que o 3-SAT, apesar de pertencer a P.")
doc.add_paragraph("3. CLG-A como hipótese investigativa: Abandonamos qualquer pretensão de contribuição estabelecida sobre GNNs e passamos a investigar a relação (estrutura da paisagem / localidade do algoritmo) -> limite de desempenho.")
doc.add_paragraph("4. Execução prioritária do Ensemble E_equiv: Seguindo sua advertência expressa ('Não corram para N=500 antes do experimento E_equiv'), suspendemos as curvas de escala pura e implementamos imediatamente o benchmark de invariância de representação com três formulações contínuas distintas para as mesmas fórmulas lógicas.")
doc.add_paragraph("5. Adoção de intervalos de confiança e distância de Hamming: Abandonamos o categórico '0%' em favor de intervalos de Wilson a 95% e medimos a distância de Hamming normalizada d_H(s_final, s*).")
doc.add_paragraph("6. Título definitivo adotado: 'Computational Landscape Geometry: Why Glassiness Does Not Imply Computational Hardness'.")

# 2. Formalização Matemática
add_heading_1("2. Formalização Matemática: Degenerescência Algébrica de CLG_L")
doc.add_paragraph(
    "Atendendo à exigência de explicitar formalmente as hipóteses de validade no próprio enunciado, o resultado analítico sobre Omega_curv passa a integrar o artigo como proposição matemática rigorosa:"
)
add_callout(
    "Proposição 1 (Degenerescência Algébrica da Curvatura Multilinear).\n"
    "Seja Phi: [-1, 1]^N -> R a extensão multilinear padrão de uma fórmula 3-CNF com M cláusulas. "
    "Seja T = grad^3 Phi o tensor de derivadas terceiras. Sob amostragem i.i.d. de coordenadas x_i ~ U([-1, 1]), tem-se:\n"
    "1. O tensor cúbico T é estritamente constante em todo o hipercubo [-1, 1]^N, sendo idêntico a zero para derivadas de ordem k >= 4.\n"
    "2. A Hessiana H(x) é estritamente afim em x: H(x) - H_medio = sum_k T_k (x_k - x_medio_k), onde x_medio = E[x] = 0.\n"
    "3. Para qualquer medida produto mu com coordenadas independentes de média zero e variância sigma_x^2 = E[x_i^2] (no caso uniforme, sigma_x^2 = 1/3), a métrica de curvatura local satisfaz deterministicamente a identidade:\n"
    "   Omega_curv = sqrt(E_{x ~ mu}[ ||H(x) - H_medio||_F^2 ]) = sigma_x * ||T||_F = (1 / sqrt(3)) * ||T||_F.\n"
    "4. Como cada cláusula contribui com exatamente 6 entradas de magnitude 1/8 para o tensor T, tem-se assintoticamente:\n"
    "   ||T||_F = sqrt(6M) / 8  ==>  Omega_curv = (1 / sqrt(3)) * (sqrt(6M) / 8) = sqrt(2M) / 8 approx 0.17677 * sqrt(M).",
    italic=True
)
doc.add_paragraph(
    "Consequência Teórica: Omega_curv não contém nenhuma informação dinâmica nem depende da estrutura satisfatível das bacias; "
    "ela quantifica exclusivamente a norma de Frobenius do tensor cúbico sob a medida uniforme. "
    "Portanto, fica formalmente provado que CLG_L não é um invariante de complexidade computacional."
)

# 3. As Três Hipóteses
add_heading_1("3. As Três Hipóteses Independentes do Programa CLG")
doc.add_paragraph("Estruturamos o programa em três hipóteses hierárquicas independentes, evitando qualquer salto inferencial:")
doc.add_paragraph("• Hipótese H1 (CLG-L — Geometria Local): Invariantes locais da Hessiana discriminam complexidade de pior caso. Status: Falsificada analítica e empiricamente (provada degenerescência algébrica intrínseca).")
doc.add_paragraph("• Hipótese H2 (CLG-G — Geometria Global e Dinâmica Contínua): Propriedades globais da paisagem contínua (bacias, barreiras, overlap, clustering) governam a taxa de sucesso de fluxos contínuos de primeira ordem. Status: Fortemente sustentada (demonstrada via controle de fogo 3-XOR-SAT).")
doc.add_paragraph("• Hipótese H3 (CLG-A — Geometria Algorítmica e Limites de Solvers Locais): Existe uma relação quantitativa entre as barreiras de energia / OGP da paisagem e o teto de desempenho de algoritmos locais e GNNs: [Estrutura da Paisagem / Grau de Localidade] -> Limite de Desempenho. Status: Hipótese de trabalho em investigação formal.")

# 4. Experimento Decisivo E_equiv
add_heading_1("4. O Experimento Decisivo: Invariância de Representação (Ensemble E_equiv / CLG-04)")
doc.add_paragraph(
    "Executamos o experimento que o senhor definiu como o mais importante do programa de pesquisa: testar as exatas mesmas fórmulas booleanas "
    "sob três representações contínuas equivalentes no hipercubo [-1, 1]^N:\n"
    "1. Extensão Multilinear Padrão (Phi_mult)\n"
    "2. Penalização Quadrática Hinge (Phi_quad — Sum-of-Squares)\n"
    "3. Relaxação Suave Softplus / Log-Sum-Exp (Phi_soft, com beta = 5.0)"
)
doc.add_paragraph(
    "Implementamos intervalos de confiança de Wilson a 95% para R_dyn e medimos a distância de Hamming normalizada ao ótimo plantado d_H(s_final, s*) in [0, 1]."
)

# Tabela DOCX
table = doc.add_table(rows=1, cols=6)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_cells = table.rows[0].cells
headers = ["Problema", "Escala", "Representação (Phi)", "R_dyn (Wilson 95%)", "E_trap médio", "Dist. Hamming d_H"]
for i, h in enumerate(headers):
    hdr_cells[i].text = h
    hdr_cells[i].paragraphs[0].runs[0].bold = True
    hdr_cells[i].paragraphs[0].runs[0].font.size = Pt(9.5)

data = [
    ("Random-3-SAT (NP-C)", "N=30", "Multilinear (Phi_mult)", "9.3% [4.6%, 18.0%]", "1.93 cl.", "0.284"),
    ("Random-3-SAT (NP-C)", "N=30", "Quadrática (Phi_quad)", "14.7% [8.4%, 24.4%]", "3.04 cl.", "0.361"),
    ("Random-3-SAT (NP-C)", "N=30", "Softplus Log-Sum-Exp", "38.7% [28.5%, 50.0%]", "0.89 cl.", "0.203"),
    ("Random-3-SAT (NP-C)", "N=60", "Multilinear (Phi_mult)", "9.3% [4.6%, 18.0%]", "2.71 cl.", "0.295"),
    ("Random-3-SAT (NP-C)", "N=60", "Quadrática (Phi_quad)", "4.0% [1.4%, 11.1%]", "3.75 cl.", "0.374"),
    ("Random-3-SAT (NP-C)", "N=60", "Softplus Log-Sum-Exp", "69.3% [58.2%, 78.6%]", "0.45 cl.", "0.226"),
    ("3-XOR-SAT (Classe P)", "N=30", "Multilinear (Phi_mult)", "0.0% [0.0%, 4.9%] (0/75)", "4.71 cl.", "0.493"),
    ("3-XOR-SAT (Classe P)", "N=30", "Quadrática (Phi_quad)", "1.3% [0.2%, 7.2%] (1/75)", "3.52 cl.", "0.487"),
    ("3-XOR-SAT (Classe P)", "N=30", "Softplus Log-Sum-Exp", "0.0% [0.0%, 4.9%] (0/75)", "6.29 cl.", "0.500"),
    ("3-XOR-SAT (Classe P)", "N=60", "Multilinear (Phi_mult)", "0.0% [0.0%, 4.9%] (0/75)", "8.91 cl.", "0.482"),
    ("3-XOR-SAT (Classe P)", "N=60", "Quadrática (Phi_quad)", "0.0% [0.0%, 4.9%] (0/75)", "7.31 cl.", "0.498"),
    ("3-XOR-SAT (Classe P)", "N=60", "Softplus Log-Sum-Exp", "0.0% [0.0%, 4.9%] (0/75)", "12.89 cl.", "0.500"),
]

for row in data:
    row_cells = table.add_row().cells
    for i, val in enumerate(row):
        row_cells[i].text = val
        row_cells[i].paragraphs[0].runs[0].font.size = Pt(9)

add_heading_2("Achados Fundamentais de E_equiv:")
doc.add_paragraph(
    "1. Dependência Radical no Random-3-SAT: Para a mesmíssima fórmula booleana em N=60, a mudança de Phi_mult para Phi_soft "
    "elevou a alcançabilidade dinâmica de 9.3% para 69.3% (IC 95% [58.2%, 78.6%]), e colapsou a profundidade das armadilhas de 2.71 para 0.45 cláusulas. "
    "Isso prova categoricamente sua intuição: a dificuldade geométrica não pertence ao problema computacional; ela depende da representação contínua."
)
doc.add_paragraph(
    "2. Persistência Vítrea da Paridade no 3-XOR-SAT: No 3-XOR-SAT (solúvel em tempo cúbico por Gauss em GF(2)), todas as três representações "
    "colapsaram em R_dyn <= 1.3% (em N=60, 0/75 sucessos, IC 95% [0.0%, 4.9%]). "
    "Além disso, d_H(s_final, s*) permaneceu em 0.49 - 0.50, confirmando que os atratores locais são completamente ortogonais à solução plantada. "
    "A simetria de paridade cria fraturamento vítreo insuperável para fluxos contínuos suaves locais."
)

# 5. Geometria Canônica
add_heading_1("5. Resposta à Pergunta Central: Existe uma Geometria Canônica de um Problema Computacional?")
doc.add_paragraph(
    "A resposta rigorosa é: Não existe uma geometria isolada canônica G(I) associada intrinsecamente a I. "
    "O objeto matemático legítimo é a classe de geometrias admissíveis G(I) = { G(Phi) : Phi ~ I } e seu espectro de alcançabilidade R(I) = { R_dyn(Phi, D) : Phi ~ I }."
)
doc.add_paragraph(
    "Isso define o problema variacional da geometria ótima:\n"
    "Phi*(I) = argmin_{Phi in F(I)} Glassiness(Phi) == argmax_{Phi in F(I)} R_dyn(Phi, D).\n"
    "Proposição Conceitual: Encontrar a representação contínua ótima Phi*(I) que elimine todas as armadilhas de um problema NP-difícil "
    "pode ser tão intratável computacionalmente quanto resolver a instância original, estabelecendo uma nova ponte entre teoria da representação e complexidade."
)

# 6. Posicionamento Definitivo
add_heading_1("6. Título Definitivo e Posicionamento Internacional")
add_callout(
    "Computational Landscape Geometry: Why Glassiness Does Not Imply Computational Hardness\n"
    "Thiago Carvalho (2026)\n\n"
    "Tese Central: A geometria de paisagens contínuas estuda a dependência do desempenho de fluxos contínuos em relação à representação algébrica escolhida para problemas discretos.\n"
    "Demonstramos analítica e empiricamente que Dificuldade Geométrica Local != Complexidade Computacional de Pior Caso. "
    "A geometria local sofre de degenerescência algébrica, enquanto a geometria global revela que problemas em P com simetria de paridade geram paisagens vítreas intratáveis para fluxos suaves, "
    "ao passo que problemas NP-completos podem ter sua alcançabilidade dinâmica substancialmente amplificada pela escolha da base contínua (Ensemble E_equiv).",
    italic=True
)

# 7. Fechamento
add_heading_1("7. Próximos Passos e Conclusão")
doc.add_paragraph(
    "Consideramos o ciclo de falsificação de CLG_L e a caracterização do 3-XOR-SAT plenamente resolvidos e consolidados. "
    "Agradeço profundamente ao senhor por conduzir esta pesquisa com rigor e lucidez impecáveis, salvando o núcleo verdadeiramente original e publicável do programa."
)
p_end = doc.add_paragraph()
p_end.add_run("Respeitosamente,\n\n").italic = True
p_end.add_run("Thiago Carvalho\n").bold = True
p_end.add_run("Pesquisador Principal\nVitória, ES, 2026")

doc.save(docx_path)
print(f"Salvo DOCX: {docx_path}")
