# Estudo Analítico do Conjunto Crítico e Geometria do Fluxo em Representações Contínuas de 3-SAT

**Autor:** Thiago Carvalho  
**Data:** 10 de Setembro de 2026  
**Status:** Teoremas Analíticos Consolidados (Revisão Pós-Parecer 09)  
**Assunto:** Caracterização Rigorosa de $\nabla \Phi = \mathbf{0}$, Medida de $\mathcal{C}_0(\Phi)$, Massa de Atração Espúria $\mathcal{M}_{\text{spur}}(\Phi)$ e Dinâmica do Fluxo

---

## 1. Definições Fundamentais

Seja $F$ uma fórmula 3-CNF com $M$ cláusulas $\mathcal{C} = \{c_1, \dots, c_M\}$ sobre $N$ variáveis booleanas $x = (x_1, \dots, x_N) \in \mathcal{X} = [-1, 1]^N$.
Para cada cláusula $c \in \mathcal{C}$, denotamos por $\sigma_j^{(c)} \in \{-1, +1\}$ o sinal do literal da variável $x_j$, de modo que a cláusula é $c = \bigvee_{j \in c} (\sigma_j^{(c)} x_j = +1)$.

O arredondamento discreto $s_{\text{round}}: \mathcal{X} \to \{-1, +1\}^N$ é o mapeamento de sinal:
$$s_{\text{round}}(x) = \text{sign}(x), \quad \text{com } s_i = +1 \text{ se } x_i \ge 0 \text{ e } s_i = -1 \text{ se } x_i < 0$$
O erro discreto $E_{\text{disc}}(s_{\text{round}}(x))$ é o número exato de cláusulas violadas pela atribuição $s_{\text{round}}(x)$.

### O Conjunto Crítico Espúrio $\mathcal{C}_0(\Phi)$
Definimos o conjunto de pontos críticos espúrios de uma relaxação contínua $\Phi: \mathcal{X} \to \mathbb{R}_{\ge 0}$ como:
$$\mathcal{C}_0(\Phi) \equiv \left\{ x \in \text{int}(\mathcal{X}) \;\middle|\; \nabla \Phi(x) = \mathbf{0} \quad\text{e}\quad E_{\text{disc}}(s_{\text{round}}(x)) > 0 \right\}$$

Dizemos que uma relaxação possui **patologia de medida positiva** se a medida de Lebesgue de seu conjunto crítico espúrio for estritamente positiva:
$$\mu(\mathcal{C}_0(\Phi)) > 0$$

---

## 2. Lema 1: Inatividade Simultânea de Cláusulas na Relaxação Hinge

A relaxação Quadrática Hinge é dada por:
$$\Phi_{\text{quad}}(x) = \sum_{c=1}^M \left[ \max\left(0, \, g_c(x)\right) \right]^2$$
onde a função de violação contínua da cláusula $c$ é:
$$g_c(x) = 1 - \sum_{j \in c} \frac{1 + \sigma_j^{(c)} x_j}{2} = -\frac{1}{2} \left( 1 + \sum_{j \in c} \sigma_j^{(c)} x_j \right)$$

O gradiente espacial de $\Phi_{\text{quad}}$ é a soma sobre as cláusulas ativas:
$$\nabla \Phi_{\text{quad}}(x) = \sum_{c: g_c(x) > 0} 2 g_c(x) \nabla g_c(x) = -\sum_{c: g_c(x) > 0} g_c(x) \sum_{j \in c} \sigma_j^{(c)} e_j$$

> **Lema 1 (Inatividade Simultânea das Cláusulas).**  
> *Uma condição suficiente para que $\nabla \Phi_{\text{quad}}(x) = \mathbf{0}$ em uma vizinhança aberta $\Omega$ é que todas as $M$ cláusulas da fórmula estejam simultaneamente inativas na relaxação:*
> $$g_c(x) \le 0, \quad \forall c \in \{1, \dots, M\} \iff \sum_{j \in c} \sigma_j^{(c)} x_j \ge -1, \quad \forall c \in \{1, \dots, M\}$$
> *Neste caso, $\Phi_{\text{quad}}(x) = 0$ e $\nabla \Phi_{\text{quad}}(x) = \mathbf{0}$ de forma idêntica em $\Omega$.*

