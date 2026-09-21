# Auditoria adversarial do Lema 10.5 — PDS, Łojasiewicz e trocas de face

## Status após auditoria

**Lema 10.5: reaberto.** A versão mergeada na PR #2 contém duas passagens que não devem ser tratadas como fechadas:

1. a preservação de nulidade de medida por “aplicações de impacto” entre faces não foi demonstrada com hipóteses suficientes e é especialmente delicada porque o semifluxo de um projected dynamical system (PDS) pode perder invertibilidade após contato com o bordo;
2. a frase “Łojasiewicz nos estratos + controle das trocas de face” não é, por si só, um teorema de convergência para o PDS.

A auditoria também encontrou uma lacuna anterior e mais estrutural: em uma hiperárvore, **não é verdade em geral que toda cláusula violada possua uma variável de grau 1**. Uma hiperaresta interna pode ter todos os seus vértices compartilhados com outras hiperarestas. Logo, energia positiva não implica automaticamente a existência de uma *cláusula violada folha*. Isso afeta o uso dessa afirmação em L10.2/L10.3 e impede declarar T10 fechado sem um lema adicional.

## 1. Formulação correta do PDS sem mapas de impacto

Seja (X=[-1,1]^n), (T_X(x)) o cone tangente de Bouligand e (N_X(x)=T_X(x)^circ) o cone normal convexo. Para (v=-\nabla\Phi(x)), a decomposição ortogonal de Moreau para os cones polares dá unicamente

[
v=\Pi_{T_X(x)}v+\Pi_{N_X(x)}v,
qquad
\langle\Pi_Tv,\Pi_Nv\rangle=0.
]

Portanto, para a solução do PDS,

[
\dot x=\Pi_{T_X(x)}(-\nabla\Phi(x)),
]

existe (n(t)\in N_X(x(t))) tal que

[
-\nabla\Phi(x(t))=\dot x(t)+n(t),
]

isto é,

[
-\dot x(t)\in \nabla\Phi(x(t))+N_X(x(t))
=\partial(\Phi+\delta_X)(x(t))
quad\text{a.e.}
]

Como (X) é convexo e (Phi) é (C^1), a última igualdade é a regra de soma padrão para a subdiferencial limitante/convexa do indicador. Além disso, a ortogonalidade de Moreau fornece

[
\frac{d}{dt}\Phi(x(t))
=\langle\nabla\Phi(x(t)),\dot x(t)\rangle
=-\|\dot x(t)\|^2
quad\text{a.e.}
]

Esta formulação é global: ela atravessa mudanças de face sem introduzir mapas de impacto.

## 2. Etapa de Łojasiewicz/Kurdyka–Łojasiewicz

Defina a função estendida

[
F=\Phi+\delta_X.
]

No caso CLG multilinear, (Phi) é polinomial e (X) é um politopo semialgébrico; logo (F) é própria, semicontínua inferior e semialgébrica (portanto subanalítica/definível no domínio compacto).

O resultado de Bolte–Daniilidis–Lewis, *SIAM Journal on Optimization* 17 (2007), 1205–1223, DOI 10.1137/050644641, estende a desigualdade de Łojasiewicz a funções subanalíticas não suaves e obtém comprimento finito/convergência para trajetórias limitadas de sistemas subgradiente sob regularidade suficiente (por exemplo, convexidade ou lower-(C^2)).

Para o nosso (F), a forma mais segura de usar essa literatura é registrar explicitamente a hipótese de regularidade exigida pelo teorema aplicado, em vez de inferir “semialgébrico ⇒ toda curva subgradiente converge”. A caixa é compacta, portanto toda trajetória do PDS é limitada; a identificação acima mostra que ela é uma curva subgradiente de (F). **A aplicação final do teorema de comprimento finito fica condicionada à verificação textual da classe de regularidade de (F=\Phi+\delta_X) no resultado citado (ou a uma referência equivalente específica para função (C^1) sobre conjunto convexo poliédrico).**

Assim, esta auditoria não usa a etapa KL para encobrir uma hipótese não verificada.

## 3. Por que a prova por aplicações de impacto é retirada

A versão anterior afirmava que, num contato transversal, a aplicação de impacto é (C^1) e que pré-imagens de conjuntos nulos permanecem nulas. Mesmo quando um tempo de primeiro impacto é regular, isso não resolve globalmente o PDS:

- a projeção no cone tangente muda de fórmula no bordo;
- o semifluxo pode deixar de ser invertível após contato com o bordo;
- uma aplicação (C^1) não preserva nulidade de pré-imagens sem uma condição de posto/não-degenerescência apropriada;
- acumulação de contatos não é automaticamente um conjunto semialgébrico de dimensão menor apenas porque o campo original é polinomial.

Consequentemente, a seção de “impact maps” da PR #2 não é usada como fundamento de T10.

A formulação por inclusão diferencial/subgradiente é a substituição correta para a **convergência através das faces**, mas ela não resolve sozinha a questão de **medida zero da bacia de equilíbrios positivos**.

## 4. Contra-ataque ao argumento da folha

A afirmação

> “se (Phi(x)>0), escolha uma cláusula violada (c); como a componente é uma árvore, (c) possui variável folha”

é falsa para hiperárvores gerais.

Uma hiperárvore 3-uniforme linear pode conter uma hiperaresta interna (c={a,b,c}) em que (a,b,c) têm grau pelo menos 2, cada um ligando (c) a um ramo distinto. A aciclicidade garante folhas **em algum lugar da componente**, não uma variável de grau 1 em cada hiperaresta.

Portanto, a tentativa de fortalecer L10.5 para

[
\mathcal E_{\rm proj}(K)\subseteq\{\Phi=0\}
]

por um único argumento local de folha **não está demonstrada**.

O mesmo ponto deve ser auditado nos Lemas 10.2 e 10.3: sempre que a prova requer uma *cláusula violada folha*, é necessário provar sua existência a partir das condições de criticidade/equilíbrio, e não apenas da aciclicidade.

## 5. Estado lógico correto

Ficam rigorosamente separados três problemas:

1. **PDS através das faces:** a equivalência por Moreau com a inclusão normal/subgradiente evita a necessidade de aplicações de impacto para formular a dinâmica global.
2. **Convergência a um ponto:** há uma rota KL/subgradiente forte, mas a referência deve ser aplicada com suas hipóteses exatas de regularidade.
3. **Exclusão/evitação de equilíbrios positivos:** continua sendo o gargalo. Nem a KL nem a inclusão diferencial provam que o limite tem energia zero. O argumento “toda cláusula violada tem folha” não pode ser usado.

Até que o item 3 seja fechado (e o item 2 citado com hipótese exata), o Lema 10.5 e o Teorema 10 devem permanecer **abertos/parciais**, não verdes.

## Referências

- J. Bolte, A. Daniilidis, A. Lewis, *The Łojasiewicz Inequality for Nonsmooth Subanalytic Functions with Applications to Subgradient Dynamical Systems*, SIAM J. Optim. 17 (2007), 1205–1223, DOI 10.1137/050644641.
- M.-G. Cojocaru, literatura de projected dynamical systems em conjuntos convexos: projeção no cone tangente e formulação por cone normal.
- Teorema de decomposição de Moreau para cones convexos fechados polares.
