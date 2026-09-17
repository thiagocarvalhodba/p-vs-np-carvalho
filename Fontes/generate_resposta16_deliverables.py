"""
Script gerador dos entregáveis formais em resposta ao Parecer nº 16 do Professor.
Gera:
1. Publicacoes/PARECER_16_AUDITORIA_CRITICA_PROFESSOR.md (e copia para a raiz C:\\MathDoCarvalho)
2. Publicacoes/RespostaAoProfessor_Analise16.md (e copia para a raiz C:\\MathDoCarvalho)
3. Publicacoes/RespostaAoProfessor_Analise16.docx (e copia para a raiz C:\\MathDoCarvalho)
4. Publicacoes/MensagemParaOAvaliador16.docx (e copia para a raiz C:\\MathDoCarvalho)
5. Publicacoes/MensagemParaOAvaliador16.txt (e copia para a raiz C:\\MathDoCarvalho)
6. Atualizacao do Publicacoes/arxiv_package.zip
"""
import os
import sys
import re
import zipfile
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

ROOT_DIR = r"C:\MathDoCarvalho"
REPO_DIR = r"C:\MathDoCarvalho\P_NP"
PUB_DIR = os.path.join(REPO_DIR, "Publicacoes")

MENSAGEM_16_TEXTO = """Prezado Professor,

Agradecemos profundamente pela leitura atenta e rigorosa da Versão 4.0.1 e pelo retorno objetivo consubstanciado no Parecer nº 16. Registramos com grande satisfação a sua chancela ao método científico adotado: a falsificação analítica e experimental do Lema 9.1, a retificação do erro de Stirling e a demarcação estrita entre o que foi formalmente demonstrado e o que permanece aberto.

Acolhemos integralmente todas as observações apontadas na auditoria e executamos pontualmente os quatro alvos cirúrgicos prescritos por Vossa Senhoria:

1. Teorema 8 — Retirada Imediata da Conclusão Assintótica:
   Retiramos integralmente a alegação assintótica lim_{N->infty} E[mu(Z)] = 0. O Teorema 8 foi rigorosamente delimitado ao seu resultado matemático demonstrado: uma COTA INFERIOR DE VOLUME EM DIMENSÃO FINITA, garantindo E[mu_norm(Z)] >= (5/6)^{floor(alpha N)} > 0 para todo N finito. Reconhecemos que uma cota inferior positiva não prova decaimento a zero, e que tal limite exigiria uma cota superior exponencial independente. O status do Teorema 8 é fixado estritamente como 🟡 FECHADO APENAS COMO COTA INFERIOR FINITA.

2. Proposição 7A — Re-Auditoria do Jacobiano da Dinâmica Contínua:
   Confirmamos o erro de sinal no texto preliminar: para cláusulas puramente negativas P_c(x) = (1+x_i)(1+x_j)(1+x_k)/8, temos d^2 P_c / dx_i dx_j = (1+x_k)/8 >= 0, de onde o Jacobiano do campo f_i = -dPhi/dx_i é J_ij = -d^2 Phi / dx_i dx_j <= 0. O sistema contínuo é estritamente COMPETITIVO / INIBITÓRIO, e NÃO cooperativo. Reclassificamos a Proposição 7A formalmente como 🟡 PRECISA DE NOVA AUDITORIA, suspendendo qualquer inferência dinâmica baseada no Teorema de Hirsch até a rederivação analítica completa.

3. Teorema 10 — Classificação das Faces d = 1 (Arestas) e Variedades Críticas Degeneradas:
   Completamos a análise da dimensionalidade de faces do hipercubo X = [-1, 1]^N:
   - Para faces de dimensão d >= 2: o Lema 10.2 garante strict saddles (lambda_min < 0) sob H_leaf via traço nulo e derivada cruzada não-nula;
   - Para vértices d = 0: ausência de mínimos locais Booleanos positivos sob H_leaf;
   - Para arestas d = 1: Phi_mult restrita à aresta é afim (Phi_mult(t) = a*t + b). Se a != 0, não existe ponto crítico no interior aberto (-1, 1); se a = 0, toda a aresta aberta constitui uma variedade crítica degenerada plana (flat critical manifold) onde grad_F Phi identicamente 0 e a energia coincide com a dos vértices adjacentes.
   Como essa variedade plana de dimensão 1 não é coberta pelos teoremas usuais de evasão de strict saddles (Lee et al. 2016), mantemos o Teorema 10 inequivocamente classificado como 🔴 NÃO FECHADO.

4. Lema 10.1 — Adoção da Formulação Segura de Primeira-Momento:
   Substituímos qualquer menção de que 'quase todas as componentes são hiperárvores lineares' pela formulação segura prescrita por Vossa Senhoria: 'A cota de primeiro momento mostra que o número esperado de pares de cláusulas com interseção de pelo menos duas variáveis é O(1) (<= 9 alpha^2). A decomposição em um núcleo de componentes lineares acíclicas mais um conjunto estocasticamente limitado O_P(1) de defeitos estruturais permanece sujeita a uma análise estrutural adicional.' Status: 🟡 PARCIAL.

5. Harmonização Editorial do Manuscrito (LaTeX e Monografia):
   - Atualizamos a data no cabeçalho do LaTeX para September 16, 2026.
   - Harmonizamos o Resumo Executivo (Abstract): os itens (8), (9) e (10) expurgam qualquer alegação de separação provada para Horn ou subcrítico, alinhando o abstract estritamente com as limitações descritas no corpo do manuscrito.

6. Adoção Integral da Matriz de Rigor da Seção 16:
   Adotamos a matriz de status exatamente como prescrita por Vossa Senhoria (T1-T6, T4A'/4B 🟢; T7B 🟡; T8 🟡 finita; T9 🔴; Lema 10.1 🟡; Lema 10.2 🟡 sob H_leaf; Teorema 10 🔴; Proposição 7A 🟡; Conjectura Central 🔵; Firewall 3-XOR 🟢).

Seguem anexos o Parecer do Avaliador (transcrição integral), o Relatório de Resposta Técnica Detalhada (MD e DOCX) e o arquivo de distribuição arXiv atualizado.

Respeitosamente,
Thiago Carvalho
Pesquisador Principal — Framework CLG-R"""

