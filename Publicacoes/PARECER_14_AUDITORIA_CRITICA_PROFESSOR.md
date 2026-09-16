# PARECER Nº 14 DO PROFESSOR (AUDITORIA CRÍTICA E TESTES DE FALSIFICAÇÃO)

**Avaliador:** O Professor (Auditor Sênior / Comitê de Avaliação Externa)  
**Destinatário:** Thiago Carvalho e Equipe do Framework CLG-R  
**Data:** 16 de Setembro de 2026  

---

A **Resposta 14** é substancialmente mais forte que a versão anterior, mas, depois de refazer a auditoria matemática dos argumentos apresentados, **não considero justificável a conclusão "aprovação total sem ressalvas"**.

O ponto importante é que agora conseguimos separar claramente o que foi realmente fechado do que apenas foi declarado como fechado.

### 1. T8 — agora está corretamente saneado

A correção assintótica está correta:

$$
\mathbb E[\mu(Z)]\ge(5/6)^{\alpha N},
\qquad
(5/6)^{\alpha N}\to0.
$$

Portanto, a cota de Jensen pode ser usada como **cota positiva para dimensão finita**, mas não como demonstração de volume assintoticamente macroscópico.

Isso resolve a objeção anterior.

---

## 2. T7B — a prova está muito melhor, mas há um detalhe que eu ainda verificaria

A estratégia

$$
x\notin Z
\Longrightarrow
\langle-\nabla\Phi_{\rm quad}(x),x\rangle<0
\Longrightarrow
-\nabla\Phi_{\rm quad}(x)\notin N_X(x)
$$

é adequada para excluir equilíbrios projetados fora de \(Z\).

E a outra inclusão é imediata:

$$
x\in Z
\Longrightarrow
\nabla\Phi_{\rm quad}(x)=0
\Longrightarrow
x\in E_{\rm proj}.
$$

Assim:

$$
E_{\rm proj}=Z.
$$

Esse é um avanço real.

Mas eu ainda gostaria que a versão formal do manuscrito apresentasse explicitamente a identidade do campo projetado e a convenção usada para o cone normal. Não porque a ideia esteja errada, mas porque **esse é exatamente o tipo de ponto em que uma prova de dinâmica projetada pode esconder uma hipótese de sinal/bordo**.

Eu classificaria:

$$
\boxed{\text{T7B: muito próximo de fechado}}
$$

e não "homologado sem ressalvas".

---

# 3. T9 — aqui continua existindo um problema objetivo

O problema que identifiquei anteriormente **continua literalmente presente na Resposta 14**.

Vocês afirmam:

$$
P(x_1^\star>0)
=
\frac{\binom{2K}{K}}{2^{2K}}
=
\frac1{\pi K}
\left(1-\frac1{8K}+O(K^{-2})\right).
$$

Isso está matematicamente errado.

A expansão correta é:

$$
\boxed{
\frac{\binom{2K}{K}}{4^K}
=
\frac1{\sqrt{\pi K}}
\left(
1-\frac1{8K}+O(K^{-2})
\right)
}
$$

e, portanto,

$$
\boxed{
P(x_1^\star>0)=\Theta(K^{-1/2})
}
$$

e não:

$$
\Theta(K^{-1}).
$$

Logo a conclusão qualitativa desejada ainda pode sobreviver:

$$
P(x_1^\star\le0)
=
1-O(K^{-1/2})
=
1-o(1).
$$

Mas a prova quantitativa escrita precisa ser corrigida.

---

# 4. Mais importante: a conservação da média ainda é incompatível com o fato unitário

Este é, para mim, o problema principal do T9.

Vocês afirmam simultaneamente:

$$
x_1=1
$$

como fato unitário, e:

$$
\frac{d}{dt}\bar x(t)=0.
$$

Mas se o fato unitário está incluído em

$$
\Phi_{\rm quad},
$$

ele produz uma força em \(x_1\).

Para a penalização do fato:

$$
h(x_1)
=
\left[\max(0,(1-x_1)/2)\right]^2,
$$

temos, para \(x_1<1\),

$$
-\frac{\partial h}{\partial x_1}
=
\frac{1-x_1}{2}>0.
$$

Portanto a soma das coordenadas recebe uma contribuição:

$$
\frac{d}{dt}\sum_kx_k>0
$$

em geral.

Então não podemos simultaneamente ter:

$$
\boxed{\text{fato unitário ativo}}
$$

