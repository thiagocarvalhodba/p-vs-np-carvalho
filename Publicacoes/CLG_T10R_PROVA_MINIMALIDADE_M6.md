# T10R — Prova formal independente da minimalidade M6

**Data:** 22 de setembro de 2026  
**Escopo:** hiperárvores conexas, lineares, 3-uniformes e Berge-acíclicas.  
**Relaxação:** energia multilinear natural de 3-SAT com fluxo de gradiente projetado no hipercubo.  
**Resultado:**

[
oxed{m_{*,HT}^{mathrm{mult}}=6.}
]

Este documento registra uma derivação independente da minimalidade. A prova evita completamente identificação finita de face, exclusão geral de Zeno, mapas de impacto, argumentos de variedade estável, Hessianas irrestritas no bordo e cascatas dimensionais por Liouville.

A estratégia usa apenas: convergência pontual do PDS via teoria KL/subgradiente; contagem exata das cláusulas positivas em um equilíbrio; existência forçada de um ramo unitário quando (mle5); monotonicidade global de uma variável-folha; e o certificado construtivo M6 já existente.

## 1. Coordenadas de fatores

Fixe uma orientação global por variável e use coordenadas (z_vin[0,1]). Para cada ocorrência literal na cláusula (c), o fator correspondente é

[
ell_{cv}(z_v)in{z_v,1-z_v}.
]

A energia é

[
Phi(z)=sum_{cin E}P_c(z),
qquad
P_c(z)=prod_{vin c}ell_{cv}(z_v).
]

Cada (P_c) é multilinear e não negativo em ([0,1]^n).

O fluxo projetado é, a menos de uma constante positiva de reparametrização temporal proveniente da mudança afim (xleftrightarrow z),

[
dot z
=
Pi_{T_{[0,1]^n}(z)}(-
ablaPhi(z)).
]

Para (z_v=0), a condição KKT é (partial_vPhige0); para (0<z_v<1), (partial_vPhi=0); para (z_v=1), (partial_vPhile0).

## 2. Convergência de toda trajetória para um equilíbrio

Defina

[
F(z)=Phi(z)+delta_X(z),
qquad
X=[0,1]^n.
]

Como (Phi) é polinomial e (X) é semialgébrico compacto, (F) é própria, l.s.c. e semialgébrica.

Para

[
d(z)=Pi_{T_X(z)}(-
ablaPhi(z)),
]

a decomposição ortogonal de Moreau fornece

[
-
ablaPhi(z)=d(z)+n(z),
qquad
n(z)in N_X(z),
qquad
langle d(z),n(z)angle=0.
]

Portanto

[
-d(z)in
ablaPhi(z)+N_X(z)=partial F(z).
]

Além disso,

[
|d(z)|
=
operatorname{dist}(-
ablaPhi(z),N_X(z))
=
operatorname{dist}(0,partial F(z)).
	ag{2.1}
]

Ao longo de uma solução absolutamente contínua,

[
rac{d}{dt}Phi(z(t))
=
langle
ablaPhi(z(t)),dot z(t)angle
=
-|dot z(t)|^2
quad	ext{a.e.}
	ag{2.2}
]

A teoria de Kurdyka--Łojasiewicz para funções subanalíticas/semialgébricas l.s.c., aplicada ao sistema subgradiente correspondente, implica comprimento finito para trajetórias limitadas. Como (X) é compacto, toda trajetória é limitada e então

[
int_0^infty |dot z(t)|,dt<infty.
]

Consequentemente (z(t)) é Cauchy e existe

[
z(t)longrightarrow z^infty.
]

Pela inclusão subgradiente, pela dissipação e pelo fechamento do gráfico de (partial F),

[
0inpartial F(z^infty)
=

ablaPhi(z^infty)+N_X(z^infty).
]

Logo toda trajetória converge a um único equilíbrio projetado.

**Fonte primária:** J. Bolte, A. Daniilidis, A. Lewis, *The Łojasiewicz Inequality for Nonsmooth Subanalytic Functions with Applications to Subgradient Dynamical Systems*, SIAM J. Optim. 17 (2007), 1205--1223, DOI 10.1137/050644641. A aplicação usa a regularidade de (F=Phi+delta_X), a compacidade da caixa, (2.1) e (2.2).

## 3. Cláusulas positivas e derivadas de cláusulas nulas

Fixe um equilíbrio (z^*) com

[
Phi(z^*)>0.
]

Chame (c) de **cláusula positiva** se

[
P_c(z^*)>0.
]

Existe ao menos uma.

### Lema 3.1 — cláusula nula não atua numa coordenada livre