RESPOSTA_16_MD = """# Resposta Técnica ao Parecer nº 16 do Professor:
## Relatório de Auditoria Cirúrgica nos Quatro Alvos, Classificação Geométrica e Matriz de Rigor 16

**Destinatário:** Ilustre Professor e Comitê de Avaliação Externa  
**Autor:** Thiago Carvalho e Equipe de Pesquisa do Framework CLG-R  
**Data:** 16 de Setembro de 2026  
**Repositório GitHub:** [https://github.com/thiagocarvalhodba/p-vs-np-carvalho](https://github.com/thiagocarvalhodba/p-vs-np-carvalho)  
**Assunto:** Acolhimento integral do Parecer nº 16; Execução cirúrgica dos 4 alvos de auditoria: (1) Saneamento do Teorema 8 para cota inferior finita estrita; (2) Re-auditoria do Jacobiano competitivo na Proposição 7A ($J_{ij} \\le 0$); (3) Classificação completa das faces $d=1$ (arestas degeneradas flat) no Teorema 10; (4) Formulação segura $\\mathcal{O}(1)$ no Lema 10.1; Atualização editorial do Abstract e data no LaTeX; e Adoção fiel da Matriz de Rigor 16.

---

## 1. Posicionamento e Acolhimento da Filosofia Científica do Parecer 16

Expressamos nosso mais sincero reconhecimento pelo rigor matemático de alto nível demonstrado no Parecer nº 16. Conforme destacado por Vossa Senhoria:

> *"A equipe fez exatamente a coisa certa com a minha crítica anterior: não tentou defender os resultados a qualquer custo. Mas agora aconteceu algo interessante: ao corrigir os problemas anteriores, o manuscrito revelou três novas fronteiras matemáticas reais: T8, T10 e Lema 10.1, além da questão da Proposição 7A. Eu não faria uma 'Resposta 16' geral agora. Faria o contrário: congelaria o manuscrito e abriria uma auditoria cirúrgica em quatro alvos..."*

Acolhemos integralmente esse direcionamento e executamos a auditoria cirúrgica exatamente nos quatro alvos prescritos.

---

## 2. Alvo 1: Teorema 8 — Retirada Imediata da Conclusão Assintótica

### 2.1. O Diagnóstico Matemático de Vossa Senhoria
Na versão anterior, o Teorema 8 deduzia via desigualdade de Jensen a cota inferior:
$$\\mathbb{E}[\\mu(Z)] \\ge \\left(\\frac{5}{6}\\right)^{\\lfloor \\alpha N \\rfloor} > 0$$
e afirmava:
$$\\lim_{N \\to \\infty} \\mathbb{E}[\\mu(Z)] = 0 \\quad \\text{com decaimento exponencial controlado}.$$
Vossa Senhoria demonstrou a falácia lógica dessa conclusão:
* Uma cota inferior que tende a zero ($\\ell(N) \\to 0$) **não prova** que a quantidade em si tende a zero. Por exemplo, a função constante $f(N) = 1/2$ satisfaz $f(N) \\ge (5/6)^N$, mas $\\lim_{N \\to \\infty} f(N) = 1/2 \\ne 0$.
* Da mesma forma, a existência da cota inferior estabelece uma cota superior sobre a taxa de decaimento (se houver decaimento), mas não demonstra que o volume decai exponencialmente para zero.

### 2.2. Ação Corretiva Executada
1. **Supressão Total da Afirmação de Limite Assintótico:** Removemos do manuscrito LaTeX (`CLG_FOUNDATIONS_ARXIV.tex`) e da monografia (`ESTUDO_ANALITICO_DO_CONJUNTO_CRITICO.md`) a alegação $\\lim_{N \\to \\infty} \\mathbb{E}[\\mu(Z)] = 0$.
2. **Redefinição Rigorosa do Enunciado:** O Teorema 8 é redefinido estritamente como:
   $$\\boxed{\\textbf{Teorema 8 (Cota Inferior de Volume do Politopo LP em Dimensão Finita): } \\mathbb{E}[\\mu_{\\text{norm}}(Z)] \\ge \\left(\\frac{5}{6}\\right)^{\\lfloor \\alpha N \\rfloor} > 0, \\quad \\forall N \\ge 3.}$$
3. **Registro Explícito:** O texto agora registra que a prova de que $\\mu(Z) \\to 0$ quando $N \\to \\infty$ exigiria uma cota superior analítica independente (e.g., $\\mathbb{E}[\\mu(Z)] \\le C \\rho^{\\alpha N}$ com $\\rho < 1$), a qual permanece um problema aberto.
4. **Status Formal Adotado:**
   $$\\boxed{\\text{Teorema 8: } \\textbf{🟡 Fechado apenas como cota inferior finita}}$$

---

## 3. Alvo 2: Proposição 7A — Re-Auditoria do Jacobiano da Dinâmica Contínua

### 3.1. O Diagnóstico de Vossa Senhoria
No texto preliminar da monografia, afirmava-se para a família de cláusulas puramente negativas que $J_{ij} = \\frac{1}{4} > 0$, invocando a teoria de sistemas cooperativos de Hirsch.

Vossa Senhoria apontou a incompatibilidade analítica com a formulação multilinear:
* Para uma cláusula multilinear negativa de 3 variáveis $c = (\\neg x_i \\lor \\neg x_j \\lor \\neg x_k)$, o potencial de penalidade é:
  $$P_c(x) = \\left(\\frac{1+x_i}{2}\\right)\\left(\\frac{1+x_j}{2}\\right)\\left(\\frac{1+x_k}{2}\\right) = \\frac{(1+x_i)(1+x_j)(1+x_k)}{8}$$
* A derivada de segunda ordem cruzada com relação a $x_i$ e $x_j$ é:
  $$\\frac{\\partial^2 P_c}{\\partial x_i \\partial x_j} = \\frac{1+x_k}{8} \\ge 0 \\quad (\\text{já que } x_k \\in [-1, 1])$$
* O campo vetorial contínuo da dinâmica do gradiente é:
  $$f_i(x) = -\\frac{\\partial \\Phi}{\\partial x_i} = -\\sum_{c} \\frac{\\partial P_c}{\\partial x_i}$$
* Portanto, as entradas fora da diagonal da matriz Jacobiana do campo $f$ são:
  $$J_{ij}(x) = \\frac{\\partial f_i}{\\partial x_j}(x) = -\\frac{\\partial^2 \\Phi}{\\partial x_i \\partial x_j}(x) = -\\sum_{c \\ni x_i, x_j} \\frac{1+x_{k(c)}}{8} \\le 0$$

### 3.2. Consequência Dinâmica e Ação Corretiva
1. **Inversão de Categoria Dinâmica:** Como $J_{ij}(x) \\le 0$ para todo $i \\ne j$, o sistema contínuo é **estritamente competitivo (inibitório)**, e NÃO cooperativo.
2. **Inaplicabilidade Direta do Teorema de Hirsch:** O Teorema de Hirsch de sistemas cooperativos exige $J_{ij} \\ge 0$. Em sistemas competitivos, a monotonicidade de ordem opera de maneira distinta (reversão de ordem ou dinâmica em variedades invariantes), exigindo uma análise completamente nova.
3. **Suspensão de Alegações de Hirsch:** Suspendemos integralmente qualquer conclusão sobre atração universal baseada em cooperatividade para famílias negativas gerais.
4. **Status Formal Adotado:**
   $$\\boxed{\\text{Proposição 7A: } \\textbf{🟡 Precisa de nova auditoria}}$$

---

## 4. Alvo 3: Teorema 10 — Classificação das Faces $d = 1$ (Arestas) e Variedades Flat

### 4.1. O Diagnóstico de Vossa Senhoria
O Lema 10.2 estabelece que em faces de dimensão $d \\ge 2$, sob a hipótese $H_{\\text{leaf}}$, o traço nulo $\\text{Tr}(\\nabla^2_{\\mathcal{F}} \\Phi_{\\text{mult}}) = 0$ e a não-nulidade do acoplamento folha $H_{\\ell p} = \\frac{\\sigma_\\ell \\sigma_p}{8}(1 - \\sigma_k x^*_k) \\ne 0$ garantem que a Hessiana tangencial é não-nula e possui $\\lambda_{\\min} < 0$, constituindo *strict saddles*.

Nos vértices ($d = 0$), demonstrou-se a ausência de mínimos Booleanos positivos sob $H_{\\text{leaf}}$.

Contudo, Vossa Senhoria identificou a lacuna estrutural no tratamento de **faces de dimensão $d = 1$ (arestas)**:
* Uma aresta $\\mathcal{F}$ do hipercubo é parametrizada por uma única coordenada livre $x_i = t \\in [-1, 1]$, com as demais $N-1$ coordenadas fixadas em $\\pm 1$.
* A restrição do potencial multilinear a essa aresta é afim:
  $$\\Phi_{\\text{mult}}(t) = a t + b$$
* Duas situações exclusivas ocorrem:
  1. **Se $a \\ne 0$:** O gradiente tangencial é constante e estritamente não-nulo: $\\nabla_{\\mathcal{F}} \\Phi = a \\ne 0$. Logo, **não existe nenhum ponto crítico no interior aberto da aresta** $(-1, 1)$. O fluxo gradiente projeta a trajetória diretamente para um dos dois vértices limítrofes ($t = +1$ ou $t = -1$).
  2. **Se $a = 0$:** O gradiente tangencial anula-se identicamente ao longo de toda a aresta: $\\nabla_{\\mathcal{F}} \\Phi \\equiv 0$. Portanto, o segmento aberto $(-1, 1)$ inteiro consiste em uma **variedade crítica degenerada plana (flat critical segment)**, onde todos os pontos têm exatamente o mesmo valor de potencial $b$, herdado dos vértices extremos.

### 4.2. Por que isso Impede o Fechamento de T10
Os teoremas clássicos de evasão de sela via Stable Manifold Theorem (Lee et al. 2016, Panageas & Piliouras 2017) exigem que todos os pontos críticos instáveis sejam **strict saddles** (i.e., $\\lambda_{\\min}(\\nabla^2 \\Phi) < 0$).
Uma variedade flat de dimensão 1 com Hessiana identicamente nula ($\nabla^2_{\\mathcal{F}} \\Phi = 0$) **não é uma sela estrita**.
Embora o fluxo gradiente tangencial seja nulo sobre a variedade degenerada, a análise das forças transversais e o acoplamento global com o potencial Hinge $\\Phi_{\\text{quad}}$ permanecem em aberto.

Por conseguinte, a cadeia de classificação completa das faces do hipercubo $\\mathcal{X} = [-1, 1]^N$ é formalizada da seguinte maneira:
* **$d \\ge 2$:** Strict saddles sob $H_{\\text{leaf}}$ ($\lambda_{\\min} < 0$);
* **$d = 0$:** Vértices discretos sem mínimos locais positivos sob $H_{\\text{leaf}}$;
* **$d = 1$:** Arestas afins sem pontos críticos interiores ($a \\ne 0$) ou segmentos críticos degenerados flat ($a = 0$).

Essa formalização confirma categoricamente o status de Teorema 10:
$$\\boxed{\\text{Teorema 10: } \\textbf{🔴 Não Fechado}}$$

---

## 5. Alvo 4: Lema 10.1 — Formulação Segura da Cota de Primeiro Momento

### 5.1. O Diagnóstico de Vossa Senhoria
Na versão anterior, a cota de primeiro momento para o número $X$ de pares de cláusulas com interseção $\\ge 2$ variáveis em $3\\text{-SAT}$ subcrítico com $M = \\alpha N$ cláusulas:
$$\\mathbb{E}[X] \\le 9 \\alpha^2 < \\frac{1}{4} \\quad (\\text{para } \\alpha < 1/6)$$
havia sido seguida da afirmação de que *"quase todas as componentes são hiperárvores lineares"*.

Vossa Senhoria advertiu que:
* $\\mathbb{E}[X] \\le 9 \\alpha^2 = \\mathcal{O}(1)$ demonstra que o número esperado de pares problemáticos é constante (não escala com $N$).
* Pela desigualdade de Markov, $\\mathbb{P}(X \\ge 1) \\le 9\\alpha^2$, donde $\\mathbb{P}(X = 0) \\ge 1 - 9\\alpha^2 > 0$. Isso não tende assintoticamente a 1 quando $N \\to \\infty$ ($\not\\to 1$).
* Afirmar que "quase todas as componentes são lineares" exigiria formalizar uma relação explícita entre $X$ e a fração de componentes conexas afetadas, o que não foi deduzido a partir da cota isolada.

### 5.2. Ação Corretiva Executada
Adotamos verbatim a redação matemática recomendada por Vossa Senhoria no manuscrito arXiv e na monografia:
> *"A cota de primeiro momento mostra que o número esperado de pares de cláusulas com interseção de pelo menos duas variáveis é $\\mathcal{O}(1)$ (limitado por $9\\alpha^2$). A decomposição em um núcleo de componentes lineares acíclicas mais um conjunto estocasticamente limitado $\\mathcal{O}_{\\mathbb{P}}(1)$ de defeitos estruturais permanece sujeita a uma análise estrutural adicional."*

Status formal:
$$\\boxed{\\text{Lema 10.1: } \\textbf{🟡 Parcial}}$$

---

## 6. Saneamento Editorial: Abstract e Data do Manuscrito arXiv

Conforme apontado no Parecer 16:
1. **Atualização da Data:** O arquivo `CLG_FOUNDATIONS_ARXIV.tex` teve sua data atualizada para `\\date{September 16, 2026}`.
2. **Harmonização do Resumo Executivo (Abstract):**
   O abstract anterior afirmava genericamente:
   *"We prove rigorous dynamical separation in monotone Horn families..."* e *"We prove rigorous separation in leaf-decoupled acyclic hypertrees and subcritical random 3-SAT..."*
   Isso entrava em contradição direta com os status do corpo do artigo (T9 Falsificado e T10 Não Fechado).
   O Abstract foi reescrito no LaTeX, retificando os itens de resultados:
   * **Item (8):** Descreve a cota de volume LP estritamente como cota inferior em dimensão finita $\\mathbb{E}[\\mu(Z)] \\ge (5/6)^{\\alpha N} > 0$, com convergência assintótica em aberto;
   * **Item (9):** Descreve a investigação de famílias Horn lineares e a identificação do regime de colapso de politopos e do caráter competitivo do Jacobiano;
   * **Item (10):** Descreve a evasão de selas estritas em faces $d \\ge 2$ sob a hipótese estrutural $H_{\\text{leaf}}$ e registra que a separação global permanece uma conjectura aberta.

---

## 7. Adoção Integral da Matriz de Rigor da Seção 16 do Parecer

Substituímos todas as matrizes anteriores pela tabela de status prescrita por Vossa Senhoria na Seção 16 do Parecer:

| Resultado | Status de Auditoria (Parecer 16) | Qualificação Técnica Formal e Limites Analíticos |
| :--- | :---: | :--- |
| **T1** (Caixa Central $\\mathcal{U}_N$) | 🟢 **Fechado** | Universal determinístico; folga interior 0.5 em toda a caixa. |
| **T2** (Medida Nula de Críticos) | 🟢 **Fechado sob hipóteses** | Fubini para $\\Phi_{\\text{mult}}$; analiticidade real para $\\Phi_{\\text{soft}}$. |
| **T3** (Harmonicidade e Selas) | 🟢 **Fechado sob hipóteses** | Princípio do Mínimo Forte e Lema de Seleção de Curvas de Milnor. |
| **T4A′** (Mínimos em Faces) | 🟢 **Fechado** | Mínimos locais em faces herdam energia de vértices. |
| **4B** (Confinamento de LaSalle) | 🟢 **Fechado, sujeito à formulação final** | Lyapunov estrito no hipercubo compacto; atratores isolados confinados a $\\{-1, 1\\}^N$. |
| **T5** (Hessiana Softplus $V^T W V$) | 🟢 **Fechado sob condições declaradas** | Fatoração exata; $\\text{rank}(V)=N \\implies$ estrita convexidade. |
| **T6** (Lipschitz e Underflow) | 🟢 **Fechado sob convenções IEEE** | $L_\\beta = \\Theta(\\beta)$ bilateral; limites de underflow e flush-to-zero. |
| **T7B** (Contração Centrípeta e LaSalle) | 🟡 **Quase fechado** | Equivalência $\\mathcal{E}_{\\text{proj}} \\equiv Z$; identidade de sinais no bordo $\\langle -\\nabla \\Phi, x \\rangle < 0$ vs $\\langle \\nu, x \\rangle \\ge 0$. |
| **T8** (Cota Inferior do Volume LP) | 🟡 **Fechado apenas como cota inferior finita** | $\\mathbb{E}[\\mu(Z)] \\ge (5/6)^{\\alpha N} > 0$ demonstrado para todo $N$ finito; limite assintótico zero retirado. |
| **T9** (Horn Linear Monótono) | 🔴 **Falsificado / abandonado** | Lema 9.1 falsificado sob fato unitário positivo ($Z=\\{(1,\\dots,1)\\}$); em aberto para DAGs gerais. |
| **Lema 10.1** (Hiperárvores Subcríticas) | 🟡 **Parcial** | $2\\text{-core} = \\emptyset$ provado a.a.s.; cota $9\\alpha^2 = \\mathcal{O}(1)$ limita defeitos, mas linearidade universal não é a.a.s. |
| **Lema 10.2** (Strict Saddle Subcrítico) | 🟡 **Fechado condicionalmente a $H_{\\text{leaf}}$** | Traço nulo e $H_{\\ell p} = \\frac{\\sigma_\\ell \\sigma_p}{8}(1 - \\sigma_k x^*_k) \\ne 0$ garantem $\\lambda_{\\min} < 0$ em faces $d \\ge 2$. |
| **Teorema 10** (Separação em 3-SAT Subcrítico) | 🔴 **Não fechado** | Evasão provada para strict saddles ($d \\ge 2$); arestas $d=1$ flat e separação de Hinge em aberto. |
| **Proposição 7A** (Famílias Negativas e Dinâmica) | 🟡 **Precisa de nova auditoria** | Jacobiano é estritamente competitivo ($J_{ij} \\le 0$), não cooperativo; Hirsch inaplicável na forma original. |
| **Conjectura Central** (Regime de Clustering) | 🔵 **Conjectura delimitada** | Formalmente restrita a $\\alpha \\in (\\alpha_d, \\alpha_s)$ e ensemble plantado. |
| **Firewall 3-XOR** | 🟢 **Resultado epistemológico** | Separação categórica entre dinâmica contínua e complexidade de Turing (sem termo "absoluto"). |

---

## 8. Conclusão e Próximos Passos Metodológicos

Ao concluir a auditoria cirúrgica sobre os quatro alvos do Parecer 16:
1. **O Teorema 8** tornou-se inatacável ao restringir-se à cota finita demonstrada;
2. **A Proposição 7A** foi formalmente reclassificada para nova auditoria perante a constatação do caráter competitivo ($J_{ij} \\le 0$);
3. **O Teorema 10** teve sua taxonomia geométrica completada com a elucidação das arestas $d=1$ (não-críticas ou variedades flat), justificando solidamente seu status vermelho;
4. **O Lema 10.1** adotou a formulação analiticamente exata de primeira-momento;
5. **O Manuscrito LaTeX** e o pacote de submissão foram 100% harmonizados editorialmente.

Reiteramos nosso profundo respeito pelo processo de avaliação, que elevou o programa CLG-R a um patamar de maturidade e rigor científico exemplar.

Respeitosamente,  
**Thiago Carvalho**  
*Pesquisador Principal — Framework CLG-R*  
16 de Setembro de 2026
"""

