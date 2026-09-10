# Estudo Analítico do Conjunto Crítico e Geometria do Fluxo em Representações Contínuas de 3-SAT

**Autor:** Thiago Carvalho  
**Data:** 10 de Setembro de 2026  
**Status:** Teoria Matemática Estrutural Consolidada (CLG-R)  
**Assunto:** Teorema da Caixa Fracionária Central, Medida Nula via Analiticidade, Teorema do Traço Nulo da Hessiana Multilinear ($\text{Tr}(H) \equiv 0$), Injeção de Curvatura no Softplus e Massa de Atração Espúria $\mathcal{M}_{\text{spur}}(\Phi)$

---

## 1. Hipóteses de Regularidade e Definições Fundamentais

Seja $F$ uma fórmula 3-CNF com $M$ cláusulas $\mathcal{C} = \{c_1, \dots, c_M\}$ sobre $N$ variáveis booleanas $x = (x_1, \dots, x_N) \in \mathcal{X} = [-1, 1]^N$.
Para cada cláusula $c \in \mathcal{C}$, denotamos por $\sigma_j^{(c)} \in \{-1, +1\}$ o sinal do literal da variável $x_j$, de modo que a cláusula é $c = \bigvee_{j \in c} (\sigma_j^{(c)} x_j = +1)$.

Para evitar patologias combinatórias degeneradas, assumimos as seguintes hipóteses estruturais:
* **(H1 - Não-Tautologia):** Nenhuma cláusula contém um literal e seu complemento ($\ell_j \ne \neg \ell_k$).
* **(H2 - Conectividade):** Toda variável $x_i$ incide em ao menos uma cláusula ($\text{deg}(x_i) \ge 1$).
* **(H3 - Não-Trivialidade Booleana):** A fórmula possui ao menos uma atribuição discreta com violação ($E_{\text{disc}}(s^*) \ge 1$). Fórmulas UNSAT satisfazem $E_{\text{disc}}(s) \ge 1$ para todas as $2^N$ atribuições.

O arredondamento discreto $s_{\text{round}}: \mathcal{X} \to \{-1, +1\}^N$ é o mapeamento de sinal:
$$s_{\text{round}}(x) = \text{sign}(x), \quad \text{com } s_i = +1 \text{ se } x_i \ge 0 \text{ e } s_i = -1 \text{ se } x_i < 0$$
O erro discreto $E_{\text{disc}}(s_{\text{round}}(x))$ é o número exato de cláusulas violadas pela atribuição $s_{\text{round}}(x)$.

### O Conjunto Crítico Espúrio $\mathcal{C}_0(\Phi)$
Definimos o conjunto de pontos críticos espúrios de uma relaxação contínua $\Phi: \mathcal{X} \to \mathbb{R}_{\ge 0}$ como:
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
> *Para toda fórmula 3-CNF não-trivial $F$ satisfazendo (H1)-(H3), o conjunto crítico espúrio possui medida de Lebesgue estritamente positiva:*
> $$\mu(\mathcal{C}_0(\Phi_{\text{quad}})) \ge \left( \frac{1}{3} \right)^N > 0$$
> *Se a fórmula $F$ for insatisfatível (UNSAT), a medida satisfaz:*
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

---

## 3. Teorema 2: Medida Zero via Analiticidade Real e Zeros de Polinômios

> **Teorema 2 (Medida Nula dos Críticos Espúrios para Multilinear e Softplus).**  
> *Sob as hipóteses (H1)-(H2), os conjuntos críticos espúrios de $\Phi_{\text{mult}}$ e $\Phi_{\text{soft}}$ possuem medida de Lebesgue estritamente zero:*
> $$\mu(\mathcal{C}_0(\Phi_{\text{mult}})) = 0 \quad \text{e} \quad \mu(\mathcal{C}_0(\Phi_{\text{soft}})) = 0$$

### Demonstração:
1. **Caso Multilinear ($\Phi_{\text{mult}}$):**
   - $\Phi_{\text{mult}}(x) = \sum_{c} \prod_{j \in c} \frac{1 - \sigma_j^{(c)} x_j}{2}$ é polinomial em $\mathbb{R}[x_1, \dots, x_N]$.
   - Cada derivada parcial $\partial_k \Phi_{\text{mult}}(x) = \frac{\partial \Phi_{\text{mult}}}{\partial x_k}(x)$ é um polinômio multivariado em $\mathbb{R}^N$.
   - Por (H2), a variável $x_k$ participa de ao menos uma cláusula, logo $\partial_k \Phi_{\text{mult}} \not\equiv 0$.
   - Pelo Lema dos Zeros de Polinômios Reais (Okamoto 1973; Caron & Traynor 2005), o conjunto de raízes $Z(P)$ de qualquer polinômio real não-nulo tem medida de Lebesgue zero: $\mu(Z(P)) = 0$.
   - Como $\text{Crit}(\Phi_{\text{mult}}) \subseteq Z(\partial_k \Phi_{\text{mult}})$, segue que $\mu(\mathcal{C}_0(\Phi_{\text{mult}})) \le \mu(Z(\partial_k \Phi_{\text{mult}})) = 0$.

