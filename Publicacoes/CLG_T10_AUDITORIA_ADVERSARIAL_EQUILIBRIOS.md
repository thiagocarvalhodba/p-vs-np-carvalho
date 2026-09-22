# Auditoria adversarial de equilíbrios projetados do Teorema 10

**Data:** 21 de setembro de 2026  
**Veredito primário:** **T10 REFUTADO.**

O resultado que decide esta rodada não é apenas a existência de um equilíbrio
positivo. Há uma hiperárvore linear 3-uniforme de **seis cláusulas** com uma
família 9-dimensional de mínimos relativos positivos e uma bacia de Lebesgue
positiva. Mais ainda, componentes isoladas desse tipo produzem uma cota
inferior assintótica estritamente positiva para a energia discreta multilinear
**em esperança** no ensemble esparso. Isso contradiz diretamente a conclusão
$\mathbb E\rho_{\rm mult}(\alpha)\to0$ de T10.

Este resultado não implica nenhuma conclusão sobre $\mathbf P$ versus
$\mathbf{NP}$.

## Matriz de obrigações

| Afirmação | Status | Certificação |
|---|---|---|
| $\mathcal E_{\rm proj}(K)\subseteq\{\Phi_K=0\}$ para toda hiperárvore | **REFUTADA** | vértice exato de $m=4$ |
| Não há equilíbrio positivo em face de dimensão positiva para $m\le4$ | **PROVADA** | redução estrutural por cláusula sem folha |
| Toda bacia positiva tem medida zero para $m\le5$ | **PROVADA** | convergência PDS/KL + folha monotônica |
| Existe continuum positivo com bacia aberta | **PROVADA** | certificado duplo-núcleo de $m=6$ |
| $m=6$ é mínimo para bacia positiva em hiperárvores da classe auditada | **PROVADA** | exclusão de medida positiva para $m\le5$ |
| Toda trajetória PDS converge a um único equilíbrio | **PROVADA** | Moreau + BDL, Teorema 3.1 e Remark 4.8 |
| $\lim \mathbb E\rho_{\rm mult}(\alpha)=0$ para $0<\alpha<1/6$ | **REFUTADA** | contagem exata de componentes M6 isoladas |
| Cota positiva para $\rho_{\rm mult}$ com alta probabilidade | **PROVADA** | concentração de McDiarmid (swap sem reposição) + Chernoff condicional exato em `PROVA_ALTA_PROBABILIDADE_M6.md` |

## Catálogo desta auditoria

| $m$ | estrutura/polaridade | dimensão da face mínima | equilíbrio positivo | $\Phi$ | tipo | classificação local | bacia conhecida | certificação |
|---:|---|---:|---|---:|---|---|---|---|
| 1--3 | todas as hiperárvores/polaridades | todas | nenhum | — | — | — | — | prova estrutural exata |
| 4 | estrela, ramos opostos ao núcleo | 0 | vértice conhecido | 1 | isolado | sela relativa | singleton | prova exata; 12 cópias rotuladas na regressão |
| 5 | todas as hiperárvores/polaridades | não catalogadas ponto a ponto | não excluídos, mas com bacias nulas | não catalogado | não necessário classificar | não alegada | medida zero | prova estrutural + monotonicidade |
| 6 | duplo núcleo abaixo | 9 | família $\mathcal M$ | 1 | continuum semialgébrico | mínimos relativos não estritos, transversalmente atraentes | contém aberto de medida $2^{-53}$ | álgebra e PDS exatos |
| 7 | estrela com dois ramos por variável central | 12 | família positiva | 1 | continuum semialgébrico | mínimos relativos não estritos | contém aberto de medida $2^{-48}$ | certificado independente exato |

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

Isto refuta, de forma independente, a propriedade determinística necessária à antiga prova de T10: não é verdade que quase toda trajetória em toda componente hiperarbórea converge para energia zero. A refutação assintótica da conclusão em esperança já é fornecida abaixo pelo motivo mínimo M6; o M7 permanece como certificado redundante e reprodutível.

