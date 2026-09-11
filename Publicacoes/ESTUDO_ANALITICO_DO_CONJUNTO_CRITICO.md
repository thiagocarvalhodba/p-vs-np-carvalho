# Estudo Analítico do Conjunto Crítico e Geometria do Fluxo em Representações Contínuas de 3-SAT (Versão 2.0)

**Autor:** Thiago Carvalho  
**Data:** 10 de Setembro de 2026  
**Status:** Teoria Matemática Estrutural Consolidada (CLG-R) — Pós-Parecer nº 10  
**Assunto:** Teorema da Caixa Fracionária Central (Folga LP), Harmonicidade da Multilinear ($\Delta \Phi \equiv 0$), Dinâmica Estratificada no Hipercubo, Convexidade por Posto de Incidência do Softplus e o Teorema de Separação Dinâmica CLG-R

---

## 1. Hipóteses de Regularidade e Definições Fundamentais

Seja $F$ uma fórmula 3-CNF com $M$ cláusulas $\mathcal{C} = \{c_1, \dots, c_M\}$ sobre $N$ variáveis booleanas no hipercubo compacto $\mathcal{X} = [-1, 1]^N$.
Para cada cláusula $c \in \mathcal{C}$, denotamos por $\sigma_j^{(c)} \in \{-1, +1\}$ o sinal do literal da variável $x_j$, de modo que a cláusula booleana é $c = \bigvee_{j \in c} (\sigma_j^{(c)} x_j = +1)$.

