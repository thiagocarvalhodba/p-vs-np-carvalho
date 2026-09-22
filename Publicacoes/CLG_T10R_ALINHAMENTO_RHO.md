# T10R — Alinhamento exato da definição de rho_mult

**Data:** 22 de setembro de 2026  
**Objetivo:** alinhar a refutação M6 com a definição histórica exata usada pelo antigo Teorema 10.

## 1. Definição histórica localizada

Na versão histórica de `Publicacoes/CLG_FOUNDATIONS_ARXIV.tex` que continha o antigo Teorema 10, a densidade residual discreta era definida por

    rho(x) = E_disc(sign(x)) / M,

onde `sign(x)` é o arredondamento booleano coordenada a coordenada.

A mesma versão definia a densidade residual assintótica em média por

    rho(alpha) = lim_{T -> infinity} E_{F,x0}[rho(x(T))].

O antigo Teorema 10 afirmava, para alpha < 1/6, que a relaxação multilinear satisfazia residual assintótico zero, tanto em expectativa quanto a.a.s.

Portanto o objeto refutado pelo M6 é exatamente o mesmo objeto normalizado por número total de cláusulas M; não há mudança de normalização entre o teorema histórico e a refutação atual.

## 2. Ambiguidade histórica de notação

A notação antiga reutilizava `rho(alpha)` para um valor já esperado sobre fórmula e inicialização, e depois escrevia afirmações probabilísticas envolvendo `rho_mult(alpha)`.

Isso mistura dois objetos diferentes:

1. a variável aleatória de tamanho finito, dependente de F e x0;
2. sua esperança conjunta.

A versão auditada passa a separar esses objetos.

Para uma fórmula F com M cláusulas e inicialização x0:

    rho_{N,T}(F,x0)
      = E_disc(sign(x_{F,x0}(T))) / M.

Como o PDS converge:

    rho_N(F,x0)
      = lim_{T -> infinity} rho_{N,T}(F,x0).

A média conjunta é

    bar_rho_N(alpha)
      = E_{F,x0}[rho_N(F,x0)].

## 3. Refutação em esperança

O motivo M6 fornece

    liminf_{N -> infinity} bar_rho_{N,mult}(alpha)
      >= (729 / 2^59) alpha^5 exp(-39 alpha)
      > 0

para todo alpha > 0 fixo no modelo uniforme de cláusulas assinadas distintas.

Isso contradiz diretamente a antiga conclusão de expectativa zero no intervalo alpha < 1/6.

## 4. Refutação com alta probabilidade

A auditoria probabilística independente também estabelece

    P_{F,x0}[
      rho_{N,mult}(F,x0)
      >= (729 / 2^60) alpha^5 exp(-39 alpha)
    ] -> 1.

Mais fortemente, com

    d(alpha) = (729/64) alpha^6 exp(-39 alpha),
    p0 = 2^-53,

temos, para N suficientemente grande,

    P_F[
      P_{x0}(
        rho_{N,mult}(F,x0)
        >= (729/2^60) alpha^5 exp(-39 alpha)
        | F
      )
      >= 1 - exp(-(3 p0 d(alpha)/128) N)
    ]
    >= 1 - exp(-(d(alpha)^2/(512 alpha)) N).

Portanto uma fórmula típica já contém uma população linear de componentes M6 isoladas e, condicionada a essa fórmula, a inicialização produto uniforme produz residual macroscópico certificado com probabilidade exponencialmente próxima de 1.

## 5. Relação lógica com o antigo T10

A cadeia correta é:

    antigo T10:
      bar_rho_{N,mult}(alpha) -> 0
      e residual zero a.a.s.

    resultado M6:
      liminf bar_rho_{N,mult}(alpha) > 0
      e rho_{N,mult}(F,x0) >= c(alpha) > 0 w.h.p.

Logo as duas versões da conclusão multilinear do antigo T10 são refutadas.

A refutação não depende de comparar numericamente Hinge e Multilinear. Ela já é completa porque uma das afirmações centrais do T10 era o desaparecimento do residual multilinear.

## 6. Escopo

O resultado vale para o ensemble explicitamente auditado:

- M = floor(alpha N);
- universo de Q_N = 8 C(N,3) cláusulas 3-SAT assinadas distintas;
- amostragem uniforme sem reposição;
- inicialização x0 produto uniforme em [-1,1]^N;
- fluxo de gradiente projetado multilinear;
- arredondamento booleano coordenada a coordenada;
- residual normalizado por M.

A expectativa no modelo iid/com reposição possui a mesma constante principal; a prova w.h.p. atualmente certificada é a do modelo uniforme sem reposição.