## Afirmação auditada
A maior face de equilíbrios explicitamente analisada tem dimensão 12 (o
certificado de sete cláusulas). Para $m\le4$, a classificação estrutural cobre
**todas** as faces mínimas, de dimensão 0 até 9, sem restringir coordenadas a
uma grade racional.

## 1. Coordenadas de fatores e KKT

Para cada variável escolha $\tau_v\in\{\pm1\}$ e ponha

$$
z_v=\frac{1-\tau_vx_v}{2}\in[0,1].
$$

Cada fator de cláusula torna-se $z_v$ ou $1-z_v$. A mudança é uma isometria
diagonal seguida de uma escala por $1/2$, logo preserva faces, nulidade de
medida, estabilidade e as condições de equilíbrio. Nas coordenadas de fatores,

$$
z_v=0:\ \partial_v\Phi\ge0,\qquad
0<z_v<1:\ \partial_v\Phi=0,\qquad
z_v=1:\ \partial_v\Phi\le0.
$$

O PDS é

$$
\dot z=\frac14\Pi_{T_{[0,1]^n}(z)}(-\nabla_z\Phi).
$$

O fator $1/4$ apenas reparametriza o tempo.

## 2. Lema estrutural de folha

Se $v$ tem grau 1 e aparece apenas na cláusula $c$, oriente sua coordenada para
que seu fator seja $z_v$. Então

$$
\partial_{z_v}\Phi
=\prod_{w\in c\setminus\{v\}}\ell_{cw}(z_w)\ge0.
$$

Se $P_c(z)>0$, temos $z_v>0$ e a derivada acima é estritamente positiva. Isso
viola KKT tanto no interior quanto em $z_v=1$. Portanto,

$$
P_c(z)>0\quad\Longrightarrow\quad
c\text{ não contém variável de grau }1. \tag{L}
$$

Este lema não remove uma cláusula de energia zero e não usa a implicação falsa
$P_c=0\Rightarrow\nabla P_c=0$.

## 3. Classificação exata de todas as faces para $m\le4$

Para $m\le3$, toda cláusula possui uma variável de grau 1. Por (L), não há
equilíbrio positivo.

Com quatro cláusulas, uma cláusula sem folhas força exatamente a estrela com
um núcleo e três ramos, um por variável central. Após gauge,

$$
\Phi=y_1y_2y_3+\sum_{i=1}^3h_i(y_i)a_ib_i,
\qquad h_i(y_i)\in\{y_i,1-y_i\}.
$$

A positividade do núcleo dá $y_i>0$. Se $h_i=y_i$, KKT nas folhas força
$a_ib_i=0$, enquanto

$$
\partial_{y_i}\Phi=y_jy_k+a_ib_i>0,
$$

impossível para $y_i>0$. Logo $h_i=1-y_i$. Se $y_i<1$, KKT nas folhas volta a
forçar $a_ib_i=0$ e dá $\partial_{y_i}\Phi=y_jy_k>0$. Assim $y_i=1$ para os
três índices. Finalmente, KKT no topo exige

$$
\partial_{y_i}\Phi=1-a_ib_i\le0,
$$

portanto $a_i=b_i=1$.

Conclui-se que, módulo gauge/isomorfismo, o vértice de quatro cláusulas já
conhecido é o único equilíbrio positivo para $m\le4$. Isso cobre coordenadas
racionais, irracionais algébricas e transcendentes, segmentos, curvas e faces
inteiras: não houve discretização do espaço contínuo.

No sistema original ele pode ser escrito como

$$
E=((0,1,2),(0,3,4),(1,5,6),(2,7,8)),
$$

com sinais $(+++),(-++),(-++),(-++)$ e $x^*=(-1)^9$. Vale
$\Phi(x^*)=1$, $\nabla\Phi(x^*)=0$. Sua expansão factível tem termo quadrático
indefinido; ele é uma sela relativa e sua bacia é exatamente o singleton
$\{x^*\}$, conforme a prova de monotonicidade foliar da rodada anterior.

