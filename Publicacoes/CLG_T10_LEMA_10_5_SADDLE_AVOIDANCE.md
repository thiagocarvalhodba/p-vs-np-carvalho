# Auditoria adversarial do Lema 10.5 — PDS, Łojasiewicz e trocas de face

## Status após auditoria

**Convergência PDS/KL: provada. Evasão universal de selas: refutada.** A versão mergeada na PR #2 contém duas passagens que não devem ser usadas:

1. a preservação de nulidade de medida por “aplicações de impacto” entre faces não foi demonstrada com hipóteses suficientes e é especialmente delicada porque o semifluxo de um projected dynamical system (PDS) pode perder invertibilidade após contato com o bordo;
2. a frase “Łojasiewicz nos estratos + controle das trocas de face” não é, por si só, um teorema de convergência para o PDS.

A auditoria também encontrou uma falha estrutural: em uma hiperárvore, **não é verdade em geral que toda cláusula violada possua uma variável de grau 1**. O vértice positivo de quatro cláusulas já refutava a exclusão de equilíbrios. A rodada atual encontrou algo decisivo: uma hiperárvore de seis cláusulas com continuum de mínimos relativos positivos e bacia aberta. O certificado está em `CLG_T10_AUDITORIA_ADVERSARIAL_EQUILIBRIOS.md` e refuta a etapa de evasão de T10.

## 1. Formulação correta do PDS sem mapas de impacto

Seja $X=[-1,1]^n$, seja $T_X(x)$ o cone tangente de Bouligand e seja
$N_X(x)=T_X(x)^\circ$ o cone normal convexo. Para
$v=-\nabla\Phi(x)$, a decomposição ortogonal de Moreau para os cones polares
dá unicamente

$$
v=\Pi_{T_X(x)}v+\Pi_{N_X(x)}v,
\qquad
\langle\Pi_Tv,\Pi_Nv\rangle=0.
$$

Portanto, para a solução do PDS,

$$
\dot x=\Pi_{T_X(x)}(-\nabla\Phi(x)),
$$

existe $n(t)\in N_X(x(t))$ tal que

$$
-\nabla\Phi(x(t))=\dot x(t)+n(t),
$$

isto é,

$$
-\dot x(t)\in \nabla\Phi(x(t))+N_X(x(t))
=\partial(\Phi+\delta_X)(x(t))
\quad\text{a.e.}
$$

Como $X$ é convexo e $\Phi$ é $C^1$, a última igualdade é a regra de soma
padrão para a subdiferencial limitante/convexa do indicador. Além disso, a
ortogonalidade de Moreau fornece

$$
\frac{d}{dt}\Phi(x(t))
=\langle\nabla\Phi(x(t)),\dot x(t)\rangle
=-\|\dot x(t)\|^2
\quad\text{a.e.}
$$

Esta formulação é global: ela atravessa mudanças de face sem introduzir mapas de impacto.

## 2. Etapa de Łojasiewicz/Kurdyka–Łojasiewicz

Defina a função estendida

$$
F=\Phi+\delta_X.
$$

No caso CLG multilinear, $\Phi$ é polinomial e $X$ é um politopo
semialgébrico; logo $F$ é própria, semicontínua inferior e semialgébrica
(portanto subanalítica/definível no domínio compacto).

O resultado de Bolte–Daniilidis–Lewis, *SIAM Journal on Optimization* 17 (2007), 1205–1223, DOI 10.1137/050644641, foi relido na fonte primária. O Teorema 3.1 fornece a propriedade de Łojasiewicz para função subanalítica com domínio fechado e continuidade relativa. O **Remark 4.8** estende explicitamente os Teoremas 4.5/4.7 quando $\widehat\partial F=\partial F$, $F$ é contínua no domínio, possui a propriedade Łojasiewicz e a inclusão tem solução global única com $F\circ x$ absolutamente contínua.

Essas hipóteses valem para $F=\Phi+\delta_X$: o indicador de um convexo
fechado é regular e a soma com uma função $C^1$ preserva regularidade, de modo
que

$$
\widehat\partial F=\partial F=\nabla\Phi+N_X.
$$

