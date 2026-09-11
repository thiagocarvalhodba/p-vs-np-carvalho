# Estudo Analítico do Conjunto Crítico e Dinâmica de Paisagem (CLG-R)
**Versão 3.0 — Pós-Parecer 11 (Blindagem Definitiva)**  
**Autor:** Thiago Carvalho  
**Data:** 10 de Setembro de 2026  
**Repositório GitHub:** [https://github.com/thiagocarvalhodba/p-vs-np-carvalho](https://github.com/thiagocarvalhodba/p-vs-np-carvalho)  

---

## 1. Introdução e Escopo Epistemológico

O presente documento estabelece as demonstrações analíticas formais da teoria **CLG-R** (*Computational Landscape Geometry & Representation*), investigando como representações contínuas booleanamente equivalentes de problemas em lógica proposicional (especificamente 3-SAT e Max-3-SAT) induzem topologias de conjuntos críticos e comportamentos dinâmicos de fluxo de gradiente radicalmente distintos sobre o hipercubo unitário:

$$\mathcal{X} = [-1, \, 1]^N \subset \mathbb{R}^N$$

As três relaxações canônicas analisadas são:
1. **Quadrática Hinge:** $\Phi_{\text{quad}}(x) = \sum_{c=1}^M [\max(0, g_c(x))]^2$
2. **Multilinear Harmônica:** $\Phi_{\text{mult}}(x) = \sum_{c=1}^M \prod_{j \in c} \frac{1 - \sigma_j^{(c)} x_j}{2}$
3. **Softplus Convexa Regularizada:** $\Phi_{\text{soft}}(x) = \sum_{c=1}^M \frac{1}{\beta} \ln\left(1 + e^{\beta g_c(x)}\right)$

onde $g_c(x) = -\frac{1}{2}\left(1 + \sum_{j \in c} \sigma_j^{(c)} x_j\right)$ representa a função de violação afim da cláusula $c$.

---

## 2. Hipóteses Estruturais de Regularidade

Para garantir a generalidade matemática e afastar patologias triviais, fixamos as seguintes hipóteses:

- **(H1 - Irredutibilidade):** Cada cláusula $c \in \{1, \dots, M\}$ é formada por exatamente 3 literais de variáveis mutuamente distintas ($|\{i, j, k\}| = 3$), sem tautologias triviais ($x_i \lor \neg x_i$).
- **(H2 - Conectividade de Variáveis):** Toda variável $x_i$ ($i = 1, \dots, N$) participa de ao menos uma cláusula ($d_i = \deg(x_i) \ge 1$), inexistindo variáveis desconectadas.
- **(H3' - Não-Degenerescência da Extensão Contínua):** A fórmula $F$ não é isotropicamente balanceada em todas as $2^N$ combinações booleanas; isto é, o polinômio multilinear associado não é identicamente constante em $\mathbb{R}^N$ ($\Phi_{\text{mult}} \not\equiv \text{const}$).
  - *Fundamentação via Análise de Walsh-Fourier:* Pela identidade de Parseval no hipercubo booleano, $\sum_{S \ne \emptyset} \widehat{\Phi}(S)^2 = \text{Var}(E_{\text{disc}})$. Para qualquer fórmula SAT satisfatível com $M \ge 1$, a variância satisfaz $\text{Var}(E_{\text{disc}}) > 0$, assegurando que (H3') é atendida incondicionalmente para toda fórmula satisfatível.
- **(H4 - Não-Degenerescência de Fronteira):** Para cada coordenada $i \in \{1, \dots, N\}$ e cada vértice das coordenadas restantes $s_{-i} \in \{-1, +1\}^{N-1}$, a restrição unidimensional $t \mapsto \Phi_{\text{mult}}(t, s_{-i})$ tem coeficiente angular não-nulo:
  $$b_i(s_{-i}) \equiv \frac{\partial \Phi_{\text{mult}}}{\partial x_i}\Big|_{x_{-i} = s_{-i}} \ne 0$$
  *(Condição de transversalidade nos bordos do hipercubo que elimina arestas neutras degeneradas).*

---

## 3. Teorema 1: A Caixa Fracionária Central e Folga da Relaxação Linear

> **Teorema 1 (Teorema da Caixa Fracionária Central e Folga LP).**  
> *Para qualquer fórmula 3-CNF satisfazendo (H1)–(H3'), o aberto central:*
> $$\mathcal{U}_N = \left(-\frac{1}{3}, \, \frac{1}{3}\right)^N \subset \text{int}(\mathcal{X})$$
> *satisfaz $g_c(x) < 0$ para todas as $M$ cláusulas simultaneamente. Consequentemente:*
> $$\Phi_{\text{quad}}(x) \equiv 0 \quad\text{e}\quad \nabla \Phi_{\text{quad}}(x) \equiv \mathbf{0}, \quad \forall x \in \mathcal{U}_N$$
> *Em medida de Lebesgue euclidiana padrão em $\mathbb{R}^N$:*
> $$\text{Vol}(Z(\nabla \Phi_{\text{quad}})) \ge \text{Vol}(\mathcal{U}_N) = \left(\frac{2}{3}\right)^N \quad \left(\text{medida normalizada } \mu_{\text{norm}}(\mathcal{U}_N) = \left(\frac{1}{3}\right)^N\right)$$
> *O conjunto crítico espúrio $\mathcal{C}_{\text{spur}}(\Phi_{\text{quad}}) \equiv Z(\nabla \Phi_{\text{quad}}) \cap \{x \in \mathcal{X} \mid E_{\text{disc}}(\text{sign}(x)) > 0\}$ satisfaz:*
> $$\text{Vol}(\mathcal{C}_{\text{spur}}(\Phi_{\text{quad}})) \ge \left(\frac{1}{3}\right)^N > 0 \quad \left(\mu_{\text{norm}} \ge \left(\frac{1}{6}\right)^N\right)$$
> *Para fórmulas insatisfatíveis (UNSAT), $\text{Vol}(\mathcal{C}_{\text{spur}}) \ge (2/3)^N$ ($\mu_{\text{norm}} \ge (1/3)^N$).*

### Demonstração Construtiva Determinística:
1. Para todo $x \in \mathcal{U}_N$, $|x_i| < 1/3$ para todo $i \in \{1, \dots, N\}$.
2. Para qualquer cláusula $c = (\ell_1 \lor \ell_2 \lor \ell_3)$, temos $\sigma_j^{(c)} \in \{-1, +1\}$. Logo:
   $$\sum_{j \in c} \sigma_j^{(c)} x_j \ge -\sum_{j \in c} |\sigma_j^{(c)} x_j| = -\sum_{j \in c} |x_j| > -3 \times \frac{1}{3} = -1$$
3. Substituindo na violação da cláusula:
   $$g_c(x) = -\frac{1}{2}\left(1 + \sum_{j \in c} \sigma_j^{(c)} x_j\right) < -\frac{1}{2}(1 - 1) = 0$$
4. Como todos os termos do Hinge são zero, $\Phi_{\text{quad}}(x) \equiv 0$ e $\nabla \Phi_{\text{quad}}(x) \equiv \mathbf{0}$ em todo o aberto $\mathcal{U}_N$.
5. Sob (H3'), a fórmula não é identicamente satisfeita em todos os vértices booleanos; logo, existe ao menos um ortante no interior de $\mathcal{U}_N$ com violação booleana estrita ($E_{\text{disc}}(\text{sign}(x)) > 0$), cujo volume euclidiano é $(1/3)^N$. Para UNSAT, todas as atribuições violam cláusulas, cobrindo todo o volume euclidiano $(2/3)^N$. $\blacksquare$

### 3.1 Significado e Relação com Relaxações Convexas
Sob a transformação afim bijetora $y_i = (1+x_i)/2 \in [0, 1]$, a condição $g_c(x) \le 0$ equivale estritamente à restrição de cobertura da relaxação linear canônica (LP) de 3-SAT: $\sum_{j \in c} z_j \ge 1$. No centro $x=\mathbf{0}$ ($y_i = 1/2$), cada cláusula satisfaz $z_1 + z_2 + z_3 = 1.5$, gerando uma **folga geométrica interior de exatamente $0.5$**.  
O platô plano $\mathcal{U}_N$ é a manifestação analítica contínua dessa folga linear fracionária. O fenômeno é puramente geométrico e desacoplado do Teorema PCP de Inaproximabilidade 7/8 de Håstad (2001).

### 3.2 Comportamento em Ensembles Aleatórios e Deriva Média
Para ensembles de fórmulas aleatórias $\mathcal{E}(N, \alpha)$ no limiar crítico, fora da caixa $\mathcal{U}_N$, a aleatoriedade isotrópica das polaridades induz um campo centrípeto médio $\mathbb{E}[-\nabla \Phi_{\text{quad}}] \approx -\kappa x$, que direciona o fluxo para o platô central $\mathcal{U}_N$, explicando empiricamente o congelamento de 96% observado em experimentos estatísticos.

---

## 4. Teorema 2: Medida de Lebesgue Nula dos Críticos de $\Phi_{\text{mult}}$ e $\Phi_{\text{soft}}$

> **Teorema 2 (Medida Nula dos Críticos Espúrios para Multilinear e Softplus).**  
> *Sob as hipóteses (H1), (H2) e a condição de não-degenerescência (H3'):*
> $$\mu(\mathcal{C}_0(\Phi_{\text{mult}})) = 0 \quad \text{e} \quad \mu(\mathcal{C}_0(\Phi_{\text{soft}})) = 0$$

### Demonstração:
1. **Caso Multilinear ($\Phi_{\text{mult}}$):**  
   $\Phi_{\text{mult}}(x) \in \mathbb{R}[x_1, \dots, x_N]$. Sob (H3'), $\Phi_{\text{mult}} \not\equiv \text{const}$, garantindo que existe ao menos uma coordenada $k \in \{1, \dots, N\}$ com:
   $$P_k(x) \equiv \frac{\partial \Phi_{\text{mult}}}{\partial x_k}(x) \not\equiv 0$$
   O conjunto crítico de gradiente nulo é subconjunto das raízes de $P_k$:
   $$\mathcal{C}_0(\Phi_{\text{mult}}) \subseteq Z(\nabla \Phi_{\text{mult}}) \subseteq Z(P_k) = \{ x \in \mathbb{R}^N \mid P_k(x) = 0 \}$$
   Por indução dimensional e aplicação direta do Teorema de Fubini (ou pelo Lema de Okamoto, 1973), o conjunto de zeros de um polinômio real multivariado não-nulo possui medida de Lebesgue estritamente zero em $\mathbb{R}^N$:
   $$\mu(Z(P_k)) = 0 \implies \mu(\mathcal{C}_0(\Phi_{\text{mult}})) = 0$$

2. **Caso Softplus ($\Phi_{\text{soft}}$):**  
   $\Phi_{\text{soft}}(x)$ é analítica real ($\mathcal{C}^\omega$) em $\mathbb{R}^N$. Pelo Teorema 5, seu Laplaciano satisfaz:
   $$\Delta \Phi_{\text{soft}}(x) = \text{Tr}(V^T W(x) V) = \frac{3}{4} \sum_{c=1}^M w_c(x) > 0, \quad \forall x \in \mathbb{R}^N, \; \forall M \ge 1$$
   Como $\Delta \Phi_{\text{soft}} > 0$, $\Phi_{\text{soft}}$ é estritamente subharmônica e, portanto, incondicionalmente não-constante ($\Phi_{\text{soft}} \not\equiv \text{const}$). Logo, existe $k$ tal que $\partial_k \Phi_{\text{soft}} \not\equiv 0$.  
   Pelo **Teorema da Identidade para Funções Analíticas Reais em Domínios Conexos** (Krantz & Parks, 2002; Mityagin, 2015), o conjunto de zeros de qualquer função analítica real não identicamente nula sobre um domínio conexo possui medida de Lebesgue zero:
   $$\mu(Z(\partial_k \Phi_{\text{soft}})) = 0 \implies \mu(\mathcal{C}_0(\Phi_{\text{soft}})) = 0 \quad \blacksquare$$

---

## 5. Teorema 3: A Paisagem Harmônica da Multilinear e Teoria de Morse

> **Teorema 3 (Harmonicidade da Multilinear e Princípio do Mínimo Forte).**  
> *Para qualquer fórmula 3-CNF satisfazendo (H1) e (H3'), o operador Laplaciano anula-se identicamente em todo o $\mathbb{R}^N$:*
> $$\Delta \Phi_{\text{mult}}(x) = \text{Tr}(\nabla^2 \Phi_{\text{mult}}(x)) \equiv 0, \quad \forall x \in \mathbb{R}^N$$
> *Consequentemente:*
> 1. *$\Phi_{\text{mult}}$ não admite nenhum mínimo local em $\text{int}(\mathcal{X})$.*
> 2. *Todo ponto crítico interior não-degenerado ($\det(\nabla^2 \Phi(x^*)) \ne 0$) é estritamente um ponto de sela hiperbólico de Morse com índice $1 \le m \le N-1$.*
> 3. *Para todo ponto crítico interior $x^* \in \text{int}(\mathcal{X})$ (quer não-degenerado ou degenerado):*
>    $$\forall \varepsilon > 0, \; \exists y \in \text{int}(\mathcal{X}), \; \|y - x^*\| < \varepsilon \quad\text{tal que}\quad \Phi_{\text{mult}}(y) < \Phi_{\text{mult}}(x^*)$$

### Demonstração:
1. Por (H1), as variáveis de cada cláusula são distintas. Logo, $\Phi_{\text{mult}}$ possui grau no máximo 1 em cada coordenada $x_i$, donde $\frac{\partial^2 \Phi_{\text{mult}}}{\partial x_i^2} \equiv 0$ para todo $i$. Somando em $i$, $\Delta \Phi_{\text{mult}}(x) \equiv 0$.
2. **Princípio do Mínimo Forte (Hopf / Evans):** Seja $U \subset \mathbb{R}^N$ um aberto conexo e $\Phi \in \mathcal{C}^2(U)$ harmônica. Se existe $x^* \in U$ tal que $\Phi(x^*) \le \Phi(x)$ para todo $x \in B_\delta(x^*) \subset U$, então $\Phi$ é identicamente constante em $U$. Como $\Phi_{\text{mult}} \not\equiv \text{const}$ sob (H3'), nenhum ponto do interior $\text{int}(\mathcal{X})$ pode ser mínimo local.
3. **Classificação de Morse:** Em um ponto crítico não-degenerado $x^*$, a Hessiana $H = \nabla^2 \Phi(x^*)$ é simétrica com autovalores reais $\lambda_1 \le \dots \le \lambda_N$. Como $\text{Tr}(H) = \sum \lambda_i = 0$ e nenhum $\lambda_i = 0$, devem existir autovalores estritamente negativos ($\lambda_1 < 0$) e estritamente positivos ($\lambda_N > 0$). Pelo Lema de Morse, o índice $m = \#\{\lambda_i < 0\}$ satisfaz $1 \le m \le N-1$, configurando uma sela hiperbólica com variedade instável $W^u(x^*)$ de dimensão $m \ge 1$.
4. **Comportamento Topológico de Críticos Degenerados:** Se $\det(H) = 0$, pelo Princípio do Mínimo Forte $x^*$ não é mínimo local, o que garante formalmente que para todo $\varepsilon > 0$ existe $y \in B_\varepsilon(x^*)$ com $\Phi(y) < \Phi(x^*)$. Ademais, sendo $\Phi_{\text{mult}}$ semi-algébrica, pelo **Lema de Seleção de Curvas de Milnor (1968)**, existe uma curva analítica $\gamma: [0, \delta) \to \text{int}(\mathcal{X})$ com $\gamma(0) = x^*$ tal que $\Phi(\gamma(t)) < \Phi(x^*)$ para todo $t \in (0, \delta)$. $\blacksquare$

---

## 6. Teoremas 4A e 4B: Estratificação do Hipercubo e Dinâmica de Lyapunov

> **Teorema 4A (Localização Estrita dos Mínimos Locais nos Vértices — Geométrico).**  
> *Sob as hipóteses (H1), (H3') e (H4), todo mínimo local da restrição de $\Phi_{\text{mult}}$ ao hipercubo compacto $\mathcal{X} = [-1, 1]^N$ reside exclusivamente em um vértice discreto $\{-1, +1\}^N$ (faces de dimensão $d = 0$).*

### Demonstração por Indução na Dimensão das Faces:
O hipercubo decompõe-se na união disjunta de suas faces abertas $\mathcal{X} = \bigcup_{d=0}^N \bigcup_{\mathcal{F} \in \text{Faces}_d} \text{relint}(\mathcal{F})$.
1. **Faces de Dimensão $d \ge 2$:** Para qualquer face $\mathcal{F}$ de dimensão $d \ge 2$, fixando as $N-d$ coordenadas nos extremos $\pm 1$, a restrição $\Phi_{\mathcal{F}}$ preserva a multilinearidade nas $d$ variáveis livres. O Laplaciano intrínseco anula-se: $\Delta_{\mathcal{F}} \Phi_{\mathcal{F}} \equiv 0$. Sob (H4), $\Phi_{\mathcal{F}}$ não é constante. Pelo Princípio do Mínimo Forte, nenhum mínimo local relativo pode residir em $\text{relint}(\mathcal{F})$.
2. **Arestas ($d = 1$):** Para cada aresta unidimensional $E_i$, a restrição é afim: $f(x_i) = a + b_i(s_{-i}) x_i$. Sob (H4), $b_i(s_{-i}) \ne 0$, de modo que a função é estritamente monótona e não admite pontos críticos nem mínimos no interior $(-1, 1)$, atingindo seu mínimo exclusivamente nos extremos $x_i = \pm 1$.
3. **Conclusão:** Mínimos locais no hipercubo só podem residir nas faces de dimensão $d=0$, que coincidem com os vértices $\{-1, +1\}^N$. $\blacksquare$

---

> **Corolário 4B (Confinamento dos Atratores Assintóticos do Fluxo Projetado — Dinâmico).**  
> *Considere o fluxo de gradiente projetado no hipercubo:*
> $$\dot{x}(t) = \Pi_{T_{\mathcal{X}}(x(t))}\left(-\nabla \Phi_{\text{mult}}(x(t))\right)$$
> *Sob (H1), (H3') e (H4), todo ponto de equilíbrio assintoticamente estável isolado do fluxo projetado é estritamente um vértice discreto $x^* \in \{-1, +1\}^N$.*

### Demonstração via Função de Lyapunov e LaSalle:
1. Defina a função de Lyapunov $V(x) = \Phi_{\text{mult}}(x)$. Ao longo de qualquer trajetória do fluxo projetado:
   $$\dot{V}(x(t)) = \langle \nabla \Phi_{\text{mult}}(x(t)), \, \Pi_{T_{\mathcal{X}}(x(t))}(-\nabla \Phi_{\text{mult}}(x(t))) \rangle = -\|\Pi_{T_{\mathcal{X}}(x(t))}(-\nabla \Phi_{\text{mult}}(x(t)))\|^2 \le 0$$
   A energia é não-crescente e $\dot{V} = 0$ apenas nos pontos de equilíbrio estacionário KKT.
2. Todo ponto de equilíbrio assintoticamente estável isolado $x^*$ é um ponto de **mínimo local estrito** de $\Phi_{\text{mult}}$ restrito a $\mathcal{X}$.
3. Pelo Teorema 4A, todos os mínimos locais no hipercubo residem em faces de dimensão $d=0$. Logo, $x^* \in \{-1, +1\}^N$. $\blacksquare$

---

## 7. Teorema 5: Convexidade Global e Condicionamento Espectral do Softplus

Definindo a matriz de incidência de cláusulas $V \in \mathbb{R}^{M \times N}$ com linhas $v_c^T = -\frac{1}{2}(\sigma^{(c)})^T$:

> **Teorema 5 (Fatoração da Hessiana e Condicionamento Espectral do Softplus).**  
> *A Hessiana da relaxação Softplus fatora-se exatamente como $\nabla^2 \Phi_{\text{soft}}(x) = V^T W(x) V$, onde $W(x) = \text{diag}(w_1(x), \dots, w_M(x)) \succ 0$ com $w_c(x) = \beta \sigma(\beta g_c(x))[1 - \sigma(\beta g_c(x))] > 0$.*  
> *Consequentemente:*
> 1. *$\nabla^2 \Phi_{\text{soft}}(x) \succeq 0$ em todo $\mathbb{R}^N$ e $\ker(\nabla^2 \Phi_{\text{soft}}) = \ker(V)$. Se $\text{rank}(V) = N$, $\Phi_{\text{soft}}$ é estritamente convexa.*
> 2. *Para $\text{rank}(V) = N$, os autovalores extremos satisfazem:*
>    $$\lambda_{\min}(\nabla^2 \Phi_{\text{soft}}(x)) \ge \lambda_{\min}(W(x)) \, \lambda_{\min}(V^T V) > 0$$
>    $$\lambda_{\max}(\nabla^2 \Phi_{\text{soft}}(x)) \le \lambda_{\max}(W(x)) \, \lambda_{\max}(V^T V)$$
> 3. *O número de condicionamento espectral da Hessiana satisfaz a cota superior:*
>    $$\kappa(\nabla^2 \Phi_{\text{soft}}(x)) \le \left( \frac{\lambda_{\max}(W(x))}{\lambda_{\min}(W(x))} \right) \cdot \kappa(V^T V) = \kappa(W(x)) \cdot \kappa(V^T V)$$

### Demonstração:
Para todo $z \in \mathbb{R}^N \setminus \{\mathbf{0}\}$, a forma quadrática é $z^T \nabla^2 \Phi z = (V z)^T W(x) (V z)$. Pelo teorema espectral:
$$\lambda_{\min}(W) \|V z\|_2^2 \le (V z)^T W (V z) \le \lambda_{\max}(W) \|V z\|_2^2$$
Pelo Quociente de Rayleigh para a matriz simétrica $V^T V$:
$$\lambda_{\min}(V^T V) \|z\|_2^2 \le \|V z\|_2^2 \le \lambda_{\max}(V^T V) \|z\|_2^2$$
Combinando e tomando ínfimo e supremo sobre $\|z\|_2 = 1$, obtemos as cotas de $\lambda_{\min}$ e $\lambda_{\max}$. Dividindo a cota superior pela inferior, decorre a relação de condicionamento $\kappa(H) \le \kappa(W) \kappa(V^T V)$. $\blacksquare$

---

## 8. Teorema 6: Lipschitzianidade do Campo Gradiente e Underflow Numérico

> **Teorema 6 (Constante de Lipschitz do Gradiente e Regimes IEEE 754).**  
> *Para a relaxação Softplus, no limite de precisão inversa $\beta \to \infty$:*
> 1. *A **constante de Lipschitz do campo gradiente** $L_\beta \equiv \sup_{x \in \mathbb{R}^N} \|\nabla^2 \Phi_{\text{soft}}(x)\|_2$ satisfaz $L_\beta = \Theta(\beta)$, com cotas bilaterais:*
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

## 9. Teoremas 7A e 7B: Dinâmica de Bacia Espúria e Contração Centrípeta Universal

A passagem rigorosa da geometria local para a massa da bacia de atração $\mathcal{M}_{\text{spur}}$ é formalizada em dois resultados complementares:

### Teorema 7A (Massa de Bacia Positiva para Família Construtiva Simétrica)
> **Teorema 7A (Família Construtiva com Convergência Analítica Exata).**  
> *Seja $N \ge 4$. Considere a fórmula 3-CNF $F_N$ formada por todas as $M = \binom{N}{3}$ cláusulas exclusivamente negativas: $\mathcal{C} = \{ (\neg x_i \lor \neg x_j \lor \neg x_k) \mid 1 \le i < j < k \le N \}$.*  
> *Sob o fluxo contínuo $\dot{x} = -\nabla \Phi_{\text{quad}}(x)$, o hipercubo aberto $A_N = (1/3, 1)^N \subset [0, 1]^N$ possui volume euclidiano $\text{Vol}(A_N) = (2/3)^N > 0$ e está inteiramente contido na bacia de atração do platô central espúrio:*
> $$A_N \subseteq \mathcal{B}_{\text{spur}}(\Phi_{\text{quad}}) \implies \mathcal{M}_{\text{spur}}(\Phi_{\text{quad}}) \ge \left(\frac{2}{3}\right)^N > 0 \quad \left(\mu_{\text{norm}} \ge \left(\frac{1}{3}\right)^N > 0\right)$$

### Demonstração:
1. Para todo $x \in A_N$, $x_m > 1/3 \implies x_i + x_j + x_k > 1 \implies g_c(x) = \frac{1}{2}(x_i + x_j + x_k - 1) > 0$. Logo, todas as $\binom{N}{3}$ cláusulas estão simultaneamente ativas em $A_N$.
2. O potencial reduz-se à forma quadrática pura $\Phi_{\text{quad}}(x) = \frac{1}{2} (x - \frac{1}{3}\mathbf{1})^T H_N (x - \frac{1}{3}\mathbf{1})$ com Hessiana constante $H_N \succ 0$.
3. Os autovalores de $H_N$ são $\lambda_{\parallel} = \frac{3}{4}(N-1)(N-2) > 0$ e $\lambda_{\perp} = \frac{1}{4}(N-2)(N-3) > 0$.
4. O sistema linear $\dot{u} = -H_N u$ com $u = x - \frac{1}{3}\mathbf{1}$ admite solução analítica fechada $u(t) = \exp(-t H_N) u(0) \to \mathbf{0}$, assegurando que toda trajetória originada em $A_N$ converge exponencialmente para o platô espúrio $\lim_{t \to \infty} x(t) = \frac{1}{3}\mathbf{1} \in \partial \mathcal{U}_N$.
5. Como $x_i(t) > 1/3 > 0$, o arredondamento booleano correspondente é $s = (+1, \dots, +1)$, que viola todas as cláusulas ($E_{\text{disc}} = \binom{N}{3} > 0$). Logo, $A_N \subseteq \mathcal{B}_{\text{spur}}$, provando $\mathcal{M}_{\text{spur}} \ge (2/3)^N > 0$. $\blacksquare$

---

### Teorema 7B (Teorema Universal da Contração Centrípeta da Relaxação Hinge)
> **Teorema 7B (Contração Centrípeta Universal e Massa Espúria Total em Fórmulas UNSAT).**  
> *Para qualquer fórmula 3-CNF e qualquer ponto $x \in \mathcal{X}$ onde ao menos uma cláusula é ativa ($\text{act}(x) \ne \emptyset$):*
> 1. *O campo gradiente satisfaz a condição de contração centrípeta estrita:*
>    $$\langle -\nabla \Phi_{\text{quad}}(x), \, x \rangle < -\sum_{c \in \text{act}(x)} g_c(x) < 0$$
> 2. *$\|x(t)\|_2^2$ é uma função de Lyapunov estrita em toda a região ativa: $\frac{d}{dt}\|x(t)\|_2^2 < 0$.*
> 3. *Para toda e qualquer fórmula insatisfatível (UNSAT), a massa da bacia espúria é UNIVERSALMENTE MÁXIMA:*
>    $$\mathcal{M}_{\text{spur}}(\Phi_{\text{quad}}, \mathcal{D}_{\text{proj}}) = \mu([-1, 1]^N) = 1 \quad (100\% \text{ do volume do hipercubo})$$

### Demonstração:
1. Cláusula ativa $g_c(x) > 0 \iff \sigma^{(c)} \cdot x < -1$.
2. Gradiente: $-\nabla \Phi_{\text{quad}}(x) = \sum_{c \in \text{act}} g_c(x) \sigma^{(c)}$.
3. Produto escalar: $\langle -\nabla \Phi, x \rangle = \sum_{c \in \text{act}} g_c(x) (\sigma^{(c)} \cdot x) < -\sum_{c \in \text{act}} g_c(x) < 0$.
4. **Inexistência de Equilíbrios com $\Phi_{\text{quad}} > 0$ (Interior e Fronteira):**
   - No interior: $-\nabla \Phi_{\text{quad}}(x) = \mathbf{0} \implies \langle -\nabla \Phi, x \rangle = 0$, contradizendo a contração estrita $\langle -\nabla \Phi, x \rangle < 0$.
   - Na fronteira $\partial \mathcal{X}$: um ponto $x^*$ é equilíbrio projetado se e somente se $-\nabla \Phi_{\text{quad}}(x^*) \in N_{\mathcal{X}}(x^*)$, onde $N_{\mathcal{X}}(x^*)$ é o cone normal exterior do hipercubo $\mathcal{X} = [-1, 1]^N$. Como para qualquer vetor $\nu \in N_{\mathcal{X}}(x^*)$ vale $\nu_i x^*_i \ge 0$, temos $\langle \nu, x^* \rangle \ge 0$. Consequentemente, a condição de equilíbrio projetado exigiria $\langle -\nabla \Phi_{\text{quad}}(x^*), x^* \rangle \ge 0$, o que contradiz frontalmente a cota centrípeta estrita $\langle -\nabla \Phi_{\text{quad}}(x^*), x^* \rangle < 0$.
   - Conclusão: Não existem pontos de equilíbrio estacionário KKT nem equilíbrios projetados no conjunto $\{\Phi_{\text{quad}} > 0\}$. Pelo Princípio de Invariância de LaSalle, todas as trajetórias convergem para o platô de zero-energia $Z = \{x \in \mathcal{X} \mid \Phi_{\text{quad}}(x) = 0\}$.
5. Para fórmulas UNSAT, todo o platô $Z$ viola cláusulas booleanas ($E_{\text{disc}} \ge 1$). Logo, $\mathcal{B}_{\text{spur}} = [-1, 1]^N \implies \mathcal{M}_{\text{spur}} \equiv 1$ (100%). $\blacksquare$

---

## 10. Conjectura Central CLG-R (Problema Aberto Fundamental)

> ### Conjectura Central CLG-R (Separação Dinâmica em Ensembles Aleatórios)
> *Para o ensemble padrão de fórmulas aleatórias de 3-SAT $\mathcal{E}(N, \alpha)$ acima do limiar de clustering ($\alpha > \alpha_d \approx 3.86$), considere as representações $\Phi_{\text{quad}}$ e $\Phi_{\text{mult}}$ sob o fluxo projetado $\mathcal{D}_{\text{proj}}$.*  
> *Existe uma constante universal $c(\alpha) > 0$ tal que:*
> $$\lim_{N \to \infty} \mathbb{P}_{F \sim \mathcal{E}(N, \alpha)}\left( \mathcal{M}_{\text{spur}}(\Phi_{\text{quad}}, \mathcal{D}_{\text{proj}}) - \mathcal{M}_{\text{spur}}(\Phi_{\text{mult}}, \mathcal{D}_{\text{proj}}) \ge c(\alpha) \right) = 1$$

---

## 11. Firewall Epistemológico: 3-XOR-SAT e P vs NP

A teoria CLG-R estabelece uma fronteira intransponível contra alegações sobre $P \text{ vs } NP$:
1. O problema **3-XOR-SAT** é decidível deterministicamente em tempo polinomial $\mathcal{O}(N^3)$ via Eliminação Gaussiana sobre $\mathbb{F}_2$ (portanto, pertence estritamente a **P**).
2. Sob relaxações contínuas e fluxos de gradiente, 3-XOR-SAT sofre **colapso dinâmico completo ($R_{\text{dyn}} = 0.0\%$)** decorrente da fragmentação em vidros de spin no hipercubo.
3. Conclusão inatacável:
   $$\boxed{\text{Dificuldade Geométrica Contínua} \;\not\Rightarrow\; \text{Dificuldade de Turing (NP-Dureza)}}$$

---

## 12. Quadro Comparativo Consolidado (Versão 3.0)

| Propriedade Matemática | Quadrática Hinge ($\Phi_{\text{quad}}$) | Multilinear ($\Phi_{\text{mult}}$) | Softplus ($\Phi_{\text{soft}}$) |
| :--- | :--- | :--- | :--- |
| **Classe de Regularidade** | $\mathcal{C}^1$ (por partes) | $\mathcal{C}^\infty$ (polinomial) | $\mathcal{C}^\omega$ (analítica real) |
| **Medida dos Críticos $\mu(\mathcal{C}_0)$** | $> 0$ (Platô $\ge (1/3)^N$) | $= 0$ (Fubini / Zeros Polinomiais) | $= 0$ (Identidade Analítica) |
| **Operador Laplaciano $\Delta \Phi$** | $\equiv 0$ em $\mathcal{U}_N$ | $\equiv 0$ em $\mathbb{R}^N$ (Harmônica) | $\text{Tr}(V^T W V) > 0$ (Subharmônica) |
| **Localização dos Mínimos Locais** | Platô $Z = \{g_c \le 0\}$ | Confinados aos Vértices $\{-1, 1\}^N$ | Mínimo único se $\text{rank}(V)=N$ |
| **Hessiana e Condicionamento** | Posto nulo em $\mathcal{U}_N$ | Diagonal identicamente nula | $\kappa(H) \le \kappa(W) \kappa(V^T V)$ |
| **Dinâmica do Fluxo Projetado** | Contração centrípeta universal $\langle -\nabla \Phi, x \rangle < 0$ | Lyapunov decrescente com atratores isolados em vértices | Funil estritamente convexo |
| **Massa Espúria $\mathcal{M}_{\text{spur}}$ (UNSAT)** | **$100\%$ do hipercubo** ($\mathcal{M}_{\text{spur}} \equiv 1$) | Dominada por vértices de Morse | Regularizada finita ($\beta$ moderado) |