## 4. Contraexemplo mínimo M6: duplo núcleo

Considere

$$
\begin{aligned}
E=\{&(0,1,2),(0,3,4),(1,5,6),\\
    &(2,7,8),(3,9,10),(4,11,12)\},
\end{aligned}
$$

com polaridades, nessa ordem,

$$
(+++),\quad(-++),\quad(-++),\quad(-++),\quad(-++),\quad(-++).
$$

É uma hiperárvore linear 3-uniforme. Em coordenadas de fatores, escreva

$$
\begin{aligned}
\Phi={}&yu_1u_2+(1-y)v_1v_2\\
&+(1-u_1)a_1b_1+(1-u_2)a_2b_2\\
&+(1-v_1)c_1d_1+(1-v_2)c_2d_2. \tag{1}
\end{aligned}
$$

### Família positiva

O conjunto

$$
\mathcal M=\left\{
\begin{array}{l}
u_1=u_2=v_1=v_2=1,\quad 0<y<1,\\
a_jb_j>y,\quad c_jd_j>1-y
\end{array}\right\} \tag{2}
$$

é uma família semialgébrica 9-dimensional de equilíbrios projetados. Em (2),

$$
\partial_y\Phi=0,\qquad
\partial_{u_j}\Phi=y-a_jb_j<0,\qquad
\partial_{v_j}\Phi=(1-y)-c_jd_j<0,
$$

e as oito derivadas foliares são zero. Todos os pontos têm $\Phi=1$.

Com $p_j=1-u_j$, $r_j=1-v_j$, $A_j=a_jb_j$ e $C_j=c_jd_j$, a identidade
exata é

$$
\begin{aligned}
\Phi-1={}&p_1(A_1-y)+p_2(A_2-y)+yp_1p_2\\
&+r_1(C_1-(1-y))+r_2(C_2-(1-y))+(1-y)r_1r_2. \tag{3}
\end{aligned}
$$

Logo os pontos de (2) são mínimos relativos não estritos numa vizinhança: a
energia é plana nas nove direções da família e cresce nas quatro direções
unilaterais transversais.

### Aberto capturado em tempo finito

Defina

$$
U=\left\{
\frac{31}{64}<y<\frac{33}{64},\quad
\frac{15}{16}<u_j,v_j<1,\quad
\frac{15}{16}<a_j,b_j,c_j,d_j<1
\right\}. \tag{4}
$$

Considere o envelope

$$
\frac7{16}<y<\frac9{16},\qquad
u_j,v_j\ge\frac{15}{16},\qquad
a_j,b_j,c_j,d_j>\frac78. \tag{5}
$$

Enquanto uma das quatro coordenadas $u_j,v_j$ está abaixo de 1, (5) implica

$$
\dot u_j,\dot v_j
\ge\frac14\left[\left(\frac78\right)^2-\frac9{16}\right]
=\frac{13}{256}. \tag{6}
$$

Cada uma atinge 1 em tempo menor que

$$
T_{\rm hit}<\frac{1/16}{13/256}=\frac{16}{13}. \tag{7}
$$

Como $u_1u_2,v_1v_2\in[(15/16)^2,1]$,

$$
|\dot y|\le\frac{31}{1024}.
$$

Até (7), o deslocamento de $y$ é menor que $31/832$ e

$$
\frac{31}{64}-\frac{31}{832}>\frac7{16},\qquad
\frac{33}{64}+\frac{31}{832}<\frac9{16}. \tag{8}
$$

Cada folha satisfaz $|\dot a|\le(1-u_j)/4\le1/64$, e portanto perde menos que
$1/52$; exatamente,

$$
\frac{15}{16}-\frac1{52}>\frac78. \tag{9}
$$

As estimativas (8)--(9) fecham o bootstrap do envelope. Ao atingir
$u_1=u_2=v_1=v_2=1$, as velocidades de $y$ e das folhas se anulam e as quatro
desigualdades ativas continuam estritas. A trajetória congela em $\mathcal M$
com $\Phi=1$.

