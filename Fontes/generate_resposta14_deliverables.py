"""
Script gerador dos entregáveis formais em resposta ao Parecer nº 14 do Professor.
Gera:
1. Publicacoes/RespostaAoProfessor_Analise14.md (e copia para a raiz C:\\MathDoCarvalho)
2. Publicacoes/RespostaAoProfessor_Analise14.docx (e copia para a raiz C:\\MathDoCarvalho)
3. Publicacoes/MensagemParaOAvaliador14.docx (e copia para a raiz C:\\MathDoCarvalho)
4. Publicacoes/MensagemParaOAvaliador14.txt (e copia para a raiz C:\\MathDoCarvalho)
5. Publicacoes/PARECER_14_AUDITORIA_CRITICA_PROFESSOR.md (e copia para a raiz)
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

MENSAGEM_14_TEXTO = """Prezado Professor,

Agradecemos profundamente pela auditoria minuciosa, linha por linha, realizada sobre a Resposta 14. Registramos com grande satisfação o seu reconhecimento de que a postura científica adotada representa exatamente o procedimento científico exigido: a falsificação real do Lema 9.1, a correção do erro de Stirling e a separação categórica entre o que está demonstrado e o que permanece em aberto.

Acolhemos integralmente todas as correções matemáticas e conceituais formuladas em sua última auditoria:

1. Lema 10.1 (Linearidade a.a.s. e Cota de Primeiro Momento):
   Reconhecemos a invalidade da inferência anterior. A cota E[X] <= 9 alpha^2 é uma constante O(1) independente de N (e.g. 0.1296 em alpha = 0.12). Pela desigualdade de Markov, isso garante P(X >= 1) <= 9 alpha^2, mas NÃO permite concluir P(X = 0) -> 1. Portanto, a linearidade estrita global através de todo o hipergrafo não é uma propriedade a.a.s. decorrente dessa cota. O status do Lema 10.1 é fixado como 🟡 PARCIALMENTE FECHADO.

2. Lema 10.2 (Dependência Lógica da Hipótese Estrutural H_leaf):
   A demonstração de que lambda_min < 0 a partir de Tr(H) = 0 e H_lp != 0 depende da existência de uma variável folha de grau global 1 na cláusula violada. Como essa estrutura de folha não foi demonstrada a.a.s. para todas as componentes, formalizamos a dependência lógica de forma explícita: o Lema 10.2 é classificado como 🟡 FECHADO CONDICIONALMENTE À HIPÓTESE ESTRUTURAL H_leaf (e não universalmente a.a.s.).

3. Correção do Fator em H_lp:
   Retificamos a derivada cruzada para d^2 P_c / dx_l dx_p = (sigma_l sigma_p / 8) * (1 - sigma_k x_k), sanando a inconsistência do fator 2. Como |x_k| < 1 implica 1 - sigma_k x_k > 0, o resultado essencial H_lp != 0 permanece perfeitamente válido.

4. Teorema 7B (Saneamento do Enunciado e Identidade de Sinais):
   Corrigimos a formulação para explicitar que para x ∉ Z vale < -grad Phi_quad(x), x > < 0 (pois act(x) != ∅), enquanto para x ∈ Z temos grad Phi_quad(x) = 0 e < -grad Phi_quad(x), x > = 0. Como < nu, x > >= 0 para todo nu ∈ N_X(x), nenhum equilíbrio projetado pode residir fora de Z, garantindo E_proj = Z. O status do Teorema 7B é fixado como 🟡 QUASE FECHADO.

5. Firewall Epistemológico (3-XOR-SAT):
   Expurgamos definitivamente a palavra 'absoluta', adotando a sua formulação exata: 'Firewall epistemológico contra inferências de dificuldade dinâmica para P != NP'.