Se (0<z_v^*<1) e (P_c(z^*)=0), então

[
partial_vP_c(z^*)=0.
]

**Prova.** O fator (ell_{cv}(z_v^*)) é estritamente positivo. Como o produto da cláusula é zero, algum outro fator da cláusula é zero. Esse fator continua presente após derivar em relação a (z_v), anulando a derivada. (square)

Assim, numa coordenada livre, somente cláusulas positivas podem contribuir ao gradiente.

## 4. Quantas folhas existem no sub-hipergrafo positivo

Considere uma componente conexa do sub-hipergrafo formado apenas pelas cláusulas positivas. Se ela contém (t) cláusulas, então, por ser 3-uniforme e Berge-acíclica,

[
|V|=2t+1.
	ag{4.1}
]

Se (L) é o número de variáveis de grau 1 dentro dessa componente positiva, então

[
Lge t+2.
	ag{4.2}
]

De fato,

[
sum_{vin V}(deg_+(v)-1)
=
3t-(2t+1)
=
t-1.
]

Cada variável com grau positivo pelo menos 2 contribui ao menos 1 para essa soma. Portanto existem no máximo (t-1) variáveis com grau (ge2), e

[
L
ge
(2t+1)-(t-1)
=
t+2.
]

Se o sub-hipergrafo positivo tem várias componentes, somando componente a componente obtemos uma desigualdade ainda mais forte. Em particular, se o número total de cláusulas positivas é (t),

[
Lge t+2.
	ag{4.3}
]

## 5. Cada folha positiva exige uma cláusula restauradora distinta

Escolha uma variável (v) que aparece em exatamente uma cláusula positiva. Oriente a coordenada (u_vin[0,1]) para que o fator dessa única cláusula positiva seja (u_v).

Como a cláusula é positiva,

[
u_v^*>0.
]

Pelo Lema 3.1, (v) não pode estar no interior: se estivesse, a única cláusula positiva produziria uma derivada não nula e nenhuma cláusula nula poderia cancelá-la. Portanto

[
u_v^*=1.
]

A cláusula positiva empurra (u_v) para o interior. Para satisfazer KKT no bordo superior, é necessária pelo menos uma cláusula nula com derivada restauradora não nula.

Numa cláusula nula, a derivada em relação a (u_v) só pode ser não nula quando o fator de (v) é o **único** fator zero da cláusula. Portanto a mesma cláusula nula não pode restaurar simultaneamente duas variáveis distintas: se tivesse dois fatores zero, a derivada em qualquer um ainda conteria o outro fator zero.

Logo as (L) folhas do sub-hipergrafo positivo exigem pelo menos (L) cláusulas nulas distintas.

Se (m) é o número total de cláusulas,

[
m-tge L.
]

Com (4.3),

[
m
ge
t+L
ge
2t+2.
	ag{5.1}
]

Se (tge2), então

[
mge6.
]

Portanto:

[
oxed{mle5Longrightarrow t=1.}
	ag{5.2}
]

Todo equilíbrio de energia positiva numa hiperárvore com no máximo cinco cláusulas possui exatamente uma cláusula positiva.

## 6. Estrutura forçada quando há uma única cláusula positiva

Seja a única cláusula positiva (C_0). Oriente seus três fatores como

[
C_0=y_1y_2y_3.
]

Pela mesma razão anterior, nenhuma das três coordenadas pode ser livre. Como (C_0) é positiva, segue

[
y_1^*=y_2^*=y_3^*=1.
	ag{6.1}
]

Cada (y_i) precisa de uma cláusula restauradora distinta. Logo já são necessárias quatro cláusulas:

[
C_0+A_1+A_2+A_3.
]

Ao remover (C_0) do grafo de incidência, a árvore se separa em três ramos, um por variável (y_i). Cada ramo contém pelo menos sua cláusula restauradora.

Se (mle5), há no máximo quatro cláusulas fora de (C_0). Distribuídas em três ramos não vazios:

- para (m=4), os tamanhos são ((1,1,1));
- para (m=5), os tamanhos são ((1,1,2)) após permutação.

Em particular existe ao menos um **ramo unitário**.

Escolha o ramo unitário ligado a (y). Sua única cláusula adicional precisa ter fator complementar em (y), pois somente esse sinal fornece derivada restauradora no ponto (y^*=1). Depois de orientar as duas folhas,

[
A_y=(1-y)ab.
	ag{6.2}
]

Como o ramo contém somente (A_y), as variáveis (a,b) são folhas globais de grau 1.

## 7. A folha monotônica força bacia de medida zero

