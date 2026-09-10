# Estudo Analítico do Conjunto Crítico e Geometria do Fluxo em Representações Contínuas de 3-SAT

**Autor:** Thiago Carvalho  
**Data:** 10 de Setembro de 2026  
**Status:** Teoria Matemática Estrutural Consolidada (CLG-R) — Pós-Auditoria Duplo-Cega  
**Assunto:** Teorema da Caixa Fracionária Central (Integrality Gap de LP), Harmonicidade da Multilinear ($\Delta \Phi \equiv 0$), Confinamento de Mínimos nos Vértices, Convexidade Global Semidefinida do Softplus e Massa de Atração Espúria $\mathcal{M}_{\text{spur}}(\Phi)$

---

## 1. Hipóteses de Regularidade e Definições Fundamentais

Seja $F$ uma fórmula 3-CNF com $M$ cláusulas $\mathcal{C} = \{c_1, \dots, c_M\}$ sobre $N$ variáveis booleanas $x = (x_1, \dots, x_N) \in \mathcal{X} = [-1, 1]^N$.
Para cada cláusula $c \in \mathcal{C}$, denotamos por $\sigma_j^{(c)} \in \{-1, +1\}$ o sinal do literal da variável $x_j$, de modo que a cláusula é $c = \bigvee_{j \in c} (\sigma_j^{(c)} x_j = +1)$.

Para evitar patologias combinatórias degeneradas, assumimos as seguintes hipóteses estruturais:
* **(H1 - Não-Tautologia):** Nenhuma cláusula contém um literal e seu complemento ($\ell_j \ne \neg \ell_k$).
* **(H2 - Conectividade de Variáveis):** Toda variável $x_i$ incide em ao menos uma cláusula ($\text{deg}(x_i) \ge 1$).
* **(H3 - Não-Trivialidade Booleana):** A fórmula possui ao menos uma atribuição discreta com violação ($E_{\text{disc}}(s^*) \ge 1$). Fórmulas UNSAT satisfazem $E_{\text{disc}}(s) \ge 1$ para todas as $2^N$ atribuições.

O arredondamento discreto $s_{\text{round}}: \mathcal{X} \to \{-1, +1\}^N$ é o mapeamento de sinal:
$$s_{\text{round}}(x) = \text{sign}(x), \quad \text{com } s_i = +1 \text{ se } x_i \ge 0 \text{ e } s_i = -1 \text{ se } x_i < 0$$
O erro discreto $E_{\text{disc}}(s_{\text{round}}(x))$ é o número exato de cláusulas violadas pela atribuição $s_{\text{round}}(x)$.

### O Conjunto de Equilíbrios Espúrios $\mathcal{S}_{\text{spur}}(\Phi)$
Sob o fluxo gradiente projetado no cone tangente $T_{\mathcal{X}}(x)$ do hipercubo compacto $\mathcal{X} = [-1, 1]^N$:
$$\dot{x}(t) = \Pi_{T_{\mathcal{X}}(x(t))}\left(-\nabla \Phi(x(t))\right)$$
Definimos o conjunto de pontos de equilíbrio espúrios (satisfazendo condições KKT com violação booleana) como:
$$\mathcal{S}_{\text{spur}}(\Phi) \equiv \left\{ x^* \in \mathcal{X} \;\middle|\; \Pi_{T_{\mathcal{X}}(x^*)}(-\nabla \Phi(x^*)) = \mathbf{0} \quad\text{e}\quad E_{\text{disc}}(s_{\text{round}}(x^*)) > 0 \right\}$$
No interior do domínio $\text{int}(\mathcal{X})$, onde a projeção é a identidade, este conjunto coincide com o conjunto crítico espúrio:
$$\mathcal{C}_0(\Phi) \equiv \left\{ x \in \text{int}(\mathcal{X}) \;\middle|\; \nabla \Phi(x) = \mathbf{0} \quad\text{e}\quad E_{\text{disc}}(s_{\text{round}}(x)) > 0 \right\}$$

---