A medida normalizada do aberto (4) é

$$
\mathbb P(U)=\frac1{32}\left(\frac1{16}\right)^{12}=2^{-53}>0. \tag{10}
$$

Qualquer desempate booleano em $y_\infty=1/2$ também viola exatamente uma das
duas cláusulas do núcleo; fora do empate, a conclusão é imediata pelo sinal de
$y_\infty-1/2$.

## 5. Minimalidade: por que $m\le5$ tem bacia positiva nula

Esta prova não usa identificação finita de face, cascata de impacto, Liouville
iterado ou hipótese de hiperbolicidade.

No grafo de incidência, que é uma árvore, duas cláusulas sem
variáveis-folha exigem pelo menos seis cláusulas. De fato, o caminho entre os
dois nós-cláusula usa no máximo uma variável vizinha em cada extremidade; os
outros dois vizinhos de cada extremidade exigem quatro nós-cláusula externos,
todos distintos para não criar ciclo. A conta mínima é, portanto, $2+4=6$,
com igualdade apenas quando as duas cláusulas centrais são adjacentes. Por
(L), um equilíbrio positivo com $m\le5$ possui exatamente uma cláusula
positiva $C$.

Oriente os fatores de $C$ como $y_1y_2y_3$. A contribuição de $C$ para
$\partial_{y_i}\Phi$ é $y_jy_k>0$. Se $y_i<1$, qualquer outra cláusula
incidente em $y_i$ tem a forma $y_iq_B$ ou $(1-y_i)q_B$. Como sua energia é
zero e ambos $y_i$ e $1-y_i$ são positivos, temos $q_B=0$ nos dois casos;
logo sua contribuição à derivada também é zero. Restaria
$\partial_{y_i}\Phi=y_jy_k>0$, incompatível com KKT no interior. Portanto
$y_i=1$ para os três índices. Equivalentemente, a única forma de obter uma
contribuição negativa não nula no bordo é

$$
(1-y_i)q_B,\qquad q_B>0.
$$

Ao remover $C$, as $m-1\le4$ cláusulas se distribuem em três ramos não vazios.
Para $m=4$ os tamanhos são $(1,1,1)$; para $m=5$, $(1,1,2)$. Num ramo unitário,
a cláusula é a única cláusula adicional incidente em $y_i$ e tem duas folhas
genuínas, com fatores $a,b$. Seu literal central precisa ser $1-y_i$: com
$y_i$ ele não forneceria a contribuição negativa necessária. KKT em $y_i=1$
exige

$$
1-ab\le0,
$$

logo $a=b=1$.

Globalmente, a dinâmica dessa folha satisfaz

$$
\dot a=\Pi_{T_{[0,1]}(a)}
\left(-\frac14(1-y_i)b\right)\le0.
$$

Portanto uma trajetória que converge para um equilíbrio positivo com
$a_\infty=1$ deve ter $a(0)=1$. Para cada uma das finitíssimas possibilidades
de cláusula positiva $C$, escolha previamente uma folha $a_C$ de um ramo
unitário. Se $\mathcal B_+$ denota o conjunto de condições iniciais com limite
de energia positiva, então

$$
\mathcal B_+\subseteq\bigcup_C\{a_C(0)=1\}.
$$

Esta é uma união **finita** de faces afins de coordenada e, portanto, tem
medida de Lebesgue ambiente zero. Não se usa uma união não enumerável de bacias
individuais.

A convergência a um ponto, demonstrada na seção seguinte, elimina a necessidade
de supor que a trajetória identifica uma face em tempo finito. Assim, na classe
de hiperárvores conexas, lineares, 3-uniformes e Berge-áciclicas,

$$
m_*^{\rm mult}=6
$$

para o tamanho mínimo de uma componente com bacia de energia-limite positiva de
medida ambiente positiva.

## 6. PDS/KL: convergência a um único equilíbrio

Defina $X=[-1,1]^n$ e $F=\Phi+\delta_X$. Como $\Phi$ é $C^1$ e $X$ é convexo,

