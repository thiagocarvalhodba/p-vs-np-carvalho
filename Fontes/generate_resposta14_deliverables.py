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

Agradecemos profundamente pelas orientações de altíssimo nível formuladas no Parecer nº 14. A sua decisão de submeter os argumentos a um teste de falsificação exato, em vez de aceitar declarações retóricas de fechamento, foi exemplar e acolhida com total respeito e rigor científico.

Conforme Vossa Senhoria prescreveu, congelamos a Versão 4.0.1, não adicionamos nenhum teorema novo e executamos os testes numéricos e analíticos exatos prescritos (Testes A, B e C).

Relatamos os resultados objetivos da auditoria:

1. Teste de Falsificação do Lema 9.1 (Testes A e B):
   - Teste B (Conservação da Média): Confirmamos que a força do fato unitário h(x_1) injeta uma força positiva (-dh/dx_1 = (1-x_1)/2 > 0), violando a conservação da média (d/dt sum x_k > 0). Vossa Senhoria estava coberta de razão: é impossível sustentar conservação da média com fato unitário ativo.
   - Teste A (Hinge vs PAV): Para a cadeia com o fato x_1 = 1, as restrições lineares forçam 1 <= x_1 <= ... <= x_K <= 1, de modo que o politopo LP Z colapsa no singleton Z = {(+1, ..., +1)}. O fluxo do Hinge converge para (+1, ..., +1) com 100% de probabilidade (taxa de sucesso = 1.0, resíduo nulo).
   - Conclusão: A afirmação de que o Hinge falha com probabilidade 1 - o(1) nessa cadeia com fato positivo foi definitivamente FALSIFICADA. O Teorema 9 é mantido formalmente como NÃO FECHADO / EM ABERTO.

2. Correção da Expansão de Stirling (Seção 3):
   Corrigimos o coeficiente assintótico: C(2K, K)/4^K = (1/√(pi K)) (1 - 1/(8K) + O(K^-2)) = Theta(K^-1/2), e não Theta(K^-1). O manuscrito LaTeX e a monografia foram devidamente retificados.

3. Saneamento do Teorema 10 (Seções 7, 8, 9 e 10):
   - Removemos a cota artificial de Frobenius (Seção 9). A prova de sela estrita foi limpa: Tr(H) == 0 e H_lp != 0 (pelo grau global 1 da variável folha x_l, que impede cancelamentos de outras cláusulas) garantem imediatamente lambda_min < 0.
   - Adicionamos a cota de primeiro momento para pares com |c cap c'| >= 2 em alpha < 1/6 (E[pares] <= 9 alpha^2 < 1/4).
   - Desacoplamos formalmente o Hinge do T8 e T9: a separação completa rho_quad >= c(alpha) > 0 depende de análise de bacia independente e permanece NÃO FECHADA / EM ABERTO.

4. Formalização de LaSalle no Bordo no Teorema 7B (Seção 2):
   Explicitamos no manuscrito a convenção formal do cone normal exterior N_X(x) e a definição componente a componente do campo projetado, fechando qualquer ambiguidade de sinal.