No equilíbrio,

[
y^*=1.
]

A derivada em (y) contém somente a contribuição da cláusula positiva e da única cláusula do ramo unitário:

[
partial_yPhi(z^*)
=
1-a^*b^*.
	ag{7.1}
]

Como (y^*=1) está no bordo superior, KKT exige

[
partial_yPhi(z^*)le0.
]

Logo

[
a^*b^*ge1.
]

Como (a^*,b^*in[0,1]),

[
oxed{a^*=b^*=1.}
	ag{7.2}
]

Agora use que (a) é folha global. Ela aparece apenas em (A_y), então em todo o hipercubo

[
partial_aPhi=(1-y)bge0.
]

Assim a velocidade projetada satisfaz

[
oxed{dot a(t)le0}
	ag{7.3}
]

para todo (t).

Portanto (a(t)) é globalmente não crescente.

Se uma trajetória converge ao equilíbrio positivo acima, (7.2) exige

[
a(t)	o1.
]

Uma função não crescente com valores em ([0,1]) só pode convergir para 1 se já começar em 1:

[
a(0)=1.
	ag{7.4}
]

Logo a bacia desse equilíbrio está contida no hiperplano de coordenada

[
{a=1},
]

que tem medida de Lebesgue ambiente zero.

## 8. União sobre todos os equilíbrios positivos

A escolha do ramo unitário ou da cláusula positiva pode depender do equilíbrio, mas a instância possui apenas finitas cláusulas e variáveis-folha.

Para cada possibilidade de cláusula positiva (C), fixe uma folha (a_C) pertencente a um ramo unitário cuja existência foi demonstrada acima.

Se

[
mathcal B_+
=
{z_0:Phi(z^infty(z_0))>0},
]

então

[
mathcal B_+
subseteq
igcup_C{a_C(0)=1}.
	ag{8.1}
]

A união é finita. Cada conjunto do lado direito é uma face afim de codimensão 1. Portanto

[
oxed{operatorname{Leb}(mathcal B_+)=0.}
	ag{8.2}
]

Essa conclusão independe do número de trocas de faces sofridas pela trajetória antes de convergir.

## 9. Energia contínua zero implica erro discreto zero após rounding

Se

[
Phi(z^infty)=0,
]

como cada (P_cge0), temos

[
P_c(z^infty)=0
]

para toda cláusula.

Logo, em cada cláusula, ao menos um fator literal vale exatamente zero. Isso significa que a variável correspondente está exatamente no endpoint booleano que satisfaz aquele literal.

Qualquer arredondamento compatível com os endpoints mantém a cláusula satisfeita. Portanto

[
Phi(z^infty)=0
Longrightarrow
E_{mathrm{disc}}(operatorname{round}(z^infty))=0.
	ag{9.1}
]

Assim toda bacia ruim está contida em (mathcal B_+), que possui medida zero para (mle5).

Conclui-se:

[
oxed{m_{*,HT}^{mathrm{mult}}ge6.}
	ag{9.2}
]

## 10. Certificado M6 e igualdade

O documento principal de auditoria já contém um motivo M6 explícito, linear, 3-uniforme e Berge-acíclico, com uma face positiva de energia 1 e um aberto de condições iniciais capturado em tempo finito.

Consequentemente,

[
oxed{m_{*,HT}^{mathrm{mult}}le6.}
	ag{10.1}
]

Com (9.2),

[
oxed{oxed{m_{*,HT}^{mathrm{mult}}=6.}}
]

## 11. O que esta prova não usa

A minimalidade acima não depende de exclusão de Zeno em PDS multilineares, identificação finita da variedade ativa, uma face final atingida em tempo finito, preservação de volume entre faces, argumentos de coárea em mapas de hitting, teoremas de variedade estável ou espectro da Hessiana irrestrita.

Mesmo que uma trajetória execute infinitas sequências de hit, stick e release, a prova permanece válida: ela usa apenas a convergência pontual (z(t)	o z^infty) e a monotonicidade global de uma folha forçada pela combinatória de (mle5).

## 12. Status

**Teorema T10R-M6 (minimalidade hiperarbórea): PROVADO.**

Na classe de hiperárvores conexas, lineares, 3-uniformes e Berge-acíclicas, seis cláusulas são necessárias e suficientes para a existência de uma bacia ruim aberta de medida de Lebesgue positiva para a relaxação multilinear projetada.

Este teorema é um resultado sobre a dinâmica dessa relaxação contínua. Ele não implica (mathbf P=mathbf{NP}), (mathbf P
emathbf{NP}), nem resolve o problema P versus NP.