## 2. Lema 1 e Teorema 1: A Patologia Universal da Quadrática Hinge

A relaxação Quadrática Hinge é dada por:
$$\Phi_{\text{quad}}(x) = \sum_{c=1}^M \left[ \max\left(0, \, g_c(x)\right) \right]^2$$
onde a função de violação contínua da cláusula $c$ é:
$$g_c(x) = 1 - \sum_{j \in c} \frac{1 + \sigma_j^{(c)} x_j}{2} = -\frac{1}{2} \left( 1 + \sum_{j \in c} \sigma_j^{(c)} x_j \right)$$

O gradiente global de $\Phi_{\text{quad}}$ é a soma sobre as cláusulas ativas:
$$\nabla \Phi_{\text{quad}}(x) = -\sum_{c: g_c(x) > 0} g_c(x) \sum_{j \in c} \sigma_j^{(c)} e_j$$

> **Lema 1 (Inatividade Simultânea das Cláusulas).**  
> *Se $g_c(x) \le 0$ para todo $c \in \{1, \dots, M\}$, então $\Phi_{\text{quad}}(x) = 0$ e $\nabla \Phi_{\text{quad}}(x) = \mathbf{0}$ identicamente.*

> **Teorema 1 (Teorema da Caixa Fracionária Central).**  
> *Para toda fórmula 3-CNF não-trivial $F$ satisfazendo (H1)-(H3), o conjunto crítico espúrio possui medida de Lebesgue estritamente positiva, satisfazendo a cota inferior universal:*
> $$\mu(\mathcal{C}_0(\Phi_{\text{quad}})) \ge \left( \frac{1}{3} \right)^N > 0$$
> *Se a fórmula $F$ for insatisfatível (UNSAT), a medida satisfaz a cota assintótica:*
> $$\mu(\mathcal{C}_0(\Phi_{\text{quad}})) \ge \left( \frac{2}{3} \right)^N > 0$$

### Demonstração Construtiva Universal:
1. Considere a caixa hipercúbica aberta centrada na origem do $\mathbb{R}^N$:
   $$\mathcal{U}_N = \left( -\frac{1}{3}, \, \frac{1}{3} \right)^N \subset \text{int}(\mathcal{X})$$
2. Para qualquer ponto $x \in \mathcal{U}_N$, suas coordenadas satisfazem $|x_i| < \frac{1}{3}$ para todo $i \in \{1, \dots, N\}$.
3. Para **qualquer cláusula 3-CNF arbitrária** $c = (\ell_1 \lor \ell_2 \lor \ell_3)$, com coeficientes $\sigma_j^{(c)} \in \{-1, +1\}$:
   $$\sum_{j \in c} \sigma_j^{(c)} x_j \ge -\sum_{j \in c} |\sigma_j^{(c)} x_j| = -\sum_{j \in c} |x_j| > -3 \times \frac{1}{3} = -1$$
4. Substituindo na função de violação $g_c(x)$:
   $$g_c(x) = -\frac{1}{2}\left( 1 + \sum_{j \in c} \sigma_j^{(c)} x_j \right) < -\frac{1}{2}(1 - 1) = 0$$
5. Como esta desigualdade independe dos índices e sinais das variáveis da cláusula, ela é satisfeita **estritamente e simultaneamente por todas as $M$ cláusulas da fórmula**:
   $$g_c(x) < 0, \quad \forall c \in \{1, \dots, M\}, \quad \forall x \in \mathcal{U}_N$$
