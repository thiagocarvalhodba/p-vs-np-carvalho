# Contraexemplo de bacia positiva em hiperárvore linear de 7 cláusulas

**Data:** 21 de setembro de 2026  
**Status:** certificado analítico exato; refuta a afirmação determinística “quase toda trajetória em toda hiperárvore linear converge para energia zero”.

## 1. Estrutura

Use três variáveis centrais (a,b,c) e, para cada (rin{a,b,c}), quatro folhas (p_{r,1},q_{r,1},p_{r,2},q_{r,2}).

As sete cláusulas são

[
C_0=(alor blor c),
]

e, para cada (rin{a,b,c}),

[
C_{r,1}=(
eg rlor p_{r,1}lor q_{r,1}),
qquad
C_{r,2}=(
eg rlor p_{r,2}lor q_{r,2}).
]

O hipergrafo é 3-uniforme, linear e acíclico. Seu grafo de incidência tem
(15+7=22) vértices e (21) arestas de incidência; é conexo, logo é uma árvore.

## 2. Coordenadas locais no vértice (-mathbf 1)

Escreva

[
x_r=-1+u_r,qquad
x_{p_{r,j}}=-1+y_{r,j},qquad
x_{q_{r,j}}=-1+z_{r,j},
]

com todas as novas coordenadas em ([0,2]).

Defina

[
A_{r,j}:=left(1-rac{y_{r,j}}2ight)
          left(1-rac{z_{r,j}}2ight),
qquad
B_r:=A_{r,1}+A_{r,2}.
]

A energia multilinear fica exatamente

[
Phi=
prod_{rin{a,b,c}}left(1-rac{u_r}{2}ight)
+sum_{rin{a,b,c}}rac{u_r}{2}B_r.
]

Em particular, em (u=y=z=0),

[
Phi=1.
]

## 3. Gradiente central e equilíbrio projetado positivo

Para cada variável central (r),

[
rac{partialPhi}{partial u_r}
=
-rac12prod_{s
e r}left(1-rac{u_s}{2}ight)
+rac12 B_r.
]

No vértice (-mathbf 1), (B_r=2), portanto

[
rac{partialPhi}{partial u_r}=rac12>0.
]

Nas folhas,

[
rac{partialPhi}{partial y_{r,j}}
=
-rac{u_r}{4}left(1-rac{z_{r,j}}2ight),
qquad
rac{partialPhi}{partial z_{r,j}}
=
-rac{u_r}{4}left(1-rac{y_{r,j}}2ight),
]

logo todas se anulam no vértice.

Como (u_r=0) corresponde à face inferior (x_r=-1), a condição de equilíbrio projetado é
(partial_{u_r}Phige0). Assim (-mathbf1) é um equilíbrio projetado positivo com (Phi=1).

Diferentemente do exemplo de 4 cláusulas, aqui a primeira variação nas três coordenadas centrais é estritamente positiva. Os termos quadráticos negativos provenientes das cláusulas exatamente-1-satisfeitas não invalidam o mínimo relativo, pois o termo linear domina localmente.

## 4. Um aberto explícito atraído para energia positiva

Considere o aberto

[
U=
left{
0<u_a,u_b,u_c<rac14,quad
0<y_{r,j},z_{r,j}<rac18
ight}.
]

Mostraremos que toda trajetória iniciada em (U) atinge em tempo finito o conjunto estacionário

[
mathcal M=
left{
u_a=u_b=u_c=0,quad
0le y_{r,j},z_{r,j}<rac14
ight},
]

onde (Phiequiv1).

Suponha provisoriamente que todas as folhas permaneçam abaixo de (1/4).
Então

[
A_{r,j}geleft(1-rac18ight)^2=rac{49}{64},
qquad
B_rgerac{49}{32}.
]

Além disso,

[
prod_{s
e r}left(1-rac{u_s}{2}ight)le1.
]

Logo, enquanto (u_r>0),

[
rac{partialPhi}{partial u_r}
ge
rac12left(rac{49}{32}-1ight)
=
rac{17}{64}.
]

No interior, o PDS coincide coordenadamente com o gradiente negativo, portanto

