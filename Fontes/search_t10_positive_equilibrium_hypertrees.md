# Ferramenta adversarial do T10: equilíbrios e bacias positivas

`search_t10_positive_equilibrium_hypertrees.py` combina certificados exatos e
buscas finitas para o potencial multilinear em hiperárvores lineares
3-uniformes. Ele é ferramenta de falsificação e reprodução; resultados
universais continuam exigindo prova matemática separada.

## Resultados codificados

- KKT projetado exato na caixa, com `fractions.Fraction`;
- geração de hiperárvores por anexação de folhas e redução de polaridades por
  gauge;
- catálogo de vértices positivos até quatro cláusulas (regressão: 12 cópias
  rotuladas da estrela conhecida);
- expansão e campo foliar do vértice-sela de quatro cláusulas;
- validadores de arestas sem folha e dos tamanhos dos ramos ao redor de um
  núcleo;
- certificado M6 de duplo núcleo, com família 9-dimensional de mínimos
  relativos positivos e aberto capturado de medida normalizada $2^{-53}$;
- certificado M7 independente, com família 12-dimensional e aberto de medida
  $2^{-48}$;
- fórmulas finitas para a expectativa de componentes M6 isoladas nos ensembles
  uniforme sem reposição e i.i.d., e constante assintótica da cota para
  $\mathbb E\rho_{\rm mult}$.

## Certificado principal M6

As arestas são

```text
(0,1,2), (0,3,4), (1,5,6),
(2,7,8), (3,9,10), (4,11,12)
```

e as polaridades são `+++` no primeiro núcleo e `-++` nas cinco cláusulas
restantes. Em coordenadas de fatores,

$$
\Phi=yu_1u_2+(1-y)v_1v_2
+\sum_{j=1}^2(1-u_j)a_jb_j
+\sum_{j=1}^2(1-v_j)c_jd_j.
$$

O conjunto $u_1=u_2=v_1=v_2=1$, com
$a_jb_j>y$ e $c_jd_j>1-y$, é um continuum de equilíbrios de energia 1.
O código avalia exatamente a identidade de mínimo relativo, o PDS adaptado e
as constantes racionais do bootstrap da bacia.

## Ensemble

No modelo com $M$ cláusulas distintas escolhidas entre
$8\binom N3$ cláusulas assinadas, a expectativa exata de cópias M6 isoladas em
toda a órbita de gauge é

$$
\frac{(N)_{13}}{128}\,2^{13}
\frac{\binom{8\binom{N-13}{3}}{M-6}}
     {\binom{8\binom N3}{M}}.
$$

No modelo i.i.d., com $Q=8\binom N3$ e
$Q_0=8\binom{N-13}{3}$, a expectativa finita é

$$
\frac{(N)_{13}}{128}\,2^{13}\frac{(M)_6Q_0^{M-6}}{Q^M}.
$$

Para $M=\lfloor\alpha N\rfloor$, dividida por $N$, ela converge a

$$
\frac{729}{64}\alpha^6e^{-39\alpha}.
$$

Multiplicando pela probabilidade certificada $2^{-53}$ da bacia e normalizando
por $M$, obtém-se

$$
\liminf_N\mathbb E\rho_{\rm mult}(\alpha)
\ge\frac{729}{2^{59}}\alpha^5e^{-39\alpha}>0.
$$

## Execução

```powershell
python -B -m pytest -p no:cacheprovider tests/test_t10_adversarial_equilibria.py
python -B Fontes/search_t10_positive_equilibrium_hypertrees.py --catalogue-vertices-m4
```

Os testes validam implementação e regressão. Uma busca negativa, por si só,
jamais é promovida a prova universal.