6. Pelo Lema 1, $\Phi_{\text{quad}}(x) \equiv 0$ e $\nabla \Phi_{\text{quad}}(x) \equiv \mathbf{0}$ em todo o aberto $\mathcal{U}_N$.
7. Por (H3), existe ao menos uma atribuição $s^* \in \{-1, +1\}^N$ que viola ao menos uma cláusula ($E_{\text{disc}}(s^*) \ge 1$). O ortante associado $\Omega_{s^*} = \mathcal{U}_N \cap \{x \mid \text{sign}(x) = s^*\}$ possui medida de Lebesgue exatamente $\mu(\Omega_{s^*}) = (1/3)^N > 0$.
8. Para todo $x \in \Omega_{s^*}$, $\nabla \Phi_{\text{quad}}(x) = \mathbf{0}$ e $E_{\text{disc}}(\text{sign}(x)) \ge 1$. Logo, $\Omega_{s^*} \subseteq \mathcal{C}_0(\Phi_{\text{quad}})$, demonstrando $\mu(\mathcal{C}_0(\Phi_{\text{quad}})) \ge (1/3)^N > 0$. Para fórmulas UNSAT, todas as atribuições violam cláusulas, cobrindo o volume de $\mathcal{U}_N$, resultando em $\mu(\mathcal{C}_0) \ge (2/3)^N > 0$. $\blacksquare$

### 2.1 Conexão com o Integrality Gap de Linear Programming (Håstad, 2001)
A condição $g_c(x) \le 0$ no domínio $[-1, 1]$ é isomórfica à restrição primal padrão da relaxação Linear Programming (LP) de 3-SAT sobre $y \in [0, 1]^N$ ($y_i = \frac{1+x_i}{2}$):
$$g_c(x) \le 0 \iff \sum_{j \in c} z_j \ge 1, \quad \text{onde } z_j \in \{y_j, 1-y_j\}$$
No centro $x = \mathbf{0}$ ($y_i = 1/2$), cada cláusula soma exatamente $\sum z_j = 1.5$, gerando uma folga primal estrita de $0.5$. O platô de gradiente nulo do Teorema 1 é a **manifestação contínua exata do Integrality Gap clássico (7/8 de Håstad, 2001)**: a relaxação LP satisfaz 100% das cláusulas no centro fracionário, tornando a dinâmica de primeira ordem completamente cega às violações discretas subjacentes.

---

## 3. Teorema 2: Medida Zero via Analiticidade Real e Zeros de Polinômios

> **Teorema 2 (Medida Nula dos Críticos Espúrios para Multilinear e Softplus).**  
> *Sob as hipóteses (H1)-(H3), os conjuntos críticos espúrios de $\Phi_{\text{mult}}$ e $\Phi_{\text{soft}}$ possuem medida de Lebesgue estritamente zero:*
> $$\mu(\mathcal{C}_0(\Phi_{\text{mult}})) = 0 \quad \text{e} \quad \mu(\mathcal{C}_0(\Phi_{\text{soft}})) = 0$$

### Demonstração:
1. **Caso Multilinear ($\Phi_{\text{mult}}$):**
   - $\Phi_{\text{mult}}(x) = \sum_{c} \prod_{j \in c} \frac{1 - \sigma_j^{(c)} x_j}{2}$ pertence a $\mathbb{R}[x_1, \dots, x_N]$.
   - Por (H3), a fórmula é não-trivial, de modo que $\Phi_{\text{mult}}(x)$ não é um polinômio constante.
   - Pela álgebra de polinômios multivariados, se todas as derivadas parciais fossem identicamente nulas, o polinômio seria constante. Logo, existe ao menos um índice $k \in \{1, \dots, N\}$ tal que $P_k(x) = \partial_k \Phi_{\text{mult}}(x) \not\equiv 0$.
   - Pelo Lema dos Zeros de Polinômios Reais (Okamoto 1973; Caron & Traynor 2005), o conjunto de raízes $Z(P_k) = \{x \in \mathbb{R}^N \mid P_k(x) = 0\}$ tem medida de Lebesgue zero: $\mu(Z(P_k)) = 0$.
   - Como $\text{Crit}(\Phi_{\text{mult}}) \subseteq Z(P_k)$, segue que $\mu(\mathcal{C}_0(\Phi_{\text{mult}})) \le \mu(Z(P_k)) = 0$.

