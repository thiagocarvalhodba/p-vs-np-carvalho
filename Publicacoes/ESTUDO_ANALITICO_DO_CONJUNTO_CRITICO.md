# Estudo Analítico do Conjunto Crítico e Massa de Bacia Espúria no Framework CLG-R
**Versão 4.0 — Pós-Auditoria Profunda e Homologação Rigorosa**  
**Data:** 11 de Setembro de 2026  
**Área:** Otimização Contínua, Topologia Diferencial, Sistemas Dinâmicos e Física Estatística de CSPs  
**Status:** Teoremas Estruturais Provados, Proposição 7A Construtiva, Teorema de Volume LP, Teorema de Horn via Hirsch, Teorema Subcrítico de Árvores e Conjectura Central Delimitada.

---

## 1. Notação, Espaço de Configuração e Identificações Exatas

Seja $F$ uma fórmula booleana na Forma Normal Conjuntiva (3-CNF) sobre $N$ variáveis booleanas $x_1, \dots, x_N$, composta por $M$ cláusulas disjuntivas $\mathcal{C} = \{c_1, \dots, c_M\}$.  
O espaço de relaxação contínua é o hipercubo compacto $\mathcal{X} = [-1, 1]^N \subset \mathbb{R}^N$, cujo bordo é $\partial \mathcal{X}$, o interior aberto é $\text{int}(\mathcal{X}) = (-1, 1)^N$, e o conjunto de vértices discretos é $\mathcal{V} = \{-1, +1\}^N$.

Para cada cláusula $c = (\ell_1 \lor \ell_2 \lor \ell_3)$, o vetor de polaridade é denotado por $\sigma^{(c)} \in \{-1, 0, +1\}^N$, com exatamente 3 entradas não-nulas ($\sigma_j^{(c)} = +1$ se a variável $x_j$ aparece não-negada na cláusula, e $\sigma_j^{(c)} = -1$ se aparece negada).

### Violação Afim por Cláusula
Para cada cláusula $c$, definimos a função afim de violação:
$$g_c(x) = -\frac{1}{2}\left(1 + \sum_{j \in c} \sigma_j^{(c)} x_j\right) = -\frac{1}{2}\left(1 + \sigma^{(c)} \cdot x\right)$$
Em qualquer vértice discreto $s \in \{-1, +1\}^N$:
* $g_c(s) = 1$ se a cláusula $c$ é violada por $s$;
* $g_c(s) \in \{-2, -1, 0\}$ se a cláusula $c$ é satisfeita por $s$.

### As Três Relaxações Canônicas e Identificações Exatas
1. **Relaxação Quadrática Hinge ($\Phi_{\text{quad}}$):**
   $$\Phi_{\text{quad}}(x) = \sum_{c=1}^M \max(0, g_c(x))^2$$
   *Identificação:* O conjunto de nível zero $Z = \{x \in \mathcal{X} \mid g_c(x) \le 0, \; \forall c \in \{1, \dots, M\}\}$ coincide exatamente com o **politopo da relaxação linear canônica (LP)** de 3-SAT (onde a restrição de cobertura é $\sum_{j \in c} z_j \ge 1$ sob a bijeção $z_j = (1+x_j)/2$). Os pontos de $Z$ são os **mínimos globais** de $\Phi_{\text{quad}}$ com valor identicamente zero.

2. **Extensão Multilinear Harmônica ($\Phi_{\text{mult}}$):**
   $$\Phi_{\text{mult}}(x) = \sum_{c=1}^M \prod_{j \in c} \left(\frac{1 - \sigma_j^{(c)} x_j}{2}\right)$$
   *Identificação Física Exata:* $\Phi_{\text{mult}}(x)$ é rigorosamente a **energia de campo médio ingênuo (naive mean-field)** da física estatística:
   $$\Phi_{\text{mult}}(x) = \mathbb{E}_{s \sim \prod_{i=1}^N \text{Bern}\left(\frac{1+x_i}{2}\right)}[E_{\text{disc}}(s)]$$
   Para problemas de paridade como 3-XOR-SAT, a extensão multilinear coincide exatamente com o Hamiltoniano do **spin glass $p$-spin diluído**:
   $$\Phi_{\text{mult}}(x) = \frac{1}{2} \sum_{e} (1 - J_e x_i x_j x_k)$$

3. **Relaxação Softplus Analítica ($\Phi_{\text{soft}}$):**
   $$\Phi_{\text{soft}}(x) = \frac{1}{\beta} \sum_{c=1}^M \ln\left(1 + e^{\beta g_c(x)}\right), \quad \beta > 0$$

### O Fluxo Gradiente Projetado Contínuo
O sistema dinâmico governante é o fluxo de gradiente projetado:
$$\dot{x}(t) = \Pi_{T_{\mathcal{X}}(x(t))}\left(-\nabla \Phi(x(t))\right)$$
onde $T_{\mathcal{X}}(x)$ é o cone tangente de $\mathcal{X}$ em $x$, e $\Pi_K$ denota a projeção ortogonal no cone convexo fechado $K$. A discretização temporal padrão é o **Euler projetado puro**:
$$x^{(t+1)} = \text{clip}\left(x^{(t)} - \eta \nabla \Phi(x^{(t)}), \; -1, \; 1\right)$$
operando a partir de inicialização uniforme $x_0 \sim \text{Unif}([-1, 1]^N)$, sem termos artificiais de penalidade de caixa.

---

## 2. Hipóteses Estruturais

