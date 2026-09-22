# Teorema de Alta Probabilidade para a Energia Residual (M6)

## 1. Definições Formais e Amostragem Sem Reposição

Seja $\Omega_N$ o conjunto das $Q_N = 8\binom{N}{3}$ cláusulas $3$-SAT assinadas possíveis sobre $N$ variáveis booleanas.
A fórmula $F$ é uma amostra uniforme de $M = \lfloor\alpha N\rfloor$ cláusulas distintas de $\Omega_N$ (modelo uniforme sem reposição).

Consideramos o motivo crítico $M6$, definido como a hiperárvore linear $3$-uniforme de $6$ cláusulas e $13$ variáveis com a estrutura de duplo núcleo e a família de equilíbrios positivos catalogada no certificado original (`CLG_T10_AUDITORIA_ADVERSARIAL_EQUILIBRIOS.md:415`).
O grupo de automorfismos não assinado tem ordem $128$, e a órbita de *gauge* contém exatamente $2^{13}$ configurações de sinais dinamicamente conjugadas.

Definimos a variável aleatória $X_N = X(F)$ como o **número de componentes conexas isoladas em $F$ pertencentes estritamente à órbita de gauge assinada do motivo $M6$**. Uma componente é isolada se nenhuma de suas $13$ variáveis ocorre em qualquer outra cláusula de $F$.

## 2. Diferenças Limitadas e Acoplamento por Troca (Swap)

Analisamos o impacto da substituição de uma única cláusula assinada $c \in F$ por outra cláusula assinada $c' \in \Omega_N \setminus F$.
Como cada cláusula contém exatamente $3$ variáveis, ela intersecta o suporte de no máximo $3$ componentes isoladas disjuntas da órbita $M6$.

*   **Remoção de $c$:** Se $c$ pertencia a uma componente $M6$ isolada, essa componente é destruída (variação $-1$). Se $c$ era a única conexão externa impedindo o isolamento de componentes $M6$, sua remoção pode isolar no máximo $3$ componentes (variação $+3$).
*   **Adição de $c'$:** A inserção de $c'$ pode completar a $6^{\rm a}$ cláusula de uma componente isolada (variação $+1$). Se $c'$ incidir sobre componentes $M6$ já isoladas, pode desisolar no máximo $3$ componentes (variação $-3$).