6. Adoção Integral da Matriz de Rigor da Seção 9:
   Adotamos sem alterações a tabela prescrita por Vossa Senhoria:
   - T1-T6, T4A'/4B: 🟢 Fechado
   - T7B: 🟡 Quase fechado
   - T8: 🟢 Fechado como cota finita
   - T9: 🔴 Falsificado / abandonado
   - Lema 10.1: 🟡 Parcialmente fechado
   - Lema 10.2: 🟡 Fechado condicionalmente à estrutura de folha
   - Teorema 10: 🔴 Não fechado
   - Conjectura Central: 🔵 Conjectura delimitada
   - 3-XOR-SAT Firewall: 🟢 Resultado epistemológico (sem 'absoluto')

7. Congelamento da Versão V4.0.1:
   Conforme sua orientação, congelamos a V4.0.1 sem introduzir nenhum novo teorema, focando na integridade analítica e na delimitação transparente das fronteiras do programa CLG-R.

Seguem anexos o documento de resposta técnica detalhado e o manuscrito LaTeX arXiv devidamente atualizado.

Respeitosamente,
Thiago Carvalho
Pesquisador Principal — Framework CLG-R"""

RESPOSTA_14_MD = """# Resposta Técnica ao Parecer nº 14 do Professor:
## Relatório de Auditoria Linha por Linha, Saneamento Probabilístico e Matriz de Rigor da Versão 4.0.1

