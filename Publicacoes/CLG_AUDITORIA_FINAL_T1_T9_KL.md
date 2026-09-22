# CLG-R v4.0.5 — Auditoria final dos Teoremas 1–9 e da convergência PDS/KL

**Data:** 22 de setembro de 2026  
**Escopo:** manuscrito `Publicacoes/CLG_FOUNDATIONS_ARXIV.tex`, com foco nos Teoremas 1–9 e na dependência externa de convergência usada no T10R/M6.

## 1. Veredito executivo

Após rederivação independente e revisão adversarial:

- Teorema 1: **PROVADO**, após correção editorial da coordenada literal na identificação LP.
- Teorema 2: **PROVADO**, com explicitação da escolha de uma derivada parcial analítica não nula no caso Softplus.
- Teorema 3: **PROVADO**.
- Teorema 4A': **PROVADO**.
- Corolário 4B: **PROVADO**, com formulação de LaSalle corrigida e argumento explícito de que estabilidade assintótica isolada força mínimo local estrito.
- Teorema 5: **PROVADO SOB A HIPÓTESE DECLARADA rank(V)=N** para o bound de número de condição.
- Teorema 6: **PROVADO**; a prova, antes ausente no manuscrito, foi adicionada.
- Teorema 7B: **PROVADO**, incluindo o efeito da projeção no Lyapunov radial.
- Proposição 7A: **PROVADA apenas quanto ao sinal competitivo do Jacobiano**; caracterização global da dinâmica permanece suspensa, como já declarado.
- Teorema 8: **PROVADO** no modelo de cláusulas independentes declarado.
- Teorema 9: **ABERTO**, como já declarado; uma antiga afirmação probabilística incondicional foi corretamente rebaixada para cálculo condicional.
- Convergência PDS/KL: **PROVADA sob o mapeamento explícito das hipóteses de Bolte–Daniilidis–Lewis + Bolte–Daniilidis–Lewis–Shiota**, detalhado abaixo.

Nenhum erro fatal foi encontrado nesta rodada.

## 2. Auditoria PDS/KL — hipótese por hipótese

Defina

    F(x) = Phi_mult(x) + delta_X(x),
    X = [-1,1]^N.

### 2.1 Proper, l.s.c., domínio e continuidade no domínio

- X é não vazio, compacto, convexo e semialgébrico.
- delta_X é própria e l.s.c.
- Phi_mult é polinomial.
- Logo F é própria, l.s.c. e semialgébrica.
- Em dom F = X, temos F|_X = Phi_mult|_X, que é contínua.

Isso verifica a condição de domínio e a alternativa “f restrita ao domínio é contínua” do Remark 4.8 de Bolte–Daniilidis–Lewis.

### 2.2 Igualdade entre subdiferenciais regular e limiting

Para uma caixa convexa X:

    hat_partial delta_X = partial delta_X = N_X.

Como Phi_mult é C^1, a soma com uma função suave preserva regularidade:

    hat_partial F
      = partial F
      = grad Phi_mult + N_X.

Portanto a condição

    hat_partial F = partial F

do Remark 4.8 está satisfeita.

### 2.3 Propriedade Kurdyka–Lojasiewicz

F é semialgébrica e l.s.c.

Bolte–Daniilidis–Lewis–Shiota, *Clarke Subgradients of Stratifiable Functions*, SIAM J. Optim. 18(2), 556–572 (2007), Theorem 11, é explicitamente o *Nonsmooth Kurdyka–Łojasiewicz inequality* para funções l.s.c. definíveis. O Remark 9 observa que a conclusão permanece válida para os subdiferenciais de Fréchet e limiting, por estarem contidos no Clarke.

Logo F possui a propriedade KL requerida pelo Remark 4.8 de BDL.

### 2.4 Equivalência PDS / inclusão subgradiente

Para

    d(x) = Proj_{T_X(x)}(-grad Phi_mult(x)),

Moreau fornece

    -grad Phi_mult = d + n,
    n in N_X,
    <d,n> = 0.

Assim:

    -d in grad Phi_mult + N_X = partial F.