Em qualquer caso, a variação líquida satisfaz rigidamente:
$$ |X(F) - X(F')| \le 4. $$

Para a amostragem sem reposição de $M$ cláusulas, consideramos o martingal de Doob gerado pela revelação sequencial das cláusulas $c_1, \dots, c_M$. Dadas duas realizações para o passo $k$, acoplamos os sorteios restantes $\{c_{k+1}, \dots, c_M\}$ por uma permutação de troca (transposição elementar). Os conjuntos de cláusulas resultantes são idênticos ou diferem por exatamente uma substituição de cláusula. Pelo limitante de sensibilidade $|X(F) - X(F')| \le 4$, a diferença entre as expectativas condicionais em cada passo do martingal é limitada por $C_{M6} \le 4$.

## 3. Concentração Macroscópica da Densidade

Pela contagem combinatória exata no ensemble (Seção 7 de `CLG_T10_AUDITORIA_ADVERSARIAL_EQUILIBRIOS.md`), a densidade assintótica esperada de componentes isoladas na órbita de gauge é:
$$ d = \frac{729}{64}\alpha^6 e^{-39\alpha}. $$
Para $N$ suficientemente grande, temos $\mathbb{E} X_N \ge \frac{7}{8} d N$.
Pela Desigualdade de Azuma-Hoeffding/McDiarmid aplicada ao martingal acoplado, com $M = \lfloor\alpha N\rfloor \le \alpha N$ e $C = 4$:
$$ \Pr\!\left(X_N < \frac{3}{4} d N\right) \le \Pr\!\left(X_N - \mathbb{E} X_N < - \frac{1}{8} d N\right) \le \exp\!\left( - \frac{2 \left(\frac{1}{8} d N\right)^2}{M \cdot 4^2} \right) \le \exp\!\left( - \frac{d^2}{512 \alpha} N \right). $$

## 4. Captura Dinâmica Condicional Exata e Chernoff

Consideramos a dinâmica contínua dada pelo Sistema Dinâmico Projetado (PDS) multilinear original sobre o hipercubo $[-1, 1]^N$, sob inicialização produto uniforme $\mu_0 = \text{Uniforme}([-1, 1]^N)$.

Pelo certificado dinâmico auditado, cada componente isolada na órbita de gauge do motivo $M6$ possui uma bacia de atração contendo uma caixa aberta especificada com probabilidade uniforme normalizada $p_0 = 2^{-53}$ (o volume bruto de Lebesgue em $[-1, 1]^{13}$ é $2^{13} \cdot 2^{-53} = 2^{-40}$).
Para cada componente isolada $i \in \{1, \dots, X_N\}$, fixamos uma tal caixa aberta certificada $B_i \subset [-1, 1]^{V(i)}$ com medida de probabilidade uniforme normalizada $\mu_{V(i)}(B_i) = p_0 = 2^{-53}$, onde $\mu_{V(i)} = \frac{1}{2^{13}}\lambda_{13}$ denota a distribuição marginal uniforme sobre $[-1, 1]^{V(i)}$.

Como as componentes isoladas possuem suportes disjuntos de variáveis ($V(i) \cap V(j) = \emptyset$ para $i \neq j$), a captura dinâmica opera **componente por componente de forma independente**: não se exige que a inicialização global caia em todas as caixas simultaneamente. Cada componente $i$ cuja coordenada inicial local satisfaça $x(0)_{V(i)} \in B_i$ evolui de forma desacoplada pelo PDS e converge para o continuum de equilíbrios positivos da sua respectiva sub-bacia, deixando ao menos uma cláusula violada no arredondamento.

Sob a medida uniforme produto $\mu_0 = \bigotimes_{j=1}^N \text{Uniforme}([-1, 1])$, os eventos de captura $\{x(0)_{V(i)} \in B_i\}$ são mutuamente independentes condicionados a $F$, cada qual ocorrendo com probabilidade exata $\mu_{V(i)}(B_i) = p_0$.
Definimos a variável de contagem de componentes certificadamente capturadas:
$$ Z_N = \sum_{i=1}^{X_N} \mathbf{1}_{\{x(0)_{V(i)} \in B_i\}}. $$
Condicionado à fórmula $F$, temos rigorosamente:
$$ Z_N \mid F \sim \operatorname{Binomial}(X_N, p_0). $$

Como cada componente capturada gera ao menos uma violação de cláusula, o número total de capturas dinâmicas da rede satisfaz $Y_N \ge Z_N$.

Aplicando o limite inferior multiplicativo de Chernoff para a variável binomial $Z_N$, no evento estrutural onde $X_N \ge \frac{3}{4} d N$:
$$ \Pr\!\left(Z_N < \frac{3}{4} p_0 X_N \;\middle|\; F \right) \le \exp\!\left( - \frac{\left(\frac{1}{4}\right)^2 p_0 X_N}{2} \right) \le \exp\!\left( - \frac{3 p_0 d}{128} N \right). $$

## 5. Teorema Limite da Cota Positiva com Alta Probabilidade

A fração normalizada de energia residual após arredondamento satisfaz $\rho_{\rm mult} \ge \frac{Y_N}{M} \ge \frac{Z_N}{M}$.
Como $M = \lfloor\alpha N\rfloor \le \alpha N$, na interseção dos eventos de concentração de $X_N$ e $Z_N$, temos:
$$ \rho_{\rm mult} \ge \frac{Z_N}{\alpha N} \ge \frac{\frac{3}{4} p_0 \left( \frac{3}{4} d N \right)}{\alpha N} = \frac{9}{16} \frac{p_0 d}{\alpha}. $$

Substituindo os valores de $d = \frac{729}{64}\alpha^6 e^{-39\alpha}$ e $p_0 = 2^{-53}$:
$$ \frac{9}{16} \frac{p_0 d}{\alpha} = \frac{9}{16} \cdot 2^{-53} \cdot \frac{729}{64} \alpha^5 e^{-39\alpha} = \frac{6561}{1024} \cdot \frac{\alpha^5 e^{-39\alpha}}{2^{53}} = \frac{6561}{2^{63}} \alpha^5 e^{-39\alpha}. $$

Como $\frac{6561}{2^3} = \frac{6561}{8} = 820{,}125 > 729$, segue que:
$$ \frac{6561}{2^{63}} = \frac{6561/8}{2^{60}} > \frac{729}{2^{60}}. $$
Portanto:
$$ \frac{9}{16} \frac{p_0 d}{\alpha} > \frac{729}{2^{60}} \alpha^5 e^{-39\alpha}. $$

Como a probabilidade de falha é majorada pela união das caudas exponenciais:
$$ \Pr\!\left( \rho_{\rm mult} < \frac{729}{2^{60}} \alpha^5 e^{-39\alpha} \right) \le \exp\!\left( - \frac{d^2}{512 \alpha} N \right) + \exp\!\left( - \frac{3 p_0 d}{128} N \right) \longrightarrow 0 \quad (N \to \infty). $$

**Teorema:** Para o fluxo de gradiente projetado multilinear original sobre o hipercubo $[-1, 1]^N$ com inicialização produto uniforme, no modelo de $M = \lfloor\alpha N\rfloor$ cláusulas $3$-SAT assinadas distintas sem reposição ($\alpha > 0$):
$$ \Pr\!\left[ \rho_{\rm mult} \ge \frac{729}{2^{60}} \alpha^5 e^{-39\alpha} \right] \longrightarrow 1 \quad \text{quando } N \to \infty. \quad \blacksquare $$
