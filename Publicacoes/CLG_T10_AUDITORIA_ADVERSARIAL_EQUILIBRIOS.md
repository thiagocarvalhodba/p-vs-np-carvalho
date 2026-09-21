# Auditoria adversarial de equilíbrios projetados do Teorema 10

**Data:** 21 de setembro de 2026  
**Veredito primário:** **A — CONTRAEXEMPLO COM BACIA POSITIVA ENCONTRADO.**

| Afirmação | Dependências | Contraexemplo/tentativa | Prova | Status |
|---|---|---|---|---|
| $\mathcal E_{\rm proj}(K)\subseteq\{\Phi_K=0\}$ em toda hiperárvore linear | KKT projetado | Certificado de 4 cláusulas abaixo | Gradiente exato nulo e $\Phi=1$ | **REFUTADO** |
| O vértice certificado é mínimo/atrator positivo | PDS no ortante | Expansão factível $u\ge0$ | Termo quadrático com ambos os sinais | **REFUTADO** |
| A bacia do vértice certificado tem medida positiva | PDS projetado | Monotonicidade exata das folhas | A bacia é o singleton $\{x^*\}$ | **REFUTADO** |
| Toda bacia de equilíbrio positivo em hiperárvores tem medida zero | Classificação global | Hiperárvore de 7 cláusulas com aberto atraído para \(\Phi=1\) | Certificado analítico em CLG_T10_CONTRAEXEMPLO_BACIA_POSITIVA_M7.md | **REFUTADO** |
| Convergência global do PDS CLG a ponto único via BDL | Hipóteses KL exatas | Leitura da fonte primária | Teorema citado não se aplica diretamente a $\Phi+\delta_X$ | **CONDICIONAL** |

## Catálogo exato: equilíbrios positivos nos vértices

Foi executada a enumeração exata de todos os vértices, para $m\le4$, sobre
as construções de anexação rotuladas e todas as classes de polaridade módulo
gauge de variável. Toda hiperárvore linear 3-uniforme pode ser obtida por uma
ordem de anexação de folhas; portanto esse espaço rotulado cobre cada tipo não
rotulado ao menos uma vez, embora deliberadamente contenha duplicatas e não
seja uma canonicalização por isomorfismo.

Foram verificados respectivamente $8$, $192$, $7680$ e $430080$ candidatos
para $m=1,2,3,4$. Não houve equilíbrio positivo nos vértices para $m\le3$.
Para $m=4$, os 12 certificados retornados são cópias por rotulagem/permutação
da mesma hiperárvore-estelar de quatro cláusulas já certificada; todos têm
$\Phi=1$, gradiente nulo e são selas relativas de bacia singleton pela prova
anterior.

| estrutura | face | $\Phi$ | classificação | bacia conhecida | certificado |
|---|---:|---:|---|---|---|
| $m\le3$, qualquer hiperárvore linear | vértices | — | nenhum equilíbrio positivo | — | enumeração exata |
| estrela 3-uniforme com 4 cláusulas | vértice | $1$ | sela relativa | $\{x^*\}$, medida zero | seção “Certificado exato” |
| demais cópias rotuladas da estrela, $m=4$ | vértice | $1$ | sela relativa | $\{x^*\}$, medida zero | mesmo certificado por simetria |

Este catálogo não classifica equilíbrios em faces de dimensão positiva e não
constitui uma prova para $m\ge5$ ou para hiperárvores arbitrárias.

## Contraexemplo de bacia positiva (7 cláusulas)

A rodada adversarial posterior encontrou uma obstrução estritamente mais forte que o certificado de quatro cláusulas. Considere a cláusula central \((a\lor b\lor c)\) e, para cada variável central \(r\in\{a,b,c\}\), duas cláusulas periféricas \((\neg r\lor p_{r,1}\lor q_{r,1})\) e \((\neg r\lor p_{r,2}\lor q_{r,2})\). O hipergrafo resultante é uma hiperárvore linear 3-uniforme com 7 cláusulas e 15 variáveis.

Em coordenadas de deslocamento a partir de \(-\mathbf1\), a energia é
\[
\Phi=\prod_r\left(1-\frac{u_r}{2}\right)+\sum_r\frac{u_r}{2}\left[\left(1-\frac{y_{r,1}}2\right)\left(1-\frac{z_{r,1}}2\right)+\left(1-\frac{y_{r,2}}2\right)\left(1-\frac{z_{r,2}}2\right)\right].
\]

