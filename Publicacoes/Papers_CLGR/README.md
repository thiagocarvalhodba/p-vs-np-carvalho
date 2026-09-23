# CLG-R — Papers derivados

Esta pasta contém três artigos derivados da versão auditada **CLG-R v4.0.5**, em inglês e português.

Contato do autor: **thiagocarvalho.dba@gmail.com**

## Paper 1 — M6

**English:** *Minimal Positive-Measure Obstructions in Projected Multilinear 3-SAT Dynamics*  
**Português:** *Obstruções Mínimas de Medida Positiva na Dinâmica Multilinear Projetada de 3-SAT*

Núcleo: minimalidade do motivo M6 em hiperárvores lineares, bacia aberta certificada, ocorrência com densidade linear em fórmulas aleatórias esparsas e cotas residuais em esperança e com alta probabilidade.

## Paper 2 — Geometria das relaxações

**English:** *Geometry of Continuous 3-SAT Relaxations*  
**Português:** *Geometria de Relaxações Contínuas de 3-SAT*

Núcleo: comparação geométrica entre Hinge quadrático, extensão multilinear e Softplus; platô LP, harmonicidade, mínimos em faces, fatoração da Hessiana, condicionamento e contração centrípeta.

## Paper 3 — Aleatoriedade, Horn e firewall de complexidade

**English:** *Random and Structured Continuous SAT Dynamics*  
**Português:** *Dinâmica Contínua de SAT em Instâncias Aleatórias e Estruturadas*

Núcleo: volume esperado do politopo LP, residual Hinge subcrítico, cadeias Horn, cálculo Sparre–Andersen condicional, sinais mistos em Horn geral e separação conceitual entre dificuldade dinâmica e complexidade de Turing.

## Aplicabilidade em Computação

Os resultados são diretamente relevantes para:

1. **SAT/CSP e lógica computacional:** explicam como a escolha da relaxação contínua altera o comportamento de solucionadores mesmo quando as representações coincidem nos vértices Booleanos.
2. **Otimização combinatória contínua:** fornecem exemplos e teoremas sobre mínimos espúrios, platôs, condicionamento, rigidez e dinâmica projetada.
3. **Neural combinatorial optimization:** ajudam a analisar surrogates diferenciáveis utilizados para treinar redes que aproximam problemas discretos.
4. **Algoritmos híbridos contínuo-discretos:** indicam quando rounding após uma dinâmica contínua pode preservar erro discreto positivo e quando isso pode ser previsto por motivos locais.
5. **Randomized algorithms e estruturas aleatórias:** a contagem M6 e as provas de concentração conectam motivos locais a comportamento macroscópico em instâncias aleatórias.
6. **Métodos numéricos:** o estudo Softplus quantifica crescimento de Lipschitz/condicionamento e regimes de subnormalidade/underflow.
7. **Sistemas dinâmicos aplicados à computação:** o formalismo PDS/KL dá uma base para estudar convergência de algoritmos contínuos sujeitos a restrições de caixa.
8. **Complexidade computacional:** o firewall com 3-XOR-SAT evita inferências incorretas entre dificuldade de uma dinâmica específica e complexidade de Turing do problema discreto.

Os papers não reivindicam resolver (P) versus (NP). O valor computacional é caracterizar rigorosamente quando e por que determinadas representações contínuas de problemas discretos criam ou evitam obstáculos geométricos e dinâmicos.
