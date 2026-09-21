# Contraexemplo M7 compartilhado: armadilha positiva dentro do 2-core

**Data:** 21 de setembro de 2026  
**Status:** certificado analítico exato.

Este exemplo preserva as 7 cláusulas do mecanismo M7, mas compartilha as 12
posições foliares em apenas 6 variáveis, todas com polaridade positiva. Isso
eleva todas as folhas a grau 2 sem alterar o mecanismo de aprisionamento do
PDS.

## Estrutura

Centros: \(a,b,c\). Folhas compartilhadas:
\(\ell_0,\ldots,\ell_5\).

Cláusula central:
\[
C_0=(a\lor b\lor c).
\]

Periféricas:
\[
\begin{aligned}
A_1&=(\neg a\lor \ell_5\lor \ell_0),\\
B_1&=(\neg b\lor \ell_0\lor \ell_1),\\
C_1&=(\neg c\lor \ell_1\lor \ell_2),\\
A_2&=(\neg a\lor \ell_2\lor \ell_3),\\
B_2&=(\neg b\lor \ell_3\lor \ell_4),\\
C_2&=(\neg c\lor \ell_4\lor \ell_5).
\end{aligned}
\]

Cada centro tem grau 3 e cada folha tem grau 2. Logo o hipergrafo inteiro é
seu próprio 2-core por grau. Ele é linear: quaisquer duas cláusulas compartilham
no máximo uma variável.

As folhas, porém, aparecem apenas positivamente. Portanto este exemplo refuta o
escudo baseado em 2-core, mas **não** sobrevive a Pure Literal Elimination.

## Equilíbrio positivo

Tome
\[
a=b=c=-1,\qquad \ell_0=\cdots=\ell_5=-1.
\]

A cláusula central tem energia 1. Cada periférica tem energia zero pelo literal
central negado.

Para cada centro, a cláusula central contribui \(-1/2\) para a derivada e as
duas periféricas contribuem \(+1/2\) cada. Assim
\[
\partial_a\Phi=\partial_b\Phi=\partial_c\Phi=\frac12>0.
\]
Todas as derivadas foliares se anulam, pois cada periférica contém o fator zero
do centro negado. O PDS projeta a velocidade central para zero no bordo inferior.
Logo o vértice é equilíbrio projetado com \(\Phi=1\).

## Bacia aberta

Escreva
\[
a=-1+u_a,\quad b=-1+u_b,\quad c=-1+u_c,
\qquad
\ell_k=-1+y_k.
\]

Considere
\[
0<u_a,u_b,u_c<\frac14,\qquad
0<y_k<\frac18.
\]

Use como bootstrap \(y_k<1/4\). Em cada periférica, cada fator foliar satisfaz
\[
1-\frac{y_k}{2}\ge\frac78.
\]
Logo o produto dos dois fatores foliares é pelo menos \(49/64\). Como cada
centro possui duas periféricas,
\[
B_r\ge\frac{49}{32},
\]
e portanto
\[
\partial_{u_r}\Phi
\ge
\frac12\left(\frac{49}{32}-1\right)
=
\frac{17}{64}.
\]
Assim
\[
\dot u_r\le-\frac{17}{64},
\qquad
T_{\rm hit}\le\frac{16}{17}.
\]

Cada folha pertence a duas periféricas de centros distintos. Sua velocidade é a
soma de duas contribuições não-negativas:
\[
0\le\dot y_k
\le
\frac{u_r+u_s}{4}
\le\frac18.
\]
Consequentemente
\[
\Delta y_k
\le
\frac18\frac{16}{17}
=
\frac{2}{17}.
\]
Como inicialmente \(y_k<1/8\),
\[
y_k(t)
<
\frac18+\frac{2}{17}
=
\frac{33}{136}
<
\frac14.
\]
A folga restante é exatamente \(1/136\), fechando o bootstrap.

Quando um centro atinge \(u_r=0\), a mesma margem positiva de gradiente o mantém
preso pelo PDS. Depois que os três centros atingem o bordo, todas as velocidades
foliares zeram, porque cada termo foliar é proporcional ao deslocamento do seu
centro. A energia fica \(\Phi=1\), e a cláusula central continua violada após
rounding.

Portanto existe uma bacia aberta de energia positiva em um hipergrafo com grau
mínimo 2.

## Consequência

A poda puramente topológica por grau (2-core) **não** imuniza o PDS contra o
mecanismo M7.

O exemplo não invalida uma formulação baseada em Pure Literal Elimination,
pois todas as \(\ell_k\) são literais puros positivos. Para essa variante mais
forte, é necessário um gadget com polaridades mistas, como o certificado
CLG_T10_CORE_COUNTEREXAMPLE_M16.md, ou uma análise probabilística específica
do core produzido pela PLE.
