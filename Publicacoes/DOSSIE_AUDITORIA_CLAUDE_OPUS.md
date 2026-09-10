# Dossiê de Auditoria Científica Independente para o Claude Opus

**Projeto:** Pesquisa P vs NP — Neuro-Meta-Heurística de Carvalho & Computational Landscape Geometry (CLG)  
**Autor:** Thiago Carvalho (2026)  
**Repositório Oficial Público:** [https://github.com/thiagocarvalhodba/p-vs-np-carvalho](https://github.com/thiagocarvalhodba/p-vs-np-carvalho)  

---

## 📋 Instruções de Uso
Copie todo o texto abaixo (a partir da linha pontilhada) e cole diretamente na interface do **Claude 3.5 / Opus**.

--------------------------------------------------------------------------------

### PROMPT DE AUDITORIA FORMAL (PEER REVIEW ANÔNIMO - JACM / ANNALS OF MATHEMATICS)

**Papel:** Você é um revisor sênior anônimo do *Journal of the ACM (JACM)* e do *Annals of Mathematics*, especialista em Teoria da Complexidade Computacional, Topologia Diferencial, Otimização Contínua e Física Estatística de Sistemas Desordenados.

**Sua Postura:** Seja implacável, cético e rigoroso. Não faça elogios protocolares. Seu objetivo é dissecar a fundamentação matemática, identificar falácias, apontar variáveis ocultas e emitir um parecer científico definitivo sobre o estado da arte da pesquisa descrita abaixo.

---

### 1. CONTEXTO DO PROJETO E REPOSITÓRIO PÚBLICO
O pesquisador Thiago Carvalho desenvolveu um arcabouço público em PyTorch e quatro artigos científicos investigando a fronteira do problema **P vs NP** através de relaxações contínuas no hipercubo $\mathcal{X} = [-1, 1]^N$:
- **Repositório:** `https://github.com/thiagocarvalhodba/p-vs-np-carvalho`
- **Paper I (SIAM):** Relaxação laplaciana contínua em Max-Cut e a Conjectura do Alinhamento Espectral Induzido por Hubs (HISAC).
- **Paper II (IEEE TPAMI):** Complexidade linear estritamente parametrizada $\mathcal{O}((N+M)d_{\text{hidden}}^2)$ com agregação atômica in-place (`index_add_`) em $N=10.000$ nós.
- **Paper III (JMLR):** Termodinâmica de não-equilíbrio e recozimento adaptativo no TSP Euclidiano.
- **Paper IV (JACM):** Relaxação diferenciável do núcleo de Cook-Levin (Max-3-SAT), obtendo $99.25\%$ de cláusulas satisfeitas em instâncias aleatórias no limiar crítico ($m/n \approx 4.267$).

---

### 2. A TRANSIÇÃO CONCEITUAL: DO ALGORITMO À GEOMETRIA (PROJETO CLG)
Após interlocução acadêmica com um professor sênior de matemática, a pesquisa mudou seu foco: a rede neural (GNN) passou a ser apenas um instrumento de controle, e o verdadeiro objeto de estudo tornou-se a **Geometria da Paisagem Computacional (CLG)**, formalizada pela 5-tupla:
$$\mathcal{L}(I) = \left( \mathcal{X}, \mathcal{E}, \mu, \Phi, \mathcal{D} \right)$$
onde $\Phi(x) = \sum_{c=1}^M \prod_{j=1}^k \frac{1 - \sigma_{c,j} x_{c,j}}{2}$ é o potencial contínuo de violação das cláusulas.

---

### 3. O EXPERIMENTO CLG-01 E O DESAFIO DO PROFESSOR
No **CLG-01**, mediu-se a dispersão de curvatura da Hessiana $\Omega_{\text{curv}} = \mathbb{E}[\|\mathcal{H}(x) - \overline{\mathcal{H}}\|_F^2]^{1/2}$:
- **2-SAT (Classe P):** Provou-se analiticamente que $\nabla^3 \Phi \equiv 0$, logo $\Omega_{\text{curv}} \equiv 0$ e a Hessiana é rigorosamente constante em todo o hipercubo.
- **3-SAT (Classe NP-Completa):** $\nabla^3 \Phi \neq 0$, logo a Hessiana é dependente de estado ($\Omega_{\text{curv}} \approx 2.2$) e o índice de rigidez $R(I) = (\Omega_{\text{curv}} / \Delta \lambda) \cdot \rho_{-}$ explodiu para $\approx 0.40$ (gap de 5 ordens de magnitude, $p = 1.53 \times 10^{-6}$).

**O Ataque do Professor:**  
O professor apontou uma variável oculta perigosa:  
*“O CLG-01 pode estar detectando apenas o grau do polinômio ($\deg=2$ vs $\deg=3$), e não a complexidade computacional. Toda função quadrática tem terceira derivada nula, independente de ser em P ou não. O teste de fogo é: o que acontece se testarmos uma subclasse de 3-SAT que comprovadamente pertence a P (como Horn-3-SAT) mantendo o grau estritamente igual a 3?”*

---

### 4. OS RESULTADOS DO EXPERIMENTO CLG-02 (DEGREE CONTROL)
Atendendo à objeção, implementou-se o **CLG-02** comparando 4 famílias com controle estrito de grau:
1. **2-SAT** (Classe P, Grau 2)
2. **Horn-3-SAT** (Classe P, Grau 3 — cláusulas com $\le 1$ literal positivo, resolvível em $\mathcal{O}(M)$ por propagação unitária)
3. **Equi-3-SAT** (Classe P, Grau 3 — 2-SAT embutido com variáveis auxiliares)
4. **Random-3-SAT** (Classe NP-Completa, Grau 3 — no limiar crítico $m/n \approx 4.267$)

**Os Dados Empíricos Obtidos:**
| Família | Classe | Grau | Curvatura Estática $\Omega_{\text{curv}}$ | Tensor 3ª Ordem $\|\mathcal{T}\|_F$ | Alcançabilidade da Bacia (Global Success %) | Densidade de Armadilhas (Unsat Cláusulas) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **2-SAT** | P | 2 | $0.0000$ | $0.0000$ | $29.0\%$ | $1.05$ |
| **Horn-3-SAT** | P | **3** | **$1.8095$** | **$3.2252$** | **$100.0\%$** | **$0.00$** |
| **Equi-3-SAT** | P | **3** | $0.0000$ | $0.0000$ | **$74.0\%$** | **$0.27$** |
| **Random-3-SAT** | NP-Comp | **3** | **$1.9041$** | **$3.4002$** | **$6.0\%$** | **$2.23$** |

**Descoberta do CLG-02:**
1. A curvatura estática local ($\Omega_{\text{curv}} \approx 1.81$ vs $1.90$) e o tensor $\|\mathcal{T}\|_F$ ($3.22$ vs $3.40$) de fato medem apenas o **grau algébrico** da penalidade (confirmando a suspeita do professor).
2. Porém, a **TOPOLOGIA DINÂMICA DA BACIA** separou drasticamente P de NP-Completo no mesmo grau ($\deg=3$):
   - No Horn-3-SAT (Classe P), a alcançabilidade é de **$100\%$ com $0.00$ armadilhas**, indicando um funil monótono sem bacias metaestáveis.
   - No Random-3-SAT (NP-Completo), a alcançabilidade despenca para **$6\%$ com $2.23$ cláusulas insatisfeitas presas**, indicando fragmentação vítrea (*spin-glass*).

---

### 5. SUAS PERGUNTAS DE AUDITORIA
Como revisor, responda fundamentadamente:
1. **Validade do CLG-02:** O desacoplamento entre curvatura estática local e topologia dinâmica de bacias resolve a crítica da variável oculta de grau?
2. **Vulnerabilidades Teóricas:** Quais são as falhas, contraexemplos potenciais ou fragilidades remanescentes nessa formulação?
3. **Ponte Assintótica:** Como formalizar matematicamente o operador de alcançabilidade de bacias $\mathcal{R}_{\text{basin}}$ para que ele se conecte rigorosamente com limites inferiores (*lower bounds*) de complexidade de circuitos ou Máquinas de Turing?
4. **Veredito:** Qual é o nível de originalidade e relevância deste programa de pesquisa perante a literatura internacional contemporânea?