def clean_math_for_docx(txt):
    txt = txt.replace('$$', '')
    txt = txt.replace('\\\\', '\\')
    replacements = [
        (r'\\mathbb\{E\}_F', '𝔼_F'),
        (r'\\mathbb\{E\}', '𝔼'),
        (r'\\mathbb\{P\}_c', 'ℙ_c'),
        (r'\\mathbb\{P\}_\{[^}]+\}', 'ℙ'),
        (r'\\mathbb\{P\}', 'ℙ'),
        (r'\\mathbf\{1\}_\{[^}]+\}', '1_{cond}'),
        (r'\\mathbf\{([^}]+)\}', r'\1'),
        (r'\\mathbb\{R\}\^N', 'ℝ^N'),
        (r'\\mathbb\{R\}\^K', 'ℝ^K'),
        (r'\\mathbb\{R\}', 'ℝ'),
        (r'\\mathbb\{Z\}_\{[^}]+\}', 'ℤ_{≥0}'),
        (r'\\mathbb\{Z\}', 'ℤ'),
        (r'\\int_\{[^}]+\}', '∫'),
        (r'\\int', '∫'),
        (r'\\ge\b|\\geq\b', '≥'),
        (r'\\le\b|\\leq\b', '≤'),
        (r'\\ne\b|\\neq\b', '≠'),
        (r'\\approx', '≈'),
        (r'\\sim', '~'),
        (r'\\to', '→'),
        (r'\\implies', '⟹'),
        (r'\\iff', '⟺'),
        (r'\\alpha_d', 'α_d'),
        (r'\\alpha_c', 'α_c'),
        (r'\\alpha_s', 'α_s'),
        (r'\\alpha_\{?\\text\{core\}\}?', 'α_core'),
        (r'\\alpha', 'α'),
        (r'\\beta', 'β'),
        (r'\\gamma', 'γ'),
        (r'\\eta', 'η'),
        (r'\\lambda_\{?\\text\{min\}\}?', 'λ_min'),
        (r'\\lambda_\{?\\text\{max\}\}?', 'λ_max'),
        (r'\\lambda', 'λ'),
        (r'\\rho_\{?\\text\{mult\}\}?', 'ρ_mult'),
        (r'\\rho_\{?\\text\{quad\}\}?', 'ρ_quad'),
        (r'\\rho', 'ρ'),
        (r'\\sigma_j\^\{\(c\)\}?', 'σ_j^(c)'),
        (r'\\sigma\^\{\(c\)\}?', 'σ^(c)'),
        (r'\\sigma', 'σ'),
        (r'\\nu_i', 'ν_i'),
        (r'\\nu', 'ν'),
        (r'\\Delta', 'Δ'),
        (r'\\nabla\^2_\{?\\mathcal\{F\}\}?', '∇²_F'),
        (r'\\nabla\^2', '∇²'),
        (r'\\nabla_\{?\\mathcal\{F\}\}?', '∇_F'),
        (r'\\nabla', '∇'),
        (r'\\Phi_\{?\\text\{mult\}\}?', 'Φ_mult'),
        (r'\\Phi_\{?\\text\{quad\}\}?', 'Φ_quad'),
        (r'\\Phi_\{?\\text\{soft\}\}?', 'Φ_soft'),
        (r'\\Phi', 'Φ'),
        (r'\\mathcal\{M\}_\{?\\text\{spur\}\}?', 'M_spur'),
        (r'\\mathcal\{B\}_\{?\\text\{spur\}\}?', 'B_spur'),
        (r'\\mathcal\{B\}\(Z\)', 'B(Z)'),
        (r'\\mathcal\{E\}_\{?\\text\{proj\}\}?', 'E_proj'),
        (r'\\mathcal\{U\}_N', 'U_N'),
        (r'\\mathcal\{X\}', 'X'),
        (r'\\mathcal\{F\}', 'F'),
        (r'\\mathcal\{H\}_\{?\\mathcal\{F\}\}?', 'H_F'),
        (r'\\mathcal\{H\}', 'H'),
        (r'\\mathcal\{R\}_K', 'R_K'),
        (r'\\mathcal\{R\}_N', 'R_N'),
        (r'\\mathcal\{C\}', 'C'),
        (r'\\mathcal\{V\}', 'V'),
        (r'\\Pi_\{T_\\mathcal\{X\}\(x\)\}', 'Π_{TX}'),
        (r'\\Pi_Z', 'Π_Z'),
        (r'\\Pi_K', 'Π_K'),
        (r'\\Pi', 'Π'),
        (r'\\partial\^2 P_c / \\partial x_\\ell \\partial x_p', '∂²P_c / ∂x_ℓ ∂x_p'),
        (r'\\partial\^2 P_c / \\partial x_i \\partial x_j', '∂²P_c / ∂x_i ∂x_j'),
        (r'\\partial\^2', '∂²'),
        (r'\\partial', '∂'),
        (r'\\lfloor', '⌊'),
        (r'\\rfloor', '⌋'),
        (r'\\left\(', '('), (r'\\right\)', ')'),
        (r'\\left\[', '['), (r'\\right\]', ']'),
        (r'\\left\\\{', '{'), (r'\\right\\\}', '}'),
        (r'\\langle', '⟨'), (r'\\rangle', '⟩'),
        (r'\\frac\{dx\}\{2\^N\}', 'dx/2^N'),
        (r'\\frac\{1\}\{8\}', '1/8'),
        (r'\\frac\{1\}\{4\}', '1/4'),
        (r'\\frac\{5\}\{6\}', '5/6'),
        (r'\\frac\{1\}\{3\}', '1/3'),
        (r'\\frac\{1\}\{6\}', '1/6'),
        (r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1/\2)'),
        (r'\\text\{Uniform\}', 'Uniform'),
        (r'\\text\{Unif\}', 'Unif'),
        (r'\\text\{act\}', 'act'),
        (r'\\text\{relint\}', 'relint'),
        (r'\\text\{sign\}', 'sign'),
        (r'\\text\{disc\}', 'disc'),
        (r'\\text\{mult\}', 'mult'),
        (r'\\text\{quad\}', 'quad'),
        (r'\\text\{soft\}', 'soft'),
        (r'\\text\{spur\}', 'spur'),
        (r'\\text\{folha\}', 'folha'),
        (r'\\text\{norm\}', 'norm'),
        (r'\\text\{int\}', 'int'),
        (r'\\text\{rank\}', 'rank'),
        (r'\\text\{diag\}', 'diag'),
        (r'\\text\{Tr\}', 'Tr'),
        (r'\\text\{Var\}', 'Var'),
        (r'\\text\{core\}', 'core'),
        (r'\\text\{min\}', 'min'),
        (r'\\text\{max\}', 'max'),
        (r'\\binom\{([^}]+)\}\{([^}]+)\}', r'C(\1, \2)'),
        (r'\\sqrt\{([^}]+)\}', r'√(\1)'),
        (r'\\sum_\{c \\in \\text\{act\}\}', '∑_{c ∈ act}'),
        (r'\\sum', '∑'),
        (r'\\prod', '∏'),
        (r'\\in', '∈'),
        (r'\\notin', '∉'),
        (r'\\subset', '⊂'),
        (r'\\subseteq', '⊆'),
        (r'\\supset', '⊃'),
        (r'\\forall', '∀'),
        (r'\\exists', '∃'),
        (r'\\dots', '...'),
        (r'\\blacksquare', '■'),
        (r'\\cdot', '·'),
        (r'\\times', '×'),
        (r'\\neg', '¬'),
        (r'\\lor', '∨'),
        (r'\\land', '∧'),
        (r'\\models', '⊨'),
        (r'\\Theta', 'Θ'),
        (r'\\Omega', 'Ω'),
        (r'\\mathcal\{O\}', 'O'),
        (r'\\,', ' '),
        (r'\\;', ' '),
        (r'\$([^$]+)\$', r'\1'),
    ]
    res = txt
    for p, r in replacements:
        res = re.sub(p, r, res)
    res = re.sub(r'\\([a-zA-Z]+)', r'\1', res)
    res = res.replace('\\', '')
    res = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', res)
    return res.strip()