O aberto \(0<u_a,u_b,u_c<1/4\), \(0<y_{r,j},z_{r,j}<1/8\) é atraído em tempo finito para o conjunto estacionário \(u_a=u_b=u_c=0\), mantendo todas as folhas abaixo de \(1/4\). A cota exata é
\[
\partial_{u_r}\Phi\ge\frac{17}{64},\qquad T_{\rm hit}\le\frac{16}{17},\qquad \Delta y,\Delta z\le\frac1{17},
\]
de modo que folhas inicialmente abaixo de \(1/8\) permanecem abaixo de \(25/136<1/4\). No conjunto limite, \(\Phi=1\) e a cláusula central continua violada após rounding.

Consequentemente, a bacia ruim possui medida de Lebesgue positiva. Sob inicialização uniforme, o subcaixote explicitamente certificado já tem probabilidade \(2^{-57}>0\).

O certificado completo está em `Publicacoes/CLG_T10_CONTRAEXEMPLO_BACIA_POSITIVA_M7.md`.

Isto refuta a propriedade determinística necessária à prova atual de T10: não é verdade que quase toda trajetória em toda componente hiperarbórea converge para energia zero. A etapa restante para uma refutação assintótica completa da formulação aleatória é contabilizar a densidade de componentes isoladas desse tipo no ensemble \(\mathcal E(N,\alpha)\).

## Afirmação auditada

Para toda hiperárvore linear 3-uniforme conexa $K$, a afirmação auditada era

$$
\mathcal E_{\rm proj}(K)\subseteq\{x\in[-1,1]^{V(K)}:\Phi_K(x)=0\},
$$

onde $\Phi_K=\sum_{c\in K}\prod_{i\in c}(1-\sigma_{ci}x_i)/2$ e
$\mathcal E_{\rm proj}$ é definido por
$\Pi_{T_{[-1,1]^n}(x)}(-\nabla\Phi_K(x))=0$.

O resultado é **refutado**. Isto invalida a passagem que usava aciclicidade
para excluir equilíbrios positivos. Não prova, nem sugere, uma resolução de
P versus NP.

## Certificado exato

Considere as quatro hiperarestas, nos vértices $0,\ldots,8$:

$$
c_0=(0,1,2),\quad c_1=(0,3,4),\quad
c_2=(1,5,6),\quad c_3=(2,7,8).
$$

Elas formam uma hiperárvore linear: cada aresta adicionada encontra as
anteriores em exatamente um vértice e introduz dois vértices novos. Em
particular, a aresta central $c_0$ não possui variável de grau 1.

Use as polaridades

$$
\sigma_{c_0}=(+,+,+),\qquad
\sigma_{c_1}=\sigma_{c_2}=\sigma_{c_3}=(-,+,+),
$$

na ordem exibida, e tome $x^*=(-1,\ldots,-1)$.

No termo central todos os fatores são 1, logo $P_{c_0}(x^*)=1$. Em cada
termo periférico, o fator da variável compartilhada é
$(1-(-1)(-1))/2=0$, logo $P_{c_j}(x^*)=0$ para $j=1,2,3$. Portanto

$$\Phi_K(x^*)=1>0.$$

Cada derivada nas seis folhas periféricas contém esse fator zero. Para cada
variável central, a derivada $-1/2$ do termo central é cancelada pela derivada
$+1/2$ do respectivo termo periférico. Assim,

$$\nabla\Phi_K(x^*)=(0,\ldots,0).$$

Consequentemente a projeção no cone tangente é exatamente zero; não há questão
de tolerância numérica nem de sinal KKT.

## Estabilidade relativa à caixa e bacia do certificado

Escreva $x=-\mathbf1+u$, com $u\in[0,2]^9$. A expansão exata (não apenas
uma aproximação de Hessiana) é

$$
\begin{aligned}
\Phi(-\mathbf1+u)-1
={}&\frac14\left[u_0u_1+u_0u_2+u_1u_2
-u_0(u_3+u_4)-u_1(u_5+u_6)-u_2(u_7+u_8)\right]\\
&-\frac18u_0u_1u_2
+\frac18\left[u_0u_3u_4+u_1u_5u_6+u_2u_7u_8\right].
\end{aligned}
$$

O primeiro termo homogêneo não nulo é a forma quadrática exibida na primeira
linha. Nas direções factíveis $u=t(e_0+e_1)$ e $u=t(e_0+e_3)$, para todo
$t>0$ pequeno, as diferenças de energia são respectivamente $+t^2/4$ e
$-t^2/4$. Logo $x^*$ é uma sela relativa à caixa: não é mínimo local nem
máximo local. Esta conclusão usa perturbações factíveis, não a Hessiana livre
como critério de estabilidade no vértice.

Há ainda uma prova direta, sem variedade estável, de que sua bacia é unitária.
As folhas $3,4$ obedecem, no PDS e em coordenadas $u$,