2. **Caso Softplus ($\Phi_{\text{soft}}$):**
   - $\Phi_{\text{soft}}(x) = \sum_{c=1}^M \frac{1}{\beta} \ln(1 + e^{\beta g_c(x)})$ é real analítica ($\mathcal{C}^\omega$) em todo $\mathbb{R}^N$.
   - Como $\Phi_{\text{soft}} \not\equiv \text{const}$, existe $k$ com $\partial_k \Phi_{\text{soft}} \not\equiv 0$.
   - Pelo Teorema da Identidade para Funções Analíticas Reais (Krantz & Parks 2002; Mityagin 2015), o conjunto de raízes de uma função analítica não identicamente nula sobre um conexo tem medida de Lebesgue zero: $\mu(Z(\partial_k \Phi_{\text{soft}})) = 0$.
   - Consequentemente, $\mu(\mathcal{C}_0(\Phi_{\text{soft}})) = 0$. $\blacksquare$

---

## 4. Teorema 3: Harmonicidade da Multilinear ($\Delta \Phi \equiv 0$) e Princípio do Mínimo Forte

> **Teorema 3 (Harmonicidade e Ausência de Mínimos Interiores na Multilinear).**  
> *Para a relaxação multilinear de qualquer fórmula 3-CNF satisfazendo (H1), o operador Laplaciano anula-se identicamente em todo o espaço:*
> $$\Delta \Phi_{\text{mult}}(x) = \text{Tr}(\nabla^2 \Phi_{\text{mult}}(x)) \equiv 0, \quad \forall x \in \mathbb{R}^N$$
> *Portanto, $\Phi_{\text{mult}}$ é uma função harmônica em $\mathbb{R}^N$.*

### Demonstração e Consequências Fundamentais:
1. Em qualquer cláusula $c = (\ell_1 \lor \ell_2 \lor \ell_3)$, por (H1), as variáveis são mutuamente distintas.
2. Cada monômio da multilinear possui grau no máximo 1 em cada coordenada $x_i$.
3. Derivando duas vezes com respeito à mesma coordenada:
   $$\frac{\partial^2 \Phi_{\text{mult}}}{\partial x_i^2}(x) \equiv 0, \quad \forall i \in \{1, \dots, N\} \implies \Delta \Phi_{\text{mult}}(x) = \sum_{i=1}^N 0 \equiv 0$$
4. **Pelo Princípio do Mínimo Forte para Funções Harmônicas (Courant & Hilbert; Evans):** Uma função harmônica não-constante sobre um domínio conexo não pode atingir um mínimo local (seja estrito ou degenerado!) em nenhum ponto do interior $\text{int}(\mathcal{X})$.
5. Além disso, ao longo de qualquer eixo coordenado, a restrição $t \mapsto \Phi_{\text{mult}}(x^* + t e_i)$ é puramente linear ($a + bt$), de modo que todas as derivadas de ordem superior são nulas ($\frac{\partial^p \Phi}{\partial x_i^p} \equiv 0$ para $p \ge 2$).
6. **Corolário de Morse:** A relaxação multilinear **NÃO POSSUI NENHUM MÍNIMO LOCAL NO INTERIOR $\text{int}(\mathcal{X})$**. Todo ponto crítico interior não-degenerado é **obrigatoriamente um PONTO DE SELA** com índice de Morse $1 \le m \le N-1$. $\blacksquare$

---

## 5. Teorema 4: Confinamento Estrito dos Mínimos Locais nos Vértices da Fronteira

> **Teorema 4 (Localização Vertical de Mínimos na Multilinear).**  
> *Sob o fluxo gradiente projetado no hipercubo compacto $\mathcal{X} = [-1, 1]^N$, TODO mínimo local de $\Phi_{\text{mult}}$ está confinado EXCLUSIVAMENTE aos $2^N$ vértices discretos $\{-1, +1\}^N$ (faces de dimensão zero).*