Como $\nabla\Phi$ é Lipschitz na caixa, a extensão
$G=\nabla\Phi\circ\Pi_X$ é globalmente Lipschitz. O cone normal $N_X$ é
maximal monotônico; o teorema padrão de perturbação Lipschitz fornece uma
solução absolutamente contínua global e única da inclusão para cada
$x_0\in X$. Além disso, $x$ absolutamente contínua, $\Phi\in C^1$ e
$\nabla\Phi$ limitada em $X$ implicam diretamente que
$F\circ x=\Phi\circ x$ é absolutamente contínua. Moreau ainda dá

$$
\|\dot x\|=\operatorname{dist}(0,\partial F(x)).
$$

Logo toda trajetória tem comprimento finito e converge a um único ponto-limite,
que é um equilíbrio projetado. Isso não afirma que o sistema possua apenas um
equilíbrio. A ressalva anterior baseada apenas em
$\operatorname{dom}F\ne\mathbb R^n$ omitia a generalização explícita do
Remark 4.8 e fica corrigida.

## 3. Por que a prova por aplicações de impacto é retirada

A versão anterior afirmava que, num contato transversal, a aplicação de impacto é $C^1$ e que pré-imagens de conjuntos nulos permanecem nulas. Mesmo quando um tempo de primeiro impacto é regular, isso não resolve globalmente o PDS:

- a projeção no cone tangente muda de fórmula no bordo;
- o semifluxo pode deixar de ser invertível após contato com o bordo;
- uma aplicação $C^1$ não preserva nulidade de pré-imagens sem uma condição de posto/não-degenerescência apropriada;
- acumulação de contatos não é automaticamente um conjunto semialgébrico de dimensão menor apenas porque o campo original é polinomial.

Consequentemente, a seção de “impact maps” da PR #2 não é usada como fundamento de T10.

A formulação por inclusão diferencial/subgradiente é a substituição correta para a **convergência através das faces**, mas ela não resolve sozinha a questão de **medida zero da bacia de equilíbrios positivos**.

## 4. Contra-ataque ao argumento da folha

A afirmação

> “se $\Phi(x)>0$, escolha uma cláusula violada $c$; como a componente é uma
> árvore, $c$ possui variável folha”

é falsa para hiperárvores gerais.

Uma hiperárvore 3-uniforme linear pode conter uma hiperaresta interna
$c=\{a,b,c'\}$ em que $a,b,c'$ têm grau pelo menos 2, cada um ligando $c$ a
um ramo distinto. A aciclicidade garante folhas **em algum lugar da
componente**, não uma variável de grau 1 em cada hiperaresta.

Portanto, a tentativa de fortalecer L10.5 para

$$
\mathcal E_{\rm proj}(K)\subseteq\{\Phi=0\}
$$

por um único argumento local de folha é **refutada** pelo certificado exato de
quatro cláusulas. Esse primeiro certificado tem bacia singleton. Porém, o
certificado duplo-núcleo de seis cláusulas no relatório principal possui uma
família 9-dimensional de mínimos relativos e um aberto explícito de medida
$2^{-53}$ que a atinge em tempo finito. Portanto a evasão universal de
equilíbrios positivos é falsa.

O mesmo ponto deve ser auditado nos Lemas 10.2 e 10.3: sempre que a prova requer uma *cláusula violada folha*, é necessário provar sua existência a partir das condições de criticidade/equilíbrio, e não apenas da aciclicidade.

## 5. Estado lógico correto

Ficam rigorosamente separados três problemas:

1. **PDS através das faces:** a equivalência por Moreau com a inclusão normal/subgradiente evita a necessidade de aplicações de impacto para formular a dinâmica global.
2. **Convergência a um ponto:** fechada por BDL, Teorema 3.1 + Remark 4.8, com as hipóteses mapeadas acima.
3. **Exclusão/evitação de equilíbrios positivos:** refutada pelo M6; KL garante que o aberto converge, mas o limite tem energia 1.

Consequentemente, a parte de convergência do Lema 10.5 está fechada, a parte de evasão está **refutada**, e o Teorema 10 original está **refutado** pela cota positiva em esperança documentada no relatório principal.

## Referências

- J. Bolte, A. Daniilidis, A. Lewis, *The Łojasiewicz Inequality for Nonsmooth Subanalytic Functions with Applications to Subgradient Dynamical Systems*, SIAM J. Optim. 17 (2007), 1205–1223, DOI 10.1137/050644641.
- M.-G. Cojocaru, literatura de projected dynamical systems em conjuntos convexos: projeção no cone tangente e formulação por cone normal.
- Teorema de decomposição de Moreau para cones convexos fechados polares.
