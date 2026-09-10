# Estudo Analítico do Conjunto Crítico e Geometria Dinâmica do Fluxo

**Autor:** Thiago Carvalho  
**Data:** 10 de Setembro de 2026  
**Ambiente:** `C:\MathDoCarvalho\P_NP` | [GitHub Repository](https://github.com/thiagocarvalhodba/p-vs-np-carvalho)  
**Status:** Monografia Analítica Formal de Apoio Teórico ao CLG-R

---

## 1. Definição do Problema e Notação

Seja $I = (N, M, \mathcal{C})$ uma fórmula booleana 3-CNF com $N$ variáveis e $M$ cláusulas. Denotamos por $\mathcal{V} = \{-1, +1\}^N$ os vértices discretos do hipercubo $\mathcal{X} = [-1, 1]^N$, e por $S(I) = \{ v \in \mathcal{V} \mid E_{\text{disc}}(v) = 0 \}$ o conjunto de soluções satisfatíveis.

Para qualquer estado contínuo $x \in \mathcal{X}$, a atribuição discreta correspondente é dada pelo operador de sinal:
$$s_{\text{round}}(x) = \text{sign}(x) \in \mathcal{V}, \quad \text{com } s_i = 1 \text{ se } x_i = 0$$

O erro discreto $E_{\text{disc}}(s_{\text{round}}(x))$ é o número exato de cláusulas violadas por $s_{\text{round}}(x)$.

### O Conjunto Crítico Espúrio $\mathcal{C}_0(\Phi)$
Definimos o conjunto de pontos críticos espúrios de uma relaxação contínua $\Phi: \mathcal{X} \to \mathbb{R}_{\ge 0}$ como:
$$\mathcal{C}_0(\Phi) \equiv \left\{ x \in \text{int}(\mathcal{X}) \;\middle|\; \nabla \Phi(x) = \mathbf{0} \quad\text{e}\quad E_{\text{disc}}(s_{\text{round}}(x)) > 0 \right\}$$

Dizemos que uma relaxação sofre de **estagnação de medida positiva** se a medida de Lebesgue do conjunto crítico espúrio for estritamente não-nula:
$$\mu(\mathcal{C}_0(\Phi)) > 0$$

---

## 2. Teorema 1: A Patologia de Medida Positiva da Quadrática Hinge

Consideremos a relaxação Quadrática Hinge (Sum-of-Squares relaxada):
$$\Phi_{\text{quad}}(x) = \sum_{c \in \mathcal{C}} \left[ \max\left(0, \, g_c(x)\right) \right]^2$$
onde $g_c(x) = 1 - \sum_{j \in c} \frac{1 + \sigma_j^{(c)} x_j}{2}$.

O gradiente espacial em qualquer ponto onde $g_c(x) \ne 0$ é dado por:
$$\nabla_i \Phi_{\text{quad}}(x) = -\sum_{c \ni i, \, g_c(x) > 0} g_c(x) \sigma_i^{(c)}$$

> **Teorema 1 (Existência de Platôs Críticos Espúrios de Medida Positiva).**  
> *Para qualquer fórmula 3-CNF não-trivial, existe uma região aberta $\Omega \subset \text{int}(\mathcal{X})$ com medida de Lebesgue $\mu(\Omega) > 0$ tal que, para todo $x \in \Omega$:*
> $$\nabla \Phi_{\text{quad}}(x) \equiv \mathbf{0} \quad\text{e}\quad E_{\text{disc}}(s_{\text{round}}(x)) \ge 1$$
> *Consequentemente, $\mu(\mathcal{C}_0(\Phi_{\text{quad}})) > 0$.*

### Demonstração Construtiva Passo a Passo:
1. Seja $c_1 = (x_1 \lor x_2 \lor x_3)$ uma cláusula da fórmula (com $\sigma_1 = \sigma_2 = \sigma_3 = +1$).
2. A função de violação associada é:
   $$g_{c_1}(x) = 1 - \left( \frac{1+x_1}{2} + \frac{1+x_2}{2} + \frac{1+x_3}{2} \right) = -\frac{1}{2}(x_1 + x_2 + x_3 + 1)$$
3. A cláusula contribui com violação nula no hinge se e somente se $g_{c_1}(x) \le 0$, o que equivale ao semi-espaço:
   $$\mathcal{H}_{c_1} = \left\{ x \in \mathbb{R}^N \;\middle|\; x_1 + x_2 + x_3 \ge -1 \right\}$$
4. Por outro lado, o arredondamento booleano $s_{\text{round}}(x)$ viola a cláusula $c_1$ se e somente se todas as três variáveis tiverem coordenadas estritamente negativas:
   $$\mathcal{O}_{c_1} = \left\{ x \in \mathbb{R}^N \;\middle|\; x_1 < 0, \; x_2 < 0, \; x_3 < 0 \right\}$$
5. A interseção $\Omega_{c_1} = \mathcal{H}_{c_1} \cap \mathcal{O}_{c_1}$ é o poliedro aberto definido por:
   $$\Omega_{c_1} = \left\{ x \in \mathbb{R}^N \;\middle|\; -1 \le x_1 + x_2 + x_3 < 0 \quad\text{com}\quad x_1, x_2, x_3 \in (-1, 0) \right\}$$
6. Para qualquer $x \in \Omega_{c_1}$ (por exemplo, o ponto central $x^* = (-0.2, -0.2, -0.2)$):
   - $x_1 + x_2 + x_3 = -0.6 \ge -1 \implies g_{c_1}(x) \le 0 \implies \max(0, g_{c_1}(x)) = 0$. A cláusula $c_1$ tem gradiente nulo: $\nabla g_{c_1} \equiv \mathbf{0}$.
   - Contudo, $s_{\text{round}}(x^*) = (-1, -1, -1)$, que viola estritamente a cláusula booleana $c_1$ ($E_{\text{disc}} \ge 1$).
7. Como $\Omega_{c_1}$ contém uma bola euclidiana aberta de raio $\epsilon = 0.1$ em torno de $x^*$, sua medida de Lebesgue satisfaz:
   $$\mu(\Omega_{c_1}) \ge \text{Vol}(B_\epsilon^N) > 0$$
8. Portanto, todo o conjunto $\Omega$ forma um platô exatamente plano onde o campo vetorial do gradiente é identicamente nulo ($\dot{x} = -\nabla \Phi_{\text{quad}}(x) = \mathbf{0}$), paralisando qualquer dinâmica de primeira ordem em estados onde a solução booleana é falsa. $\blacksquare$

---

## 3. Teorema 2: Medida Nula dos Conjuntos Críticos nas Relaxações Analíticas

Consideremos agora as relaxações $\mathcal{C}^\infty$ / analíticas reais ($\mathcal{C}^\omega$): a **Multilinear** ($\Phi_{\text{mult}}$) e a **Softplus** ($\Phi_{\text{soft}}$).

### 3.1 O Caso Multilinear ($\Phi_{\text{mult}}$)
$$\Phi_{\text{mult}}(x) = \sum_{c \in \mathcal{C}} \prod_{j \in c} \frac{1 - \sigma_j^{(c)} x_j}{2}$$

A $i$-ésima componente do gradiente é um polinômio quadrático em $x$:
$$\nabla_i \Phi_{\text{mult}}(x) = -\frac{1}{2} \sum_{c \ni i} \sigma_i^{(c)} \prod_{j \in c \setminus \{i\}} \frac{1 - \sigma_j^{(c)} x_j}{2}$$

> **Proposição 2.1 (Variedade Algébrica Crítica da Multilinear).**  
> *Para qualquer fórmula onde cada variável $x_i$ participa de ao menos uma cláusula, $\nabla \Phi_{\text{mult}}(x) \not\equiv \mathbf{0}$ em $\mathbb{R}^N$. O conjunto crítico:*
> $$\text{Crit}(\Phi_{\text{mult}}) = \left\{ x \in \mathbb{R}^N \;\middle|\; \nabla_1 \Phi_{\text{mult}}(x) = 0, \dots, \nabla_N \Phi_{\text{mult}}(x) = 0 \right\}$$
> *é uma variedade algébrica afim real de dimensão topológica $\le N-1$.*  
> *Pelo Teorema de Medida de Variedades Algébricas Reais (Whitney, 1957), tem-se estritamente:*
> $$\mu(\text{Crit}(\Phi_{\text{mult}})) = 0 \implies \mu(\mathcal{C}_0(\Phi_{\text{mult}})) = 0$$

### 3.2 O Caso Softplus ($\Phi_{\text{soft}}$)
$$\Phi_{\text{soft}}(x) = \sum_{c \in \mathcal{C}} \frac{1}{\beta} \ln\left(1 + \exp\left(\beta g_c(x)\right)\right)$$

A derivada espacial é dada por:
$$\nabla_i \Phi_{\text{soft}}(x) = -\frac{1}{2} \sum_{c \ni i} \sigma_i^{(c)} \sigma\left(\beta g_c(x)\right), \quad \text{com } \sigma(z) = \frac{1}{1 + e^{-z}}$$

> **Proposição 2.2 (Analiticidade Real e Medida Nula no Softplus).**  
> *A função $\Phi_{\text{soft}}$ é analítica real ($\mathcal{C}^\omega$) em todo $\mathbb{R}^N$. Pelo Teorema da Identidade para Funções Analíticas Conexas (Krantz & Parks, 2002), se o conjunto de zeros de um campo analítico $F(x) = \nabla \Phi_{\text{soft}}(x) = \mathbf{0}$ possuísse medida de Lebesgue positiva ($\mu(Z(F)) > 0$), então $F$ deveria ser identicamente nulo em todo o $\mathbb{R}^N$.*  
> *Como $\nabla_i \Phi_{\text{soft}}(x)$ varia estritamente com $x$ ao longo das direções normais aos hiperplanos de cláusula, $\nabla \Phi_{\text{soft}} \not\equiv \mathbf{0}$. Consequentemente:*
> $$\mu(\text{Crit}(\Phi_{\text{soft}})) = 0 \implies \mu(\mathcal{C}_0(\Phi_{\text{soft}})) = 0$$

---

## 4. O Teorema da Geometria Dinâmica da Representação

Podemos agora estabelecer formalmente a cadeia causal que conecta a representação à acessibilidade dinâmica:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   A CADEIA CAUSAL DE CLG-R                             │
└────────────────────────────────────────────────────────────────────────┘
  Representação Contínua Φ(x)
       │
       ▼
  Topologia e Medida do Conjunto Crítico Espúrio C_0(Φ)
       │
       ├─► [Quadrática Hinge]: μ(C_0) > 0  (Platô com interior aberto)
       │     └─► Fluxo colide com ponto crítico espúrio com probabilidade > 0
       │
       └─► [Softplus / Multilinear]: μ(C_0) = 0  (Variedade de codimensão >= 1)
             └─► Trajetórias quase certamente não colidem com platôs abertos;
                 Acessibilidade governada pelo campo vetorial e selas
```

> **Teorema 3 (Teorema de Bloqueio Dinâmico por Medida Positiva).**  
> *Seja $\mathcal{D}_{\text{GD}}$ o fluxo contínuo de descida de gradiente $\dot{x} = -\nabla \Phi(x)$ iniciado sob distribuição absolutamente contínua $x_0 \sim \mu_0$ no hipercubo $\mathcal{X}$.*  
> 1. *Para a relaxação Quadrática Hinge, existe probabilidade estritamente positiva de captura imediata em platôs espúrios:*
>    $$P_{x_0 \sim \mu_0}\left( x_0 \in \mathcal{C}_0(\Phi_{\text{quad}}) \right) \ge \mu(\Omega) > 0$$
>    *onde a velocidade instantânea colapsa a zero ($\|\dot{x}\| = 0$) enquanto $E_{\text{disc}} \ge 1$.*
> 2. *Para as relaxações Softplus e Multilinear, o conjunto de pontos críticos espúrios tem medida nula ($\mu(\mathcal{C}_0) = 0$). O fluxo gradiente possui velocidade estritamente não-nula quase em toda parte:*
>    $$P_{x_0 \sim \mu_0}\left( \|\nabla \Phi(x_0)\| = 0 \right) = 0$$

### Consequência Teórica Formal:
Este teorema demonstra no papel o mecanismo analítico que os experimentos da Fase II revelaram: a relaxação Quadrática Hinge falha não por mero desbalanceamento de constante de passo ($\eta$), mas porque sua topologia introduz **subvariedades de gradiente identicamente nulo com interior aberto** onde o discrete rounding é falso, criando aprisionamento absoluto de medida positiva.

Por outro lado, o Softplus e a Multilinear preservam $\mu(\mathcal{C}_0) = 0$, transferindo a navegabilidade para a suavidade das bacias e o condicionamento hessiano $\kappa_2(H)$.