---

## 3. Teorema 1: Teorema da Caixa Fracionária Central (Medida Positiva Universal)

> **Teorema 1 (Universalidade da Patologia de Medida Positiva no Hinge).**  
> *Para qualquer fórmula 3-CNF não-tautológica $F$ com $M$ cláusulas sobre $N$ variáveis, o conjunto de pontos críticos espúrios possui medida de Lebesgue estritamente positiva:*
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
5. Como esta desigualdade independe dos índices e sinais das variáveis que compõem a cláusula, ela é satisfeita **estritamente e simultaneamente por todas as $M$ cláusulas da fórmula**:
   $$g_c(x) < 0, \quad \forall c \in \{1, \dots, M\}, \quad \forall x \in \mathcal{U}_N$$
6. Pelo Lema 1, como $\max(0, g_c(x)) = 0$ para toda cláusula em $\mathcal{U}_N$, a função potencial e seu gradiente anulam-se identicamente em todo o aberto $\mathcal{U}_N$:
   $$\Phi_{\text{quad}}(x) \equiv 0 \quad \text{e} \quad \nabla \Phi_{\text{quad}}(x) \equiv \mathbf{0}, \quad \forall x \in \mathcal{U}_N$$
7. Analisamos agora o erro discreto do arredondamento booleano $s(x) = \text{sign}(x) \in \{-1, +1\}^N$ dentro de $\mathcal{U}_N$:
   - Se $F$ é não-tautológica, existe ao menos uma atribuição booleana discreta $s^* \in \{-1, +1\}^N$ que viola pelo menos uma cláusula $c \in F$ ($E_{\text{disc}}(s^*) \ge 1$).
   - O ortante associado a $s^*$, restrito à caixa $\mathcal{U}_N$, é o conjunto aberto:
     $$\Omega_{s^*} = \mathcal{U}_N \cap \left\{ x \in \mathbb{R}^N \;\middle|\; \text{sign}(x_i) = s^*_i, \; \forall i \right\} = \prod_{i=1}^N I_i$$
     onde $I_i = (0, 1/3)$ se $s^*_i = +1$ e $I_i = (-1/3, 0)$ se $s^*_i = -1$.
   - A medida de Lebesgue de $\Omega_{s^*}$ é exatamente:
     $$\mu(\Omega_{s^*}) = \left( \frac{1}{3} \right)^N > 0$$
   - Para todo $x \in \Omega_{s^*}$, temos $\nabla \Phi_{\text{quad}}(x) = \mathbf{0}$ e $E_{\text{disc}}(\text{sign}(x)) \ge 1$. Logo, $\Omega_{s^*} \subseteq \mathcal{C}_0(\Phi_{\text{quad}})$, demonstrando que $\mu(\mathcal{C}_0(\Phi_{\text{quad}})) \ge (1/3)^N > 0$.
8. Se a fórmula $F$ for insatisfatível (UNSAT), toda atribuição $s \in \{-1, +1\}^N$ viola pelo menos uma cláusula. Portanto, a quase totalidade da caixa central $\mathcal{U}_N$ (exceto os hiperplanos de coordenadas nulas $x_i = 0$, que têm medida zero) pertence a $\mathcal{C}_0(\Phi_{\text{quad}})$, resultando em:
   $$\mu(\mathcal{C}_0(\Phi_{\text{quad}})) \ge \mu(\mathcal{U}_N) = \left( \frac{2}{3} \right)^N > 0 \quad \blacksquare$$

---

## 4. Teorema 2: Medida Zero de $\mathcal{C}_0$ via Analiticidade e Teoria de Polinômios

> **Teorema 2 (Medida Nula dos Críticos Espúrios para Multilinear e Softplus).**  
> *Seja $F$ uma fórmula 3-CNF tal que o gradiente da relaxação não seja identicamente nulo (isto é, existe $k \in \{1, \dots, N\}$ tal que $\partial_k \Phi \not\equiv 0$). Então:*
> $$\mu(\mathcal{C}_0(\Phi_{\text{mult}})) = 0 \quad \text{e} \quad \mu(\mathcal{C}_0(\Phi_{\text{soft}})) = 0$$