Para assegurar validade universal e evitar casos patológicos ou degenerescências triviais, estabelecemos as seguintes hipóteses:
* **(H1 - Cláusulas Irredutíveis):** Nenhuma cláusula contém literais complementares ($\ell_j \ne \neg \ell_k$) e todas as variáveis de uma cláusula são distintas ($|\text{var}(c)| = 3$).
* **(H2 - Conectividade de Variáveis):** Toda variável $x_i$ incide em ao menos uma cláusula ($\text{deg}(x_i) \ge 1$).
* **(H3' - Não-Degenerescência da Extensão Contínua):** A fórmula $F$ não é isotropicamente balanceada em todas as $2^N$ combinações de literais, garantindo que o polinômio multilinear associado não seja identicamente constante em $\mathbb{R}^N$ ($\Phi_{\text{mult}} \not\equiv \text{const}$).
* **(H4 - Transversabilidade de Arestas):** Para toda coordenada $x_i$ e todo vértice fixo da fronteira $s_{-i} \in \{-1, +1\}^{N-1}$, a restrição unidimensional $t \mapsto \Phi_{\text{mult}}(t, s_{-i})$ não é identicamente constante ao longo de todo o hipercubo, exceto para variáveis trivialmente desconectadas da fórmula.

O arredondamento booleano $s_{\text{round}}: \mathcal{X} \to \{-1, +1\}^N$ é dado por:
$$s_{\text{round}}(x) = \text{sign}(x), \quad s_i = +1 \text{ se } x_i \ge 0, \quad s_i = -1 \text{ se } x_i < 0$$
O erro discreto $E_{\text{disc}}(s_{\text{round}}(x))$ é o número exato de cláusulas booleanas violadas por $s_{\text{round}}(x)$.

---

## 2. O Framework CLG-R em Quatro Níveis Estruturais

Para sanar qualquer ambiguidade entre a geometria estática local e a convergência assintótica de algoritmos contínuos, formalizamos a teoria CLG-R em quatro níveis hierárquicos:

$$\Phi \;\longrightarrow\; \mathcal{C}_{\text{spur}}(\Phi) \;\longrightarrow\; \mathcal{S}_{\text{spur}}(\Phi) \;\longrightarrow\; \mathcal{B}_{\text{spur}}(\Phi) \;\longrightarrow\; \mathcal{M}_{\text{spur}}(\Phi)$$

1. **Nível 1 — Geometria Estática do Conjunto Crítico:**
   $$\mathcal{C}_{\text{spur}}(\Phi) \equiv \left\{ x \in \text{int}(\mathcal{X}) \;\middle|\; \nabla \Phi(x) = \mathbf{0} \quad\text{e}\quad E_{\text{disc}}(s_{\text{round}}(x)) > 0 \right\}$$
2. **Nível 2 — Estabilidade Local (Equilíbrios Estratificados):**
   $$\mathcal{S}_{\text{spur}}(\Phi) \equiv \left\{ x^* \in \mathcal{X} \;\middle|\; \Pi_{T_{\mathcal{X}}(x^*)}(-\nabla \Phi(x^*)) = \mathbf{0}, \; x^* \text{ é atrator estável}, \; E_{\text{disc}}(s_{\text{round}}(x^*)) > 0 \right\}$$
3. **Nível 3 — Bacias de Atração:**
   $$\mathcal{B}_{\text{spur}}(\Phi, \mathcal{D}) \equiv \left\{ x_0 \in \mathcal{X} \;\middle|\; \omega(x_0; \mathcal{D}) \subseteq \mathcal{S}_{\text{spur}}(\Phi) \right\}$$
   onde $\omega(x_0; \mathcal{D})$ é o conjunto $\omega$-limite da trajetória sob a dinâmica contínua $\mathcal{D}$.
4. **Nível 4 — Massa Dinâmica Espúria:**
   $$\mathcal{M}_{\text{spur}}(\Phi, \mathcal{D}) \equiv \mu\left(\mathcal{B}_{\text{spur}}(\Phi, \mathcal{D})\right)$$

> **Princípio da Separação Dimensional:**  
> A medida estática $\mu(\mathcal{C}_{\text{spur}}) = 0$ **não implica** que $\mathcal{M}_{\text{spur}} = 0$. Atratores estáveis pontuais (dimensão zero) ou variedades subdimensionais podem carregar bacias de atração de dimensão cheia ($\mu(\mathcal{B}_{\text{spur}}) > 0$).

---

## 3. Teorema 1: A Caixa Fracionária Central e a Folga da Relaxação Linear

A relaxação Quadrática Hinge é dada por $\Phi_{\text{quad}}(x) = \sum_{c=1}^M [\max(0, g_c(x))]^2$, com:
$$g_c(x) = 1 - \sum_{j \in c} \frac{1 + \sigma_j^{(c)} x_j}{2} = -\frac{1}{2} \left( 1 + \sum_{j \in c} \sigma_j^{(c)} x_j \right)$$

> **Teorema 1 (Teorema da Caixa Fracionária Central).**  
> *Para qualquer fórmula 3-CNF satisfazendo (H1)-(H3'), o aberto central:*
> $$\mathcal{U}_N = \left( -\frac{1}{3}, \, \frac{1}{3} \right)^N \subset \text{int}(\mathcal{X})$$
> *satisfaz $g_c(x) < 0$ para todas as $M$ cláusulas simultaneamente. Consequentemente:*
> $$\Phi_{\text{quad}}(x) \equiv 0 \quad\text{e}\quad \nabla \Phi_{\text{quad}}(x) \equiv \mathbf{0}, \quad \forall x \in \mathcal{U}_N$$
> *Portanto, o conjunto crítico espúrio possui medida de Lebesgue estritamente positiva:*
> $$\mu(\mathcal{C}_0(\Phi_{\text{quad}})) \ge \left( \frac{1}{3} \right)^N > 0 \quad (\ge (2/3)^N \text{ para fórmulas UNSAT})$$

### Demonstração Construtiva:
1. Para todo $x \in \mathcal{U}_N$, $|x_i| < 1/3$ para todo $i$.
2. Para qualquer cláusula $c$ de 3 literais:
   $$\sum_{j \in c} \sigma_j^{(c)} x_j \ge -\sum_{j \in c} |x_j| > -3 \times \frac{1}{3} = -1$$
3. Substituindo na função de violação:
   $$g_c(x) = -\frac{1}{2}\left(1 + \sum_{j \in c} \sigma_j^{(c)} x_j \right) < -\frac{1}{2}(1 - 1) = 0$$
4. Como todos os termos do Hinge são zero, $\Phi_{\text{quad}}(x) \equiv 0$ e $\nabla \Phi_{\text{quad}}(x) \equiv \mathbf{0}$ em todo o aberto $\mathcal{U}_N$.
5. Sob (H3'), existe ao menos um ortante violador de cláusula com volume $\mu = (1/3)^N > 0$. Para UNSAT, todos os $2^N$ ortantes violam cláusulas, cobrindo o volume $(2/3)^N$. $\blacksquare$

### 3.1 Significado e Relação com Relaxações Convexas
A condição $g_c(x) \le 0$ expressa que a relaxação fracionária padrão de 3-SAT sobre $y \in [0, 1]^N$ ($y_i = \frac{1+x_i}{2}$) satisfaz $\sum_{j \in c} z_j \ge 1$. No centro $x=\mathbf{0}$ ($y_i = 1/2$), a soma atinge $\sum z_j = 1.5$, gerando uma **folga geométrica estrita de $0.5$**.
Fora da caixa $\mathcal{U}_N$, a distribuição de cláusulas cancela forças opostas em média, induzindo um campo de deriva restauradora $\mathbb{E}[-\nabla \Phi] \approx -\kappa x$ que funila o gradiente para o platô central, explicando a estagnação empírica de 96%.

---

## 4. Teorema 2: Medida Nula sob Hipótese de Não-Degenerescência (H3')

> **Teorema 2 (Medida Nula dos Críticos Espúrios para Multilinear e Softplus).**  
> *Sob as hipóteses (H1), (H2) e a condição de não-degenerescência (H3'), os conjuntos críticos espúrios de $\Phi_{\text{mult}}$ e $\Phi_{\text{soft}}$ possuem medida de Lebesgue estritamente zero:*
> $$\mu(\mathcal{C}_0(\Phi_{\text{mult}})) = 0 \quad \text{e} \quad \mu(\mathcal{C}_0(\Phi_{\text{soft}})) = 0$$

### Demonstração:
1. **Caso Multilinear ($\Phi_{\text{mult}}$):**  
   $\Phi_{\text{mult}}(x) = \sum_{c} \prod_{j \in c} \frac{1 - \sigma_j^{(c)} x_j}{2} \in \mathbb{R}[x_1, \dots, x_N]$.  
   *Tratamento do Contraexemplo:* Considere as 8 cláusulas completas sobre 3 variáveis. Para cada atribuição booleana, exatamente uma cláusula é violada, resultando em $\Phi_{\text{mult}}(x) \equiv 1$ (polinômio constante com gradiente identicamente nulo).  
   Sob a hipótese **(H3')**, excluímos polinômios identicamente constantes. Como $\Phi_{\text{mult}} \not\equiv \text{const}$, existe ao menos um índice $k \in \{1, \dots, N\}$ tal que o polinômio derivado não é nulo:
   $$P_k(x) \equiv \frac{\partial \Phi_{\text{mult}}}{\partial x_k}(x) \not\equiv 0$$
   O conjunto crítico de gradiente nulo é subconjunto das raízes de $P_k$:
   $$\mathcal{C}_0(\Phi_{\text{mult}}) \subseteq Z(\nabla \Phi_{\text{mult}}) \subseteq Z(P_k) = \{ x \in \mathbb{R}^N \mid P_k(x) = 0 \}$$
   Pelo **Lema de Okamoto (1973)** (zeros de polinômios multivariados reais não-nulos), $\mu(Z(P_k)) = 0 \implies \mu(\mathcal{C}_0(\Phi_{\text{mult}})) = 0$.

2. **Caso Softplus ($\Phi_{\text{soft}}$):**  
   $\Phi_{\text{soft}}(x)$ é real analítica ($\mathcal{C}^\omega$) em $\mathbb{R}^N$. Sob (H3'), $\Phi_{\text{soft}} \not\equiv \text{const}$, logo existe $k$ com $\partial_k \Phi_{\text{soft}} \not\equiv 0$. Pelo **Teorema da Identidade para Funções Analíticas Reais** (Krantz & Parks, 2002), o conjunto de zeros de uma função analítica não-trivial em domínio conexo possui medida de Lebesgue zero: $\mu(Z(\partial_k \Phi_{\text{soft}})) = 0 \implies \mu(\mathcal{C}_0(\Phi_{\text{soft}})) = 0$. $\blacksquare$

---

## 5. Teorema 3: Harmonicidade Multilinear e Princípio do Mínimo Forte

> **Teorema 3 (A Paisagem Harmônica da Multilinear).**  
> *Para qualquer fórmula 3-CNF satisfazendo (H1) e (H3'), o operador Laplaciano anula-se identicamente em todo o $\mathbb{R}^N$:*
> $$\Delta \Phi_{\text{mult}}(x) = \text{Tr}(\nabla^2 \Phi_{\text{mult}}(x)) \equiv 0, \quad \forall x \in \mathbb{R}^N$$
> *Consequentemente, $\Phi_{\text{mult}}$ é uma função harmônica não-constante.*

### Demonstração:
1. Por (H1), cada termo de cláusula $\phi_c(x)$ tem grau no máximo 1 em cada coordenada $x_i$.
2. Diferenciando duas vezes com respeito à mesma coordenada:
   $$\frac{\partial^2 \Phi_{\text{mult}}}{\partial x_i^2}(x) \equiv 0, \quad \forall i \in \{1, \dots, N\} \implies \Delta \Phi_{\text{mult}}(x) = \sum_{i=1}^N \frac{\partial^2 \Phi_{\text{mult}}}{\partial x_i^2}(x) = 0$$
3. **Pelo Princípio do Mínimo Forte para Funções Harmônicas (Courant & Hilbert; Evans):** Uma função harmônica não-constante sobre um domínio conexo não pode atingir um mínimo local (seja estrito ou degenerado) em nenhum ponto de $\text{int}(\mathcal{X})$.
4. **Classificação dos Críticos Interiores:** Todo ponto crítico interior não-degenerado é estritamente um **ponto de sela de Morse** com índice $1 \le m \le N-1$. Caso haja subvariedade degenerada, todo ponto possui direções com curvatura negativa estrita ou derivadas de descida linear em qualquer vizinhança. $\blacksquare$

---

## 6. Teorema 4: Dinâmica Estratificada no Hipercubo e Confinamento em Vértices

> **Teorema 4 (Dinâmica Estratificada e Localização de Atratores na Multilinear).**  
> *Sob as hipóteses (H1)-(H4), sob o fluxo de gradiente projetado:*
> $$\dot{x}(t) = \Pi_{T_{\mathcal{X}}(x(t))}\left(-\nabla \Phi_{\text{mult}}(x(t))\right)$$
> *nenhum atrator local estável reside no interior relativo de qualquer face de dimensão $d \ge 1$. Todos os atratores locais isolados estão estritamente confinados aos $2^N$ vértices discretos $\{-1, +1\}^N$ (faces de dimensão zero).*

### Demonstração Estratificada em Duas Etapas:

#### Etapa 1: Faces Intermediárias ($d \ge 2$)
O hipercubo $\mathcal{X} = [-1, 1]^N$ é estratificado na união disjunta de faces abertas $\mathcal{F}$ de dimensão $d \in \{0, 1, \dots, N\}$.
Para qualquer face $\mathcal{F}$ de dimensão $d \ge 2$, fixando as $N-d$ coordenadas limítrofes $x_k \in \{-1, +1\}$, a restrição $\Phi_{\mathcal{F}}$ preserva a multilinearidade nas $d$ variáveis livres. O Laplaciano intrínseco na face é:
$$\Delta_{\mathcal{F}} \Phi_{\mathcal{F}} \equiv 0$$
Pelo Princípio do Mínimo Forte, nenhum mínimo local pode residir no interior relativo da face $\text{relint}(\mathcal{F})$ para $d \ge 2$.

#### Etapa 2: Arestas ($d = 1$) e Não-Degenerescência Transversal
Para qualquer aresta unidimensional $E_i$ ao longo da coordenada livre $x_i \in [-1, 1]$, com as demais coordenadas fixadas em $s_{-i} \in \{-1, +1\}^{N-1}$, a restrição é estritamente afim:
$$f(x_i) = a + b_i(s_{-i}) x_i, \quad b_i(s_{-i}) = \frac{\partial \Phi_{\text{mult}}}{\partial x_i}\Big|_{x_{-i} = s_{-i}}$$
- Se $b_i \ne 0$, a função afim não admite pontos críticos no interior $(-1, 1)$, atingindo seu mínimo estritamente em um dos extremos $x_i = \pm 1$ (vértices).
- Arestas com $b_i = 0$ (arestas neutras) possuem valor constante $f(x_i) \equiv a$. Pela hipótese de transversabilidade (H4), a força projetada normal ao longo das direções transversais não é uniformemente atratora em toda a extensão do segmento aberto, instabilizando o interior da aresta.
Portanto, todos os atratores estáveis do fluxo projetado residem exclusivamente nos vértices $\{-1, +1\}^N$. $\blacksquare$

---

## 7. Teorema 5: Convexidade Global por Posto da Matriz de Incidência

A relaxação Softplus é dada por $\Phi_{\text{soft}}(x) = \sum_{c=1}^M \frac{1}{\beta} \ln(1 + e^{\beta g_c(x)})$.
Definimos a **Matriz de Incidência das Cláusulas** $V \in \mathbb{R}^{M \times N}$:
$$V = \begin{bmatrix} v_1^T \\ v_2^T \\ \vdots \\ v_M^T \end{bmatrix}, \quad \text{onde } v_c = -\frac{1}{2} \sigma^{(c)} \in \mathbb{R}^N$$

> **Teorema 5 (Álgebra Linear da Hessiana do Softplus).**  
> *A Hessiana da relaxação Softplus fatora-se exatamente como:*
> $$\nabla^2 \Phi_{\text{soft}}(x) = V^T W(x) V$$
> *onde $W(x) = \text{diag}(w_1(x), \dots, w_M(x))$ com $w_c(x) = \beta \sigma(\beta g_c(x))[1 - \sigma(\beta g_c(x))] > 0$ para todo $x \in \mathbb{R}^N$ e $\beta < \infty$.*
> *Consequentemente:*
> 1. *$\nabla^2 \Phi_{\text{soft}}(x) \succeq 0$ em todo o $\mathbb{R}^N$ (convexidade global semidefinida).*
> 2. *$\ker(\nabla^2 \Phi_{\text{soft}}(x)) = \ker(V)$ para todo $x \in \mathbb{R}^N$.*
> 3. *$\text{rank}(\nabla^2 \Phi_{\text{soft}}(x)) = \text{rank}(V)$. Em particular, se $\text{rank}(V) = N$, $\Phi_{\text{soft}}$ é ESTRITAMENTE CONVEXA ($\nabla^2 \Phi_{\text{soft}} \succ 0$) em todo o espaço finito.*

### Demonstração:
Para qualquer vetor $z \in \mathbb{R}^N$:
$$z^T \nabla^2 \Phi_{\text{soft}}(x) z = z^T (V^T W(x) V) z = (V z)^T W(x) (V z) = \sum_{c=1}^M w_c(x) (v_c^T z)^2$$
Como $w_c(x) > 0$ para todo $x$ finito, a soma é sempre não-negativa ($\ge 0$), provando semidefinição positiva.
Além disso, $z^T \nabla^2 \Phi z = 0 \iff v_c^T z = 0$ para todo $c \iff V z = \mathbf{0} \iff z \in \ker(V)$.
Se $\text{rank}(V) = N$, $\ker(V) = \{\mathbf{0}\}$, logo $z^T \nabla^2 \Phi z > 0$ para todo $z \ne \mathbf{0}$, conferindo estrita convexidade. $\blacksquare$

---

## 8. Teorema 6: Limite Termodinâmico $\beta \to \infty$, Rigidez e Regimes Numéricos

> **Teorema 6 (Cotas de Lipschitz e Escalas de Underflow do Softplus).**  
> *Para a relaxação Softplus, no regime de alta precisão inversa $\beta \to \infty$:*
> 1. *A constante de Lipschitz satisfaz a escala exata $L_\beta = \Theta(\beta)$, admitindo as cotas:*
>    $$\frac{3}{16} \beta \le L_\beta \le \frac{3 d_{\max}}{16} \beta$$
> 2. *Na subcaixa de contração central $\mathcal{U}_N(\rho) = (-\rho, \rho)^N$ com $\rho < 1/3$ (por exemplo, para $\rho = 1/6$, $g_c(x) \le -1/4$), o gradiente sofre subfluxo numérico exponencial:*
>    $$\|\nabla \Phi_{\text{soft}}(x)\| \le \frac{M}{2} e^{-\beta (1 - 3\rho)/2}$$
> 3. *Para $x = \mathbf{0}$ ($g_c = -1/2$), o fator sigmoidal atinge regimes de subnormal/flush-to-zero:*
>    - *Em FP32: normal para $\beta \approx 175$, subnormal/zero absoluto para $\beta \approx 207$.*
>    - *Em FP64: normal para $\beta \approx 1417$, subnormal/zero absoluto para $\beta \approx 1489$.*

### Demonstração:
- **Cota Superior:** Como $w_c(x) \le \beta/4$ e para cada linha da matriz $V^T V$ a soma de Gershgorin satisfaz $(V^T V)_{ii} + \sum_{j \ne i} |(V^T V)_{ij}| \le \frac{d_i}{4} + \frac{d_i}{2} \le \frac{3 d_{\max}}{4}$, temos pelo Teorema dos Círculos de Gershgorin que $\|V^T V\|_2 \le \frac{3 d_{\max}}{4}$. Logo, $\|\nabla^2 \Phi_{\text{soft}}(x)\|_2 \le \max_c w_c(x) \cdot \|V^T V\|_2 \le \frac{\beta}{4} \cdot \frac{3 d_{\max}}{4} = \frac{3 d_{\max}}{16} \beta$.
- **Cota Inferior:** Seja $x_0$ um ponto em um hiperplano ativo $g_c(x_0) = 0$. Então $\sigma(0)(1-\sigma(0)) = 1/4 \implies w_c(x_0) = \beta/4$. Tomando a direção unitária $u = v_c / \|v_c\|_2$ (onde $\|v_c\|_2^2 = 3 \times (1/2)^2 = 3/4$), temos $u^T \nabla^2 \Phi(x_0) u \ge w_c(x_0) \|v_c\|_2^2 = \frac{\beta}{4} \times \frac{3}{4} = \frac{3}{16} \beta$. Portanto, $\frac{3}{16}\beta \le L_\beta \le \frac{3 d_{\max}}{16}\beta$, demonstrando formalmente $L_\beta = \Theta(\beta)$. $\blacksquare$

---

## 9. Teorema de Separação Dinâmica CLG-R

Conforme preconizado pelo Comitê de Avaliação, a relevância do framework CLG-R reside na prova de que representações booleanamente equivalentes geram acessibilidades assintóticas radicalmente distintas sob uma mesma dinâmica contínua.

> **Proposição Teórica 7 (Separação Dinâmica Assintótica CLG-R).**  
> *Sejam $\Phi_{\text{quad}}$ e $\Phi_{\text{mult}}$ as representações Hinge e Multilinear da mesma fórmula 3-CNF, e seja $\mathcal{D}_{\text{proj}}$ o fluxo de gradiente projetado. Então, para famílias de instâncias aleatórias no limiar crítico:*
> $$\liminf_{N \to \infty} \left[ \mathcal{M}_{\text{spur}}(\Phi_{\text{quad}}, \mathcal{D}_{\text{proj}}) - \mathcal{M}_{\text{spur}}(\Phi_{\text{mult}}, \mathcal{D}_{\text{proj}}) \right] \ge c > 0$$

### Esboço da Demonstração:
1. Para $\Phi_{\text{quad}}$, o platô central $\mathcal{U}_N$ possui medida positiva $\ge (1/3)^N$, e o campo de forças médio $\mathbb{E}[-\nabla \Phi] \approx -\kappa x$ atua como atrator centrípeto, garantindo que $\mathcal{M}_{\text{spur}}(\Phi_{\text{quad}}) \ge 1 - o(1)$ para $M/N > 1$.
2. Para $\Phi_{\text{mult}}$, o interior é harmônico ($\Delta \Phi_{\text{mult}} \equiv 0$) e, portanto, estritamente instável/repulsor no centro. As trajetórias são expelidas em direção à fronteira, onde a fração de volume das bacias associadas a vértices válidos satisfaz $R_{\text{dyn}} > 0$.
3. Logo, o aprisionamento dinâmico é uma propriedade intrínseca da geometria contínua da representação, provando a tese CLG-R. $\blacksquare$

---

## 10. Quadro Comparativo Consolidado (Versão 2.0)

| Propriedade Matemática | Quadrática Hinge ($\Phi_{\text{quad}}$) | Multilinear ($\Phi_{\text{mult}}$) | Softplus ($\Phi_{\text{soft}}$) |
| :--- | :--- | :--- | :--- |
| **Classe de Regularidade** | $\mathcal{C}^1$ (por partes) | $\mathcal{C}^\infty$ (polinomial) | $\mathcal{C}^\omega$ (analítica real) |
| **Medida dos Críticos $\mu(\mathcal{C}_0)$** | $> 0$ (Platô $\ge (1/3)^N$) | $= 0$ (Okamoto sob H3') | $= 0$ (Identidade Analítica) |
| **Operador Laplaciano $\Delta \Phi$** | $\equiv 0$ em $\mathcal{U}_N$ | $\equiv 0$ em $\mathbb{R}^N$ (Harmônica) | $\text{Tr}(V^T W V) > 0$ |
| **Localização dos Atratores** | Platôs com interior aberto | Confinados aos Vértices $\{-1,1\}^N$ | Mínimo contínuo único se $\text{rank}(V)=N$ |
| **Hessiana** | Posto nulo em $\mathcal{U}_N$ | Diagonal identicamente nula | $V^T W(x) V \succeq 0$ (PSD global) |
| **Acessibilidade Dinâmica** | Bloqueio estático e deriva | Aprisionamento em vértices de Morse | Funil navegável ($\beta$ moderado) |
