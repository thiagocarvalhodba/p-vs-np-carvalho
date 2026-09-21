# Auditoria adversarial de equilíbrios projetados do Teorema 10

**Data:** 21 de setembro de 2026  
**Veredito primário:** **A — CONTRAEXEMPLO ENCONTRADO.**

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
do certificado de quatro cláusulas, antes de tentar qualquer novo argumento de
peeling ou qualquer inferência sobre o ensemble aleatório.