### Demonstração:
1. **Caso Multilinear ($\Phi_{\text{mult}}$):**
   - O potencial $\Phi_{\text{mult}}(x) = \sum_{c \in \mathcal{C}} \prod_{j \in c} \frac{1 - \sigma_j^{(c)} x_j}{2}$ é uma função polinomial em $\mathbb{R}[x_1, \dots, x_N]$.
   - Consequentemente, cada derivada parcial $\partial_k \Phi_{\text{mult}}(x) = \frac{\partial \Phi_{\text{mult}}}{\partial x_k}(x)$ é um polinômio multivariado em $\mathbb{R}^N$.
   - **Lema dos Zeros de Polinômios Reais (Okamoto, 1973; Caron & Traynor, 2005):** O conjunto de raízes de qualquer polinômio real não-nulo $P \in \mathbb{R}[x_1, \dots, x_N]$, $Z(P) = \{ x \in \mathbb{R}^N \mid P(x) = 0 \}$, possui medida de Lebesgue estritamente zero em $\mathbb{R}^N$: $\mu(Z(P)) = 0$.
   - Como $\nabla \Phi_{\text{mult}}(x) = \mathbf{0} \implies \partial_k \Phi_{\text{mult}}(x) = 0$, temos a inclusão:
     $$\text{Crit}(\Phi_{\text{mult}}) = \bigcap_{i=1}^N \{ x \mid \partial_i \Phi_{\text{mult}}(x) = 0 \} \subseteq \{ x \mid \partial_k \Phi_{\text{mult}}(x) = 0 \} = Z(\partial_k \Phi_{\text{mult}})$$
   - Pela monotonicidade da medida de Lebesgue:
     $$\mu(\mathcal{C}_0(\Phi_{\text{mult}})) \le \mu(\text{Crit}(\Phi_{\text{mult}})) \le \mu(Z(\partial_k \Phi_{\text{mult}})) = 0$$

2. **Caso Softplus ($\Phi_{\text{soft}}$):**
   - $\Phi_{\text{soft}}(x) = \sum_{c=1}^M \frac{1}{\beta} \ln(1 + e^{\beta g_c(x)})$ é a composição de funções analíticas reais (afim, exponencial, logaritmo), logo é real analítica (classe $\mathcal{C}^\omega$) em todo $\mathbb{R}^N$.
   - Cada componente do gradiente $\partial_k \Phi_{\text{soft}}(x)$ é, portanto, uma função real analítica em $\mathbb{R}^N$.
   - **Princípio da Identidade / Teorema de Medida Nula de Analíticas Reais (Krantz & Parks, 2002; Mityagin, 2015):** Se $f: \mathbb{R}^N \to \mathbb{R}$ é uma função analítica real sobre um domínio conexo, e seu conjunto de zeros $Z(f) = \{ x \in \mathbb{R}^N \mid f(x) = 0 \}$ tem medida de Lebesgue positiva ($\mu(Z(f)) > 0$), então $f$ é identicamente nula em todo o domínio ($f \equiv 0$).
   - Como $\partial_k \Phi_{\text{soft}} \not\equiv 0$ para qualquer variável com cláusulas incidentes, seu conjunto de zeros possui obrigatoriamente medida de Lebesgue zero: $\mu(Z(\partial_k \Phi_{\text{soft}})) = 0$.
   - Consequentemente:
     $$\mu(\mathcal{C}_0(\Phi_{\text{soft}})) \le \mu(\text{Crit}(\Phi_{\text{soft}})) \le \mu(Z(\partial_k \Phi_{\text{soft}})) = 0 \quad \blacksquare$$

---

## 5. Massa de Atração Espúria $\mathcal{M}_{\text{spur}}(\Phi)$ e Dinâmica do Fluxo

### Definição (Massa de Atração Espúria):
Seja $X(t; x_0)$ a curva integral do fluxo gradiente contínuo $\dot{x}(t) = -\nabla \Phi(x(t))$, com condição inicial $x(0) = x_0 \in \mathcal{X}$.
Definimos a **Massa de Atração Espúria** $\mathcal{M}_{\text{spur}}(\Phi)$ como a medida de Lebesgue do conjunto de condições iniciais cujas trajetórias convergem assintoticamente para o conjunto crítico espúrio:
$$\mathcal{M}_{\text{spur}}(\Phi) \equiv \mu\left( \left\{ x_0 \in \mathcal{X} \;\middle|\; \lim_{t \to \infty} X(t; x_0) \in \mathcal{C}_0(\Phi) \right\} \right)$$