e

$$
\boxed{\sum_kx_k=\text{constante}}
$$

sem uma compensação adicional no sistema.

Esse ponto precisa ser resolvido **na equação diferencial**, não por uma explicação textual.

---

# 5. Consequentemente, o salto

$$
T(x_0)=\Pi_Z(x_0)
$$

continua não demonstrado

A Resposta 14 afirma:

$$
T(x_0)=\Pi_Z(x_0)
$$

e então aplica PAV.

Mas existem três objetos diferentes:

### A. Fluxo Hinge

$$
\dot x=-\nabla\Phi_{\rm quad}(x)
$$

### B. Projeção Euclidiana

$$
\Pi_Z(x_0)
=
\arg\min_{z\in Z}\|z-x_0\|^2
$$

### C. Algoritmo PAV

que calcula B.

Para usar Sparre Andersen, precisamos provar:

$$
\boxed{A=B}
$$

para esse sistema.

A resposta demonstra essencialmente propriedades de B/PAV, mas ainda não demonstra rigorosamente:

$$
\boxed{
\lim_{t\to\infty}\phi_t(x_0)
=
\Pi_Z(x_0).
}
$$

E isso é exatamente o elo crítico.

---

# 6. Há ainda uma distinção fundamental sobre o conjunto \(Z\)

O Teorema 7B estabelece que:

$$
\lim_{t\to\infty}x(t)\in Z.
$$

Isso dá:

$$
\mu(B(Z))=1.
$$

Excelente.

Mas T9 precisa de algo muito mais específico:

$$
\mu\left(
T^{-1}(R_K)
\right)
=
1-o(1).
$$

Ou seja:

$$
\boxed{
\text{não basta cair em }Z;
\text{ é preciso saber onde dentro de }Z\text{ o fluxo cai.}
}
$$

Esse é exatamente o motivo pelo qual T7B não fecha T9 sozinho.

A Resposta 14 reconhece isso formalmente, mas depois pressupõe que o mapa é PAV.

---

# 7. T10.1 também não está completamente fechado

A nova utilização do 2-core é uma boa direção:

$$
\alpha<1/6
$$

é suficientemente abaixo do limiar de 2-core citado.

Mas:

$$
2\text{-core}(H)=\varnothing
$$

não implica automaticamente a afirmação mais forte:

$$
|c\cap c'|\le1
$$

para todas as cláusulas.

São propriedades diferentes.

É necessário demonstrar separadamente que, no ensemble usado:

$$
P\left(
\exists c\neq c':
|c\cap c'|\ge2
\right)=o(1).
$$

Isso provavelmente é tratável por primeira-momento/união, mas precisa aparecer na prova.

---

# 8. E o T10.2 ainda possui uma falha estrutural

A primeira parte é correta:

$$
\frac{\partial^2\Phi_{\rm mult}}
{\partial x_i^2}
=0.
$$

Logo:

$$
\operatorname{diag}(H)=0
$$

e:

$$
\operatorname{Tr}(H)=0.
$$

Então:

$$
H\neq0
\quad\Longrightarrow\quad
\lambda_{\min}(H)<0
$$

é uma consequência válida para matriz Hessiana simétrica com traço zero.

**Mas falta provar \(H\neq0\).**

A resposta tenta fazer isso através de uma cláusula violada e de uma variável folha.

O problema é a passagem:

$$
\text{variável folha}
\Rightarrow
H_{\ell p}\neq0
$$

na **Hessiana total**.

É preciso eliminar rigorosamente a possibilidade de outras cláusulas contribuírem para a mesma entrada ou demonstrar que, pela incidência da variável folha, elas não podem.

---

# 9. E eu removeria esta desigualdade

A resposta afirma:

$$
\lambda_{\min}(H_F)
\le
-\frac{1}{d(d-1)}
\|H_F\|_F
\le-b<0.
$$

Não precisamos dela.

Para provar strict saddle basta:

$$
H_F=H_F^T,
\qquad
\operatorname{Tr}(H_F)=0,
\qquad
H_F\neq0.
$$

Então necessariamente:

$$
\boxed{\lambda_{\min}(H_F)<0.}
$$

É uma prova mais limpa e mais difícil de atacar.

A cota quantitativa introduz uma obrigação adicional de prova que não traz benefício para o teorema.

---

# 10. Há um problema ainda maior no fechamento do T10

Vocês concluem:

$$
\rho_{\rm mult}(\alpha)\to0
$$