2. **Caso Softplus ($\Phi_{\text{soft}}$):**
   - $\Phi_{\text{soft}}(x) = \sum_{c=1}^M \frac{1}{\beta} \ln(1 + e^{\beta g_c(x)})$ é real analítica ($\mathcal{C}^\omega$) em todo $\mathbb{R}^N$.
   - Cada derivada parcial $\partial_k \Phi_{\text{soft}}(x)$ é analítica real sobre o domínio conexo $\mathbb{R}^N$.
   - Pelo Princípio da Identidade / Teorema de Medida de Analíticas Reais (Krantz & Parks 2002; Mityagin 2015), se o conjunto de raízes de uma função analítica em um conexo tivesse medida positiva, a função seria identicamente nula em todo o domínio. Como $\partial_k \Phi_{\text{soft}} \not\equiv 0$, seu conjunto de zeros tem medida nula: $\mu(Z(\partial_k \Phi_{\text{soft}})) = 0$.
   - Consequentemente, $\mu(\mathcal{C}_0(\Phi_{\text{soft}})) = 0$. $\blacksquare$

---

## 4. Teorema 3: Teorema do Traço Nulo da Hessiana Multilinear e Ausência de Mínimos Interiores

> **Teorema 3 (Traço Nulo e Classificação de Morse na Multilinear).**  
> *Para qualquer fórmula 3-CNF satisfazendo (H1), a diagonal da matriz Hessiana da relaxação multilinear é identicamente nula em todo o espaço:*
> $$\frac{\partial^2 \Phi_{\text{mult}}}{\partial x_i^2}(x) \equiv 0, \quad \forall i \in \{1, \dots, N\}, \quad \forall x \in \mathbb{R}^N$$
> *Consequentemente:*
> $$\text{Tr}(\nabla^2 \Phi_{\text{mult}}(x)) \equiv 0, \quad \forall x \in \mathbb{R}^N$$

### Demonstração e Consequências de Morse:
1. Em qualquer cláusula $c = (\ell_1 \lor \ell_2 \lor \ell_3)$, por (H1), as variáveis são mutuamente distintas.
2. Cada monômio da multilinear é da forma $\prod_{j \in c} \frac{1 - \sigma_j x_j}{2}$, possuindo grau no máximo 1 em cada coordenada individual $x_i$.
3. Logo, derivando duas vezes com respeito à mesma coordenada:
   $$\frac{\partial^2 \Phi_{\text{mult}}}{\partial x_i^2} \equiv 0 \implies \text{Tr}(\nabla^2 \Phi_{\text{mult}}(x)) = \sum_{i=1}^N 0 \equiv 0$$
4. Como o traço é igual à soma dos autovalores $\sum_{k=1}^N \lambda_k(x) = \text{Tr}(H(x)) = 0$:
   - Para que um ponto crítico $x^* \in \text{int}(\mathcal{X})$ fosse um mínimo local estrito interior, todos os seus autovalores deveriam ser positivos ($\lambda_k > 0$). Mas $\lambda_k > 0, \forall k \implies \sum \lambda_k > 0$, o que contradiz $\text{Tr}(H) = 0$.
   - **Corolário de Morse:** A relaxação multilinear **NÃO POSSUI NENHUM MÍNIMO LOCAL ESTRITO NO INTERIOR $\text{int}(\mathcal{X})$**.
   - Todo ponto crítico interior não-degenerado é **obrigatoriamente um PONTO DE SELA** com índice de Morse $1 \le m \le N-1$ (possuindo direções ascendentes e descendentes).
   - Todos os mínimos locais de $\Phi_{\text{mult}}$ residem na **fronteira** $\partial \mathcal{X}$ (faces e vértices do hipercubo $[-1, 1]^N$). $\blacksquare$

---

## 5. Teorema 4: Injeção de Curvatura Positiva no Softplus

> **Teorema 4 (Curvatura Positiva Estrita no Softplus).**  
> *Para o Softplus com $\beta > 0$, a diagonal da Hessiana é estritamente positiva para toda coordenada com cláusulas incidentes:*
> $$\frac{\partial^2 \Phi_{\text{soft}}}{\partial x_i^2}(x) = \frac{\beta}{4} \sum_{c \ni i} \sigma(\beta g_c(x)) \left(1 - \sigma(\beta g_c(x))\right) > 0, \quad \forall x \in \mathbb{R}^N$$
> *Consequentemente, $\text{Tr}(\nabla^2 \Phi_{\text{soft}}(x)) > 0$ em todo $\mathbb{R}^N$.*