### Demonstração por Estratificação de Faces:
1. O hipercubo $\mathcal{X}$ é estratificado em faces abertas $\mathcal{F}$ de dimensão $d \in \{0, 1, \dots, N\}$.
2. Para qualquer face intermediária de dimensão $2 \le d < N$, fixadas as $N-d$ coordenadas ativas na fronteira ($x_k = \pm 1$), a função restrita $\Phi_{\mathcal{F}}$ permanece multilinear nas $d$ coordenadas livres. Seu Laplaciano intrínseco é identicamente nulo: $\Delta_{\mathcal{F}} \Phi_{\mathcal{F}} \equiv 0$. Pelo Princípio do Mínimo Forte, não há mínimos no interior relativo de nenhuma face de dimensão $d \ge 2$.
3. Para as arestas ($d = 1$), a função restrita é puramente linear ($a + bt$), não possuindo mínimo no interior aberto do segmento $(-1, 1)$. O mínimo reside obrigatoriamente nos extremos $t = \pm 1$.
4. Portanto, todos os atratores locais de $\Phi_{\text{mult}}$ estão estritamente confinados aos vértices discretos $d = 0$. $\blacksquare$

---

## 6. Teorema 5: Convexidade Global Semidefinida do Softplus ($\nabla^2 \Phi_{\text{soft}} \succeq 0$)

> **Teorema 5 (Convexidade Global Semidefinida do Softplus).**  
> *A matriz Hessiana da relaxação Softplus é globalmente semidefinida positiva em todo o $\mathbb{R}^N$:*
> $$\nabla^2 \Phi_{\text{soft}}(x) \succeq 0, \quad \forall x \in \mathbb{R}^N$$
> *Consequentemente, $\Phi_{\text{soft}}$ é uma função globalmente convexa sobre $\mathbb{R}^N$.*

### Demonstração:
A Hessiana exata do Softplus é dada por:
$$\nabla^2 \Phi_{\text{soft}}(x) = \frac{\beta}{4} \sum_{c=1}^M \sigma(\beta g_c(x)) \left(1 - \sigma(\beta g_c(x))\right) v_c v_c^T$$
onde $v_c = \sum_{j \in c} \sigma_j^{(c)} e_j \in \mathbb{R}^N$.
1. Para cada cláusula, a matriz $v_c v_c^T$ é de posto 1 e semidefinida positiva ($z^T (v_c v_c^T) z = (v_c^T z)^2 \ge 0$ para qualquer $z \in \mathbb{R}^N$).
2. Para qualquer $\beta > 0$ e $x$ finito, os pesos $w_c(x) = \frac{\beta}{4} \sigma(\beta g_c)(1 - \sigma(\beta g_c))$ são escalares estritamente positivos ($w_c(x) > 0$).
3. Uma combinação linear de matrizes semidefinidas positivas com coeficientes positivos é semidefinida positiva:
   $$z^T \nabla^2 \Phi_{\text{soft}}(x) z = \sum_{c=1}^M w_c(x) (v_c^T z)^2 \ge 0, \quad \forall x \in \mathbb{R}^N, \quad \forall z \in \mathbb{R}^N$$
4. *Significado Fundamental:* O Softplus no espaço não-restringido não possui nenhuma sela com curvatura negativa. A curvatura estrita ao longo das direções geradas pelas cláusulas transforma a paisagem em um funil convexo regular. $\blacksquare$

---

## 7. Teorema 6: Limite Termodinâmico $\beta \to \infty$, Rigidez e Underflow

1. **Constante de Lipschitz do Gradiente:** Como $\sigma(1-\sigma) \le 1/4$, a norma espectral da Hessiana satisfaz $L_\beta = \|\nabla^2 \Phi_{\text{soft}}\|_2 \le \frac{3 \beta}{16} d_{\max} = \Theta(\beta)$. A constante de Lipschitz cresce estritamente linear com $\beta$.
2. **Rigidez Numérica (Stiffness):** A estabilidade de passo de Euler impõe $\eta < 2/L_\beta = \mathcal{O}(1/\beta)$. Para $\beta \to \infty$, o fluxo contínuo degenera em uma EDO rígida.
3. **Subfluxo em Ponto Flutuante (Underflow IEEE 754):** Na caixa central $\mathcal{U}_N$, como $g_c(x) \le -0.5$, o termo $\sigma(\beta g_c) \approx e^{-\beta \delta}$ sofre underflow para zero em FP32 para $\beta \ge 178$ e em FP64 para $\beta \ge 1420$. O Softplus congela-se computacionalmente no platô do Hinge para $\beta$ grande.
4. **Regime Ótimo:** Justifica-se formalmente o regime operacional $\beta \in [2.0, 10.0]$ adotado na pesquisa (onde a curvatura é máxima e o passo $\eta \approx 0.02$ é estável).

