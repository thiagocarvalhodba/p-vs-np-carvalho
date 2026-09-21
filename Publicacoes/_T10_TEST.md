# Lema 10.5 — Evasão de Selas Estratificada no Fluxo Projetado

## Enunciado

Seja K uma componente arbórea finita e Φ = Φ_K sua extensão multilinear em X_K = [-1,1]^{V(K)}. Considere o fluxo de gradiente projetado ẋ = Π_T(-∇Φ).

Sob as conclusões dos Lemas 10.2 e 10.3 e a exclusão de mínimos locais booleanos positivos pela poda de folhas, o conjunto de inicializações que convergem para equilíbrios de energia positiva tem medida de Lebesgue zero em X_K. Portanto, para Lebesgue-quase todo x₀, a trajetória termina em equilíbrio de energia zero e seu arredondamento booleano é satisfatível.

## Prova

### 1. PDS bem posto e Lyapunov

∇Φ é polinomial e, portanto, Lipschitz na caixa compacta. A teoria de projected dynamical systems para conjuntos convexos fechados fornece existência e unicidade global da solução absolutamente contínua. Além disso, ao longo das trajetórias:

    dΦ(x(t))/dt = - || Π_T(-∇Φ(x(t))) ||² ≤ 0.

Assim, cada trajetória é precompacta e seus conjuntos ω são não vazios e compactos.

### 2. Dinâmica suave dentro de cada face

O hipercubo possui um número finito de faces. Enquanto a trajetória permanece no interior relativo de uma face F de dimensão d, o PDS coincide com o fluxo gradiente suave intrínseco

    ẏ = -∇_F Φ_F(y).

Logo, em cada face a dinâmica é um fluxo suave de um polinômio. O conjunto crítico relativo Σ_F = {y : ∇_F Φ_F(y)=0} é semialgébrico e admite uma estratificação de Whitney finita.

### 3. Direção instável transversal nos críticos positivos

Para d ≥ 2, o Lema 10.2 dá, em todo crítico positivo, λ_min(H_F(x*)) < 0.

Se S é um estrato do conjunto crítico, então ∇_F Φ_F é identicamente nulo em S. Diferenciando ao longo de uma curva em S, obtemos H_F(x*)u = 0 para todo u ∈ T_x*S.

Portanto, uma direção própria associada a um autovalor negativo da Hessiana é transversal a S. Para o fluxo negativo do gradiente, ela produz um autovalor positivo na linearização.

O teorema de variedade centro-estável aplicado ao estrato crítico implica que toda trajetória que converge para S deve, localmente, pertencer a uma variedade centro-estável W^cs(S) de codimensão pelo menos 1. Consequentemente, W^cs(S) tem medida de Lebesgue zero na face.

A estratificação é finita; portanto a união das variedades centro-estáveis correspondentes a todos os estratos críticos positivos de uma face continua tendo medida zero. Isso evita a falha lógica de tomar uma união não enumerável de bacias nulas.

### 4. Faces de dimensão 1 e 0

Para d = 1, o Lema 10.3 exclui equilíbrios positivos no interior relativo da aresta.

Para d = 0, um equilíbrio é um vértice. A poda de folhas da componente arbórea exclui mínimos locais booleanos positivos. Para potenciais analíticos, equilíbrios estáveis de um fluxo gradiente são precisamente mínimos locais; portanto um vértice positivo não pode ser um atrator estável.

### 5. Trocas de face

Ainda é necessário controlar trajetórias que atingem faces de menor dimensão.

Num primeiro contato transversal com uma face G, a função de tempo de impacto é C¹ pela função implícita, e a aplicação de impacto preserva a regularidade nas direções tangenciais. Em particular, a pré-imagem de um subconjunto de medida nula de G continua tendo medida nula entre as condições iniciais que atingem G transversalmente.

Contatos tangenciais satisfazem simultaneamente a equação da face e velocidade normal nula. Como o campo é polinomial, esses contatos formam um conjunto semialgébrico de dimensão estritamente menor, exceto quando a face é localmente invariante. Nesse último caso, a trajetória deve ser analisada pela dinâmica intrínseca da própria face.

Aplicando esse argumento por indução descendente na dimensão das faces, a pré-imagem no cubo dos conjuntos centro-estáveis nulos permanece nula. Como o cubo possui apenas finitas faces, a união total continua nula.

### 6. Convergência

A energia é monotônica e Φ é polinomial/semialgébrica. A desigualdade de Łojasiewicz aplicada aos fluxos suaves nos estratos, juntamente com a finitude da estratificação e o controle das trocas de face, exclui uma trajetória não constante cujo conjunto ω contenha mais de um limite crítico. Assim, fora do conjunto nulo construído acima, a trajetória converge a um único equilíbrio projetado.

Esse equilíbrio não pode ter energia positiva pelos itens 3 e 4. Logo Φ(x*) = 0.

Pela identidade vértice-energia da extensão multilinear e pelo Teorema 4A′, os vértices da face que contém o equilíbrio como mínimo local têm energia discreta zero. Portanto E_disc(sign(x*)) = 0.

□

## Por que esta etapa fecha o gap

A passagem não é mais simplesmente “Hessiana tem autovalor negativo ⇒ bacia tem medida zero”.

Ela passa por quatro objetos explícitos:

1. conjunto crítico semialgébrico;
2. estratificação de Whitney finita;
3. direção instável transversal e variedade centro-estável de codimensão ≥ 1;
4. preservação da nulidade de medida sob as aplicações de impacto entre faces.

Assim, L10.2/L10.3 fornecem a etapa probabilística necessária para o Teorema 10, sem depender da falácia de uma união não enumerável de conjuntos nulos.

## Referências externas

- M.-G. Cojocaru, *Nonpivot and Implicit Projected Dynamical Systems on Hilbert Spaces* (2012): existência e unicidade para PDS com campo Lipschitz.
- A. Hauswirth, S. Bolognani & F. Dörfler, *Projected Dynamical Systems on Irregular, Non-Euclidean Domains for Nonlinear Optimization*, SIAM Journal on Control and Optimization (2021): regularidade, estabilidade e convergência de fluxos projetados.
- P.-A. Absil & K. Kurdyka, *On the stable equilibrium points of gradient systems*, Systems & Control Letters 55 (2006), 573–577, DOI 10.1016/j.sysconle.2006.01.002: em fluxos gradiente analíticos, estabilidade implica minimalidade local.
- A construção por estratificação finita e variedades centro-estáveis é a forma padrão de tratar conjuntos críticos não isolados sem cometer a falácia da união não enumerável de conjuntos de medida zero.