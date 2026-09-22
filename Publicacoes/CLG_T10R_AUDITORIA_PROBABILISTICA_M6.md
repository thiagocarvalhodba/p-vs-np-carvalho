# T10R — Auditoria independente da propagação probabilística do motivo M6

**Data:** 22 de setembro de 2026  
**Objeto:** contagem e concentração de componentes M6 isoladas no modelo uniforme de M = floor(alpha N) cláusulas 3-SAT assinadas distintas, sem reposição.  
**Veredito:** a rota probabilística M6 sobrevive à auditoria independente, com duas correções de formulação: a prova de diferenças limitadas deve usar o comprimento do intervalo condicional do martingale, e a afirmação com alta probabilidade deve distinguir claramente a aleatoriedade da fórmula da aleatoriedade da inicialização.

## 1. Motivo M6 e automorfismos

O suporte estrutural M6 possui 13 variáveis e 6 cláusulas:

    (0,1,2),
    (0,3,4),
    (1,5,6),
    (2,7,8),
    (3,9,10),
    (4,11,12).

O grafo de incidência é uma árvore. No grafo de adjacência entre cláusulas, há duas cláusulas centrais de grau 3 ligadas entre si; cada uma possui duas cláusulas-folha.

Os automorfismos estruturais são:

- troca das duas cláusulas centrais: fator 2;
- troca das duas cláusulas-folha em cada lado: fator 2^2;
- troca das duas variáveis-folha dentro de cada uma das quatro cláusulas-folha: fator 2^4.

Logo

    |Aut(M6)| = 2 * 2^2 * 2^4 = 128.

Uma verificação computacional independente do grafo de incidência bipartido também retorna exatamente 128 automorfismos preservando os tipos variável/cláusula.

## 2. Tamanho da órbita de gauge assinada

Fixada uma cópia estrutural rotulada do M6, o grupo de gauge {±1}^13 age nas polaridades trocando simultaneamente o sinal de todas as ocorrências de cada variável.

Essa ação é livre: se uma transformação de gauge deixa todas as 18 ocorrências literais inalteradas, então cada uma das 13 variáveis deve ter flip trivial, pois toda variável aparece em ao menos uma cláusula.

Portanto a órbita de gauge possui exatamente

    2^13

signings distintos.

Consequentemente o número de candidatos M6 assinados em N variáveis é

    A_N = (N)_13 / 128 * 2^13
        = 64 (N)_13.

Não há sobrecontagem escondida nessa expressão: (N)_13 / 128 conta cópias estruturais não orientadas do hipergrafo rotulado, e para cada conjunto fixo de 6 arestas estruturais a órbita assinada contém 2^13 conjuntos distintos de cláusulas assinadas.

## 3. Probabilidade exata de uma cópia ser uma componente isolada

O universo de cláusulas assinadas é

    Q_N = 8 C(N,3).

Para um suporte fixo S de 13 variáveis, o número de cláusulas assinadas que não tocam S é

    Q_0 = 8 C(N-13,3).

Fixe uma cópia assinada específica do M6. Para que ela apareça como componente isolada, as seis cláusulas do motivo devem ser selecionadas, e as M-6 cláusulas restantes devem pertencer ao conjunto das Q_0 cláusulas que evitam completamente S.

Logo

    P(cópia fixa isolada)
      = C(Q_0, M-6) / C(Q_N, M).

Portanto

    E X_N
      = 64 (N)_13
        C(8 C(N-13,3), M-6)
        / C(8 C(N,3), M).                         (3.1)

Esta é a expressão finita exata para o modelo sem reposição.

## 4. Assintótica da expectativa

Com M = floor(alpha N), alpha > 0 fixo,

    (N)_13 = N^13 (1 + O(1/N)),

e o custo de incluir as seis cláusulas específicas é assintoticamente

    (M)_6 / Q_N^6
      = alpha^6 (3/4)^6 N^-12 (1+O(1/N)).

O fator de isolamento satisfaz

    Q_0 / Q_N
      = C(N-13,3)/C(N,3)
      = 1 - 39/N + O(1/N^2),

e portanto

    (Q_0/Q_N)^(M-6)
      -> exp(-39 alpha).