Além disso, d é o vetor de menor norma da inclusão:

    ||d|| = dist(0, partial F).

### 2.5 Dissipação e regra da cadeia

Como x(.) é absolutamente contínua e Phi_mult é C^1:

    d/dt Phi_mult(x(t))
      = <grad Phi_mult(x(t)), xdot(t)>
      = -||xdot(t)||^2

quase em todo lugar.

Como x(t) permanece em X,

    F(x(t)) = Phi_mult(x(t)),

logo F∘x é absolutamente contínua.

### 2.6 Existência e unicidade global

O vetor

    -grad Phi_mult

é Lipschitz em X, pois Phi_mult é polinomial e X é compacto.

Para conjunto não vazio, fechado e convexo, PDS com campo Lipschitz possui solução global absolutamente contínua única; equivalentemente,

    xdot + N_X(x) contains -grad Phi_mult(x)

é uma inclusão de evolução com operador normal maximal monotone perturbado por mapa Lipschitz.

Isso verifica a hipótese adicional de solução global única do Remark 4.8.

### 2.7 Teorema exato usado

A citação antiga do manuscrito para “Theorem 3.1” como resultado dinâmico era imprecisa.

O mapeamento correto é:

- **BDL Theorem 4.5:** trajetória maximal limitada possui comprimento finito e converge a ponto crítico sob as hipóteses do sistema subgradiente;
- **BDL Theorem 4.7:** fornece convergência/rates em função do expoente de Łojasiewicz;
- **BDL Remark 4.8:** estende Theorems 4.5 e 4.7 para funções l.s.c. com:
  1. dom não vazio e hat_partial f = partial f;
  2. f convexa ou contínua no domínio;
  3. propriedade Łojasiewicz;
  4. solução global única e f∘x absolutamente contínua;
- **BDLS Theorem 11:** fornece a propriedade KL para a função definível/l.s.c. usada aqui.

Todas essas condições foram verificadas acima.

Consequentemente:

    integral_0^infinity ||xdot(t)|| dt < infinity,

e cada trajetória converge a um único equilíbrio projetado.

## 3. Teoremas 1–9 — achados específicos

### Teorema 1

O argumento da caixa central é correto.

Foi corrigida uma formulação inadequada que escrevia genericamente

    sum z_j >= 1

para cláusulas com sinais mistos.

A forma correta usa coordenadas de satisfação literal:

    q_cj = (1 + sigma_j^(c) x_j)/2,

de modo que

    g_c <= 0  iff  sum_j q_cj >= 1.

A cota de volume (1/3)^N e a subcota espúria (1/6)^N permanecem inalteradas.

### Teorema 2

O caso multilinear está correto: uma função multilinear não constante possui pelo menos uma derivada parcial polinomial não nula, e o conjunto crítico está contido em seu zero-set de medida zero.

No caso Softplus, Delta Phi_soft > 0 implica não constância; foi explicitado que se escolhe uma derivada parcial analítica não identicamente nula antes de aplicar o teorema de zero-set analítico.

### Teorema 3

A harmonicidade é exata porque todas as diagonais da Hessiana multilinear são zero.

Em ponto crítico não degenerado, Hessiana invertível + traço zero implica ao menos um autovalor positivo e um negativo.

Em ponto crítico degenerado, a ausência de mínimo local já garante pontos de energia menor em toda vizinhança.

### Teorema 4A' / Corolário 4B

A restrição a qualquer face continua multilinear e harmônica.

Um mínimo relativo interior da face força constância na face, logo herda o valor de todos os vértices.

Para 4B foi removida a formulação forte demais de LaSalle (“converge ao maior conjunto invariante”); a forma correta é que omega-limits ficam contidos / trajetórias se aproximam do maior conjunto invariante.

Também foi adicionada a prova de que equilíbrio isolado assintoticamente estável precisa ser mínimo local estrito.

### Teorema 5

A fatoração

    H = V^T W V

está correta.

O bound do número de condição foi explicitamente condicionado a

    rank(V)=N,

pois somente então V^T V é definida positiva e kappa é finito.

