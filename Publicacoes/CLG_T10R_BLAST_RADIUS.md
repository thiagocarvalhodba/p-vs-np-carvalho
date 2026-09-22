# T10R — Auditoria de impacto ("blast radius") da refutação do antigo Teorema 10

**Data:** 22 de setembro de 2026  
**Escopo:** documentos públicos da branch `master` afetados logicamente pela refutação M6.

## 1. Resultado que dispara a revisão

No ensemble uniforme de M = floor(alpha N) cláusulas 3-SAT assinadas distintas, com inicialização produto uniforme e fluxo projetado multilinear, foi estabelecido:

    liminf_{N -> infinity} bar_rho_{N,mult}(alpha)
      >= (729 / 2^59) alpha^5 exp(-39 alpha) > 0,

e

    P_{F,x0}[
      rho_{N,mult}(F,x0)
      >= (729 / 2^60) alpha^5 exp(-39 alpha)
    ] -> 1.

Além disso, dentro da classe de hiperárvores conexas, lineares, 3-uniformes e Berge-acíclicas,

    m_{*,HT}^{mult} = 6.

Logo qualquer afirmação dependente de "rho_mult -> 0 no regime subcrítico" deve ser retirada ou reformulada.

## 2. Afirmações diretamente refutadas

### Antigo Teorema 10

A conclusão

    rho_mult(alpha) -> 0

em expectativa ou a.a.s. para alpha < 1/6 está refutada.

A antiga conclusão de "complete subcritical dynamic separation" baseada em

    rho_quad > 0 = rho_mult

também está refutada.

### Lema 10.2 universal de sela estrita

Não pode ser usado para excluir todos os atratores positivos em componentes árvore: o M6 possui um continuum positivo de mínimos relativos não estritos com bacia aberta.

### Reduções por face que excluíam atratores não isolados

Qualquer argumento que passasse de "isolated asymptotically stable equilibria are vertices" para "all attracting sets are vertices" é inválido. O primeiro enunciado pode permanecer; o segundo é contradito pelo M6.

## 3. Resultados que sobrevivem

Os seguintes resultados não são refutados pelo M6:

- harmonicidade da relaxação multilinear;
- exclusão de mínimos estritos no interior;
- caracterização de mínimos relativos em faces como funções constantes tangencialmente;
- confinamento a vértices de equilíbrios **isolados** assintoticamente estáveis;
- convergência pontual do PDS para um único equilíbrio via Moreau + KL;
- resultados Hinge independentes do T10 multilinear;
- firewall epistemológico: dificuldade do fluxo contínuo não implica separação P versus NP.

A palavra **isolado** é essencial no resultado de confinamento a vértices.

## 4. Conjectura central após M6

Para o ensemble aleatório uniforme, a positividade de rho_mult deixa de ser conjectural: há lower bound positivo em expectativa e w.h.p. para todo alpha > 0 fixo.

Assim, no intervalo de clustering, a parte ainda conjectural é comparativa:

    rho_quad > rho_mult,

e não mais

    rho_quad > rho_mult > 0.

Para ensembles plantados, a frequência M6 não foi provada neste trabalho; a comparação residual deve ser tratada separadamente.

## 5. Alterações aplicadas ao manuscrito

O arquivo `Publicacoes/CLG_FOUNDATIONS_ARXIV.tex` foi atualizado para:

- separar a variável aleatória rho_N(F,x0) de sua esperança bar_rho_N(alpha);
- declarar a refutação do antigo T10 em expectativa e w.h.p.;
- incorporar a prova de concentração M6 ao corpo do teorema;
- registrar a minimalidade M6 no resumo;
- reduzir a Conjectura Central à comparação Hinge versus Multilinear no ensemble aleatório;
- atualizar a tabela de síntese e a matriz formal de status;
- atualizar a conclusão;
- avançar a versão editorial para CLG-R v4.0.5.

## 6. Documentos auxiliares canônicos

A trilha de evidência atual é:

- `CLG_T10R_PROVA_MINIMALIDADE_M6.md`: minimalidade determinística m*=6;
- `CLG_T10R_AUDITORIA_PROBABILISTICA_M6.md`: contagem, automorfismos, concentração e captura;
- `CLG_T10R_ALINHAMENTO_RHO.md`: alinhamento exato com a definição histórica de rho;
- `CLG_T10_AUDITORIA_ADVERSARIAL_EQUILIBRIOS.md`: auditoria principal do T10;
- `../PROVA_ALTA_PROBABILIDADE_M6.md`: prova detalhada w.h.p.

## 7. Pacote arXiv regenerado

O arquivo `Publicacoes/arxiv_package.zip` foi regenerado automaticamente a partir da versão 4.0.5 do fonte. O pacote contém o TeX atual, bibliografia, BBL pré-compilado, as três figuras raster referenciadas e `ARXIV_PACKAGE_MANIFEST.txt` com hashes SHA-256 dos componentes.

A regeneração também restaura automaticamente PNGs a partir dos SVGs canônicos quando o TeX referencia uma figura raster ausente. O workflow correspondente é `.github/workflows/rebuild_arxiv_package.yml`.

## 8. Estado final da auditoria de impacto

Após as correções no fonte principal:

- não permanece no `.tex` atual nenhuma afirmação de `rho_mult = 0`;
- referências à antiga "complete subcritical separation" aparecem apenas como afirmações explicitamente refutadas;
- o resultado "isolated asymptotically stable equilibria are vertices" permanece, pois não é contradito pelo M6;
- a conjectura central foi reduzida para não tratar positividade de rho_mult como questão aberta no ensemble aleatório;
- o pacote arXiv foi regenerado e possui manifesto de integridade sincronizado com a versão 4.0.5.
