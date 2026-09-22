# CLG-R v4.0.5 — Final release audit

**Data:** 22 de setembro de 2026  
**Escopo:** regressão final pós-referee + compilação TeX real da versão destinada ao pacote arXiv.

## 1. Resultado

A fase de auditoria interna de publicação é encerrada sem erro matemático fatal conhecido.

A versão compilada corresponde ao commit-fonte:

`a092a656a3bf30c9062ecdb5ba0148ce93d3b882`

O workflow de compilação e empacotamento concluiu com sucesso:

- GitHub Actions run: `35798253253`
- run number: 23
- conclusão: **success**
- PDF: 20 páginas, A4, 2,382,267 bytes
- artifact: `clg-r-v4.0.5-compiled`
- artifact id: `10724986693`
- SHA-256 do ZIP arXiv:
  `7967e4f0d0c4ab597dab6053b12d21b9c933ac335bc5b3d58e8b705616da118c`

O pacote regenerado foi gravado pela automação no commit:

`032d57d0bbbca553f11adb9ac9a5299aa7863883`

O manifesto registra corretamente:

`Source commit: a092a656a3bf30c9062ecdb5ba0148ce93d3b882`.

## 2. Teste de compilação

O workflow executa `latexmk -pdf` em ambiente Ubuntu/TeX Live real e falha em caso de:

- erro fatal do pdfLaTeX;
- referência indefinida após a convergência do latexmk;
- citação indefinida após a convergência;
- labels multiplicados.

A primeira tentativa desta rodada encontrou um problema operacional real:

> pdfTeX error (font expansion): auto expansion is only possible with scalable fonts.

A causa era a combinação de microtype com fontes não escaláveis do ambiente mínimo. O manuscrito passou a usar Latin Modern escalável e o workflow instala explicitamente `lmodern`. A compilação subsequente passou.

## 3. Regressão final

A regressão pós-referee verificou e/ou corrigiu:

1. **Horn 3-SAT:** removida a caracterização incorreta de Horn geral como sistema competitivo. A família geral possui sinais mistos no Jacobiano; a Proposição 7A permanece restrita a cláusulas puramente negativas.
2. **IEEE 754:** separados os níveis de mínimo normal, mínimo subnormal e limiar idealizado de round-to-zero; o texto ressalta dependência da implementação e FTZ/DAZ.
3. **Ensembles:** introduzidas as notações distintas
   [
   mathcal E_{m iid}(N,alpha)
   quad	ext{e}quad
   mathcal E_{m unif}(N,alpha).
   ]
4. **Rounding:** fixada uma convenção global determinística para (operatorname{sign}(0)).
5. **T5/T6:** condições de posto e limites espectrais permanecem explícitos.
6. **T9:** permanece formalmente **Open**; Sparre--Andersen continua apenas condicional à identificação isotônica não provada.
7. **PDS/KL:** permanece o mapeamento explícito para BDLS Theorem 11 e BDL Theorem 4.5 / 4.7 / Remark 4.8.
8. **M6:** nenhuma regressão no fator temporal (1/4), caixa certificada, (p_0=2^{-53}), contagem, concentração ou constantes residuais.
9. **Tabelas e resumo:** escopos foram alinhados aos teoremas finais; afirmações condicionais não aparecem como universais.
10. **Formatação:** equações longas e tabelas foram quebradas/convertidas para layouts com wrap. A compilação final não apresenta overfull boxes materiais; permanecem apenas avisos cosméticos de underfull em algumas células de tabelas.

## 4. Checks estruturais finais

Na versão final auditada:

- citações ausentes: **0**
- referências internas ausentes: **0**
- labels duplicados: **0**
- notação ambígua antiga `E(N,alpha)`: **0**
- antiga frase “Horn geral é competitivo”: **0**
- antiga redação ambígua de underflow: **0**
- compile TeX real: **PASS**
- geração do PDF: **PASS**
- geração do pacote arXiv: **PASS**

Avisos de citações/referências aparecem naturalmente no primeiro passe do LaTeX, mas o `latexmk` converge; o check do log final passou sem referências ou citações indefinidas.

## 5. Status matemático após a auditoria

- T1–T8: fechados dentro das hipóteses declaradas.
- T9: aberto, explicitamente.
- PDS/KL: auditado hipótese por hipótese.
- Minimalidade M6: provada no escopo HT declarado.
- Contagem M6: provada no ensemble uniforme auditado.
- Propagação w.h.p.: provada.
- Antigo Teorema 10 de separação subcrítica completa: refutado e substituído pelo lower bound M6.
- Conjectura central remanescente: comparativa, não existential.
- Nenhuma implicação para (P) versus (NP) é reivindicada.

## 6. Veredito

**FINAL INTERNAL RELEASE AUDIT: PASS.**

Isto significa que a versão sobreviveu ao processo interno de derivação, red-team, múltiplos referees adversariais e compilação reprodutível. Não significa certificação absoluta nem substitui peer review humano externo.