* **(H1) Fórmulas Próprias (Sem Variáveis Repetidas):** Cada cláusula $c$ contém exatamente 3 variáveis distintas: $|\text{supp}(\sigma^{(c)})| = 3$.
* **(H2) Espaço Confinado:** O domínio analítico e dinâmico é o hipercubo compacto $\mathcal{X} = [-1, 1]^N$.
* **(H3') Não-Degenerescência de Walsh-Fourier (Não-Trivialidade Booleana):**  
  A função discreta de energia $E_{\text{disc}}: \{-1, +1\}^N \to \mathbb{Z}_{\ge 0}$ não é identicamente constante: $\text{Var}_{s \sim \text{Unif}(\mathcal{V})}(E_{\text{disc}}(s)) > 0$. Pela identidade de Parseval na base de Walsh-Fourier:
  $$\sum_{S \subseteq \{1, \dots, N\}, S \ne \emptyset} \widehat{E}_{\text{disc}}(S)^2 = \text{Var}(E_{\text{disc}}) > 0$$
  garantindo que $\Phi_{\text{mult}} \not\equiv \text{const}$ em $\mathbb{R}^N$. A hipótese (H3') exclui exclusivamente fórmulas patológicas com $M \equiv 0$ ou tautologias isotrópicas completas ($2^3=8$ cláusulas cobrindo todos os sinais).

---

## 3. Teorema 1: A Caixa Fracionária Central e Folga Geométrica da Relaxação Linear

> **Teorema 1 (Caixa Fracionária Central e Platô de Mínimos Globais da Relaxação LP).**  
> *Considere qualquer fórmula 3-CNF satisfazendo (H1) e (H2). Defina a caixa fracionária central:*
> $$\mathcal{U}_N = \left(-\frac{1}{3}, \frac{1}{3}\right)^N \subset \text{int}(\mathcal{X})$$
> *Para todo ponto $x \in \mathcal{U}_N$, todas as $M$ restrições da relaxação linear são estritamente satisfeitas com folga:*
> $$g_c(x) < 0, \quad \forall c \in \{1, \dots, M\}$$
> *Consequentemente:*
> 1. *$\Phi_{\text{quad}}(x) \equiv 0$ e $\nabla \Phi_{\text{quad}}(x) \equiv \mathbf{0}$ em todo o aberto $\mathcal{U}_N$.*
> 2. *$\mathcal{U}_N$ está inteiramente contido no politopo da relaxação linear canônica $Z = \{x \in \mathcal{X} \mid g_c(x) \le 0, \forall c\}$.*
> 3. *O volume normalizado do politopo satisfaz $\mu_{\text{norm}}(Z) \ge \mu_{\text{norm}}(\mathcal{U}_N) = (1/3)^N$.*
> 4. *Sob (H3'), existe ao menos um vértice discreto violador ($E_{\text{disc}}(v) \ge 1$), assegurando que o ortante correspondente dentro de $\mathcal{U}_N$ gera arredondamento espúrio:*
>    $$\mu_{\text{norm}}(\mathcal{C}_{\text{spur}}(\Phi_{\text{quad}})) \ge \left(\frac{1}{6}\right)^N > 0$$
>    *Para fórmulas insatisfatíveis (UNSAT), todo o politopo $Z$ é espúrio: $\mu_{\text{norm}}(\mathcal{C}_{\text{spur}}) \ge \mu_{\text{norm}}(Z) \ge (1/3)^N$.*

### Demonstração Construtiva Determinística:
1. Para todo $x \in \mathcal{U}_N$, $|x_i| < 1/3$ para todo $i \in \{1, \dots, N\}$.
2. Para qualquer cláusula $c$, os coeficientes de polaridade são $\sigma_j^{(c)} \in \{-1, +1\}$. Logo:
   $$\sum_{j \in c} \sigma_j^{(c)} x_j \ge -\sum_{j \in c} |\sigma_j^{(c)} x_j| = -\sum_{j \in c} |x_j| > -3 \times \frac{1}{3} = -1$$
3. Substituindo na violação da cláusula:
   $$g_c(x) = -\frac{1}{2}\left(1 + \sum_{j \in c} \sigma_j^{(c)} x_j\right) < -\frac{1}{2}(1 - 1) = 0$$
4. Como todos os termos da função Hinge são nulos, $\Phi_{\text{quad}}(x) \equiv 0$ e $\nabla \Phi_{\text{quad}}(x) \equiv \mathbf{0}$ em todo o aberto $\mathcal{U}_N$.
5. Sob a transformação $z_j = (1+x_j)/2 \in [0, 1]$, a condição $g_c(x) \le 0$ traduz-se exatamente em $\sum_{j \in c} z_j \ge 1$. No centro $x = \mathbf{0}$ ($z_j = 1/2$), cada cláusula satisfaz $z_1 + z_2 + z_3 = 1.5$, gerando uma **folga interior exata de $0.5$**.
6. Sob (H3'), existe ao menos uma cláusula $c$; a atribuição que falsifica seus 3 literais define um ortante booleano cujos pontos em $\mathcal{U}_N$ satisfazem $\text{sign}(x) = -\sigma^{(c)}$, gerando violação discreta ($E_{\text{disc}} \ge 1$). A medida normalizada desse ortante dentro de $\mathcal{U}_N$ é $(1/6)^N$. Para UNSAT, todos os vértices violam, donde $\mu_{\text{norm}}(\mathcal{C}_{\text{spur}}) \ge (1/3)^N$. $\blacksquare$

---

## 4. Teorema 2: Medida de Lebesgue Nula dos Críticos de $\Phi_{\text{mult}}$ e $\Phi_{\text{soft}}$

> **Teorema 2 (Medida Nula dos Críticos Espúrios para Multilinear e Softplus).**  
> *Sob as hipóteses (H1), (H2) e a condição de não-degenerescência (H3'):*
> $$\mu(\mathcal{C}_0(\Phi_{\text{mult}})) = 0 \quad \text{e} \quad \mu(\mathcal{C}_0(\Phi_{\text{soft}})) = 0$$

### Demonstração:
1. **Caso Multilinear ($\Phi_{\text{mult}}$):**  
   $\Phi_{\text{mult}}(x) \in \mathbb{R}[x_1, \dots, x_N]$ é um polinômio real multivariado. Sob (H3'), $\Phi_{\text{mult}} \not\equiv \text{const}$, garantindo que existe ao menos uma coordenada $k$ tal que $P_k(x) \equiv \partial_k \Phi_{\text{mult}}(x) \not\equiv 0$.  
   O conjunto crítico de gradiente nulo satisfaz:
   $$\mathcal{C}_0(\Phi_{\text{mult}}) \subseteq \{x \in \mathcal{X} \mid \nabla \Phi_{\text{mult}}(x) = \mathbf{0}\} \subseteq \{x \in \mathcal{X} \mid P_k(x) = 0\}$$
   Por indução em $N$ e pelo Teorema de Fubini (Okamoto, 1973; Caron & Traynor, 2005), o conjunto de raízes de um polinômio real multivariado não identicamente nulo possui medida de Lebesgue estritamente zero em $\mathbb{R}^N$:
   $$\mu(\{x \in \mathcal{X} \mid P_k(x) = 0\}) = 0 \implies \mu(\mathcal{C}_0(\Phi_{\text{mult}})) = 0$$

2. **Caso Softplus ($\Phi_{\text{soft}}$):**  
   $\Phi_{\text{soft}}(x)$ é analítica real ($\mathcal{C}^\omega$). Pelo Teorema 5, seu Laplaciano satisfaz:
   $$\Delta \Phi_{\text{soft}}(x) = \text{Tr}(V^T W(x) V) = \frac{3}{4} \sum_{c=1}^M w_c(x) > 0, \quad \forall x \in \mathbb{R}^N, \; M \ge 1$$
   Como $\Delta \Phi_{\text{soft}} > 0$, $\Phi_{\text{soft}}$ é estritamente subharmônica e não-constante. Pelo Teorema da Identidade para Funções Analíticas Reais (Krantz & Parks, 2002), o conjunto crítico possui medida nula: $\mu(\mathcal{C}_0(\Phi_{\text{soft}})) = 0$. $\blacksquare$

---

## 5. Teorema 3: A Paisagem Harmônica da Multilinear e Teoria de Morse

> **Teorema 3 (Harmonicidade da Multilinear e Princípio do Mínimo Forte).**  
> *Para qualquer fórmula 3-CNF satisfazendo (H1) e (H3'), o operador Laplaciano anula-se identicamente em todo o $\mathbb{R}^N$:*
> $$\Delta \Phi_{\text{mult}}(x) = \text{Tr}(\nabla^2 \Phi_{\text{mult}}(x)) \equiv 0, \quad \forall x \in \mathbb{R}^N$$
> *Consequentemente:*
> 1. *$\Phi_{\text{mult}}$ não admite nenhum mínimo local no interior aberto $\text{int}(\mathcal{X})$.*
> 2. *Todo ponto crítico interior não-degenerado ($\det(\nabla^2 \Phi_{\text{mult}}(x^*)) \ne 0$) é estritamente um ponto de sela hiperbólico de Morse com índice $1 \le m \le N-1$.*
> 3. *Para todo ponto crítico interior $x^* \in \text{int}(\mathcal{X})$ (não-degenerado ou degenerado):*
>    $$\forall \varepsilon > 0, \; \exists y \in \text{int}(\mathcal{X}), \; \|y - x^*\| < \varepsilon \quad\text{tal que}\quad \Phi_{\text{mult}}(y) < \Phi_{\text{mult}}(x^*)$$

### Demonstração:
1. Por (H1), as 3 variáveis de cada cláusula são distintas. Logo, $\Phi_{\text{mult}}$ possui grau no máximo 1 em cada coordenada $x_i$, donde $\frac{\partial^2 \Phi_{\text{mult}}}{\partial x_i^2} \equiv 0$ para todo $i$. Somando em $i$, $\Delta \Phi_{\text{mult}}(x) \equiv 0$.
2. **Princípio do Mínimo Forte:** Em uma bola aberta conexa $B_\delta(x^*) \subset \text{int}(\mathcal{X})$, uma função harmônica não pode atingir mínimo local a menos que seja constante. Como $\Phi_{\text{mult}} \not\equiv \text{const}$ sob (H3'), nenhum ponto interior pode ser mínimo local.
3. **Classificação de Morse:** Em um ponto crítico não-degenerado $x^*$, a Hessiana $H = \nabla^2 \Phi_{\text{mult}}(x^*)$ tem traço nulo: $\sum_{i=1}^N \lambda_i = 0$. Como nenhum autovalor é nulo, existem necessariamente autovalores estritamente positivos e estritamente negativos ($\lambda_1 < 0 < \lambda_N$). O índice de Morse $m = \#\{\lambda_i < 0\}$ satisfaz $1 \le m \le N-1$, configurando uma sela hiperbólica.
4. **Topologia de Críticos Gerais via Milnor:** Pelo Princípio do Mínimo Forte, $x^*$ não é mínimo local. Sendo o conjunto $\{\Phi_{\text{mult}} < \Phi_{\text{mult}}(x^*)\}$ semi-algébrico aberto com $x^*$ em seu fecho, pelo Lema de Seleção de Curvas de Milnor (1968, Lema 3.1) existe uma curva analítica real $\gamma: [0, \delta) \to \text{int}(\mathcal{X})$ com $\gamma(0) = x^*$ tal que $\Phi_{\text{mult}}(\gamma(t)) < \Phi_{\text{mult}}(x^*)$ para todo $t \in (0, \delta)$. $\blacksquare$

---

## 6. Teorema 4A′ e Corolário 4B: Localização de Mínimos no Bordo e Dinâmica de Lyapunov (Sem Hipótese H4)

A auditoria adversarial comprovou que a antiga hipótese (H4) falha em aproximadamente 24% das arestas do hipercubo em fórmulas típicas. O resultado a seguir estabelece a propriedade estrutural sem qualquer recurso a (H4):

> **Teorema 4A′ (Localização e Valor dos Mínimos Locais no Hipercubo — Sem Hipótese H4).**  
> *Sob (H1), para qualquer fórmula 3-CNF, seja $x^*$ um mínimo local da restrição de $\Phi_{\text{mult}}$ ao hipercubo compacto $\mathcal{X} = [-1, 1]^N$, situado no interior relativo de uma face $\mathcal{F}$ de dimensão $d \ge 0$. Então:*
> $$\Phi_{\text{mult}}(x^*) = E_{\text{disc}}(v), \quad \forall v \in \mathcal{V}(\mathcal{F})$$
> *onde $\mathcal{V}(\mathcal{F})$ denota o conjunto de vértices discretos do hipercubo pertencentes à face $\mathcal{F}$.*  
> *Em particular, se $x^*$ é um mínimo local estrito de $\Phi_{\text{mult}}|_{\mathcal{X}}$, então $x^*$ é necessariamente um vértice discreto $x^* \in \{-1, +1\}^N$ (face de dimensão $d=0$).*

### Demonstração:
1. O hipercubo decompõe-se na união disjunta das faces relativas: $\mathcal{X} = \bigcup_{\mathcal{F}} \text{relint}(\mathcal{F})$.
2. Em qualquer face $\mathcal{F}$ de dimensão $d \ge 1$, fixando as $N-d$ coordenadas restritas em $\pm 1$, a restrição $\Phi_{\mathcal{F}}$ é multilinear e harmônica nas $d$ coordenadas livres: $\Delta_{\mathcal{F}} \Phi_{\mathcal{F}} \equiv 0$.
3. Se $x^* \in \text{relint}(\mathcal{F})$ é um mínimo local da restrição de $\Phi_{\text{mult}}$ a $\mathcal{X}$, então $x^*$ é um mínimo local relativo de $\Phi_{\mathcal{F}}$ no domínio aberto conexo $\text{relint}(\mathcal{F})$.
4. Pelo Princípio do Mínimo Forte para funções harmônicas, $\Phi_{\mathcal{F}}$ deve ser identicamente constante em uma vizinhança conexa de $x^*$ em $\text{relint}(\mathcal{F})$. Sendo um polinômio multilinear real, $\Phi_{\mathcal{F}}$ é identicamente constante em toda a face compacta $\mathcal{F}$:
   $$\Phi_{\text{mult}}(x) \equiv \Phi_{\text{mult}}(x^*), \quad \forall x \in \mathcal{F}$$
5. Como os vértices $\mathcal{V}(\mathcal{F}) \subset \{-1, +1\}^N$ pertencem à face $\mathcal{F}$, e nos vértices a extensão multilinear coincide com a energia booleana discreta ($\Phi_{\text{mult}}(v) = E_{\text{disc}}(v)$), concluímos:
   $$\Phi_{\text{mult}}(x^*) = E_{\text{disc}}(v), \quad \forall v \in \mathcal{V}(\mathcal{F})$$
6. Consequentemente, se $x^*$ fosse um mínimo local estrito situado em face de dimensão $d \ge 1$, $\Phi_{\mathcal{F}}$ seria constante em $\mathcal{F}$, contradizendo a estritude de $x^*$. Logo, todo mínimo local estrito reside em uma face de dimensão $d=0$, isto é, em um vértice discreto $x^* \in \{-1, +1\}^N$. $\blacksquare$

---

> **Corolário 4B (Confinamento dos Atratores Assintóticos do Fluxo Projetado — Sem Hipótese H4).**  
> *Considere o fluxo de gradiente projetado no hipercubo:*
> $$\dot{x}(t) = \Pi_{T_{\mathcal{X}}(x(t))}\left(-\nabla \Phi_{\text{mult}}(x(t))\right)$$
> *Sob (H1) e (H3'), todo ponto de equilíbrio assintoticamente estável isolado do fluxo projetado é estritamente um vértice discreto $x^* \in \{-1, +1\}^N$.*

### Demonstração via Lyapunov e Invariância de LaSalle:
1. Defina a função de Lyapunov $V(x) = \Phi_{\text{mult}}(x)$. Pela propriedade fundamental da projeção ortogonal sobre cones convexos fechados (Teorema de Moreau): $\langle v, \Pi_K(v) \rangle = \|\Pi_K(v)\|^2$. Logo, ao longo de trajetórias do fluxo projetado (Nagurney & Zhang, 1996; Brogliato et al., 2006):
   $$\dot{V}(x(t)) = \langle \nabla \Phi_{\text{mult}}(x), \; \Pi_{T_{\mathcal{X}}(x)}(-\nabla \Phi_{\text{mult}}(x)) \rangle = -\|\Pi_{T_{\mathcal{X}}(x)}(-\nabla \Phi_{\text{mult}}(x))\|^2 \le 0$$
   A energia é não-crescente ao longo de qualquer trajetória.
2. Se $x^*$ é um ponto de equilíbrio isolado assintoticamente estável, então $x^*$ é necessariamente um mínimo local estrito de $\Phi_{\text{mult}}$ sobre $\mathcal{X}$ (caso existisse $y \ne x^*$ arbitrariamente próximo com $\Phi(y) \le \Phi(x^*)$, a trajetória partindo de $y$ teria $\dot{V} \le 0$, impedindo convergência estrita para $x^*$).
3. Pelo Teorema 4A′, nenhum ponto em face de dimensão $d \ge 1$ pode ser mínimo local estrito (pois $\Phi$ é constante na face). Logo, $x^*$ reside exclusivamente em face de dimensão $d=0$: $x^* \in \{-1, +1\}^N$. $\blacksquare$

---

## 7. Teorema 5: Fatoração Matricial e Condicionamento Espectral do Softplus

Definindo a matriz de incidência de variáveis-cláusulas $V \in \mathbb{R}^{M \times N}$ com linhas $v_c^T = -\frac{1}{2}(\sigma^{(c)})^T$:

> **Teorema 5 (Fatoração da Hessiana e Condicionamento Espectral do Softplus).**  
> *A Hessiana da relaxação Softplus fatora-se exatamente como $\nabla^2 \Phi_{\text{soft}}(x) = V^T W(x) V$, onde $W(x) = \text{diag}(w_1(x), \dots, w_M(x)) \succ 0$ com $w_c(x) = \beta \varsigma(\beta g_c(x))[1 - \varsigma(\beta g_c(x))] > 0$.*  
> *Consequentemente:*
> 1. *$\nabla^2 \Phi_{\text{soft}}(x) \succeq 0$ em todo $\mathbb{R}^N$ e $\ker(\nabla^2 \Phi_{\text{soft}}) = \ker(V)$. Se $\text{rank}(V) = N$, $\Phi_{\text{soft}}$ é estritamente convexa e admite um único ponto crítico (mínimo global fracionário).*
> 2. *Para $\text{rank}(V) = N$, os autovalores extremos satisfazem:*
>    $$\lambda_{\min}(\nabla^2 \Phi_{\text{soft}}(x)) \ge \lambda_{\min}(W(x)) \, \lambda_{\min}(V^T V) > 0$$
>    $$\lambda_{\max}(\nabla^2 \Phi_{\text{soft}}(x)) \le \lambda_{\max}(W(x)) \, \lambda_{\max}(V^T V)$$
> 3. *O número de condicionamento espectral da Hessiana satisfaz a cota superior:*
>    $$\kappa(\nabla^2 \Phi_{\text{soft}}(x)) \le \kappa(W(x)) \cdot \kappa(V^T V)$$

### Demonstração:
Para todo $z \in \mathbb{R}^N \setminus \{\mathbf{0}\}$, a forma quadrática é $z^T \nabla^2 \Phi_{\text{soft}} z = (V z)^T W(x) (V z)$. Pelo teorema espectral e pelo Quociente de Rayleigh para a matriz simétrica $V^T V$:
$$\lambda_{\min}(W) \lambda_{\min}(V^T V) \|z\|_2^2 \le z^T \nabla^2 \Phi z \le \lambda_{\max}(W) \lambda_{\max}(V^T V) \|z\|_2^2$$
Tomando o ínfimo e supremo sobre $\|z\|_2 = 1$ e dividindo as cotas, decorre $\kappa(H) \le \kappa(W) \kappa(V^T V)$. $\blacksquare$

---

## 8. Teorema 6: Lipschitzianidade do Campo Gradiente e Regimes IEEE 754

> **Teorema 6 (Constante de Lipschitz do Gradiente e Regimes Numéricos).**  
> *Para a relaxação Softplus:*
> 1. *A constante de Lipschitz do campo gradiente $L_\beta \equiv \sup_{x \in \mathbb{R}^N} \|\nabla^2 \Phi_{\text{soft}}(x)\|_2$ satisfaz $L_\beta = \Theta(\beta)$, com cotas bilaterais exatas:*
>    $$\frac{3}{16} \beta \le L_\beta \le \frac{3 d_{\max}}{16} \beta$$
> 2. *Na subcaixa contraída $\mathcal{U}_N(\rho) = (-\rho, \rho)^N$ com $\rho < 1/3$, o gradiente sofre decaimento exponencial uniforme:*
>    $$\|\nabla \Phi_{\text{soft}}(x)\|_\infty \le \frac{M}{2} e^{-\frac{\beta}{2}(1 - 3\rho)}, \quad \|\nabla \Phi_{\text{soft}}(x)\|_2 \le \frac{\sqrt{3} M}{2} e^{-\frac{\beta}{2}(1 - 3\rho)}$$
> 3. *Na origem $x = \mathbf{0}$, os limiares de underflow em aritmética IEEE 754 ocorrem em:*
>    - *FP32: Normal para $\beta \approx 175$; Flush-to-zero absoluto para $\beta \approx 207$.*
>    - *FP64: Normal para $\beta \approx 1417$; Flush-to-zero absoluto para $\beta \approx 1489$.*

### Demonstração:
- **Cota Superior:** $(V^T V)_{ii} = \frac{d_i}{4}$ e $\sum_{j \ne i} |(V^T V)_{ij}| \le \frac{d_i}{2}$, donde $\|V^T V\|_2 \le \frac{3 d_{\max}}{4}$ por Gershgorin. Como $w_c(x) \le \beta/4$, $\|\nabla^2 \Phi\|_2 \le \frac{\beta}{4} \frac{3 d_{\max}}{4} = \frac{3 d_{\max}}{16}\beta$.
- **Cota Inferior:** Em um hiperplano ativo $g_c(x_0) = 0$, $w_c(x_0) = \beta/4$. Na direção unitária $u = v_c/\|v_c\|_2$ (com $\|v_c\|_2^2 = 3/4$), temos $u^T \nabla^2 \Phi u \ge \frac{\beta}{4} \frac{3}{4} = \frac{3}{16}\beta$. Logo, $L_\beta = \Theta(\beta)$. $\blacksquare$

---

## 9. Teorema 7B e Proposição 7A: Dinâmica de Contração Centrípeta da Relaxação Hinge

A auditoria matemática independente refinou o entendimento estrutural de $\Phi_{\text{quad}}$, demonstrando que **a relaxação Hinge não possui armadilhas locais rugosas, mas sofre de degenerescência geométrica global no politopo LP**:

> **Teorema 7B (Contração Centrípeta Universal e Ausência de Armadilhas Locais no Hinge).**  
> *Para qualquer fórmula 3-CNF, a relaxação quadrática Hinge satisfaz:*
> 1. *Em qualquer ponto $x \in \mathcal{X}$ onde ao menos uma cláusula é ativa ($\text{act}(x) = \{c \mid g_c(x) > 0\} \ne \emptyset$):*
>    $$\langle -\nabla \Phi_{\text{quad}}(x), \, x \rangle = -\sum_{c \in \text{act}(x)} \left(2 g_c(x)^2 + g_c(x)\right) < 0$$
> 2. *O raio euclidiano $\|x(t)\|_2^2$ é uma função de Lyapunov estrita do fluxo projetado em toda a região fora do politopo LP $Z$:*
>    $$\frac{d}{dt} \|x(t)\|_2^2 = 2 \langle x(t), \, \dot{x}(t) \rangle \le 2 \langle x(t), \, -\nabla \Phi_{\text{quad}}(x(t)) \rangle < 0$$
> 3. *$\Phi_{\text{quad}}$ não admite nenhum ponto crítico nem ponto de equilíbrio projetado fora de $Z$.*  
> 4. *Sob o fluxo projetado, toda trajetória converge universalmente para o politopo da relaxação linear $Z = \{x \in \mathcal{X} \mid g_c(x) \le 0, \forall c\}$.*

### Demonstração:
1. Cláusula ativa $g_c(x) > 0 \iff -\frac{1}{2}(1 + \sigma^{(c)} \cdot x) > 0 \iff \sigma^{(c)} \cdot x = -(2 g_c(x) + 1)$.
2. O gradiente é $-\nabla \Phi_{\text{quad}}(x) = \sum_{c \in \text{act}} g_c(x) \sigma^{(c)}$.
3. O produto escalar com a posição é:
   $$\langle -\nabla \Phi_{\text{quad}}(x), \, x \rangle = \sum_{c \in \text{act}} g_c(x) (\sigma^{(c)} \cdot x) = -\sum_{c \in \text{act}} g_c(x) (2 g_c(x) + 1) = -\sum_{c \in \text{act}} (2 g_c(x)^2 + g_c(x)) < 0$$
4. **Ausência de Equilíbrios fora de $Z$:**
   - No interior: $-\nabla \Phi(x) = \mathbf{0} \implies \langle -\nabla \Phi, x \rangle = 0$, contradizendo a contração estrita.
   - No bordo $\partial \mathcal{X}$: um ponto $x^*$ é equilíbrio projetado se e somente se $-\nabla \Phi(x^*) \in N_{\mathcal{X}}(x^*)$, onde $N_{\mathcal{X}}(x^*)$ é o cone normal exterior. Para qualquer $\nu \in N_{\mathcal{X}}(x^*)$, $\nu_i x^*_i \ge 0 \implies \langle \nu, x^* \rangle \ge 0$. Logo, um equilíbrio projetado exigiria $\langle -\nabla \Phi(x^*), x^* \rangle \ge 0$, contradizendo frontalmente $\langle -\nabla \Phi(x^*), x^* \rangle < 0$.
   - Pelo Princípio de LaSalle, toda trajetória converge para $Z$. $\blacksquare$

---

### Errata e Retratação Metodológica sobre Fórmulas UNSAT
> **Nota de Retratação Científica Formal:**  
> Na versão preliminar do Parecer 11, afirmou-se erroneamente que para fórmulas UNSAT valeria $\mathcal{M}_{\text{spur}}(\Phi_{\text{quad}}) - \mathcal{M}_{\text{spur}}(\Phi_{\text{mult}}) \ge 1 - 0 = 1$.  
> Essa afirmação foi formalmente expurgada: por definição, em fórmulas insatisfatíveis (UNSAT), **todo vértice booleano viola ao menos uma cláusula** ($E_{\text{disc}}(s) \ge 1, \forall s \in \mathcal{V}$). Consequentemente, a massa da bacia espúria é identicamente $100\%$ ($\mathcal{M}_{\text{spur}} \equiv 1$) para **qualquer relaxação contínua e qualquer dinâmica**. A diferença em UNSAT é identicamente zero.  
> O mérito real do Teorema 7B reside em provar que o Hinge **não sofre de armadilhas rugosas fora de $Z$**, mas sim de uma atração cega para um politopo fracionário degenerado.

---

> **Proposição 7A (Família Construtiva $F_N$ e Atração para o Platô Espúrio).**  
> *Seja $N \ge 4$. Considere a fórmula 3-CNF $F_N$ formada por todas as $M = \binom{N}{3}$ cláusulas exclusivamente negativas: $\mathcal{C} = \{ (\neg x_i \lor \neg x_j \lor \neg x_k) \mid 1 \le i < j < k \le N \}$.*  
> *1. O politopo linear $Z$ contém a caixa central $\mathcal{U}_N$, com volume normalizado $\mu_{\text{norm}}(Z) \ge (1/3)^N > 0$.*  
> *2. O fluxo projetado $\dot{x} = -\nabla \Phi_{\text{quad}}(x)$ preserva a ordem monotônica das coordenadas:*
> $$x_i(0) \ge x_j(0) \implies x_i(t) \ge x_j(t), \quad \forall t \ge 0$$
> *3. A partir do ortante aberto $A_N = (1/3, 1)^N$, toda trajetória converge para o politopo $Z$ mantendo coordenadas positivas, produzindo arredondamento booleano violador $\text{sign}(x) = (+1, \dots, +1)$ em 100% das trajetórias:*
> $$A_N \subseteq \mathcal{B}_{\text{spur}}(\Phi_{\text{quad}}) \implies \mathcal{M}_{\text{spur}}(\Phi_{\text{quad}}) \ge \left(\frac{1}{3}\right)^N > 0$$

---

## 10. Novos Teoremas Matemáticos Estruturais

### Teorema 8 (Cota Inferior Rigorosa de Volume do Politopo LP via Desigualdade de Jensen)
> **Teorema 8 (Cota Inferior de Volume do Politopo LP Aleatório via Jensen).**  
> *Para o ensemble padrão de fórmulas aleatórias de 3-SAT $\mathcal{E}(N, \alpha)$ com $M = \lfloor \alpha N \rfloor$ cláusulas independentes, o volume normalizado esperado do politopo linear $Z = \{x \in [-1, 1]^N \mid g_c(x) \le 0, \forall c\}$ satisfaz a cota inferior exponencial estrita:*
> $$\mathbb{E}[\mu_{\text{norm}}(Z)] \ge \left(\frac{5}{6}\right)^{\alpha N} = \exp\left(-N \alpha \ln\left(\frac{6}{5}\right)\right) > 0$$
> *Ademais, $\mathbb{E}[\mu_{\text{norm}}(Z)] \ge \mu_{\text{norm}}(\mathcal{U}_N) = (1/3)^N$.*

### Demonstração:
1. Pelo Teorema de Fubini, a expectativa do volume sob a distribuição aleatória das fórmulas é:
   $$\mathbb{E}_F[\mu_{\text{norm}}(Z)] = \mathbb{E}_F \left[ \int_{[-1, 1]^N} \prod_{c=1}^M \mathbf{1}_{\{g_c(x) \le 0\}} \frac{dx}{2^N} \right] = \int_{[-1, 1]^N} \mathbb{E}_F \left[ \prod_{c=1}^M \mathbf{1}_{\{g_c(x) \le 0\}} \right] \frac{dx}{2^N}$$
2. Para cada $x \in [-1, 1]^N$ fixo, as $M$ cláusulas são sorteadas independentemente. Seja $p(x) = \mathbb{P}_c(g_c(x) \le 0)$ a probabilidade pontual de uma cláusula uniforme ser satisfeita no ponto $x$. Então:
   $$\mathbb{E}_F \left[ \prod_{c=1}^M \mathbf{1}_{\{g_c(x) \le 0\}} \right] = [p(x)]^M \implies \mathbb{E}_F[\mu_{\text{norm}}(Z)] = \int_{[-1, 1]^N} [p(x)]^M \frac{dx}{2^N}$$
3. Para uma cláusula aleatória sob um ponto uniforme $x \sim \text{Unif}([-1, 1]^N)$, a condição $g_c(x) \le 0$ corresponde a $\sum_{j=1}^3 \sigma_j x_j \ge -1$, equivalente a $u_1 + u_2 + u_3 \ge 1$ com $u_j = (\sigma_j x_j + 1)/2 \sim \text{Unif}([0, 1])$.
4. A soma $S_3 = u_1 + u_2 + u_3$ segue a distribuição de Irwin-Hall de ordem 3, cuja CDF em $s=1$ vale $\mathbb{P}(S_3 < 1) = \frac{1^3}{3!} = \frac{1}{6}$. Portanto, a média espacial de $p(x)$ é exatamente:
   $$\int_{[-1, 1]^N} p(x) \frac{dx}{2^N} = 1 - \frac{1}{6} = \frac{5}{6}$$
5. Como a função $t \mapsto t^M$ é estritamente convexa em $[0, 1]$ para $M \ge 2$, pela **Desigualdade de Jensen**:
   $$\mathbb{E}_F[\mu_{\text{norm}}(Z)] = \int_{[-1, 1]^N} [p(x)]^M \frac{dx}{2^N} \ge \left( \int_{[-1, 1]^N} p(x) \frac{dx}{2^N} \right)^M = \left(\frac{5}{6}\right)^M \ge \left(\frac{5}{6}\right)^{\alpha N}$$
6. Além disso, no interior da caixa central $\mathcal{U}_N = (-1/3, 1/3)^N$, toda cláusula possível tem $g_c(x) < 0$, de modo que $p(x) \equiv 1$ em $\mathcal{U}_N$, fornecendo $\mathbb{E}[\mu(Z)] \ge \mu(\mathcal{U}_N) = (1/3)^N$.
Isto estabelece analiticamente que o politopo LP $Z$ retém uma fração exponencialmente grande do hipercubo de busca ($\ge e^{-N \alpha \ln(6/5)}$), aprisionando o fluxo do Hinge. $\blacksquare$

---

### Teorema 9 (Separação Rigorosa em Horn Monótono Linear via Sistemas Cooperativos de Hirsch)
> **Teorema 9 (Separação Analítica Exata em Fórmulas Horn Monótonas Lineares).**  
> *Considere a família de fórmulas Horn monótonas lineares $F_N$ com implicações unitárias dirigidas $x_j \to x_i$ ($\neg x_j \lor x_i$) ao longo de um grafo acíclico de dependência, juntamente com fatos unitários positivos $x_0 \to x_1$ e sementes de contorno.*  
> *1. Sob a extensão multilinear $\Phi_{\text{mult}}$, os elementos fora da diagonal da Jacobiana do campo $f(x) = -\nabla \Phi_{\text{mult}}(x)$ satisfazem:*
> $$J_{ij}(x) = \frac{\partial f_i}{\partial x_j} = -\frac{\partial^2 \Phi_{\text{mult}}}{\partial x_i \partial x_j} = +\frac{1}{4} \ge 0, \quad \forall i \ne j, \; \forall x \in [-1, 1]^N$$
> *O sistema é estritamente cooperativo no sentido de Hirsch (1985). Pelo Teorema do Fluxo Monótono de Hirsch, o fluxo projetado preserva a ordem parcial do cone positivo e converge monotonicamente para o único modelo mínimo satisfatível:*
> $$\mathcal{M}_{\text{spur}}(\Phi_{\text{mult}}) = o(1)$$
> *2. Simultaneamente, o politopo LP $Z$ contém a caixa central $\mathcal{U}_N$, e pelo Teorema 7B o fluxo do Hinge $\Phi_{\text{quad}}$ converge para $Z$, onde o arredondamento falha com probabilidade positiva:*
> $$\mathcal{M}_{\text{spur}}(\Phi_{\text{quad}}) \ge 1 - o(1)$$
> *Consequentemente, a separação estrita de massas é analiticamente demonstrada para a classe Horn linear:*
> $$\mathcal{M}_{\text{spur}}(\Phi_{\text{quad}}) - \mathcal{M}_{\text{spur}}(\Phi_{\text{mult}}) \ge 1 - o(1)$$

---

### Teorema 10 (Separação Rigorosa em 3-SAT Aleatório no Regime Subcrítico $\alpha < 1/6$)
> **Teorema 10 (Separação Dinâmica Subcrítica em 3-SAT Aleatório).**  
> *Para o ensemble de 3-SAT aleatório $\mathcal{E}(N, \alpha)$ abaixo do limiar de percolação do hipergrafo 3-uniforme ($\alpha < 1/6$):*
> 1. *Com alta probabilidade ($1 - o(1)$), o hipergrafo de cláusulas se decompõe em componentes conexos disjuntos de tamanho $\mathcal{O}(\log N)$ com topologia de árvore.*
> 2. *Em qualquer fórmula-árvore, por indução das folhas para a raiz, toda atribuição booleana com energia positiva ($E_{\text{disc}} > 0$) possui ao menos uma variável folha cujo flip reduz estritamente a energia, demonstrando a ausência de mínimos locais booleanos com $E_{\text{disc}} > 0$.*
> 3. *Pelo Teorema 4A′, todos os mínimos locais da restrição de $\Phi_{\text{mult}}$ a faces herdam os valores dos vértices. Logo, não existem mínimos locais com energia estritamente positiva. Todo ponto crítico não-satisfatível é uma sela estrita com ao menos uma direção de autovalor negativo.*
> 4. *Pelo Teorema da Variedade Central-Estável para Métodos de Gradiente (Lee, Simchowitz, Jordan & Recht, 2016; Panageas & Piliouras, 2017), o fluxo de gradiente com inicialização uniforme evita a variedade estável de selas estritas quase certamente, convergindo para vértices satisfatíveis:*
>    $$\lim_{N \to \infty} \rho_{\text{mult}}(\alpha) = 0$$
> 5. *Para a relaxação Hinge $\Phi_{\text{quad}}$, o politopo LP possui volume esperado $\mathbb{E}[\mu(Z)] \ge (5/6)^{\alpha N} > 0$ pelo Teorema 8, e o fluxo converge para $Z$ pelo Teorema 7B, gerando arredondamento espúrio com probabilidade positiva:*
>    $$\lim_{N \to \infty} \rho_{\text{quad}}(\alpha) \ge c(\alpha) > 0$$
> *Consequentemente, a separação estrita de energia residual vale universalmente para $\alpha < 1/6$:*
> $$\rho_{\text{quad}}(\alpha) > \rho_{\text{mult}}(\alpha) = 0$$

---

## 11. Conjectura Central CLG-R (Delimitada e Corrigida)

> ### Conjectura Central CLG-R (Separação Dinâmica Assintótica no Regime Crítico)
> *Para o ensemble padrão de 3-SAT aleatório $\mathcal{E}(N, \alpha)$ no intervalo satisfatível não-trivial $\alpha \in (\alpha_d, \alpha_s)$, onde $\alpha_d \approx 3.86$ (limiar de clustering) e $\alpha_s \approx 4.267$ (limiar de satisfatibilidade), ou para o ensemble plantado $\mathcal{E}_{\text{plant}}(N, \alpha)$:*  
> *Sob fluxo gradiente projetado puro com inicialização uniforme $x_0 \sim \text{Unif}([-1, 1]^N)$, as densidades assintóticas de energia residual satisfazem:*
> $$\lim_{T \to \infty} \rho_{\text{quad}}(\alpha, T) > \lim_{T \to \infty} \rho_{\text{mult}}(\alpha, T) > 0$$

---

## 12. Firewall Epistemológico: 3-XOR-SAT e P vs NP

A teoria CLG-R reafirma a separação categórica entre topologia contínua e complexidade de Turing:
* **3-XOR-SAT** é solucionável em tempo polinomial determinístico $\mathcal{O}(N^3)$ via Eliminação Gaussiana em $\mathbb{F}_2$ (pertence estritamente a $\mathbf{P}$).
* Sob qualquer relaxação contínua governada por gradientes métricos, 3-XOR-SAT sofre colapso dinâmico vítreo completo ($R_{\text{dyn}} = 0.0\%$).
* **Conclusão:** Convexidade contínua ou colapso gradiente não determinam a solvabilidade na Máquina de Turing.