$$
\dot u_3=\frac{u_0}{4}\left(1-\frac{u_4}{2}\right)\ge0,
\qquad
\dot u_4=\frac{u_0}{4}\left(1-\frac{u_3}{2}\right)\ge0,
$$

e as quatro fórmulas análogas valem para os pares $(5,6)$ e $(7,8)$,
com centros $u_1$ e $u_2$. A projeção no cone tangente preserva essas fórmulas,
pois $-\partial_{u_\ell}\Phi$ já aponta para dentro do ortante.

Se uma trajetória converge para $u=0$, cada folha, não negativa e não
decrescente, tem de ser identicamente zero desde o instante inicial. Então as
equações acima forçam $u_0=u_1=u_2=0$ em todo instante. Portanto

$$
\{x_0:\ x(t;x_0)\to x^*\}=\{x^*\},
$$

cuja medida de Lebesgue é zero. O certificado derruba a exclusão de
equilíbrios positivos, mas **não** fornece uma bacia positiva e não refuta por
si só a conclusão quase-em-toda-parte de T10.

## Checagens de implementação

O programa `Fontes/search_t10_positive_equilibrium_hypertrees.py` usa
`fractions.Fraction` para $\Phi$, gradiente e condições KKT. Ele enumera
hiperárvores de anexação, reduz polaridades por gauge de sinais das variáveis e
testa exatamente os vértices. A execução encontrou o certificado acima na
primeira família de quatro cláusulas que o contém. Antes disso, a busca exata
de vértices não encontrou candidato para 1, 2 ou 3 cláusulas.

Os testes em `tests/test_t10_adversarial_equilibria.py` verificam derivadas,
sinais KKT, projeção no cone tangente, geração estrutural, o certificado de
quatro cláusulas e um controle não-linear.

## PDS, Moreau e dissipação

Para $X=[-1,1]^n$, $N_X(x)=T_X(x)^\circ$. A decomposição de Moreau de
$v=-\nabla\Phi(x)$ dá $v=\Pi_Tv+\Pi_Nv$ ortogonalmente. Assim

$$
\dot x=\Pi_T(-\nabla\Phi)
\quad\Longleftrightarrow\quad
-\dot x\in\nabla\Phi(x)+N_X(x).
$$

Coordenadamente, em $x_i=1$ o equilíbrio requer
$\partial_i\Phi\le0$; em $x_i=-1$ requer $\partial_i\Phi\ge0$; no interior
requer igualdade. A ortogonalidade fornece
$d\Phi(x(t))/dt=-\|\dot x(t)\|^2$ quase em todo ponto onde a solução é
diferenciável. Essas identidades formulam o PDS globalmente, mas não excluem
o certificado acima.

## Checagem bibliográfica KL

Foi verificado o PDF autoral de Bolte--Daniilidis--Lewis (SIAM J. Optim. 17,
2007, DOI 10.1137/050644641). Sua seção dinâmica assume, para o teorema de
comprimento finito, uma função convexa semicontínua inferior ou lower-$C^2$
**com domínio $\mathbb R^n$**. Para
$F=\Phi+\delta_{[-1,1]^n}$, o domínio é a caixa, não $\mathbb R^n$, e o
indicador não torna automaticamente $F$ lower-$C^2$. Logo essa referência não
certifica, na forma citada, comprimento finito ou convergência a ponto único
do PDS CLG. Esse passo fica **não verificado**, até uma referência aplicável a
um potencial $C^1$ restrito a um politopo convexo ser mapeada hipótese a
hipótese.

## Consequência lógica e próximo teste barato

O menor elo que falha é a exclusão universal de equilíbrios positivos em
hiperárvores. A conclusão assintótica multilinear de T10 permanece aberta; o
contraexemplo não determina sozinho a medida de sua bacia nem a densidade de
componentes que contribuem dinamicamente.

O próximo passo matematicamente válido é classificar a estabilidade e a bacia
de outros equilíbrios positivos de hiperárvores pequenas, em particular um
mínimo relativo positivo ou atrator não pontual, antes de tentar qualquer novo
argumento de peeling ou qualquer inferência sobre o ensemble aleatório.

## Obstrução adicional ao peeling ingênuo

Mesmo em uma única cláusula positiva $(0,1,2)$, no ponto
$(x_0,x_1,x_2)=(1,-1,-1)$ vale $P_c=0$, mas

$$\nabla P_c=(-1/2,0,0).$$

Assim, remover uma cláusula apenas porque seu valor é zero não preserva o
gradiente na variável compartilhada. Qualquer indução por peeling precisa de
uma condição mais forte (por exemplo, fatores nulos suficientes para anular
todas as derivadas relevantes), ainda não obtida.