**Destinatário:** Ilustre Professor e Comitê de Avaliação Externa  
**Autor:** Thiago Carvalho e Equipe de Pesquisa do Framework CLG-R  
**Data:** 16 de Setembro de 2026  
**Repositório GitHub:** [https://github.com/thiagocarvalhodba/p-vs-np-carvalho](https://github.com/thiagocarvalhodba/p-vs-np-carvalho)  
**Assunto:** Acolhimento integral da auditoria crítica linha por linha; Saneamento do Lema 10.1 (cota de primeiro momento O(1)); Condicionalidade do Lema 10.2 à hipótese H_leaf; Correção do fator de H_lp; Correção de sinais no Teorema 7B; Falsificação do Lema 9.1; Saneamento epistemológico do Firewall 3-XOR-SAT; e Adoção estrita da Matriz de Rigor da Seção 9.

---

## 1. Posicionamento e Acolhimento da Filosofia Científica do Parecer 14

Expressamos nossa mais sincera gratidão pelo rigor demonstrado na auditoria linha por linha do Parecer nº 14. A sua avaliação direta e precisa capturou exatamente as lacunas remanescentes:
> *"A mudança de postura é substancialmente melhor que a da versão anterior: vocês realmente falsificaram uma afirmação própria, corrigiram o erro de Stirling e separaram o que está demonstrado do que continua aberto. Isso é exatamente o procedimento científico que eu havia solicitado. Mas, fazendo agora a auditoria linha por linha, eu ainda não colocaria a matriz de rigor como 'inatacável'."*

Acolhemos integralmente todas as correções apontadas:
1. Reconhecemos que $\\mathbb{E}[X] \\le 9\\alpha^2 = \\mathcal{O}(1)$ não implica que o hipergrafo seja linear a.a.s.;
2. Reconhecemos que o Lema 10.2 depende criticamente da hipótese estrutural de existência de folhas de grau 1 ($H_{\\text{leaf}}$);
3. Corrigimos a expressão de $H_{\\ell p}$ para $\\frac{\\sigma_\\ell \\sigma_p}{8}(1 - \\sigma_k x_k)$;
4. Sanamos o enunciado de sinais do Teorema 7B ($x \\notin Z \\implies \\langle -\\nabla \\Phi, x \\rangle < 0$, enquanto em $Z$, $\\nabla \\Phi = \\mathbf{0}$);
5. Expurgamos o termo "blindagem absoluta", adotando "Firewall epistemológico contra inferências de dificuldade dinâmica para $P \\ne NP$";
6. Adotamos a Matriz de Rigor exata prescrita na Seção 9 do seu parecer;
7. Congelamos a Versão 4.0.1 sem adicionar novos teoremas.

---

## 2. Saneamento do Lema 10.1: Primeira-Momento e a Falácia de Linearidade a.a.s.

Na versão preliminar, calculou-se a cota de primeiro momento para o número $X$ de pares de cláusulas que compartilham $\\ge 2$ variáveis em 3-SAT com $M = \\alpha N$ cláusulas:
$$\\mathbb{E}[X] \\le \\binom{M}{2} \\frac{18(N-3)}{N(N-1)(N-2)} \\le 9 \\alpha^2 < \\frac{1}{4}$$
E inferiu-se precipitadamente: *"Portanto, a quase totalidade das componentes subcríticas consiste em hiperárvores lineares estritas."*

### Diagnóstico Analítico:
Vossa Senhoria identificou com perfeita precisão a falha lógica:
* $\\mathbb{E}[X] \\le 9\\alpha^2$ é uma **cota constante**, totalmente independente de $N$.
* Para $\\alpha = 0.12$, temos $9\\alpha^2 = 0.1296$.
* Pela desigualdade de Markov:
  $$\\mathbb{P}(X \\ge 1) \\le \\frac{\\mathbb{E}[X]}{1} \\le 0.1296 \\implies \\mathbb{P}(X = 0) \\ge 1 - 0.1296 = 0.8704$$
* Uma probabilidade $\\ge 0.8704$ **não tende a 1 quando $N \\to \\infty$** ($\not\\to 1$).
* Em 3-hipergrafos esparsos com $M = \\alpha N$, o número de ciclos curtos e sobreposições de 2 variáveis converge tipicamente para uma distribuição de Poisson com média de ordem constante $\\mathcal{O}(1)$. Portanto, **a linearidade estrita global não é uma propriedade a.a.s. obtida por primeira momento**.

### Consequência e Status Formal:
O Lema 10.1 permanece formalmente classificado como:
$$\\boxed{\\text{Lema 10.1: } \\textbf{🟡 Parcialmente Fechado}}$$
* **O que está demonstrado:** $2\\text{-core} = \\emptyset$ ocorre a.a.s. para $\\alpha < 1/6$ (pois $\\alpha_c \\ll \\alpha_{\\text{core}} \\approx 0.8183$), garantindo aciclicidade topológica grosseira; e o número esperado de sobreposições de 2 variáveis é estritamente cotado por $9\\alpha^2 = \\mathcal{O}(1)$.
* **O que não está demonstrado:** A linearidade estrita global ($|c \\cap c'| \\le 1$ para todo par) a.a.s. em todo o hipergrafo.
* **Direção Futura Acolhida:** A proposta de Vossa Senhoria de decompor o grafo em $G = G_{\\text{tree}} + G_{\\text{defect}}$ com $O_{\\mathbb{P}}(1)$ defeitos localmente tratáveis é o caminho científico correto para investigações futuras.

---

## 3. Lema 10.2: Condicionalidade à Hipótese $H_{\\text{leaf}}$ e Correção de Fator

### 3.1. Dependência Lógica Estrutural
O Lema 10.2 fundamenta-se na propriedade de que para o potencial multilinear $\\Phi_{\\text{mult}}(x) = \\sum_c P_c(x)$, cada entrada diagonal da Hessiana é identicamente nula ($\\frac{\\partial^2 \\Phi_{\\text{mult}}}{\\partial x_i^2} \\equiv 0$), logo $\\text{Tr}(\\mathcal{H}_{\\mathcal{F}}) = 0$.

Para concluir $\\lambda_{\\min}(\\mathcal{H}_{\\mathcal{F}}) < 0$, é estritamente necessário demonstrar que $\\mathcal{H}_{\\mathcal{F}} \\ne \\mathbf{0}$. O argumento utilizado baseia-se na existência de uma cláusula violada $c$ contendo uma variável livre de folha $x_\\ell$ de grau global 1 e uma variável interna $x_p$. Como $x_\\ell$ não pertence a nenhuma outra cláusula, a entrada $H_{\\ell p}$ não sofre cancelamento.

Reconhecemos a dependência lógica destacada por Vossa Senhoria:
$$\\boxed{\\text{Estrutura apropriada de folha } (H_{\\text{leaf}}) \\implies H_{\\ell p} \\ne 0 \\implies \\mathcal{H} \\ne \\mathbf{0} \\implies \\lambda_{\\min} < 0}$$
Como o primeiro passo depende da aciclicidade linear estrita (Lema 10.1), que não foi provada a.a.s. para todo o grafo, o Lema 10.2 não pode ser considerado universalmente fechado.

Seu status formal é retificado para:
$$\\boxed{\\text{Lema 10.2: } \\textbf{🟡 Fechado condicionalmente à hipótese estrutural } H_{\\text{leaf}}}$$

### 3.2. Correção do Fator em $H_{\\ell p}$
Sanamos o erro de fator apontado na auditoria. Para a cláusula multilinear $P_c(x) = \\prod_{j \\in c} \\frac{1 - \\sigma_j x_j}{2}$, a derivada de segunda ordem com relação a $x_\\ell$ e $x_p$ (com $k$ sendo a terceira variável) é exatamente:
$$\\frac{\\partial^2 P_c}{\\partial x_\\ell \\partial x_p} = \\frac{(-\\sigma_\\ell)(-\\sigma_p)}{2 \\cdot 2} \\left(\\frac{1 - \\sigma_k x_k}{2}\\right) = \\frac{\\sigma_\\ell \\sigma_p}{8}(1 - \\sigma_k x_k)$$
No texto anterior, havia uma notação ambígua que sugeria $(1 - \\sigma_k x_k / 2)$. Corrigimos para a expressão exata com denominador $8$. Como $|x_k^*| < 1 \\implies 1 - \\sigma_k x_k^* > 0$, a conclusão essencial de não-nulidade ($H_{\\ell p} \\ne 0$) permanece plenamente preservada.

---

## 4. Teorema 7B: Correção de Sinais e Equivalência no Bordo

Acolhemos a retificação pontual do Teorema 7B:
* Para qualquer $x \\in Z$, todas as restrições lineares são satisfeitas ($g_c(x) \\le 0, \\forall c$), donde $\\text{act}(x) = \\emptyset$. Portanto, o gradiente anula-se identicamente: $\\nabla \\Phi_{\\text{quad}}(x) = \\mathbf{0}$, o que implica $\\langle -\\nabla \\Phi_{\\text{quad}}(x), x \\rangle = 0$ em $Z$. Como $\\mathbf{0} \\in N_{\\mathcal{X}}(x)$, temos $Z \\subseteq \\mathcal{E}_{\\text{proj}}$.
* Para qualquer $x \\notin Z$, o conjunto de cláusulas ativas é não-vazio ($\\text{act}(x) \\ne \\emptyset$), o que garante a contração estrita:
  $$\\langle -\\nabla \\Phi_{\\text{quad}}(x), \\, x \\rangle = -\\sum_{c \\in \\text{act}(x)} (2 g_c(x)^2 + g_c(x)) < 0$$
* Para qualquer vetor do cone normal exterior $\\nu \\in N_{\\mathcal{X}}(x)$, a condição de sinal $\\nu_i x_i = |\\nu_i| \\ge 0$ impõe:
  $$\\langle \\nu, x \\rangle = \\sum_{|x_i|=1} \\nu_i x_i = \\sum_{|x_i|=1} |\\nu_i| \\ge 0$$
* Sendo $\\langle -\\nabla \\Phi_{\\text{quad}}(x), x \\rangle < 0$ incompatível com $\\langle \\nu, x \\rangle \\ge 0$, o vetor $-\\nabla \\Phi_{\\text{quad}}(x)$ jamais pode pertencer a $N_{\\mathcal{X}}(x)$ fora de $Z$. Logo, $\\mathcal{E}_{\\text{proj}} \\subseteq Z$.
* Conclui-se $\\mathcal{E}_{\\text{proj}} \\equiv Z$. Pelo Princípio de Invariância de LaSalle, todas as trajetórias convergem assintoticamente para $Z$.

Conforme prescrito pelo Professor, o status do Teorema 7B é fixado como:
$$\\boxed{\\text{Teorema 7B: } \\textbf{🟡 Quase Fechado}}$$

---

## 5. Falsificação do Lema 9.1 e a Nova Pergunta de Pesquisa

A auditoria experimental prescrita pelo Parecer 14 (Testes A e B) foi plenamente documentada:
1. **Teste B (Conservação da Média):** Confirmou-se numericamente que o fato unitário $h(x_1) = [\\max(0, (1 - x_1)/2)]^2$ injeta uma força $-\\frac{\\partial h}{\\partial x_1} = \\frac{1 - x_1}{2} > 0$, violando a conservação da média ($\\sum \\dot{x}_k = +0.60 > 0$).
2. **Teste A (Hinge vs PAV):** Para a cadeia com fato positivo $x_1 = 1$, as restrições forçam $1 \\le x_1 \\le \\dots \\le x_K \\le 1$, colapsando o politopo LP em $Z = \\{(+1, \\dots, +1)\\}$. O Hinge converge para $(+1, \\dots, +1)$ com $100\\%$ de taxa de sucesso. A alegação de armadilha espúria com probabilidade $1 - o(1)$ caiu definitivamente.
3. **Correção de Stirling:** Retificou-se $\\frac{\\binom{2K}{K}}{4^K} = \\frac{1}{\\sqrt{\\pi K}}(1 - \\frac{1}{8K} + \\mathcal{O}(K^{-2})) = \\Theta(K^{-1/2})$, expurgando $\\Theta(K^{-1})$.

### A Nova Pergunta Científica Formulada pelo Avaliador:
A falsificação do Lema 9.1 redefine a fronteira da investigação:
$$\\boxed{\\text{Quais estruturas SAT possuem } \\mathcal{M}_{\\text{spur}}(\\Phi_{\\text{quad}}) \\text{ grande, mas } \\mathcal{M}_{\\text{spur}}(\\Phi_{\\text{mult}}) \\text{ pequena?}}$$
Essa questão passa a orientar as investigações futuras do programa CLG-R, com foco em famílias com fatos negativos ou ramificações concorrentes (como na Proposição 7A).  
Status do Teorema 9: **🔴 Falsificado / Abandonado**.

---

## 6. Saneamento do Firewall Epistemológico (3-XOR-SAT)

Acolhemos integralmente a advertência de Vossa Senhoria quanto ao uso da palavra "absoluta". O resultado com 3-XOR-SAT demonstra rigorosamente que:
$$\\text{falha de dinâmica contínua} \\not\\Rightarrow P \\ne NP$$
e
$$\\text{dificuldade de landscape} \\not\\Rightarrow \\text{dificuldade computacional de Turing}$$
O texto foi formalmente retificado para:
$$\\boxed{\\textbf{Firewall epistemológico contra inferências de dificuldade dinâmica para } P \\ne NP}$$

---

## 7. Adoção Estrita da Matriz de Rigor da Seção 9 do Parecer do Professor

Substituímos integralmente qualquer formulação anterior pela tabela de status prescrita por Vossa Senhoria:

| Resultado | Status de Auditoria (Parecer do Professor) | Qualificação Técnica Formal e Limites Analíticos |
| :--- | :---: | :--- |
| **T1** (Caixa Central $\\mathcal{U}_N$) | 🟢 **Fechado** | Universal determinístico; folga interior 0.5 em toda a caixa. |
| **T2** (Medida Nula de Críticos) | 🟢 **Fechado, sob hipóteses declaradas** | Fubini para $\\Phi_{\\text{mult}}$; analiticidade real para $\\Phi_{\\text{soft}}$. |
| **T3** (Harmonicidade e Selas) | 🟢 **Fechado, com hipóteses** | Princípio do Mínimo Forte e Lema de Seleção de Curvas de Milnor. |
| **T4A′** (Mínimos em Faces) | 🟢 **Fechado** | Mínimos locais em faces herdam energia de vértices. |
| **4B** (Confinamento de LaSalle) | 🟢 **Fechado** | Lyapunov estrito no hipercubo compacto; atratores isolados confinados a $\\{-1, 1\\}^N$. |
| **T5** (Hessiana Softplus $V^T W V$) | 🟢 **Fechado, com condições explicitadas** | Fatoração exata; $\\text{rank}(V)=N \\implies$ estrita convexidade. |
| **T6** (Lipschitz e Underflow) | 🟢 **Fechado, com convenções IEEE** | $L_\\beta = \\Theta(\\beta)$ bilateral; limites de underflow e flush-to-zero. |
| **T7B** (Contração Centrípeta e LaSalle) | 🟡 **Quase Fechado** | Equivalência $\\mathcal{E}_{\\text{proj}} \\equiv Z$; convenção de cone normal exterior explicitada. |
| **T8** (Cota de Jensen no Volume LP) | 🟢 **Fechado como cota finita** | Cota analítica $\\mathbb{E}[\\mu(Z)] \\ge (5/6)^{\\alpha N} > 0$; decaimento assintótico reconhecido. |
| **T9** (Horn Linear Monótono) | 🔴 **Falsificado / Abandonado** | Lema 9.1 falsificado sob fato unitário positivo ($Z=\\{(1,\\dots,1)\\}$); em aberto para DAGs gerais. |
| **Lema 10.1** (Hiperárvores Subcríticas) | 🟡 **Parcialmente Fechado** | $2\\text{-core} = \\emptyset$ provado a.a.s.; cota $9\\alpha^2 = \\mathcal{O}(1)$ não implica $P(X=0)\\to 1$. |
| **Lema 10.2** (Strict Saddle Subcrítico) | 🟡 **Fechado sob hipótese $H_{\\text{leaf}}$** | Traço nulo e $H_{\\ell p} = \\frac{\\sigma_\\ell \\sigma_p}{8}(1 - \\sigma_k x^*_k) \\ne 0$ garantem $\\lambda_{\\min} < 0$. |
| **Teorema 10** (Separação em 3-SAT Subcrítico) | 🔴 **Não Fechado** | Evasão de sela provada para $\\Phi_{\\text{mult}}$; separação analítica com Hinge permanece em aberto. |
| **Conjectura Central** (Regime de Clustering) | 🔵 **Conjectura Delimitada** | Formalmente restrita a $\\alpha \\in (\\alpha_d, \\alpha_s)$ e ensemble plantado. |
| **3-XOR-SAT Firewall** | 🟢 **Resultado Epistemológico** | Separação categórica entre dinâmica contínua e complexidade de Turing (sem "absoluto"). |

---

## 8. Conclusão e Congelamento da Versão 4.0.1

Atendendo estritamente à recomendação de Vossa Senhoria, **congelamos a Versão 4.0.1 e não acrescentamos absolutamente nenhum teorema novo**.

As correções pontuais foram incorporadas ao manuscrito LaTeX ([`CLG_FOUNDATIONS_ARXIV.tex`](file:///C:/MathDoCarvalho/P_NP/Publicacoes/CLG_FOUNDATIONS_ARXIV.tex)) e à monografia ([`ESTUDO_ANALITICO_DO_CONJUNTO_CRITICO.md`](file:///C:/MathDoCarvalho/P_NP/Publicacoes/ESTUDO_ANALITICO_DO_CONJUNTO_CRITICO.md)).

A vulnerabilidade matemática central do programa foi isolada na transição **Lema 10.1 $\\to$ Lema 10.2**, e futuras investigações concentrar-se-ão no tratamento de componentes com defeitos pontuais ($G = G_{\\text{tree}} + G_{\\text{defect}}$).

Renovamos nosso profundo apreço pela orientação rigorosa e transformadora proporcionada pelo processo de avaliação.

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

    # 1. Salvar RespostaAoProfessor_Analise14.md
    with open(os.path.join(PUB_DIR, "RespostaAoProfessor_Analise14.md"), "w", encoding="utf-8") as f:
        f.write(RESPOSTA_14_MD)
    with open(os.path.join(ROOT_DIR, "RespostaAoProfessor_Analise14.md"), "w", encoding="utf-8") as f:
        f.write(RESPOSTA_14_MD)
    print("Salvo: RespostaAoProfessor_Analise14.md")

    # 2. Gerar RespostaAoProfessor_Analise14.docx
    doc_resp = docx.Document()
    for s in doc_resp.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    p_title = doc_resp.add_paragraph()
    run_title = p_title.add_run("Resposta Técnica ao Parecer nº 14 do Professor:\nRelatório de Falsificação e Saneamento da Versão 4.0.1")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(18)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x1F, 0x4E, 0x78)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_sub = doc_resp.add_paragraph()
    run_sub = p_sub.add_run("Acolhimento Integral da Auditoria Crítica, Falsificação do Lema 9.1 e Matriz de Rigor da Seção 12\nAutor: Thiago Carvalho e Equipe CLG-R | Data: 16 de Setembro de 2026")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(10.5)
    run_sub.font.italic = True
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc_resp.add_paragraph()

    lines = RESPOSTA_14_MD.split("\n")
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

    doc_resp.save(os.path.join(PUB_DIR, "RespostaAoProfessor_Analise14.docx"))
    doc_resp.save(os.path.join(ROOT_DIR, "RespostaAoProfessor_Analise14.docx"))
    print("Salvo: RespostaAoProfessor_Analise14.docx")

    # 3. Gerar MensagemParaOAvaliador14
    doc_msg = docx.Document()
    for s in doc_msg.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    p_mtitle = doc_msg.add_paragraph()
    rm_title = p_mtitle.add_run("Atualização Formal — Parecer nº 14 e Falsificação do Lema 9.1")
    rm_title.font.name = "Calibri"
    rm_title.font.size = Pt(16)
    rm_title.font.bold = True
    rm_title.font.color.rgb = RGBColor(0x1F, 0x4E, 0x78)
    p_mtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc_msg.add_paragraph()

    for par in MENSAGEM_14_TEXTO.split("\n\n"):
        p = doc_msg.add_paragraph()
        clean_par = clean_math_for_docx(par.strip())
        add_formatted_runs(p, clean_par, font_size=Pt(11))

    doc_msg.save(os.path.join(PUB_DIR, "MensagemParaOAvaliador14.docx"))
    doc_msg.save(os.path.join(ROOT_DIR, "MensagemParaOAvaliador14.docx"))
    print("Salvo: MensagemParaOAvaliador14.docx")

    with open(os.path.join(PUB_DIR, "MensagemParaOAvaliador14.txt"), "w", encoding="utf-8") as f:
        f.write(MENSAGEM_14_TEXTO)
    with open(os.path.join(ROOT_DIR, "MensagemParaOAvaliador14.txt"), "w", encoding="utf-8") as f:
        f.write(MENSAGEM_14_TEXTO)
    print("Salvo: MensagemParaOAvaliador14.txt")

    # 4. Atualizar zip
    zip_path = os.path.join(PUB_DIR, "arxiv_package.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
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
                print(f"[ZIP] Adicionado: {fname}")
    print("Salvo: arxiv_package.zip atualizado!")

if __name__ == "__main__":
    build_deliverables()
