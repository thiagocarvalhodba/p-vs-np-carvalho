# Lema 10.5 — Convergência do Fluxo Projetado em Componentes Arbóreas

## Enunciado

Seja K uma componente arbórea finita e Φ = Φ_K sua extensão multilinear em X_K = [-1,1]^{V(K)}. Considere

    ẋ = Π_{T_X(x)}(-∇Φ(x)).

Então **toda** trajetória do fluxo projetado converge a um equilíbrio projetado de energia zero. Em particular, para toda inicialização x₀ ∈ X_K, existe um vértice booleano satisfatível na face limite contendo o equilíbrio; sob a convenção de arredondamento do Teorema 4A′, o resultado é uma atribuição satisfatível.

Este lema é mais forte que a formulação anterior de “quase toda trajetória”: não é necessário um argumento de medida-zero para eliminar equilíbrios positivos.

## Prova

### 1. O PDS é um fluxo subgradiente com restrição convexa

Defina a função estendida

    F(x) = Φ(x) + δ_X(x),

onde δ_X é o indicador de X. Como X é o hipercubo fechado e convexo, a condição de primeira ordem para o equilíbrio projetado é

    0 ∈ ∇Φ(x*) + N_X(x*).

Equivalentemente, a dinâmica projetada pode ser escrita como a inclusão subgradiente

    ẋ(t) + N_X(x(t)) ∋ -∇Φ(x(t)),

isto é, ẋ(t) ∈ -∂F(x(t)). Para o hipercubo, esta é exatamente a forma normal-cone do PDS. A literatura de PDS caracteriza seus equilíbrios por variational inequalities e pela condição de normal cone. Cojocaru estabelece a formulação por cones tangentes/normais; Nagurney–Zhang e trabalhos posteriores tratam a equivalência com sistemas de complementaridade.

### 2. Convergência de toda trajetória por KL — sem argumento de troca de face

F é próprio, limitado inferiormente, fechado e semialgébrico: Φ é polinomial e X é semialgébrico. Portanto F é uma função KL/subanalítica.

A energia satisfaz, para quase todo t,

    dΦ(x(t))/dt = -||ẋ(t)||² ≤ 0.

Como X é compacto, toda trajetória é limitada. A teoria de subgradient flows para funções subanalíticas/KL implica então que uma trajetória limitada tem comprimento total finito e converge a um único ponto crítico de F. Esta é precisamente a situação tratada por Bolte–Daniilidis–Lewis: a desigualdade de Łojasiewicz é estendida ao subdiferencial e, sob a regularidade aplicável, trajetórias limitadas do sistema subgradiente têm comprimento finito e convergem.

Portanto não precisamos mais decompor a trajetória em uma sequência de faces nem introduzir mapas de impacto. A mudança de face já está incorporada na inclusão normal-cone ẋ ∈ -∂F.

### 3. Nenhum equilíbrio projetado de energia positiva em uma componente arbórea

Suponha, por absurdo, que x* seja um equilíbrio projetado com Φ(x*) > 0.

Como

    Φ(x*) = Σ_{c∈K} P_c(x*),

com P_c(x) = ∏_{j∈c}(1-σ_j^c x_j)/2 ≥ 0, existe uma cláusula violada c tal que P_c(x*) > 0.

Como K é uma hiperfloresta, c possui uma variável folha ℓ, isto é, deg_K(ℓ)=1.

Como P_c(x*) > 0, temos

    (1 - σ_ℓ^c x_ℓ*)/2 > 0,

logo x_ℓ* ≠ σ_ℓ^c.

Além disso, ℓ não aparece em nenhuma outra cláusula. Consequentemente, a derivada em relação a ℓ recebe contribuição somente de c:

    ∂_ℓ Φ(x*) = -(σ_ℓ^c/2) ∏_{j∈c\{ℓ}} (1-σ_j^c x_j*)/2.

Como P_c(x*) > 0, todos os fatores do produto são positivos; portanto

    σ_ℓ^c ∂_ℓ Φ(x*) < 0.

