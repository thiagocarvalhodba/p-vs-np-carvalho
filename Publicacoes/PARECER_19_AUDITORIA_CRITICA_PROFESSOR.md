# Parecer Crítico nº 19 — Auditoria Independente do Pacote Enviar_18.zip
**Avaliador:** Professor / Revisor Matemático Independente  
**Data:** 17 de Setembro de 2026  
**Documento Auditado:** Pacote `Enviar_18.zip` e Manuscrito `CLG_FOUNDATIONS_ARXIV.tex` (Versão 4.0.2)

---

## 0. Veredito Geral do Enviar_18
A versão do `Enviar_18.zip` incorporou praticamente todas as correções do Parecer 18, mas, fazendo uma auditoria independente do pacote — e não simplesmente conferindo se as respostas dizem que a correção foi feita — encontrei dois problemas matemáticos que continuam no manuscrito, sendo um deles relevante.

O ponto que mais me preocupa está abaixo:

---

## 1. A Proposição 7A ainda não foi realmente "suspensa"
Vocês mudaram corretamente o título para:  
*Jacobian Structure for Purely Negative Clause Families (Under Re-Audit)*.  
Isso foi bom.

Mas o corpo da proposição ainda contém o item 2:
$$A_N = (1/3, 1)^N$$
e afirma:
*"The flow projected ... attracts the orthant $A_N$ to the polytope $Z$ maintaining positive coordinates, producing rounding $\text{sign}(x) = (+1, \dots, +1)$ in 100% of trajectories."*

Esse trecho é muito mais forte do que o status "Under Re-Audit" sugere.

E existe um contraexemplo numérico simples:
Para $N=4$, considere:
$$x_0 = (0.334, 1, 1, 1).$$
Esse ponto pertence a $(1/3, 1)^4$.
Integrando o próprio fluxo Hinge definido no artigo, obtém-se aproximadamente um estado limite do tipo:
$$x^* \approx (-0.004, \, 1/3, \, 1/3, \, 1/3).$$
Ou seja: $x_1(t)$ **não permanece positivo**.
Portanto a frase *" $A_N$ mantém todas as coordenadas positivas"* é **falsa como afirmação universal**.
E consequentemente também é falsa a conclusão imediata:
$$\text{sign}(x^*) = (+1, +1, +1, +1)$$
para 100% das trajetórias.

Isso é particularmente importante porque a proposição continua sendo apresentada como parte formal do artigo.

### O que sobrevive?
Uma afirmação diferente pode continuar verdadeira:
$$A_N \subseteq \mathcal{B}_{\text{spur}}$$
se vocês demonstrarem que toda trajetória iniciada em $A_N$ termina em uma região de $Z$ cuja arredondagem continua violando pelo menos uma cláusula. Mas isso é outra proposição.

Não confundam:
* *"permanece no ortante positivo"*  
com
* *"termina em uma configuração fracionária cuja arredondagem é espúria"*.

A primeira já pode ser falsificada. A segunda ainda pode ser investigada.

### Minha recomendação
Retirar completamente o item 2 da Proposição 7A da versão atual.
Deixaria apenas:
$$J_{ij}(x) \le 0$$
e a conclusão:
a família é competitiva/inibitória e, portanto, resultados de monotonicidade cooperativa de Hirsch não podem ser invocados diretamente.
Isso fecha exatamente aquilo que vocês realmente demonstraram.

---

## 2. T7B: Encontrei uma sutileza importante na igualdade $\Phi = 0 = Z$
A derivação do produto interno está correta:
$$\langle -\nabla \Phi_{\text{quad}}(x), \, x \rangle = -\sum_{c \in \text{act}(x)} (2 g_c^2 + g_c) < 0.$$
E o argumento do cone normal também está essencialmente correto.
Porém, há uma questão de redação no passo:
$$\dot{\Phi} = -\|\Pi_T(-\nabla \Phi)\|^2.$$
Isso é válido para o gradiente projetado no cone tangente, usando a propriedade de projeção, mas convém explicitar que o campo projetado é o operador de projeção ortogonal no cone tangente naquele ponto.