[
dot u_r
=
-rac{partialPhi}{partial u_r}
le-rac{17}{64}.
]

Assim cada (u_r) atinge zero em tempo no máximo

[
T_rle
rac{1/4}{17/64}
=
rac{16}{17}.
]

Uma folha satisfaz

[
0le dot y_{r,j}
=
rac{u_r}{4}left(1-rac{z_{r,j}}2ight)
lerac1{16},
]

e analogamente para (z_{r,j}). Durante um intervalo de comprimento no máximo (16/17), seu aumento é no máximo

[
rac1{16}rac{16}{17}
=
rac1{17}.
]

Como inicialmente cada folha é menor que (1/8),

[
y_{r,j}(t),z_{r,j}(t)
<
rac18+rac1{17}
=
rac{25}{136}
<
rac14.
]

Isto fecha o bootstrap: a hipótese usada para obter a cota do gradiente é preservada por toda a trajetória até os centros atingirem o bordo.

Quando (u_r=0), as velocidades de suas quatro folhas zeram. Além disso, como as folhas permanecem abaixo de (1/4),

[
rac{partialPhi}{partial u_r}
gerac{17}{64}>0,
]

de modo que a projeção no cone tangente mantém (u_r=0) para sempre.

Após tempo no máximo (16/17), temos

[
u_a=u_b=u_c=0,
]

todas as folhas param, e

[
Phi=1.
]

Portanto (U) é um subconjunto aberto da bacia de um conjunto de equilíbrios projetados positivos.

## 5. Medida positiva

O aberto (U) tem medida de Lebesgue positiva em dimensão 15.

Sob inicialização uniforme em ([-1,1]^{15}), uma cota explícita para sua probabilidade é

[
mathbb P(x_0in U)
=
left(rac{1/4}{2}ight)^3
left(rac{1/8}{2}ight)^{12}
=
2^{-57}>0.
]

Essa cota é deliberadamente pequena e não pretende aproximar a bacia total; basta sua positividade.

## 6. Falha discreta após rounding

No conjunto limite, (a=b=c=-1). Logo a cláusula central

[
(alor blor c)
]

continua violada após arredondamento de sinal. As seis cláusulas periféricas permanecem satisfeitas pelo literal negado central.

Assim cada trajetória iniciada em (U) produz pelo menos uma cláusula discreta violada.

## 7. Consequência lógica

Este certificado é mais forte que o contraexemplo de 4 cláusulas:

- o exemplo (m=4) refutava apenas “todo equilíbrio positivo tem energia zero”, mas tinha bacia singleton;
- o exemplo (m=7) possui uma **bacia aberta de medida positiva** e termina em energia positiva.

Logo é falsa a afirmação determinística

[
operatorname{Leb}
{x_0:lim_{t	oinfty}Phi(x(t;x_0))>0}=0
]

para toda hiperárvore linear 3-uniforme.

Para converter isto em refutação assintótica completa da formulação aleatória de T10, resta apenas registrar formalmente a contagem padrão de componentes isoladas de um tipo fixo de hiperárvore no ensemble (mathcal E(N,alpha)). Para qualquer (alpha>0) fixo no regime subcrítico, a expectativa de cópias isoladas desse tipo é linear em (N); com a concentração apropriada, a probabilidade positiva (2^{-57}) da bacia por componente gera densidade residual positiva, embora extremamente pequena.

## 8. Falha precisa no Lema D1 proposto pelo relatório Gemini

O argumento “um termo Hessiano negativo no cone tangente contradiz estabilidade” é inválido quando a primeira variação nessa direção é estritamente positiva.

As condições de segunda ordem devem ser impostas no **cone crítico**, isto é, nas direções factíveis onde a primeira variação se anula.

Neste exemplo, cada variável central recebe uma contribuição (-1/2) da cláusula central violada e duas contribuições (+1/2) das cláusulas periféricas exatamente-1-satisfeitas, deixando gradiente total (+1/2). Essa margem linear estabiliza a aproximação ao bordo, apesar dos termos Hessianos cruzados negativos.

Esse é exatamente o mecanismo que transforma a sela (m=4) em uma armadilha positiva (m=7).