e:

$$
\rho_{\rm quad}(\alpha)\ge c(\alpha)>0.
$$

Mas a única cota explícita de volume apresentada anteriormente foi:

$$
(5/6)^{\alpha N},
$$

que tende a zero.

Logo o argumento de:

$$
\rho_{\rm quad}\ge c(\alpha)>0
$$

precisa vir **inteiramente de uma análise de bacia**, não do T8.

Isso precisa ficar cristalino no manuscrito.

E, nesse caso, T9 e T10 não podem compartilhar silenciosamente o mesmo argumento.

---

# 11. Há uma diferença importante entre T9 e T10 que eu preservaria

### T9

Problema específico:

$$
\text{cadeia Horn linear + fato unitário}.
$$

Aqui vocês querem demonstrar:

$$
\mathcal M_{\rm spur}\to1.
$$

### T10

Problema:

$$
\text{random 3-SAT},\quad\alpha<1/6.
$$

Aqui vocês querem:

$$
\mathcal M_{\rm spur}(\Phi_{\rm mult})\to0
$$

e uma separação para Hinge.

Esses são resultados diferentes.

Eu **não tentaria usar T9 como evidência matemática para T10**.

---

# 12. Minha avaliação após a Resposta 14

Se eu tivesse que colocar um status rigoroso — sem "aprovação", sem ranking — ficaria:

$$
\boxed{
\begin{array}{c|c}
\text{Resultado}&\text{Estado}\\
\hline
T1, T2\text{ etc.}&\text{fechados sob hipóteses}\\
T4A'&\text{fechado/provável}\\
T7B&\text{quase fechado}\\
T8&\text{fechado como cota finita}\\
T9&\textbf{não fechado}\\
T10.1&\text{parcialmente fechado}\\
T10.2&\textbf{não fechado}\\
T10&\textbf{não fechado}
\end{array}
}
$$

O motivo não é "falta de polimento". São **lacunas matemáticas identificáveis**.

---

# 13. Mas agora eu faria algo diferente

Eu **não pediria outra "Resposta 15" geral**.

Isso provavelmente produziria mais texto e mais declarações de fechamento.

Eu transformaria o próximo passo em um **teste de falsificação**.

### Teste A — T9

Para \(K=2,\ldots,10\):

$$
\dot x=-\nabla\Phi_{\rm quad}(x)
$$

com o fato unitário exatamente como definido no código.

Para cada \(x_0\):

1. integrar até estacionar;
2. obter \(T_{\rm Hinge}(x_0)\);
3. calcular \(\Pi_Z(x_0)\) por PAV;
4. comparar:

$$
\|T_{\rm Hinge}(x_0)-\Pi_Z(x_0)\|_\infty.
$$

Se for diferente para **um único ponto**, o Lema 9.1 como está escrito cai.

### Teste B — conservação

Calcular numericamente:

$$
\frac{d}{dt}\sum_i x_i.
$$

Se o fato estiver no potencial, espero encontrar imediatamente a violação da alegada conservação.

### Teste C — T10.2

Gerar todos os pontos críticos relevantes para pequenos \(N\) e verificar:

$$
\Phi_{\rm mult}(x^\star)>0
$$

versus:

$$
\lambda_{\min}(H(x^\star)).
$$

Isso pode revelar exatamente se existem os temidos pontos degenerados/flat.

---

## O ponto central

A Resposta 14 conseguiu **transformar as críticas anteriores em três problemas matemáticos muito concretos**. Isso é bom.

Mas ela ainda comete um erro metodológico:

$$
\boxed{
\text{"Lema formulado + argumento plausível + simulação = lema demonstrado".}
}
$$

Não.

Neste estágio, eu congelaria a V4.0.1 e **não acrescentaria absolutamente nenhum teorema**.

O próximo movimento deve ser:

$$
\boxed{
\textbf{tentar derrubar o Lema 9.1 por contraexemplo computacional exato.}
}
$$

E, paralelamente, corrigir imediatamente:

$$
\frac{1}{\pi K}
\quad\longrightarrow\quad
\frac{1}{\sqrt{\pi K}}.
$$

Se o Lema 9.1 sobreviver ao teste \(K=2,\ldots,10\) **com o fato unitário incluído**, aí vale a pena investir numa prova analítica de

$$
T_{\rm Hinge}=\Pi_Z.
$$

Esse é, neste momento, o gargalo científico real do CLG-R.