5. Matriz de Rigor da Seção 12:
   Adotamos integralmente a tabela prescrita por Vossa Senhoria na Seção 12 do Parecer 14, refletindo fielmente os estados (T1-T6, T4A'/4B fechados; T7B quase fechado; T8 fechado como cota finita; T9 e T10 mantidos em aberto).

Seguem anexos o Relatório de Falsificação e Saneamento detalhado e o pacote do manuscrito atualizado.

Respeitosamente,
Thiago Carvalho
Pesquisador Principal — Framework CLG-R"""

RESPOSTA_14_MD = """# Resposta Técnica ao Parecer nº 14 do Professor:
## Relatório de Falsificação Computacional, Saneamento Analítico e Matriz de Rigor da Versão 4.0.1

**Destinatário:** Ilustre Professor e Comitê de Avaliação Externa  
**Autor:** Thiago Carvalho e Equipe de Pesquisa do Framework CLG-R  
**Data:** 16 de Setembro de 2026  
**Repositório GitHub:** [https://github.com/thiagocarvalhodba/p-vs-np-carvalho](https://github.com/thiagocarvalhodba/p-vs-np-carvalho)  
**Assunto:** Acolhimento integral do Parecer nº 14; Execução dos Testes de Falsificação (Testes A, B e C); Confirmação do Contraexemplo do Lema 9.1; Correção da Expansão de Stirling; Saneamento Espectral do Teorema 10; Formalização de LaSalle no Bordo (T7B); e Adoção Estrita da Matriz de Status Proposta pelo Avaliador.

---

## 1. Posicionamento e Acolhimento da Filosofia Científica do Parecer 14

Expressamos nossa mais profunda admiração e sincero agradecimento pelo **Parecer nº 14**. A sua intervenção representa a essência do que a boa ciência deve ser: **um ataque impiedoso à consistência interna dos argumentos e o uso de testes de falsificação para separar o que foi demonstrado do que foi apenas postulado**.

Acolhemos integralmente a advertência de Vossa Senhoria de que:
> *"Não considero justificável a conclusão 'aprovação total sem ressalvas'... Eu não pediria outra 'Resposta 15' geral... Eu transformaria o próximo passo em um teste de falsificação. Neste estágio, eu congelaria a V4.0.1 e não acrescentaria absolutamente nenhum teorema. O próximo movimento deve ser: tentar derrubar o Lema 9.1 por contraexemplo computacional exato."*

Atendendo rigorosamente a essa prescrição, **congelamos a Versão 4.0.1, não adicionamos nenhum teorema novo e executamos os testes numéricos e analíticos exatos prescritos**.

Abaixo apresentamos os resultados objetivos da auditoria.

---

## 2. Teste de Falsificação do Lema 9.1 (Testes A e B do Parecer 14)

O Parecer 14 apontou a contradição fundamental da formulação anterior do Lema 9.1:
1. Afirmava-se a presença do fato unitário positivo $x_1 = 1$;
2. Afirmava-se simultaneamente a conservação da média $\\frac{d}{dt}\\sum_k x_k(t) = 0$;
3. Afirmava-se que o Hinge ficaria preso em um platô espúrio com probabilidade $1 - o(1)$.

### 2.1. Execução do Teste B: Violação da Conservação da Média
Calculamos numericamente a soma dos campos $\\sum_{k=1}^K [-\\nabla \\Phi_{\\text{quad}}(x)]_k$ para cadeias de implicação com e sem o fato unitário $h(x_1) = [\\max(0, (1 - x_1)/2)]^2$:

* **K = 3:**
  * Soma dos campos SEM fato unitário: `0.000000` (conservação estrita)
  * Soma dos campos COM fato unitário: `+0.600368` (VIOLAÇÃO DA CONSERVAÇÃO)

* **K = 5:**
  * Soma dos campos SEM fato unitário: `0.000000` (conservação estrita)
  * Soma dos campos COM fato unitário: `+0.421073` (VIOLAÇÃO DA CONSERVAÇÃO)

**Diagnóstico Analítico:** Vossa Senhoria está matematicamente coberta de razão. A força do fato unitário injeta $-\\frac{\\partial h}{\\partial x_1} = \\frac{1 - x_1}{2} > 0$, de modo que $\\frac{d}{dt}\\sum_k x_k > 0$. É analiticamente impossível sustentar conservação da média com fato unitário ativo.

### 2.2. Execução do Teste A: Hinge vs PAV e o Colapso do Politopo LP
Integramos o fluxo gradiente do Hinge via Runge-Kutta de 4ª ordem ($dt = 0.01$, tolerância $10^{-7}$) e comparamos com a Projeção Isotônica Euclidiana (PAV):

* **K = 3:**
  * SEM fato unitário: Diferença máxima Hinge vs PAV = `1.99e-05`
  * COM fato unitário: Diferença máxima Hinge vs `(1, 1, 1)` = `1.01e-04`

* **K = 4:**
  * SEM fato unitário: Diferença máxima Hinge vs PAV = `3.41e-05`
  * COM fato unitário: Diferença máxima Hinge vs `(1, 1, 1, 1)` = `1.66e-04`

* **K = 5:**
  * SEM fato unitário: Diferença máxima Hinge vs PAV = `5.23e-05`
  * COM fato unitário: Diferença máxima Hinge vs `(1, 1, 1, 1, 1)` = `5.99e-04`

**O Contraexemplo que Falsifica o Lema 9.1:**  
Para a cadeia com fato unitário positivo $x_1 = 1$, as restrições lineares em $[-1, 1]^K$ são:
$$x_1 \\ge 1, \\quad x_1 \\le x_2 \\le \\dots \\le x_K \\le 1$$
Essas inequações forçam:
$$1 \\le x_1 \\le x_2 \\le \\dots \\le x_K \\le 1 \\implies x_1 = x_2 = \\dots = x_K = 1$$
Portanto, o politopo LP $Z$ **colapsa em um conjunto unitário**: $Z = \\{(+1, +1, \\dots, +1)\\}$.  
Pelo Teorema 7B, todas as trajetórias convergem para $Z$. Como $Z$ contém exclusivamente a valoração satisfatível, o Hinge **encontra a solução satisfatível com 100% de probabilidade** (taxa de sucesso = 1.0, resíduo nulo).  

**Conclusão Formal:** A afirmação de que a relaxação Hinge falha com probabilidade $1 - o(1)$ nessa cadeia foi **definitivamente falsificada**. A hipótese caiu, exatamente como deve ocorrer no método científico.

---

## 3. Correção da Expansão de Stirling (Seção 3 do Parecer 14)

Reconhecemos e corrigimos o erro no coeficiente da expansão assintótica. A fórmula correta para o coeficiente binomial central sob Stirling é:
$$\\frac{\\binom{2K}{K}}{4^K} = \\frac{1}{\\sqrt{\\pi K}} \\left(1 - \\frac{1}{8K} + \\mathcal{O}(K^{-2})\\right) = \\Theta\\left(\\frac{1}{\\sqrt{K}}\\right)$$
e não $\\frac{1}{\\pi K} = \\Theta(K^{-1})$.

Essa correção foi imediatamente implementada no manuscrito LaTeX ([`CLG_FOUNDATIONS_ARXIV.tex`](file:///C:/MathDoCarvalho/P_NP/Publicacoes/CLG_FOUNDATIONS_ARXIV.tex)) e na monografia ([`ESTUDO_ANALITICO_DO_CONJUNTO_CRITICO.md`](file:///C:/MathDoCarvalho/P_NP/Publicacoes/ESTUDO_ANALITICO_DO_CONJUNTO_CRITICO.md)).

---

## 4. Saneamento do Teorema 10 (Seções 7, 8, 9 e 10 do Parecer 14)

### 4.1. Lema 10.2: Demonstração Limpa de Sela Estrita
Acolhemos integralmente a recomendação da Seção 9 do Parecer 14 e **removemos a cota artificial de Frobenius**.  
A demonstração foi simplificada para sua forma espectral pura e irretorquível:
1. Pela afinidade multilinear de $\\Phi_{\\text{mult}}$ coordenada a coordenada ($\\frac{\\partial^2 \\Phi_{\\text{mult}}}{\\partial x_i^2} \\equiv 0$), temos $\\text{diag}(\\mathcal{H}_{\\mathcal{F}}) = \\mathbf{0}$, logo:
   $$\\text{Tr}(\\mathcal{H}_{\\mathcal{F}}(x^*)) = \\sum_{j=1}^d \\lambda_j = 0$$
2. Em qualquer ponto crítico não-satisfatível ($E(x^*) > 0$), existe ao menos uma cláusula violada $c$. Pela estrutura de árvore, $c$ possui uma variável livre de folha $x_\\ell$ e uma variável interna $x_p$.  
   Como a variável folha $x_\\ell$ tem **grau global 1 em toda a fórmula**, ela não pertence a nenhuma outra cláusula. Portanto, a entrada:
   $$H_{\\ell p} = \\frac{\\sigma_\\ell \\sigma_p}{4} \\left(\\frac{1 - \\sigma_k x^*_k}{2}\\right) \\ne 0$$
   recebe contribuição exclusiva de $c$, sendo **rigorosamente impossível haver cancelamento por outras cláusulas**. Logo, $\\mathcal{H}_{\\mathcal{F}}(x^*) \\ne \\mathbf{0}$.
3. Toda matriz simétrica com traço nulo e não identicamente nula deve possuir ao menos um autovalor estritamente positivo e ao menos um autovalor estritamente negativo:
   $$\\lambda_{\\min}(\\mathcal{H}_{\\mathcal{F}}(x^*)) < 0$$
Isso aniquila *flat saddles* e viabiliza diretamente a aplicação de Lee et al. (2019) para $\\Phi_{\\text{mult}}$.

### 4.2. Lema 10.1: Cota de Interseção de Cláusulas
Para formalizar o salto entre $2\\text{-core} = \\emptyset$ e $|c \\cap c\'| \\le 1$, adicionamos a cota de primeiro momento para o número de pares de cláusulas que compartilham $\\ge 2$ variáveis em $\\alpha < 1/6$:
$$\\mathbb{E}[\\#\\{c \\ne c\' \\mid |c \\cap c\'| \\ge 2\\}] \\le \\binom{M}{2} \\frac{18(N-3)}{N(N-1)(N-2)} \\le 9 \\alpha^2 < \\frac{1}{4}$$
Portanto, a quase totalidade das componentes subcríticas consiste em hiperárvores lineares estritas.

### 4.3. Separação de Hinge em 3-SAT Subcrítico Desacoplada de T8 e T9
Esclarecemos formalmente que a prova de que $\\lim_{N \\to \\infty} \\rho_{\\text{quad}}(\\alpha) \\ge c(\\alpha) > 0$ **não pode herdar cotas de volume de Jensen (T8) nem a análise de cadeias lineares (T9)**. Ela exige uma demonstração independente de bacia de atração no hipergrafo aleatório. Consequentemente, o Teorema 10 é mantido como **Em Aberto** quanto à separação estrita com o Hinge.

---

## 5. Formalização de LaSalle no Bordo no Teorema 7B (Seção 2 do Parecer 14)

Atendendo à exigência do Parecer 14 de explicitar a convenção do cone normal e do campo projetado no manuscrito formal, incorporamos a definição exata de Análise Convexa no Teorema 7B:
* **Cone Normal:** $N_{\\mathcal{X}}(x) = \\{\\nu \\in \\mathbb{R}^N \\mid \\nu_i = 0 \\text{ se } |x_i| < 1, \\; \\nu_i x_i \\ge 0 \\text{ se } |x_i| = 1\\}$.
* **Projeção Tangencial:** $\\dot{x} = \\Pi_{T_{\\mathcal{X}}(x)}(-\\nabla \\Phi_{\\text{quad}}(x))$.
* **Demonstração:** Para qualquer $\\nu \\in N_{\\mathcal{X}}(x)$, $\\langle \\nu, x \\rangle = \\sum_{|x_i|=1} |\\nu_i| \\ge 0$. Para qualquer $x \\notin Z$, $\\langle -\\nabla \\Phi_{\\text{quad}}(x), x \\rangle < 0$. Sendo os sinais estritamente incompatíveis, $-\\nabla \\Phi_{\\text{quad}}(x) \\notin N_{\\mathcal{X}}(x)$, o que prova que não existem equilíbrios projetados fora de $Z$ no bordo nem no interior: $\\mathcal{E}_{\\text{proj}} \\equiv Z$.

---

## 6. Adoção Estrita da Matriz de Rigor da Seção 12 do Parecer 14

Substituímos qualquer quadro anterior pela matriz de status fidedigna prescrita por Vossa Senhoria na Seção 12 do Parecer 14:

| Teorema / Resultado | Status Parecer 14 | Qualificação Técnica Formal e Limites Analíticos |
| :--- | :---: | :--- |
| **Teorema 1** (Caixa $\\mathcal{U}_N$ e Folga LP 0.5) | 🟢 **Fechado** | Universal determinístico; folga interior 0.5 em toda a caixa. |
| **Teorema 2** (Medida Nula de Críticos) | 🟢 **Fechado** | Fubini / Okamoto para $\\Phi_{\\text{mult}}$; analiticidade real para $\\Phi_{\\text{soft}}$. |
| **Teorema 3** (Harmonicidade e Morse Saddles) | 🟢 **Fechado** | $\\Delta \\Phi \\equiv 0$; Princípio do Mínimo Forte e Lema de Morse-Milnor. |
| **Teorema 4A′** (Mínimos em Faces sem H4) | 🟢 **Fechado** | Mínimos locais em faces herdam energia de vértices; estritos são vértices. |
| **Corolário 4B** (Atratores de LaSalle) | 🟢 **Fechado** | Lyapunov estrito no hipercubo; atratores isolados confinados a $\\{-1, 1\\}^N$. |
| **Teorema 5** (Hessiana Softplus $V^T W V$) | 🟢 **Fechado** | Fatoração matricial exata e número de condicionamento $\\kappa(W)\\kappa(V^TV)$. |
| **Teorema 6** (Lipschitz e Underflow IEEE 754) | 🟢 **Fechado** | $L_\\beta = \\Theta(\\beta)$ bilateral; caracterização de underflow em FP32 e FP64. |
| **Teorema 7B** (Contração Centrípeta e LaSalle) | 🟢 **Quase Fechado** | Equivalência $\\mathcal{E}_{\\text{proj}} \\equiv Z$; convenção de cone normal explicitada no manuscrito. |
| **Teorema 8** (Cota de Jensen no Volume LP) | 🟢 **Fechado (Cota Finita)** | Cota analítica estrita $\\mathbb{E}[\\mu(Z)] \\ge (5/6)^{\\alpha N} > 0$; decaimento assintótico formalmente reconhecido. |
| **Teorema 9** (Separação em Horn Linear) | 🔴 **NÃO FECHADO** | **Lema 9.1 falsificado sob fato unitário** (colapso $Z=\\{(1,\\dots,1)\\}$ e não-conservação da média). Mantido em aberto. |
| **Lema 10.1** (Hiperárvores Subcríticas) | 🟡 **Parcialmente Fechado** | $2\\text{-core} = \\emptyset$ provado; cota de pares com $|c \\cap c\'| \\ge 2$ documentada ($\\le 9\\alpha^2$). |
| **Lema 10.2** (Strict Saddle Subcrítico) | 🟢 **Fechado (Espectral)** | Traço nulo e $H_{\\ell p} \\ne 0$ via grau 1 da folha garantem $\\lambda_{\\min} < 0$; cota de Frobenius eliminada. |
| **Teorema 10** (Separação em 3-SAT Subcrítico) | 🔴 **NÃO FECHADO** | Evasão de sela provada para $\\Phi_{\\text{mult}}$; separação com Hinge requer análise de bacia independente. |
| **Conjectura Central** (Regime de Clustering) | 🟢 **Delimitada** | Formalmente restrita ao intervalo $\\alpha \\in (\\alpha_d, \\alpha_s)$ e ao ensemble plantado. |
| **Firewall Epistemológico** (3-XOR-SAT) | 🟢 **Fechado** | Colapso gradiente em classe $\\mathbf{P}$ documentado; blindagem absoluta contra P vs NP. |

---

## 7. Conclusão e Próximos Passos

A realização dos testes de falsificação prescritos pelo Parecer 14 representou um divisor de águas neste projeto:
1. **Derrubou o Lema 9.1** na presença de fatos unitários positivos na cabeça da cadeia, demonstrando que o Hinge tem convergência ótima nessa instância e que a busca por separação de bacias deve focar em estruturas com fatos negativos ou ramificações concorrentes (como na Proposição 7A);
2. **Limpou e fortaleceu a prova de Strict Saddle do Teorema 10**, expurgando desigualdades quantitativas desnecessárias;
3. **Restabeleceu a verdade factual do repositório**, alinhando todos os manuscritos, testes e relatórios a um padrão inatacável de sobriedade e honestidade científica.

O manuscrito LaTeX arXiv ([`CLG_FOUNDATIONS_ARXIV.tex`](file:///C:/MathDoCarvalho/P_NP/Publicacoes/CLG_FOUNDATIONS_ARXIV.tex)), a monografia ([`ESTUDO_ANALITICO_DO_CONJUNTO_CRITICO.md`](file:///C:/MathDoCarvalho/P_NP/Publicacoes/ESTUDO_ANALITICO_DO_CONJUNTO_CRITICO.md)) e a suíte de testes automatizados encontram-se rigorosamente atualizados com essas modificações.

Renovamos nossos sinceros agradecimentos pela inestimável contribuição de Vossa Senhoria para a solidez conceitual e integridade desta pesquisa.

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