Há dois casos:

**Caso A — x_ℓ* ∈ (-1,1).** Então a direção ℓ pertence integralmente ao cone tangente. Logo a projeção do campo possui componente

    σ_ℓ^c ẋ_ℓ* = -σ_ℓ^c ∂_ℓ Φ(x*) > 0,

e portanto x* não é equilíbrio.

**Caso B — x_ℓ* = -σ_ℓ^c.** Esta é a única possibilidade de fronteira compatível com P_c(x*) > 0. A direção factível no ponto -σ_ℓ^c é precisamente o semieixo σ_ℓ^c. Como

    σ_ℓ^c ẋ_ℓ* = -σ_ℓ^c ∂_ℓ Φ(x*) > 0,

o campo projetado aponta estritamente para o interior do cubo. Portanto x* também não é equilíbrio.

Assim, nenhum equilíbrio projetado positivo pode existir em uma componente arbórea:

    E_proj(K) ⊆ {x : Φ(x)=0}.

Observe que esta conclusão é estritamente mais forte que L10.2 + L10.3: aqueles lemas classificam críticos relativos em faces; o argumento da folha exclui diretamente **todos os KKT/PDS positivos**, inclusive os localizados no bordo.

### 4. O equilíbrio limite é uma solução booleana

Pelo item 2, x(t) → x* e Φ(x*) = 0. Como Φ é uma extensão multilinear não negativa, x* é um mínimo global de Φ sobre X.

Considere a menor face G de X que contém x*. A extensão multilinear em G é a combinação multilinear dos valores nos vértices de G. Como Φ(x*)=0 e todos os valores nos vértices são não negativos, todo vértice de G com peso positivo na representação de x* também tem energia zero.

Em particular, existe um vértice v ∈ {−1,+1}^{V(K)} com

    Φ(v)=E_disc(v)=0.

Esse v é uma atribuição satisfatível da componente. Pelo Teorema 4A′, a estrutura de mínimo local na face é compatível com a identidade vértice–energia usada no arredondamento.

□

## Consequência dinâmica

O argumento anterior elimina completamente a necessidade da passagem

    strict saddle → bacia de medida zero → quase toda trajetória.

Também elimina a necessidade de provar que mapas de impacto entre faces preservam conjuntos nulos. Isso seria uma rota frágil para PDS: ao contrário de um ODE suave, o mapa de fluxo de um PDS pode não ser invertível depois que uma trajetória atinge a fronteira. A literatura de sistemas projetados registra explicitamente essa possibilidade.

A rota correta para este T10 é portanto:

    componente arbórea
        → existência de folha em toda cláusula
        → nenhum equilíbrio projetado positivo
        → F = Φ + δ_X é KL/semialgébrica
        → toda trajetória limitada do subgradient flow converge
        → equilíbrio de energia zero
        → solução booleana.

Isso é mais forte e tecnicamente mais limpo do que o argumento estratificado anterior.

## Referências externas

- M.-G. Cojocaru, *Nonpivot and Implicit Projected Dynamical Systems on Hilbert Spaces* (2012): cones tangentes/normais e formulação de PDS.
- J. Bolte, A. Daniilidis & A. Lewis, *The Łojasiewicz inequality for nonsmooth subanalytic functions with applications to subgradient dynamical systems*, SIAM Journal on Optimization 17 (2007), 1205–1223, DOI 10.1137/050644641: extensão da desigualdade de Łojasiewicz ao subdiferencial e convergência de trajetórias subgradientes limitadas sob hipóteses de regularidade.
- P.-A. Absil & K. Kurdyka, *On the stable equilibrium points of gradient systems*, Systems & Control Letters 55 (2006), 573–577, DOI 10.1016/j.sysconle.2006.01.002: estabilidade versus minimalidade para fluxos gradiente analíticos.
- A literatura de PDS também mostra que o mapa de fluxo em conjuntos com fronteira pode não ser invertível; por isso a prova atual não depende de preservar medida zero por pré-imagens de mapas de impacto.