Mais importante:
$$\dot{\Phi} = 0 \iff \Pi_T(-\nabla \Phi) = 0 \iff -\nabla \Phi \in N_{\mathcal{X}}(x).$$
Isso dá o conjunto de equilíbrios projetados. E vocês demonstram: $\mathcal{E}_{\text{proj}} = Z$.
Então a conclusão de LaSalle é defensável.

### Diferença Terminológica Essencial:
"Todas as trajetórias convergem a $Z$" significa rigorosamente:
$$\lim_{t \to \infty} \text{dist}(x(t), Z) = 0.$$
Não significa necessariamente:
$$x(t) \to x^* \quad \text{para algum } x^* \in Z.$$
Como $Z$ normalmente é um conjunto contínuo de equilíbrios, uma trajetória pode ter $\omega$-limite dentro de $Z$ sem que vocês tenham demonstrado convergência a um ponto específico.

Eu escreveria:
*"every trajectory approaches the equilibrium set $Z$, i.e., $\lim_{t \to \infty} \text{dist}(x(t), Z) = 0$."*  
Isso elimina uma possível objeção de dinâmica assintótica.  
**T7B:** 🟢 matematicamente muito próximo de fechado; 🟡 apenas ajustar a formulação.

---

## 3. T8 agora está correto — mas existe uma pequena questão de $M$
A prova de Jensen está correta:
$$\mathbb{E}[\mu(Z)] = \int p(x)^M \, d\mu(x) \ge \left(\int p(x) \, d\mu(x)\right)^M = (5/6)^M.$$
E $M = \lfloor \alpha N \rfloor$ dá $\mathbb{E}[\mu(Z)] \ge (5/6)^{\lfloor \alpha N \rfloor}$. Tudo certo.

Só mudaria:
"$t \mapsto t^M$ é estritamente convexa para $M \ge 2$"  
para simplesmente:
"$t \mapsto t^M$ é convexa para $M \ge 1$."  
Porque o resultado que vocês precisam é Jensen; "estritamente convexa" não é necessário.  
Também há o caso $M=0$, se $\alpha N < 1$. É trivial, mas pode ser excluído explicitamente assumindo $M \ge 1$.  
Nada disso afeta o resultado.

---

## 4. Lema 10.1: agora a redação está adequada
A atualização retirou $1 - \mathcal{O}(1/N)$ e colocou $\mathbb{P}(2\text{-core} = \emptyset) \to 1$. Isso foi uma correção importante.
Também está correta a distinção entre $\mathbb{E}[X] = \mathcal{O}(1)$ e uma afirmação estrutural global. Vocês não estão mais cometendo o erro:
$$\mathbb{E}[X] = \mathcal{O}(1) \implies X = 0 \text{ a.a.s.}$$
Isso está bom.

### Dependência explícita:
O argumento de leaf-peeling exige a hipótese estrutural $|c \cap c'| \le 1$. Logo, 2-core vazio não é, sozinho, suficiente para tudo que o item 3 afirma. O texto atual diz *"conditioned on the linear hyperforest structure"*, portanto está razoavelmente protegido. Eu manteria exatamente essa condicionante.

---

## 5. Lema 10.2: o argumento matemático está bom
Aqui eu não encontrei um novo erro fundamental.
A cadeia é: $\text{Tr}(H) = 0$ e, graças à variável privada,
$$H_{\ell p} = \frac{\sigma_\ell \sigma_p}{8}(1 - \sigma_k x^*_k) \ne 0.$$
Logo, $H \ne 0$. Como $H$ é simétrica ($H = H^T$), se todos os autovalores fossem não negativos, então $\text{Tr}(H) = \sum \lambda_i > 0$ pois $H \ne 0$. Contradição com $\text{Tr}(H) = 0$.
Portanto $\lambda_{\min}(H) < 0$. Esse argumento está correto.
A única coisa que eu preservaria em negrito no manuscrito é: **CONDICIONALMENTE A $H_{\text{leaf}}$**, porque isso é essencial.

---

## 6. O caso $d=1$ agora está corretamente tratado
O texto diz $\Phi_{\mathcal{F}}(t) = a t + b$. E separa:
* $a \ne 0 \implies \nabla_{\mathcal{F}}\Phi = a \ne 0$ (não há crítico interior).
* $a = 0 \implies \nabla_{\mathcal{F}}\Phi \equiv 0$ (a aresta inteira é crítica).
Isso está correto. E o mais importante: vocês não tentaram mais esconder esse caso dentro do strict-saddle theorem. Isso é exatamente o que deveria ser feito.