$$
\widehat\partial F(x)=\partial F(x)=\nabla\Phi(x)+N_X(x).
$$

Para $d(x)=\Pi_{T_X(x)}(-\nabla\Phi(x))$, a decomposição de Moreau dá

$$
-d(x)\in\partial F(x),
$$

e, mais fortemente,

$$
\|d(x)\|
=\operatorname{dist}(-\nabla\Phi(x),N_X(x))
=\operatorname{dist}(0,\partial F(x)). \tag{11}
$$

Ao longo da solução,

$$
\frac d{dt}\Phi(x(t))=-\|\dot x(t)\|^2\quad\text{a.e.} \tag{12}
$$

O Teorema 3.1 de Bolte--Daniilidis--Lewis aplica a desigualdade de
Łojasiewicz a funções subanalíticas com domínio fechado e continuidade relativa
ao domínio. O **Remark 4.8** do mesmo artigo estende explicitamente os Teoremas
4.5/4.7 quando $\widehat\partial F=\partial F$, $F$ é contínua no domínio, tem a
propriedade Łojasiewicz e a inclusão possui solução global única com $F\circ x$
absolutamente contínua.

Todas essas hipóteses valem aqui: $F$ é regular e semialgébrica; $X$ é compacto;
$\nabla\Phi$ é Lipschitz na caixa; $N_X$ é maximal monotônico; a perturbação
Lipschitz fornece solução global única; e (12) dá a continuidade absoluta. Logo
toda trajetória possui comprimento finito e converge para um único equilíbrio
projetado.

Fonte primária verificada em 21/09/2026: J. Bolte, A. Daniilidis e A. Lewis,
*The Łojasiewicz Inequality for Nonsmooth Subanalytic Functions with
Applications to Subgradient Dynamical Systems*, SIAM J. Optim. 17 (2007),
1205--1223, DOI 10.1137/050644641,
<https://www.arisdaniilidis.at/pr_loja.pdf>. O PDF foi lido na fonte autoral;
nenhuma cópia local/cache ou hash foi criada nesta rodada.

Isso fecha convergência pontual, mas não provaria sozinho energia zero. O M6
mostra precisamente por que essa conclusão adicional é falsa.

## 7. Propagação exata ao ensemble e refutação de T10

Considere primeiro o modelo uniforme sem reposição, com

$$
Q_N=8\binom N3,\qquad M=\lfloor\alpha N\rfloor,
$$

e $M$ cláusulas assinadas distintas. O M6 tem 13 variáveis, grupo de
automorfismos não assinado de ordem

$$
2\cdot2^2\cdot2^4=128,
$$

e $2^{13}$ polaridades na órbita de gauge, todas dinamicamente conjugadas.
Se $X_{M6}$ conta componentes isoladas nessa órbita, então a expectativa exata
é

$$
\mathbb E X_{M6}
=\frac{(N)_{13}}{128}\,2^{13}
\frac{\binom{8\binom{N-13}{3}}{M-6}}
     {\binom{8\binom N3}{M}}. \tag{13}
$$

No modelo de $M$ cláusulas assinadas i.i.d. (com reposição), ponha
$Q=8\binom N3$ e $Q_0=8\binom{N-13}{3}$. A expressão finita correspondente é

$$
\mathbb E X_{M6}^{\rm iid}
=\frac{(N)_{13}}{128}\,2^{13}
\frac{(M)_6Q_0^{M-6}}{Q^M}. \tag{13-iid}
$$

Aqui $(M)_6$ escolhe uma injeção ordenada das seis cláusulas do motivo nos
slots de amostragem, e os $M-6$ draws restantes evitam todas as 13 variáveis.

Com $M=\lfloor\alpha N\rfloor$ e $\alpha>0$ fixo,

$$
\frac{\mathbb E X_{M6}}N
\longrightarrow
\frac{729}{64}\alpha^6e^{-39\alpha}. \tag{14}
$$