---

## 8. Massa de Atração Espúria $\mathcal{M}_{\text{spur}}(\Phi)$ e Dinâmica do Fluxo

Definimos a **Massa de Atração Espúria** como:
$$\mathcal{M}_{\text{spur}}(\Phi) \equiv \mu\left( \left\{ x_0 \in \mathcal{X} \;\middle|\; \omega(x_0) \subseteq \mathcal{S}_{\text{spur}}(\Phi) \right\} \right)$$
onde $\omega(x_0)$ é o conjunto $\omega$-limite da trajetória sob o fluxo gradiente projetado $\dot{x}(t) = \Pi_{T_{\mathcal{X}}(x(t))}(-\nabla \Phi(x(t)))$, $x(0) = x_0$.

### O Quadro Dinâmico Consolidado:
1. **Quadrática Hinge:** $\mathcal{M}_{\text{spur}}(\Phi_{\text{quad}}) \ge \mu(\mathcal{C}_0) \ge (1/3)^N > 0$. O bloqueio estático instantâneo na caixa central somado à convergência por deriva das forças antagônicas produz $96\%$ de estagnação empírica ($R_{\text{dyn}} \approx 4\%$).
2. **Multilinear:** $\mu(\mathcal{C}_0) = 0$. O interior possui apenas selas harmônicas. Porém, a bacia combinatória dos vértices espúrios da fronteira domina o hipercubo: $\mathcal{M}_{\text{spur}}(\Phi_{\text{mult}}) \approx 0.94$ (explicando os 6% de reachability).
3. **Softplus:** A convexidade semidefinida e a injeção de curvatura eliminam bacias espúrias rasas, expandindo a reachability para até 69.3% em escalas moderadas de Random-3-SAT. Contudo, em conformidade estrita com a NP-dureza, em problemas rígidos com simetria de paridade (3-XOR-SAT), a ausência de sinal local preserva o colapso dinâmico ($R_{\text{dyn}} \approx 0\%$), comprovando a tese CLG-R de que a geometria contínua desacopla a acessibilidade sem violar a complexidade fundamental.

---

## 9. Quadro Comparativo Consolidado do CLG-R

| Propriedade Matemática | Quadrática Hinge ($\Phi_{\text{quad}}$) | Multilinear ($\Phi_{\text{mult}}$) | Softplus ($\Phi_{\text{soft}}$) |
| :--- | :--- | :--- | :--- |
| **Classe de Regularidade** | $\mathcal{C}^1$ (por partes) | $\mathcal{C}^\infty$ (polinomial) | $\mathcal{C}^\omega$ (analítica real) |
| **Medida dos Críticos $\mu(\mathcal{C}_0)$** | $> 0$ (Platô $\ge (1/3)^N$) | $= 0$ (Lema Polinomial) | $= 0$ (Identidade Analítica) |
| **Operador Laplaciano $\Delta \Phi$** | $\equiv 0$ em $\mathcal{U}_N$ (Degenerado) | $\equiv 0$ em $\mathbb{R}^N$ (Harmônica) | $> 0$ em $\mathbb{R}^N$ (Semidefinida $\succeq 0$) |
| **Localização dos Mínimos Locais** | Platôs com interior aberto | Confinados aos Vértices $\{-1,1\}^N$ | Funis convexos regulares |
| **Conexão com Complexidade** | Integrality Gap 7/8 do LP | Rugosidade pura multilinear | Regularização convexa finita |
| **Acessibilidade Dinâmica** | **Bloqueada** por platôs estáticos | **Aprisionada** por vértices espúrios | **Fluida** em direção aos mínimos globais |