---

## 7. Problema de apresentação no próprio título do artigo
O título atual é:
*"Exact Critical Sets, Harmonic Vertex Confinement, and Rigorous Dynamic Separations in Continuous Relaxations of 3-SAT"*

O problema está em: **Rigorous Dynamic Separations**.
O artigo não demonstra atualmente uma separação dinâmica global. O próprio corpo diz:
* T9 = abandonado / falsificado para cadeias simples;
* T10 = não fechado.
Portanto o título promete mais do que o artigo entrega. Isso é perigoso em revisão por pares porque o avaliador pode chegar ao artigo com a expectativa de encontrar uma prova de separação dinâmica e descobrir que ela está explicitamente aberta.

Eu recomendaria algo como:  
*Computational Landscape Geometry and Representation (CLG-R): Rigorous Structural Results and Open Dynamical Problems for Continuous 3-SAT Relaxations*  
Isso alinha título e conteúdo.

---

## 8. A conclusão do artigo também está um pouco forte demais
No final:
*"We have established the rigorous analytical foundations ... and ... explain why continuous relaxations exhibit divergent algorithmic accessibility..."*  
O verbo "explain" é forte demais considerando que a parte central da acessibilidade dinâmica continua conjectural. Vocês demonstraram diferenças estruturais rigorosas entre representações. Mas:
$$\text{diferença estrutural} \centernot\implies \text{separação algorítmica assintótica}.$$
Eu escreveria algo como:
*"provide a rigorous framework for studying divergent dynamical accessibility"*  
em vez de:
*"explain why ... exhibit divergent algorithmic accessibility."*

---

## 9. Síntese do Progresso Científico
A versão atual está fazendo algo que considero cientificamente muito saudável:
$$\text{Resultado provado} \ne \text{resultado conjecturado} \ne \text{hipótese de trabalho}$$
A matriz está explicitando isso. Especialmente:
* **T8:** provado
* **T9:** falsificado / em aberto
* **T10:** aberto
Isso é muito melhor do que tentar transformar todo o projeto em uma cadeia artificial de "teoremas fechados".

---

## 10. Decisão Final e Recomendações
Se este fosse o meu próprio manuscrito, eu faria uma última correção antes:

### Correção obrigatória:
Remover da Proposição 7A o item $A_N = (1/3, 1)^N$, "mantendo coordenadas positivas" e "100% sign = (+1, ..., +1)". Essa afirmação é vulnerável a contraexemplo.

### Correções recomendadas:
1. Trocar "Rigorous Dynamic Separations" no título.
2. Trocar "explain why ... divergent algorithmic accessibility" na conclusão.
3. Em T7B, escrever explicitamente $\lim_{t \to \infty} \text{dist}(x(t), Z) = 0$.
4. Em T8, trocar "strictly convex" por "convex" para a aplicação de Jensen.
5. Manter a condicionalidade de $H_{\text{leaf}}$ visível em todo T10.

### Consequência Estrutural:
Depois de retirar o item 2 da Proposição 7A, o núcleo rigoroso do artigo fica mais limpo, não mais fraco:
$$T_1 \text{--} T_6 \implies T_{7B} (\text{Hinge} \to Z) \implies T_8 (\text{volume LP}) \implies T_9 (\text{Horn}) \implies T_{10} (\text{strict saddle parcial})$$
E a Conjectura Central fica claramente separada de tudo isso.

| Item | Situação após auditoria |
| :--- | :---: |
| T8 — cota $(5/6)^M$ | 🟢 Correto |
| T9 — cadeia + fato unitário | 🟢 Falsificação corretamente registrada |
| PAV/isotonic projection | 🟢 Corretamente deixado em aberto |
| L10.1 — 2-core | 🟡 Parcial |
| L10.2 — strict saddle | 🟢 Correto condicionalmente |
| T10 — separação subcrítica | 🔴 Corretamente não fechado |
| T7B — Hinge | 🟡 Muito próximo, mas há uma questão de formulação |
| Proposição 7A | 🔴 Ainda contém afirmação dinâmica não demonstrada |
| Título/Conclusão geral do artigo | 🟠 Ainda excessivamente forte |