def add_formatted_runs(p, text, font_name="Calibri", font_size=Pt(11), default_bold=False, default_italic=False, default_color=None):
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**') and len(part) >= 4:
            run_text = part[2:-2]
            r = p.add_run(run_text)
            r.bold = True
        else:
            r = p.add_run(part)
            r.bold = default_bold
        r.font.name = font_name
        r.font.size = font_size
        r.italic = default_italic
        if default_color:
            r.font.color.rgb = default_color

def build_deliverables():
    os.makedirs(PUB_DIR, exist_ok=True)
    os.makedirs(ROOT_DIR, exist_ok=True)

    # 1. Salvar PARECER_16_AUDITORIA_CRITICA_PROFESSOR.md
    parecer_txt_path = os.path.join(PUB_DIR, "Analise16_TextoCompleto.txt")
    if os.path.exists(parecer_txt_path):
        with open(parecer_txt_path, "r", encoding="utf-8") as f:
            raw_parecer = f.read()
        parecer_md = f"""# Parecer nº 16 do Professor: Auditoria Crítica do Pacote V4.0.1
**Data:** 16 de Setembro de 2026  
**Documento Original:** `AnaliseReportadaPeloProfessor16.docx`  
**Escopo:** Auditoria Linha por Linha do Respostas.zip (LaTeX, Monografia e Mensagens)

---

{raw_parecer}
"""
        with open(os.path.join(PUB_DIR, "PARECER_16_AUDITORIA_CRITICA_PROFESSOR.md"), "w", encoding="utf-8") as f:
            f.write(parecer_md)
        with open(os.path.join(ROOT_DIR, "PARECER_16_AUDITORIA_CRITICA_PROFESSOR.md"), "w", encoding="utf-8") as f:
            f.write(parecer_md)
        print("Salvo: PARECER_16_AUDITORIA_CRITICA_PROFESSOR.md")

    # 2. Salvar RespostaAoProfessor_Analise16.md
    with open(os.path.join(PUB_DIR, "RespostaAoProfessor_Analise16.md"), "w", encoding="utf-8") as f:
        f.write(RESPOSTA_16_MD)
    with open(os.path.join(ROOT_DIR, "RespostaAoProfessor_Analise16.md"), "w", encoding="utf-8") as f:
        f.write(RESPOSTA_16_MD)
    print("Salvo: RespostaAoProfessor_Analise16.md")

    # 3. Gerar RespostaAoProfessor_Analise16.docx
    doc_resp = docx.Document()
    for s in doc_resp.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    p_title = doc_resp.add_paragraph()
    run_title = p_title.add_run("Resposta Técnica ao Parecer nº 16 do Professor:\nRelatório de Auditoria Cirúrgica nos Quatro Alvos da Versão 4.0.1")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(18)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x1F, 0x4E, 0x78)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_sub = doc_resp.add_paragraph()
    run_sub = p_sub.add_run("Acolhimento Integral da Auditoria Crítica, Classificação de Faces d=1 e Matriz de Rigor 16\nAutor: Thiago Carvalho e Equipe CLG-R | Data: 16 de Setembro de 2026")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(10.5)
    run_sub.font.italic = True
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc_resp.add_paragraph()

    lines = RESPOSTA_16_MD.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("# Resposta Técnica") or line.startswith("## Relatório"):
            i += 1
            continue
        elif line.startswith("## "):
            h = doc_resp.add_paragraph()
            add_formatted_runs(h, clean_math_for_docx(line.replace("## ", "").strip()), font_size=Pt(14), default_bold=True, default_color=RGBColor(0x1F, 0x4E, 0x78))
            i += 1
        elif line.startswith("### "):
            h = doc_resp.add_paragraph()
            add_formatted_runs(h, clean_math_for_docx(line.replace("### ", "").strip()), font_size=Pt(12), default_bold=True, default_color=RGBColor(0x2F, 0x55, 0x97))
            i += 1
        elif line.startswith("> "):
            p = doc_resp.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.4)
            add_formatted_runs(p, clean_math_for_docx(line.replace("> ", "").strip()), font_size=Pt(10.5), default_italic=True)
            i += 1
        elif line.strip().startswith("$$") and line.strip().endswith("$$") and len(line.strip()) > 4:
            p = doc_resp.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            clean_eq = clean_math_for_docx(line.strip())
            r = p.add_run(clean_eq)
            r.font.name = "Cambria Math"
            r.font.size = Pt(11)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
            i += 1
        elif line.strip().startswith("* ") or line.strip().startswith("- "):
            p = doc_resp.add_paragraph(style='List Bullet')
            clean_txt = clean_math_for_docx(line.strip()[2:].strip())
            add_formatted_runs(p, clean_txt, font_size=Pt(10.5))
            i += 1
        elif any(line.strip().startswith(f"{num}. ") for num in range(1, 10)):
            p = doc_resp.add_paragraph(style='List Number')
            num_prefix_len = line.strip().find(". ") + 2
            clean_txt = clean_math_for_docx(line.strip()[num_prefix_len:].strip())
            add_formatted_runs(p, clean_txt, font_size=Pt(10.5))
            i += 1
        elif line.strip() == "---":
            p = doc_resp.add_paragraph()
            r = p.add_run("―" * 40)
            r.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            i += 1
        elif line.strip().startswith("|") and line.strip().endswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            parsed_rows = []
            for tl in table_lines:
                cells = [c.strip() for c in tl.split("|")[1:-1]]
                if all(re.match(r'^:?-+:?$', c) for c in cells):
                    continue
                parsed_rows.append(cells)
            if parsed_rows:
                num_cols = max(len(r) for r in parsed_rows)
                tbl = doc_resp.add_table(rows=len(parsed_rows), cols=num_cols)
                tbl.style = 'Table Grid'
                tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
                for r_idx, row_data in enumerate(parsed_rows):
                    for c_idx, cell_data in enumerate(row_data):
                        cell = tbl.cell(r_idx, c_idx)
                        p_cell = cell.paragraphs[0]
                        p_cell.paragraph_format.space_before = Pt(2)
                        p_cell.paragraph_format.space_after = Pt(2)
                        is_hdr = (r_idx == 0)
                        clean_cell = clean_math_for_docx(cell_data)
                        add_formatted_runs(p_cell, clean_cell, font_size=Pt(9.0 if not is_hdr else 9.5), default_bold=is_hdr)
                doc_resp.add_paragraph()
        elif line.strip():
            p = doc_resp.add_paragraph()
            clean_txt = clean_math_for_docx(line.strip())
            add_formatted_runs(p, clean_txt, font_size=Pt(10.5))
            i += 1
        else:
            i += 1

    doc_resp.save(os.path.join(PUB_DIR, "RespostaAoProfessor_Analise16.docx"))
    doc_resp.save(os.path.join(ROOT_DIR, "RespostaAoProfessor_Analise16.docx"))
    print("Salvo: RespostaAoProfessor_Analise16.docx")

    # 4. Gerar MensagemParaOAvaliador16
    doc_msg = docx.Document()
    for s in doc_msg.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    p_mtitle = doc_msg.add_paragraph()
    rm_title = p_mtitle.add_run("Atualização Formal — Parecer nº 16 e Auditoria Cirúrgica nos Quatro Alvos")
    rm_title.font.name = "Calibri"
    rm_title.font.size = Pt(16)
    rm_title.font.bold = True
    rm_title.font.color.rgb = RGBColor(0x1F, 0x4E, 0x78)
    p_mtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc_msg.add_paragraph()

    for par in MENSAGEM_16_TEXTO.split("\n\n"):
        p = doc_msg.add_paragraph()
        clean_par = clean_math_for_docx(par.strip())
        add_formatted_runs(p, clean_par, font_size=Pt(11))

    doc_msg.save(os.path.join(PUB_DIR, "MensagemParaOAvaliador16.docx"))
    doc_msg.save(os.path.join(ROOT_DIR, "MensagemParaOAvaliador16.docx"))
    print("Salvo: MensagemParaOAvaliador16.docx")

    with open(os.path.join(PUB_DIR, "MensagemParaOAvaliador16.txt"), "w", encoding="utf-8") as f:
        f.write(MENSAGEM_16_TEXTO)
    with open(os.path.join(ROOT_DIR, "MensagemParaOAvaliador16.txt"), "w", encoding="utf-8") as f:
        f.write(MENSAGEM_16_TEXTO)
    print("Salvo: MensagemParaOAvaliador16.txt")

    # 5. Atualizar zip do arxiv
    zip_arxiv = os.path.join(PUB_DIR, "arxiv_package.zip")
    with zipfile.ZipFile(zip_arxiv, 'w', zipfile.ZIP_DEFLATED) as z:
        for fname in [
            "CLG_FOUNDATIONS_ARXIV.tex",
            "clg_references.bib",
            "fig_clg_teorema1_caixa_fracionaria.png",
            "fig_clg_teorema3_4_harmonic_saddles_vertices.png",
            "fig_clg_teorema5_6_softplus_convexity_bifurcation.png"
        ]:
            fpath = os.path.join(PUB_DIR, fname)
            if os.path.exists(fpath):
                z.write(fpath, arcname=fname)
                print(f"[ZIP arXiv] Adicionado: {fname}")
    print("Salvo: arxiv_package.zip atualizado!")

    # 6. Gerar Enviar_17.zip completo na raiz e em Publicacoes/
    enviar_zip_pub = os.path.join(PUB_DIR, "Enviar_17.zip")
    enviar_zip_root = os.path.join(ROOT_DIR, "Enviar_17.zip")
    enviar_files = [
        ("MensagemParaOAvaliador16.docx", os.path.join(PUB_DIR, "MensagemParaOAvaliador16.docx")),
        ("MensagemParaOAvaliador16.txt", os.path.join(PUB_DIR, "MensagemParaOAvaliador16.txt")),
        ("RespostaAoProfessor_Analise16.docx", os.path.join(PUB_DIR, "RespostaAoProfessor_Analise16.docx")),
        ("RespostaAoProfessor_Analise16.md", os.path.join(PUB_DIR, "RespostaAoProfessor_Analise16.md")),
        ("PARECER_16_AUDITORIA_CRITICA_PROFESSOR.md", os.path.join(PUB_DIR, "PARECER_16_AUDITORIA_CRITICA_PROFESSOR.md")),
        ("ESTUDO_ANALITICO_DO_CONJUNTO_CRITICO.md", os.path.join(PUB_DIR, "ESTUDO_ANALITICO_DO_CONJUNTO_CRITICO.md")),
        ("CLG_FOUNDATIONS_ARXIV.tex", os.path.join(PUB_DIR, "CLG_FOUNDATIONS_ARXIV.tex")),
        ("arxiv_package.zip", os.path.join(PUB_DIR, "arxiv_package.zip"))
    ]
    for target_zip in [enviar_zip_pub, enviar_zip_root]:
        with zipfile.ZipFile(target_zip, 'w', zipfile.ZIP_DEFLATED) as z:
            for arcname, filepath in enviar_files:
                if os.path.exists(filepath):
                    z.write(filepath, arcname=arcname)
                    print(f"[ZIP Enviar_17] Adicionado: {arcname}")
                else:
                    print(f"[ZIP Enviar_17] AVISO: Arquivo nao encontrado: {filepath}")
    print("Salvo: Enviar_17.zip gerado com sucesso na raiz e em Publicacoes/!")

if __name__ == "__main__":
    build_deliverables()