### Teorema 6

A prova estava faltando e foi incorporada.

Com w_c <= beta/4 e Gershgorin:

    lambda_max(V^T V) <= 3 d_max / 4,

logo

    L_beta <= 3 d_max beta / 16.

Escolhendo uma cláusula com g_c=0:

    L_beta >= 3 beta / 16.

Os bounds exponenciais do gradiente no box central também conferem.

A terminologia IEEE foi reforçada para distinguir:
- cruzamento do menor normal;
- cruzamento do menor subnormal;
- limiar idealizado de arredondamento para zero em round-to-nearest (metade do menor subnormal);
- modos FTZ/DAZ e dependência da implementação concreta da sigmoid.

### Teorema 7B

A contração centrípeta está correta.

Foi explicitado o passo de projeção:

    v = d+n,
    n in N_X,
    <x,n> >= 0,

logo

    <x,d> <= <x,v> < 0

fora de Z.

A identidade entre equilíbrios projetados e Z permanece válida.

### Proposição 7A

O sinal

    J_ij <= 0

para cláusulas puramente negativas foi rechecado e está correto.

Nenhuma conclusão global de Hirsch é reivindicada; o status de caracterização dinâmica permanece suspenso.

### Teorema 8

Para cláusulas independentes:

    E[mu_norm(Z)]
      = integral p(x)^M dx/2^N
      >= (integral p(x) dx/2^N)^M
      = (5/6)^M.

A aplicação de Jensen é correta.

O domínio foi ajustado editorialmente para N>=3, natural para 3-SAT.

### Teorema 9

O status permanece aberto.

A antiga expressão

    P(x_1^*>0) = C(2K,K)/4^K

não pode ser apresentada como resultado incondicional enquanto a identidade entre o limite do fluxo e a projeção isotônica permanecer sem prova. O manuscrito a apresenta apenas como cálculo **condicional** à hipótese

    x^* = Pi_Z(x_0).

Uma auditoria externa posterior encontrou ainda uma caracterização intermediária incorreta: Horn 3-SAT geral não tem Jacobiano off-diagonal de sinal único. Por exemplo, para

    (not x1 or not x2 or x3),

há um par com J_12<=0 e pares com J_13,J_23>=0. A versão atual foi corrigida para afirmar que Horn geral possui interações de sinais mistos e, portanto, não é automaticamente cooperativo nem competitivo na ordem ortante padrão. A Proposição 7A continua válida apenas para a família puramente negativa.

## 4. Alterações aplicadas à master

Nesta auditoria foram aplicadas correções para:

- coordenadas literais na identificação LP;
- zero-set analítico do Softplus;
- formulação precisa de LaSalle;
- condição rank(V)=N para kappa;
- prova completa do Teorema 6;
- terminologia de underflow IEEE;
- detalhe da projeção no Teorema 7B;
- caráter condicional do cálculo Sparre–Andersen no Teorema 9;
- mapeamento exato dos teoremas KL/PDS;
- nova referência BDLS 2007.

## 5. Riscos residuais

Não foi encontrado risco fatal nos Teoremas 1–8.

Os riscos residuais são:

1. **Teorema 9 permanece deliberadamente aberto.**
2. Os ensembles agora são nomeados separadamente como iid e uniforme sem reposição para evitar promoção silenciosa entre modelos.
3. Uma convenção determinística global para sign(0) foi fixada; resultados tie-independent continuam indicados como tais.
4. A parte Hinge do antigo T10 mantém seu escopo subcrítico explicitamente indicado na tabela síntese.
5. A compilação arXiv deve continuar sendo usada como teste operacional separado da validade matemática.

## 6. Veredito

A dependência PDS/KL que sustentava a minimalidade M6 passa de “citação plausível” para **mapeamento formal hipótese-por-hipótese**.

Não foi encontrado erro fatal.

**Veredito desta rodada: NÃO CONSEGUI REFUTAR APÓS AUDITORIA DOS TEoremas 1–9 E DA DEPENDÊNCIA KL/PDS, com o Teorema 9 explicitamente mantido como problema aberto.**