Assim

    E X_N / N
      -> 64 (3/4)^6 alpha^6 exp(-39 alpha)
       = (729/64) alpha^6 exp(-39 alpha).          (4.1)

Defina

    d(alpha) = (729/64) alpha^6 exp(-39 alpha).

Então

    E X_N = d(alpha) N + o(N).

## 5. Diferenças limitadas para uma troca de cláusula

Sejam F e F' fórmulas de M cláusulas que diferem por uma única troca

    F' = F - {e} + {e'}.

Afirmamos:

    |X(F') - X(F)| <= 4.                           (5.1)

### Remoção de e

Se e pertence a uma componente M6 isolada, sua remoção pode destruir no máximo essa única componente: contribuição -1.

Se e não está numa componente M6 isolada, sua remoção pode separar a componente conexa que contém e. Como e possui exatamente três variáveis, após removê-la há no máximo três blocos conexos distintos adjacentes a essas três variáveis. Portanto no máximo três novas componentes isoladas M6 podem surgir.

Assim

    -1 <= Delta_remove <= 3.

### Adição de e'

A cláusula e' toca no máximo três componentes conexas distintas, uma por variável. Logo sua adição pode destruir no máximo três componentes M6 isoladas, fundindo-as a uma componente maior.

Por outro lado, e' pode criar no máximo uma nova componente M6: a componente conexa final que contém e' é única.

Assim

    -3 <= Delta_add <= 1.

Somando,

    -4 <= X(F') - X(F) <= 4,

provando (5.1).

## 6. Concentração sem reposição: a constante correta

Represente a amostra uniforme sem reposição pelas primeiras M posições de uma permutação uniforme das Q_N cláusulas assinadas.

Considere o martingale de Doob obtido revelando sequencialmente essas M cláusulas.

Fixado um prefixo até o passo k-1, compare duas possibilidades a e b para a k-ésima cláusula. Acople os sufixos por uma transposição a <-> b. Os conjuntos finais produzidos pelo acoplamento são iguais ou diferem por exatamente uma troca de cláusula.

Pelo Lema (5.1), os valores finais de X diferem por no máximo 4. Logo, para cada passo k, as possíveis expectativas condicionais ocupam um intervalo de comprimento no máximo 4.

A forma de Hoeffding para martingales com intervalos condicionais de comprimento c_k dá

    P(X_N - E X_N <= -t)
      <= exp( -2 t^2 / sum_k c_k^2 )
      <= exp( -2 t^2 / (16 M) ).                  (6.1)

Este é o fundamento correto para o fator 2 no expoente. Não basta dizer apenas que cada incremento tem módulo <= 4.

Como E X_N >= (7/8)dN para N suficientemente grande, tomando t = dN/8,

    P(X_N < (3/4)dN)
      <= exp( - d^2 N / (512 alpha) )              (6.2)

para N suficientemente grande.

Portanto há linearmente muitas componentes M6 isoladas com probabilidade 1 - exp(-Theta(N)) sobre a fórmula.

## 7. Captura dinâmica condicional à fórmula

Cada componente M6 isolada possui uma caixa aberta certificada de probabilidade produto uniforme

    p_0 = 2^-53.

Componentes isoladas possuem suportes de variáveis disjuntos. Como a inicialização global é produto uniforme, condicionada a uma fórmula F com X_N componentes isoladas, os eventos de captura são independentes e

    Z_N | F ~ Binomial(X_N, p_0).                  (7.1)

Se X_N >= (3/4)dN, Chernoff com delta = 1/4 dá

    P_x( Z_N < (3/4)p_0 X_N | F )
      <= exp( - p_0 X_N / 32 )
      <= exp( - 3 p_0 d N / 128 ).                (7.2)

Cada captura produz pelo menos uma cláusula violada distinta após rounding.

## 8. Lower bound de energia residual

Como M <= alpha N,

    rho_mult >= Z_N / M.

Na interseção dos eventos bons de (6.2) e (7.2),

    rho_mult
      >= (9/16) p_0 d / alpha
       = (6561 / 2^63) alpha^5 exp(-39 alpha).

Como

    6561 / 2^63 > 729 / 2^60,

segue a cota conservadora

    rho_mult
      >= (729 / 2^60) alpha^5 exp(-39 alpha).      (8.1)

## 9. Formulação probabilística correta em dois níveis

Há duas fontes de aleatoriedade distintas:

1. a fórmula F;
2. a inicialização x(0), condicionada a F.

A forma mais informativa do resultado é:

Para todo alpha > 0 fixo, existem c_1(alpha), c_2(alpha) > 0 tais que, para N suficientemente grande,

    P_F[
      P_x(
        rho_mult >= (729/2^60) alpha^5 exp(-39 alpha)
        | F
      )
      >= 1 - exp(-c_2 N)
    ]
    >= 1 - exp(-c_1 N).                            (9.1)

Pode-se tomar

    c_1 = d(alpha)^2 / (512 alpha),

e

    c_2 = 3 p_0 d(alpha) / 128,

até ajustes inofensivos de N grande.

Em particular, integrando sobre F,

    P_{F,x}[
      rho_mult >= (729/2^60) alpha^5 exp(-39 alpha)
    ]
    -> 1.                                           (9.2)

Assim a afirmação conjunta w.h.p. é verdadeira, mas (9.1) é mais forte e deixa explícito que uma fórmula típica já possui probabilidade condicional exponencialmente alta de apresentar a densidade residual certificada sob inicialização produto uniforme.

## 10. Relação com a afirmação em esperança

A refutação em esperança não precisa de concentração. Pela linearidade da esperança,

    liminf E rho_mult
      >= (729 / 2^59) alpha^5 exp(-39 alpha) > 0,

usando diretamente E X_N e p_0.

A prova de alta probabilidade fortalece essa refutação e mostra que a energia residual positiva não é sustentada por uma cauda rara de fórmulas.

## 11. Status após auditoria

- ordem do grupo de automorfismos 128: **VERIFICADA**;
- tamanho da órbita de gauge 2^13: **VERIFICADO**;
- expressão finita da expectativa: **VERIFICADA**;
- constante assintótica 729/64: **VERIFICADA**;
- expoente de isolamento exp(-39 alpha): **VERIFICADO**;
- sensibilidade por troca <= 4: **PROVADA**;
- concentração exponencial de X_N: **PROVADA**, usando intervalo condicional do martingale;
- independência condicional das capturas: **PROVADA**;
- Chernoff: **PROVADA**;
- lower bound w.h.p. da energia residual: **PROVADO** no modelo uniforme sem reposição + inicialização produto uniforme.

A única cautela editorial restante é alinhar a notação rho_mult e o espaço de probabilidade exatamente com a formulação histórica de T10 no manuscrito principal, para evitar ambiguidade entre probabilidade sobre fórmulas, sobre inicializações, ou conjunta.


## 11. Resolução da auditoria de escala temporal do certificado M6

Uma auditoria externa apontou uma aparente discrepância de fator 4 entre as derivadas de Φ escritas em coordenadas-fator e as velocidades usadas no bootstrap quantitativo M6.

A discrepância é apenas de parametrização temporal. Para uma coordenada-fator

    z = (1±x)/2,

temos

    ∂_x Φ = ±(1/2) ∂_z Φ
    e
    ż = ±(1/2) ẋ.

Como o fluxo original é ẋ = Proj(-∇_x Φ), no tempo original t:

    ż = (1/4) Proj(-∇_z Φ).

Assim, no envelope usado no M6:

    |∂_y Φ| ≤ 31/256
    => |ẏ| ≤ (1/4)(31/256) = 31/1024,

e para uma folha:

    |∂_a Φ| ≤ 1/16
    => |ȧ| ≤ 1/64.

Do mesmo modo, para um fator central u,

    -∂_u Φ ≥ 13/64
    => u̇ ≥ 13/256,

de forma que o tempo para atravessar no máximo 1/16 é

    (1/16)/(13/256) = 16/13.

Consequentemente os deslocamentos usados no bootstrap permanecem exatamente

    (31/1024)(16/13) = 31/832,

e

    (1/64)(16/13) = 1/52.

Logo a caixa certificada, sua massa p0=2^-53 e todas as constantes probabilísticas derivadas dela permanecem inalteradas. O manuscrito principal passou a declarar explicitamente essa conversão de tempo para eliminar a ambiguidade.