O fator $e^{-39\alpha}$ é a probabilidade assintótica de nenhuma cláusula
adicional tocar os 13 vértices. As expressões (13) e (13-iid) têm a mesma
constante principal.

Cada componente é dinamicamente desacoplada e cai no aberto (4) com
probabilidade $2^{-53}$. Ela deixa exatamente uma cláusula violada. Pela
linearidade da esperança e pela não negatividade das demais contribuições,

$$
\liminf_{N\to\infty}\mathbb E\rho_{\rm mult}(\alpha)
\ge
\frac{729}{2^{59}}\alpha^5e^{-39\alpha}>0
\qquad(\alpha>0). \tag{15}
$$

Não é necessário provar concentração para refutar T10: o enunciado reivindica
simultaneamente colapso a.a.s. **e em esperança**, e (15) contradiz a segunda
reivindicação para todo $0<\alpha<1/6$.

A conclusão com alta probabilidade foi formalizada e provada rigorosamente no documento `P_NP/PROVA_ALTA_PROBABILIDADE_M6.md` via martingal acoplado por troca sem reposição (McDiarmid com $C_{M6}\le 4$) combinado com concentração de Chernoff para a captura binomial condicional exata, estabelecendo $\Pr[\rho_{\rm mult}\ge \frac{729}{2^{60}}\alpha^5e^{-39\alpha}]\to 1$.

## 8. Auditoria dos documentos Gemini

O arquivo `GEMINI_T10_PROVA_INDEPENDENTE.md` foi útil como alvo adversarial,
mas sua prova não sobrevive:

1. segunda ordem deve ser testada no cone crítico, não em todo o cone tangente;
2. uma direção de descida não implica instabilidade nem bacia nula;
3. vértices de uma face não controlam atração transversal da face inteira;
4. união não enumerável de bacias nulas pode ter medida positiva;
5. hiperbolicidade não pode ser declarada sem não degenerescência;
6. teoremas de variedade estável suaves não se transferem automaticamente ao
   PDS não suave no bordo.

O M6 contradiz diretamente o “Lema D1”: ele possui mínimos relativos positivos,
continuum não hiperbólico e bacia aberta.

Os arquivos não rastreados `GEMINI_T10R_PROGRAMA_COMPLETO.md` e
`ROADMAP_T10R.md` ainda afirmam minimalidade $m=7$; essa afirmação está
refutada pelo certificado M6 e esses arquivos não são evidência aceita.

A parte PDS/KL pode ser reparada independentemente pelo Teorema 3.1 e Remark
4.8 de BDL, como feito acima. Esse reparo fortalece a refutação: as trajetórias
do aberto M6 convergem efetivamente a pontos do continuum positivo.

## 9. Cobertura computacional e limites

O programa `Fontes/search_t10_positive_equilibrium_hypertrees.py` contém:

- aritmética `Fraction` para $\Phi$, gradiente, KKT e campos adaptados;
- o catálogo de vértices até $m=4$ como regressão;
- validadores estruturais de aresta sem folha e tamanhos de ramos;
- os certificados M6 e M7;
- as identidades exatas de energia e os campos PDS adaptados;
- a medida dos abertos $2^{-53}$ e $2^{-48}$;
- a expectativa finita (13) e a constante assintótica (15).

Os testes validam a implementação; a prova matemática está nas seções
anteriores. Não se usa Monte Carlo negativo como prova, e não se afirma uma
enumeração simbólica ponto a ponto de todos os equilíbrios de $m=5$ ou $m=6$.

## 10. Estado final e próxima lacuna

O gargalo anterior — encontrar uma bacia positiva — está resolvido por
contraexemplo. O Teorema 10 original deve permanecer marcado **REFUTADO**, e
qualquer manuscrito que afirme $\rho_{\rm mult}=0$ no regime subcrítico precisa
ser corrigido.

A próxima questão legítima não é tentar restaurar T10, mas caracterizar a
densidade completa de motivos atratores e comparar cotas inferiores/superiores
das duas relaxações sem extrapolar isso para complexidade de Turing.