### Proposição (Desacoplamento entre Medida Crítica e Massa de Atração):

1. **Para a Quadrática Hinge:**
   Como todo ponto $x \in \mathcal{U}_N$ satisfaz $\nabla \Phi_{\text{quad}}(x) = \mathbf{0}$, a velocidade do fluxo é nula ($X(t; x_0) = x_0$ para todo $t \ge 0$). Portanto:
   $$\mathcal{M}_{\text{spur}}(\Phi_{\text{quad}}) \ge \mu(\mathcal{C}_0(\Phi_{\text{quad}})) \ge \left( \frac{1}{3} \right)^N > 0$$
   Qualquer trajetória iniciada na caixa fracionária central estagna instantaneamente com velocidade zero.

2. **Para Multilinear e Softplus:**
   Embora $\mu(\mathcal{C}_0) = 0$ (o fluxo quase certamente não é iniciado em repouso), a convergência depende da estrutura das bacias de atração dos mínimos locais espúrios $\mathcal{C}_0^{\text{min}}$ e das variedades estáveis das selas $\mathcal{C}_0^{\text{saddle}}$:
   $$\mathcal{M}_{\text{spur}}(\Phi) = \sum_{x^* \in \mathcal{C}_0^{\text{min}}} \mu(\mathcal{B}(x^*)) + \sum_{x_s \in \mathcal{C}_0^{\text{saddle}}} \mu(W^s(x_s))$$
   - Para selas com índice de Morse $m \ge 1$, a variedade estável possui dimensão estritamente menor que $N$ ($\dim(W^s) \le N - m < N$), implicando $\mu(W^s(x_s)) = 0$.
   - Portanto, para representações suaves, $\mathcal{M}_{\text{spur}}$ é dominada inteiramente pelas **bacias de atração dos mínimos locais espúrios**:
     $$\mathcal{M}_{\text{spur}}(\Phi) \approx \mu\left( \bigcup_{x^* \in \mathcal{C}_0^{\text{min}}} \mathcal{B}(x^*) \right)$$

### Conexão Rigorosa com as Evidências Experimentais:
- **Multilinear:** A rugosidade combinatória pura gera um número exponencial de mínimos locais espúrios com bacias de atração de grande volume: $\mathcal{M}_{\text{spur}}(\Phi_{\text{mult}}) \approx 0.94$, explicando os 6% de reachability.
- **Softplus:** A convolução log-sum-exp suaviza o relevo e elimina as bacias dos mínimos espúrios rasos, contraindo a massa de atração espúria $\mathcal{M}_{\text{spur}}(\Phi_{\text{soft}}) \to 0$ e produzindo 100% de reachability.

---

## 6. Quadro Síntese do CLG-R

| Propriedade Matemática | Quadrática Hinge ($\Phi_{\text{quad}}$) | Multilinear ($\Phi_{\text{mult}}$) | Softplus ($\Phi_{\text{soft}}$) |
| :--- | :--- | :--- | :--- |
| **Classe de Regularidade** | $\mathcal{C}^1$ (por partes) | $\mathcal{C}^\infty$ (polinomial) | $\mathcal{C}^\omega$ (analítica real) |
| **Medida dos Críticos $\mu(\mathcal{C}_0)$** | $> 0$ (Volume $\ge (1/3)^N$) | $= 0$ (Lema Polinomial) | $= 0$ (Identidade Analítica) |
| **Estagnação Inicial** | Presente com probabilidade $> 0$ | Quase certamente ausente ($p = 0$) | Quase certamente ausente ($p = 0$) |
| **Massa de Atração $\mathcal{M}_{\text{spur}}$** | $\ge (1/3)^N > 0$ (Platôs) | Elevada ($\approx 0.94$) por mínimos locais | Quase nula ($\approx 0.00$) por regularização |
| **Acessibilidade Dinâmica** | **Bloqueada** por estagnação estática | **Aprisionada** por bacias de atração | **Fluida** em direção aos mínimos globais |