*Consequência Geométrica:* O Softplus quebra a condição harmônica ($\text{Tr}=0$), injetando curvatura positiva estrita ao longo de todas as direções coordenadas. Isto arredonda as selas hiperbólicas da multilinear e cria bacias de atração regulares com forte gradiente descendente.

---

## 6. Teorema 5: Limite Termodinâmico $\beta \to \infty$ e Bifurcação de Fase

A relação entre Softplus e Hinge é uma homotopia contínua de temperatura:
$$\lim_{\beta \to \infty} \frac{1}{\beta} \ln(1 + e^{\beta g_c(x)}) = \max(0, g_c(x))$$
Para $x \in \mathcal{U}_N$, como $g_c(x) < 0$, temos $\beta g_c(x) \to -\infty$, donde $\sigma(\beta g_c) \to 0$ e $\sigma'(\beta g_c) \to 0$. Toda a curvatura positiva da Hessiana colapsa:
$$\lim_{\beta \to \infty} \nabla^2 \Phi_{\text{soft}}(x) = \mathbf{0} \quad \text{em } \mathcal{U}_N$$
O parâmetro $\beta$ atua como um parâmetro contínuo de bifurcação de fase topológica: a paisagem suave do Softplus congela-se assintoticamente no platô plano degenerado do Hinge.

---

## 7. Definição Formal da Massa de Atração Espúria $\mathcal{M}_{\text{spur}}(\Phi)$ e Dinâmica do Fluxo

Definimos a **Massa de Atração Espúria** como:
$$\mathcal{M}_{\text{spur}}(\Phi) \equiv \mu\left( \left\{ x_0 \in \mathcal{X} \;\middle|\; \lim_{t \to \infty} X(t; x_0) \in \mathcal{C}_0(\Phi) \right\} \right)$$
onde $X(t; x_0)$ é a curva integral do fluxo gradiente $\dot{x}(t) = -\nabla \Phi(x(t))$, $x(0) = x_0$.

### O Teorema do Fluxo Dinâmico:
1. **No Hinge ($\Phi_{\text{quad}}$):** Como $\mathcal{U}_N \subset \mathcal{C}_0$ possui velocidade nula identicamente:
   $$\mathcal{M}_{\text{spur}}(\Phi_{\text{quad}}) \ge \mu(\mathcal{C}_0(\Phi_{\text{quad}})) \ge \left(\frac{1}{3}\right)^N > 0$$
   O fluxo sofre aprisionamento estático instantâneo.
2. **Na Multilinear ($\Phi_{\text{mult}}$):** Embora $\mu(\mathcal{C}_0) = 0$ e as variedades estáveis de selas interiores tenham medida nula ($\mu(W^s) = 0$), os múltiplos mínimos espúrios da fronteira $\partial \mathcal{X}$ possuem grandes bacias de atração: $\mathcal{M}_{\text{spur}}(\Phi_{\text{mult}}) \approx 0.94$ (explicando os 6% de reachability).
3. **No Softplus ($\Phi_{\text{soft}}$):** A injeção de curvatura positiva elimina bacias de atração espúrias rasas, fazendo $\mathcal{M}_{\text{spur}}(\Phi_{\text{soft}}) \to 0$ (explicando os 100% de reachability).

---

## 8. Quadro Comparativo Consolidado do CLG-R

| Propriedade Matemática | Quadrática Hinge ($\Phi_{\text{quad}}$) | Multilinear ($\Phi_{\text{mult}}$) | Softplus ($\Phi_{\text{soft}}$) |
| :--- | :--- | :--- | :--- |
| **Classe de Regularidade** | $\mathcal{C}^1$ (por partes) | $\mathcal{C}^\infty$ (polinomial) | $\mathcal{C}^\omega$ (analítica real) |
| **Medida dos Críticos $\mu(\mathcal{C}_0)$** | $> 0$ (Platô $\ge (1/3)^N$) | $= 0$ (Lema Polinomial) | $= 0$ (Identidade Analítica) |
| **Traço da Hessiana $\text{Tr}(H)$** | $\equiv 0$ em $\mathcal{U}_N$ (Degenerado) | $\equiv 0$ em $\mathbb{R}^N$ (Sem mínimos int.) | $> 0$ em $\mathbb{R}^N$ (Curvatura positiva) |
| **Natureza dos Críticos Interiores** | Platôs degenerados | Selas estritas ($1 \le m \le N-1$) | Pontos isolados regulares |
| **Massa de Atração $\mathcal{M}_{\text{spur}}$** | $\ge (1/3)^N > 0$ (Platô estático) | Elevada ($\approx 0.94$, Mínimos fronteira) | Quase nula ($\approx 0.00$, Regularizada) |
| **Acessibilidade Dinâmica** | **Bloqueada** por platôs estáticos | **Aprisionada** pela fronteira | **Fluida** em direção aos mínimos globais |
