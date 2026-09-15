# Parecer de Auditoria Matemática e Topológica — Resolução do Parecer nº 12

**Nível de Rigor:** Annals of Mathematics / Inventiones Mathematicae  
**Especialidade:** Topologia Diferencial, Teoria de Sistemas Dinâmicos Suaves e Descontínuos, Otimização Contínua em Variedades com Bordo  
**Data da Auditoria:** 15 de Setembro de 2026  
**Documentos Auditados:**
1. `Publicacoes/RespostaAoProfessor_Analise12.md`
2. `Publicacoes/CLG_FOUNDATIONS_ARXIV.tex`
3. `Publicacoes/ESTUDO_ANALITICO_DO_CONJUNTO_CRITICO.md`
4. `Fontes/clg_framework.py`
5. `tests/test_clg_theorems.py`

---

## 1. Veredito Executivo

A reformulação apresentada na **Resposta ao Parecer nº 12** eleva significativamente a maturidade analítica do programa CLG-R. Em especial:
* O acolhimento da **Desigualdade de Jensen** no Teorema 8 resolve com perfeição o problema da integração espacial sobre $x \in [-1, 1]^N$.
* A identidade centrípeta do **Teorema 7B** ($\langle -\nabla \Phi_{\text{quad}}(x), x \rangle < 0$) e a eliminação de equilíbrios de bordo via cone normal $N_{\mathcal{X}}(x^*)$ representam uma demonstração definitiva da ausência de atratores locais espúrios fora do politopo LP $Z$.
* A redação do **Teorema 4A′** através do Princípio do Mínimo Forte em faces relativas é irrepreensível.

Contudo, submetendo o texto ao padrão dos periódicos matemáticos de primeira linha (*Annals of Mathematics*, *Inventiones Mathematicae*), identificamos **três vulnerabilidades técnicas de alta gravidade**, sendo uma delas uma **falácia lógica com contraexemplo construtivo explícito**:

1. **Vulnerabilidade Fatal no Passo 2 do Teorema 10 (Falácia da Indução Folha-Raiz):** A afirmação de que em qualquer fórmula com topologia de árvore não existem mínimos locais discretos com $E_{\text{disc}} > 0$ é matematicamente falsa. Construímos um contraexemplo exato (uma hiperárvore acíclica de 7 cláusulas e 15 variáveis) onde a atribuição $s_0 = (-\mathbf{1})$ possui $E_{\text{disc}} = 1 > 0$, todo 1-flip aumenta a energia ($\Delta E \in \{0, +1\}$), e no espaço contínuo $s_0$ é um mínimo local relativo de $\Phi_{\text{mult}}$ sobre o hipercubo com energia $1.0$. A dedução escrita assumiu erroneamente que a variável folha pertence à cláusula violada.
2. **Inconsistência Topológica na Aplicação de Lee et al. (2016) / Panageas & Piliouras (2017):** Os teoremas de escape de *strict saddles* baseados no *Stable Manifold Theorem* aplicam-se a difeomorfismos suaves em variedades abertas ou sem bordo. A projeção métrica $\Pi_{\mathcal{X}}$ no hipercubo não é um difeomorfismo (possui posto deficiente e colapsa abertos em faces). A aplicação ao hipercubo exige análise estratificada face-a-face (Lee et al., Math. Programming 2019), ignorada na Resposta 12.
3. **Conflito entre Irredutibilidade de Hirsch e Redutibilidade de DAGs no Teorema 9:** O Teorema do Fluxo Monótono Forte de Hirsch (1985) requer irredutibilidade da matriz Jacobiana (grafo de dependência fortemente conexo). Redes acíclicas de implicação unitária (DAGs) são estritamente redutíveis (Jacobiana triangularizável). Para DAGs, o fechamento deve decorrer de sistemas dinâmicos em cascata (indução na ordenação topológica), e não de Hirsch clássico. Ademais, o fluxo genérico converge para o conjunto de modelos satisfatíveis, e não exclusivamente para o modelo mínimo.

Apresentamos a seguir o detalhamento analítico exaustivo de cada um dos quatro eixos solicitados.

---

## 2. Ponto 1: Teorema 7B e Fechamento de LaSalle no Hinge

### 2.1. A Identidade Centrípeta e a Eliminação de Equilíbrios no Bordo
Para qualquer cláusula ativa $c \in \text{act}(x)$, temos $g_c(x) > 0$. A violação afim satisfaz:
$$g_c(x) = -\frac{1}{2}(1 + \sigma^{(c)} \cdot x) \iff \sigma^{(c)} \cdot x = -(2 g_c(x) + 1)$$
O campo gradiente negativo do potencial quadrático $\Phi_{\text{quad}}(x) = \sum_{c=1}^M \max(0, g_c(x))^2$ é:
$$-\nabla \Phi_{\text{quad}}(x) = \sum_{c \in \text{act}(x)} g_c(x) \, \sigma^{(c)}$$
Tomando o produto interno canônico com a posição $x$:
$$\langle -\nabla \Phi_{\text{quad}}(x), \, x \rangle = \sum_{c \in \text{act}(x)} g_c(x) (\sigma^{(c)} \cdot x) = -\sum_{c \in \text{act}(x)} \left(2 g_c(x)^2 + g_c(x)\right)$$
Como $g_c(x) > 0$ para todo $c \in \text{act}(x)$, e fora de $Z$ o conjunto $\text{act}(x)$ é não-vazio, segue com estrito rigor:
$$\langle -\nabla \Phi_{\text{quad}}(x), \, x \rangle < 0, \quad \forall x \in \mathcal{X} \setminus Z$$

No bordo $\partial \mathcal{X}$, um ponto $x^*$ é um equilíbrio projetado se e somente se:
$$\Pi_{T_{\mathcal{X}}(x^*)}(-\nabla \Phi_{\text{quad}}(x^*)) = \mathbf{0} \iff -\nabla \Phi_{\text{quad}}(x^*) \in N_{\mathcal{X}}(x^*)$$
onde $N_{\mathcal{X}}(x^*)$ é o cone normal da análise convexa:
$$N_{\mathcal{X}}(x^*) = \{ \nu \in \mathbb{R}^N \mid \langle \nu, y - x^* \rangle \le 0, \; \forall y \in \mathcal{X} \}$$
Para o hipercubo $\mathcal{X} = [-1, 1]^N$, o cone normal é o produto cartesiano:
$$N_{\mathcal{X}}(x^*) = \prod_{i=1}^N N_{[-1, 1]}(x^*_i), \quad N_{[-1, 1]}(x^*_i) = \begin{cases} [0, +\infty), & x^*_i = +1 \\ (-\infty, 0], & x^*_i = -1 \\ \{0\}, & x^*_i \in (-1, 1) \end{cases}$$
Consequentemente, para qualquer vetor normal $\nu \in N_{\mathcal{X}}(x^*)$:
$$\nu_i x^*_i \ge 0, \quad \forall i \in \{1, \dots, N\} \implies \langle \nu, x^* \rangle = \sum_{i=1}^N \nu_i x^*_i \ge 0$$
com $\langle \nu, x^* \rangle > 0$ sempre que $\nu \ne \mathbf{0}$.

Portanto, se existisse um equilíbrio projetado $x^* \in \partial \mathcal{X} \setminus Z$, teríamos $-\nabla \Phi_{\text{quad}}(x^*) \in N_{\mathcal{X}}(x^*)$, o que exigiria:
$$\langle -\nabla \Phi_{\text{quad}}(x^*), \, x^* \rangle \ge 0$$
Isso entra em contradição frontal com a identidade centrípeta $\langle -\nabla \Phi_{\text{quad}}(x^*), \, x^* \rangle < 0$.  
Logo, **não existem equilíbrios projetados (interiores ou de bordo) fora do politopo LP $Z$**.

### 2.2. Fechamento Formal via Invariância de LaSalle e Patologias de Bordo
O argumento via Princípio de Invariância de LaSalle é essencialmente sólido, mas requer atenção a duas sutilezas analíticas para publicação em nível *Annals*:

1. **Regularidade das Soluções e Descontinuidade do Campo Projetado:**
   O campo $\Pi_{T_{\mathcal{X}}(x)}(-\nabla \Phi_{\text{quad}}(x))$ é descontínuo nas transições entre faces de diferentes dimensões. O sistema dinâmico governante é a inclusão diferencial de Moreau:
   $$\dot{x}(t) \in -\nabla \Phi_{\text{quad}}(x(t)) - N_{\mathcal{X}}(x(t))$$
   Como $-\nabla \Phi_{\text{quad}}$ é globalmente Lipschitziano e $N_{\mathcal{X}}$ é o subgradiente da função indicadora do convexo $\mathcal{X}$, o operador $-\nabla \Phi_{\text{quad}} - N_{\mathcal{X}}$ é maximal monótono no espaço de Hilbert $\mathbb{R}^N$. Pelo Teorema clássico de Brézis (1973) e Nagurney & Zhang (1996), para qualquer condição inicial $x_0 \in \mathcal{X}$, existe uma **única solução forte** $x(t)$, que é absolutamente contínua em $[0, \infty)$ e diferenciável quase em toda parte.
2. **Função de Lyapunov Correta no Teorema de LaSalle:**
   O texto do manuscrito (`CLG_FOUNDATIONS_ARXIV.tex`, linha 333) afirma que $\|x(t)\|_2^2$ é uma função de Lyapunov estrita. Essa afirmação é geometricamente esclarecedora, pois:
   $$\langle x, \dot{x} \rangle = \langle x, -\nabla \Phi - \nu \rangle = \langle x, -\nabla \Phi \rangle - \langle x, \nu \rangle \le \langle x, -\nabla \Phi \rangle < 0$$
   mostrando contração radial estrita. No entanto, para aplicar LaSalle e concluir convergência para $Z$, **a função de Lyapunov deve ser o próprio potencial** $V(x) = \Phi_{\text{quad}}(x)$:
   $$\dot{V}(x(t)) = \langle \nabla \Phi_{\text{quad}}(x(t)), \, \dot{x}(t) \rangle = -\|\Pi_{T_{\mathcal{X}}(x(t))}(-\nabla \Phi_{\text{quad}}(x(t)))\|^2 \le 0$$
   O conjunto onde $\dot{V}(x) = 0$ é exatamente o conjunto de equilíbrios projetados:
   $$\mathcal{E} = \{x \in \mathcal{X} \mid \Pi_{T_{\mathcal{X}}(x)}(-\nabla \Phi_{\text{quad}}(x)) = \mathbf{0}\}$$
   Pelo item 2.1, $\mathcal{E} \cap (\mathcal{X} \setminus Z) = \emptyset$. Como em todo $x \in Z$, $\Phi_{\text{quad}}(x) \equiv 0 \implies \nabla \Phi_{\text{quad}}(x) \equiv \mathbf{0} \implies \dot{x} \equiv \mathbf{0}$, todo ponto de $Z$ é um ponto de equilíbrio. Portanto:
   $$\{\dot{V} = 0\} = Z$$
   Sendo $Z$ compacto e trivialmente invariante (todo ponto de $Z$ é estacionário), o maior conjunto invariante contido em $\{\dot{V} = 0\}$ é o próprio $Z$.
3. **Convergência Pontual via Desigualdade de Kurdyka-Łojasiewicz (KL):**
   O Teorema de LaSalle garante apenas que $\lim_{t \to \infty} \text{dist}(x(t), Z) = 0$. Como $\Phi_{\text{quad}}$ é uma função semialgébrica (polinomial quadrática por partes), ela satisfaz a desigualdade de Kurdyka-Łojasiewicz com expoente $\theta = 1/2$. Isso assegura que o comprimento da trajetória é finito ($\int_0^\infty \|\dot{x}(t)\| dt < \infty$) e que toda trajetória converge para um **único ponto limite** $z^* \in Z$.

> **Conclusão do Ponto 1:** O Teorema 7B está **matematicamente blindado**. Sugere-se apenas explicitar no artigo a citação à teoria de inclusões diferenciais monótonas de Brézis (1973) e a propriedade KL para fechamento definitivo.

---

## 3. Ponto 2: Teorema 9 e Cooperatividade de Hirsch

### 3.1. Cálculo Algébrico da Jacobiana para Cláusulas Lineares
Para a implicação linear unitária $c = (x_j \to x_i) \iff (\neg x_j \lor x_i)$, temos $\sigma_i = +1$ e $\sigma_j = -1$. O polinômio multilinear associado é:
$$P_c(x) = \left(\frac{1 - x_i}{2}\right) \left(\frac{1 + x_j}{2}\right) = \frac{1}{4}(1 - x_i + x_j - x_i x_j)$$
O campo gradiente negativo $f(x) = -\nabla P_c(x)$ possui componentes:
$$f_i(x) = -\frac{\partial P_c}{\partial x_i} = +\frac{1}{4}(1 + x_j), \quad f_j(x) = -\frac{\partial P_c}{\partial x_j} = -\frac{1}{4}(1 - x_i)$$
Calculando os elementos da matriz Jacobiana $J(x) = Df(x)$:
$$J_{ij}(x) = \frac{\partial f_i}{\partial x_j} = -\frac{\partial^2 P_c}{\partial x_i \partial x_j} = +\frac{1}{4} > 0$$
$$J_{ji}(x) = \frac{\partial f_j}{\partial x_i} = -\frac{\partial^2 P_c}{\partial x_j \partial x_i} = +\frac{1}{4} > 0$$
Ambos os termos cruzados são positivos. Se a fórmula contém múltiplas cláusulas de implicação linear, a Jacobiana total é a soma das contribuições de cada cláusula:
$$J_{ik}(x) = \sum_{c} \left(-\frac{\partial^2 P_c}{\partial x_i \partial x_k}\right) = \frac{1}{4} \cdot (\text{número de implicações entre } i \text{ e } k) \ge 0, \quad \forall i \ne k$$
Portanto, a condição de Kamke-Müller ($J_{ik}(x) \ge 0, \forall i \ne k$) é universalmente satisfeita em todo o espaço $\mathbb{R}^N$.

### 3.2. Preservação da Monotonicidade pelo Fluxo Projetado no Hipercubo
Como o hipercubo $\mathcal{X} = \prod_{i=1}^N [-1, 1]$ é um produto cartesiano de intervalos, o cone tangente $T_{\mathcal{X}}(x) = \prod_{i=1}^N T_{[-1, 1]}(x_i)$ desacopla coordenada a coordenada. O operador de projeção $\Pi_{T_{\mathcal{X}}(x)}(v)$ atua independentemente em cada entrada:
$$[\Pi_{T_{\mathcal{X}}(x)}(v)]_i = \begin{cases} \min(0, v_i), & x_i = +1 \\ \max(0, v_i), & x_i = -1 \\ v_i, & x_i \in (-1, 1) \end{cases}$$
Seja $F(x) = \Pi_{T_{\mathcal{X}}(x)}(f(x))$. Para verificar a condição de Kamke no bordo:
Suponha $x \le y$ (ordem parcial no cone positivo $\mathbb{R}^N_+$) com $x_k = y_k$.
* Se $x_k = y_k \in (-1, 1)$: $F_k(x) = f_k(x) \le f_k(y) = F_k(y)$ pela cooperatividade de $f$.
* Se $x_k = y_k = +1$: como $f_k(x) \le f_k(y)$ e a função escalar $u \mapsto \min(0, u)$ é não-decrescente, segue $\min(0, f_k(x)) \le \min(0, f_k(y)) \implies F_k(x) \le F_k(y)$.
* Se $x_k = y_k = -1$: analogamente, $u \mapsto \max(0, u)$ é não-decrescente, logo $\max(0, f_k(x)) \le \max(0, f_k(y)) \implies F_k(x) \le F_k(y)$.

Logo, o campo projetado satisfaz estritamente a condição de Kamke-Müller em todo o hipercubo compacto $\mathcal{X}$, preservando a monotonicidade da ordem parcial:
$$x(0) \le y(0) \implies x(t) \le y(t), \quad \forall t \ge 0$$

### 3.3. As Brechas Analíticas do Teorema 9: Irredutibilidade e Modelo Mínimo

Aqui reside uma **imprecisão teórica severa** no texto de `CLG_FOUNDATIONS_ARXIV.tex` e na Resposta 12:

1. **A Falha de Irredutibilidade (Redutibilidade em DAGs):**
   O Teorema de Hirsch (1985, Teorema 7.1) exige que o sistema seja **fortemente cooperativo**, o que requer que a matriz Jacobiana seja **irredutível** (o digrafo de dependências deve ser fortemente conexo).
   Porém, o próprio enunciado do Teorema 9 define a família como uma **rede de implicação acíclica (DAG)**!
   Em um DAG acíclico, o grafo não possui ciclos direcionados. Consequentemente, a matriz Jacobiana é permutável para uma forma **estritamente triangular superior**, sendo por definição **redutível**!
   Para sistemas cooperativos redutíveis, o Teorema do Fluxo Monótono de Hirsch não garante que o conjunto de pontos que convergem para equilíbrios tem medida total sem hipóteses adicionais.
   *A Solução Rigorosa:* Para um DAG acíclico, a convergência decorre não de Hirsch clássico, mas da **teoria de sistemas dinâmicos em cascata** (Sontag, 1995; Smith, 1995): existe uma ordenação topológica $x_{\pi(1)}, \dots, x_{\pi(N)}$. A variável raiz $x_{\pi(1)}$ obedece a uma EDO autônoma unidimensional $\dot{x}_1 = f_1(x_1)$, que converge monotonicamente para seu atrator. Por indução ao longo do DAG, cada variável subsequente torna-se uma EDO unidimensional assintoticamente autônoma que converge monotonicamente. Essa prova é 100% analítica e dispensa o recurso indevido à irredutibilidade.
2. **Imprecisão sobre "Convergência para o Modelo Mínimo":**
   A Resposta 12 e o Teorema 9 afirmam que "as trajetórias partindo de quase todo ponto inicial convergem para o único modelo mínimo satisfatível".
   Isso é logicamente falso se existirem múltiplos modelos satisfatíveis (por exemplo, a fórmula $x_1 \to x_2$ sem fatos unitários admite três modelos: $(-1, -1)$, $(-1, +1)$ e $(+1, +1)$). Uma trajetória iniciando em $x_0 = (+0.8, +0.8)$ converge para $(+1, +1)$ e jamais para o modelo mínimo $(-1, -1)$.
   O que o Teorema prova é que o fluxo converge para o **conjunto de modelos satisfatíveis**, de modo que a energia discreta final é $E_{\text{disc}} = 0$, garantindo $\mathcal{M}_{\text{spur}}(\Phi_{\text{mult}}) = o(1)$. A convergência exclusiva para o *modelo mínimo* só ocorre sob inicialização na base $x_0 = (-\mathbf{1})$ ou sob presença de fatos unitários que determinem um único modelo satisfatível.

---

## 4. Ponto 3: Teorema 10 e Lee et al. (2016)

### 4.1. A Lacuna Topológica da Variedade com Bordo
O Teorema de Lee, Simchowitz, Jordan & Recht (COLT 2016) e Panageas & Piliouras (ITCS 2017) demonstra que métodos de gradiente evitam *strict saddles* quase certamente partindo de inicialização aleatória.  
Entretanto, esses trabalhos formulam o resultado para o mapa de passo de gradiente $g_\eta(x) = x - \eta \nabla f(x)$ como um **difeomorfismo local $\mathcal{C}^1$ em $\mathbb{R}^N$** (ou variedades Riemannianas sem bordo), utilizando o Teorema da Variedade Central-Estável de Shub (1987).

No hipercubo $\mathcal{X} = [-1, 1]^N$, o operador de projeção $\Pi_{\mathcal{X}}$:
* Não é diferenciável na transição entre o interior e as faces.
* Não é injetor: mapeia conjuntos abertos de $\mathbb{R}^N$ em subvariedades de dimensão inferior (as faces de $\mathcal{X}$).
* Direções de escape com curvatura negativa ($\lambda_{\min} < 0$) que apontem para fora do cubo são bloqueadas pela projeção $\Pi_{T_{\mathcal{X}}(x)}$.

Para que o teorema de escape de selas se sustente no hipercubo, é indispensável utilizar a extensão para otimização com restrições convexas de **Lee, Panageas, Piliouras, Simchowitz, Jordan & Recht (Mathematical Programming, 2019)**, realizando uma decomposição estratificada:
$$\mathcal{X} = \bigcup_{\mathcal{F} \in \text{Faces}} \text{relint}(\mathcal{F})$$
Em cada estrato $\text{relint}(\mathcal{F})$, a dinâmica projetada é governada pelo gradiente intrínseco $-\nabla_{\mathcal{F}} \Phi$. O escape de selas deve ser provado estrato por estrato, assegurando que o conjunto de trajetórias que colapsa em variedades estáveis de selas restritas a cada face possui medida de Lebesgue nula em $\mathcal{X}$. Tratar isso como um corolário imediato de Lee et al. (2016) sem menção aos estratos é inaceitável para o corpo editorial do *Annals*.

---

### 4.2. A Falsificação do Passo 2 (Indução Folha-Raiz): O Contraexemplo Construtivo

O Passo 2 da demonstração do Teorema 10 na Resposta 12 afirma:
> *"Em qualquer fórmula com topologia de árvore, considere qualquer atribuição discreta $s \in \{-1, +1\}^N$ com energia positiva ($E_{\text{disc}}(s) > 0$). Existe ao menos uma cláusula violada. Percorrendo a árvore até a folha mais distante dessa componente, a variável folha $x_{\text{folha}}$ aparece em exatamente uma cláusula. Invertendo o sinal de $x_{\text{folha}}$, essa cláusula torna-se satisfeita sem alterar nenhuma outra cláusula da fórmula, reduzindo estritamente a energia discreta. Logo, não existem mínimos locais discretos com $E_{\text{disc}} > 0$."*

**Esta dedução contém um erro lógico elementar de identificação:**  
A variável folha $x_{\text{folha}}$ pertence à cláusula folha, e **NÃO** à cláusula violada que motivou o percurso! Inverter o sinal de $x_{\text{folha}}$ satisfaz uma cláusula folha que já poderia estar satisfeita, sem alterar em nada o estado da cláusula violada na raiz ou centro da árvore!

#### Construção Exata do Contraexemplo:
Considere a fórmula 3-CNF $F_{\text{tree}}$ composta por 7 cláusulas e 15 variáveis. O hipergrafo de incidência bipartido cláusula-variável é estritamente uma **árvore acíclica** (sem nenhum ciclo):
* Cláusula central (raiz): $c_0 = (x_1 \lor x_2 \lor x_3)$.
* Ramo 1: $c_{1a} = (\neg x_1 \lor y_1 \lor z_1)$, $c_{1b} = (\neg x_1 \lor u_1 \lor v_1)$.
* Ramo 2: $c_{2a} = (\neg x_2 \lor y_2 \lor z_2)$, $c_{2b} = (\neg x_2 \lor u_2 \lor v_2)$.
* Ramo 3: $c_{3a} = (\neg x_3 \lor y_3 \lor z_3)$, $c_{3b} = (\neg x_3 \lor u_3 \lor v_3)$.

O grafo possui $7 + 15 = 22$ vértices e exatamente $3 \times 7 = 21$ arestas conexas, sendo topologicamente uma árvore pura.

Avalie a atribuição discreta de falsidade global:
$$s_0 = (-1, -1, \dots, -1) \in \{-1, +1\}^{15}$$
1. **Estado das Cláusulas:**
   * $c_0 = (-1 \lor -1 \lor -1)$ está **violada**;
   * $c_{1a}, c_{1b}$ possuem $\neg x_1 = +1$, logo estão **satisfeitas**;
   * $c_{2a}, c_{2b}$ possuem $\neg x_2 = +1$, logo estão **satisfeitas**;
   * $c_{3a}, c_{3b}$ possuem $\neg x_3 = +1$, logo estão **satisfeitas**.  
   Energia discreta: $E_{\text{disc}}(s_0) = 1 > 0$.
2. **Teste de Todos os 1-Flips Booleanos:**
   * Se invertermos $x_1$ (de $-1$ para $+1$): $c_0$ torna-se satisfeita, mas $\neg x_1$ torna-se falsa e, como $y_1=z_1=u_1=v_1=-1$, as duas cláusulas $c_{1a}$ e $c_{1b}$ **tornam-se violadas simultaneamente**! A energia salta de $1$ para $2$ ($\Delta E = +1$).
   * Pela mesma razão, invertendo $x_2$, a energia salta para $2$ ($\Delta E = +1$).
   * Invertendo $x_3$, a energia salta para $2$ ($\Delta E = +1$).
   * Invertendo qualquer uma das 12 variáveis folha ($y_i, z_i, u_i, v_i$): a cláusula folha já estava satisfeita por $\neg x_i$, e $c_0$ continua violada. A energia permanece invariável ($\Delta E = 0$).
3. **Conclusão Discreta:**  
   Não existe nenhum vizinho de Hamming 1 com energia menor que $1$. O ponto $s_0$ é um **mínimo local discreto estrito em relação às variáveis centrais e fracamente local no hipercubo com $E_{\text{disc}} = 1 > 0$**.
4. **Análise Contínua em $\Phi_{\text{mult}}$:**
   Calculando o gradiente contínuo no ponto $s_0$:
   $$\nabla \Phi_{\text{mult}}(s_0) = (0.5, \; 0.5, \; 0.5, \; 0, \; 0, \; \dots, \; 0)$$
   Como $x_1 = x_2 = x_3 = -1$, o campo gradiente negativo $-\nabla \Phi$ aponta para $(-0.5, -0.5, -0.5)$ (para fora do hipercubo $[-1, 1]^{15}$).
   A projeção no cone tangente é identicamente nula:
   $$\Pi_{T_{\mathcal{X}}(s_0)}(-\nabla \Phi_{\text{mult}}(s_0)) = \mathbf{0}$$
   Portanto, **$s_0$ é um ponto de equilíbrio projetado exato com energia $\Phi_{\text{mult}}(s_0) = 1.0 > 0$**!
   Para qualquer direção $d \ge 0$ apontando para o interior do hipercubo com $d_1 + d_2 + d_3 > 0$, a derivada direcional de primeira ordem é:
   $$\langle \nabla \Phi_{\text{mult}}(s_0), \, d \rangle = 0.5(d_1 + d_2 + d_3) > 0$$
   mostrando que a energia aumenta ao entrar no cubo. Ao longo da face de dimensão 12 formada por $x_1 = x_2 = x_3 = -1$, $\Phi_{\text{mult}}$ é identicamente constante e igual a $1.0$. Logo, **$s_0$ é um mínimo local da restrição de $\Phi_{\text{mult}}$ a $\mathcal{X}$ com energia estritamente positiva**, invalidando a tese de que todos os pontos críticos positivos são selas estritas!

---

## 5. Ponto 4: Teorema 4A′ e Corolário 4B

### 5.1. A Formulação do Teorema 4A′
A alteração para *"mínimo local da restrição de $\Phi_{\text{mult}}$ relativo à face $\mathcal{F}$"* é impecável e metodologicamente perfeita.
A demonstração analítica sustenta-se solidamente:
1. Em qualquer face $\mathcal{F}$ de dimensão $d \ge 1$, fixar as coordenadas restritas preserva o caráter multilinear da função.
2. Como cada variável livre possui grau no máximo 1 em cada monômio, $\frac{\partial^2 \Phi_{\mathcal{F}}}{\partial x_i^2} \equiv 0$, o que implica que a restrição é uma **função harmônica intrínseca**:
   $$\Delta_{\mathcal{F}} \Phi_{\mathcal{F}}(x) \equiv 0, \quad \forall x \in \text{relint}(\mathcal{F})$$
3. Pelo **Princípio do Mínimo Forte para Funções Harmônicas**, se uma função harmônica atinge um mínimo local no domínio aberto conexo $\text{relint}(\mathcal{F})$, ela é identicamente constante em uma vizinhança aberta.
4. Sendo $\Phi_{\mathcal{F}}$ um polinômio real, se ele é constante em uma vizinhança aberta, ele é **identicamente constante em toda a face compacta $\mathcal{F}$**.
5. Em particular, seu valor na face coincide com o valor assumido em todos os vértices booleanos dessa face:
   $$\Phi_{\text{mult}}(x^*) = E_{\text{disc}}(v), \quad \forall v \in \mathcal{V}(\mathcal{F})$$
Isso fecha definitivamente as objeções anteriores do parecerista relativas ao Teorema 4A′.

### 5.2. Análise do Corolário 4B: Atratores Isolados vs. Manifolds de Equilíbrio
O Corolário 4B estabelece que:
> *"todo equilíbrio assintoticamente estável isolado do fluxo projetado é estritamente um vértice discreto $x^* \in \{-1, +1\}^N$."*

Esta formulação é matematicamente verdadeira, pois em qualquer face de dimensão $d \ge 1$ onde $\Phi_{\mathcal{F}}$ seja constante, os equilíbrios formam um contínuo, não sendo **isolados**.

Contudo, alertamos para o perigo epistêmico:
* O Corolário 4B exclui equilíbrios *isolados* de dimensão $d \ge 1$.
* **Ele NÃO exclui a existência de conjuntos atratores não-isolados (manifólios planos de equilíbrio em faces)!**
No contraexemplo apresentado na Seção 4.2, a face de dimensão 12 com $x_1 = x_2 = x_3 = -1$ atua como um platô atrator onde trajetórias colidem e estagnam com energia $1.0$. Portanto, o Corolário 4B não é suficiente para garantir que toda trajetória convirja para um vértice satisfatível.

---

## 6. Quadro Geral de Auditoria e Recomendações de Blindagem para a Versão 4.1

| Teorema | Status Atual | Diagnóstico Rigoroso | Ação de Blindagem Necessária para V4.1 |
| :--- | :---: | :--- | :--- |
| **Teorema 7B (Contração Centrípeta no Hinge)** | 🟢 **Aprovado** | Prova elegante, $\langle -\nabla \Phi, x \rangle < 0$ elimina equilíbrios de bordo via cone normal $N_{\mathcal{X}}$. LaSalle fecha em $Z$. | Citar Brézis (1973) para inclusões diferenciais e propriedade KL para convergência pontual. |
| **Teorema 8 (Cota de Volume LP via Jensen)** | 🟢 **Aprovado** | Jensen $\mathbb{E}[\mu(Z)] \ge (5/6)^{\alpha N}$ resolve a dependência espacial das variáveis. | Manter a cota como cota analítica inferior rigorosa. |
| **Teorema 9 (Cooperatividade em Horn)** | 🟡 **Requer Correção** | $J_{ij} = +1/4$ está correto. Porém, DAGs acíclicos são redutíveis (Hirsch clássico não se aplica). O fluxo não converge unicamente para o modelo mínimo. | Substituir a citação de Hirsch por **sistemas em cascata** (Sontag / Smith) e corrigir o texto para "converge para um modelo satisfatível". |
| **Teorema 10 (Separação Subcrítica)** | 🔴 **Falha no Passo 2** | A indução folha-raiz é falsa (contraexemplo construtivo com árvore de 7 cláusulas). Lee et al. requer análise de variedades estratificadas com bordo. | Restringir o Teorema a famílias onde toda cláusula possui variável folha (árvores-caterpillar/estrelas) ou demonstrar via probabilidade de Poisson que a fração de armadilhas tende a 0. |
| **Teorema 4A′ (Mínimos em Faces)** | 🟢 **Aprovado** | Nomenclatura corrigida. Prova por harmonicidade e Princípio do Mínimo Forte é definitiva. | Manter integralmente como está. |
| **Corolário 4B (Vértices Atratores)** | 🟡 **Atenção Conceitual** | Correto para equilíbrios isolados, mas não impede conjuntos atratores contínuos em faces planas. | Explicitar no manuscrito que atratores de bordo contínuos são selas na direção normal ou neutros tangencialmente. |

---

## 7. Parecer Final do Revisor

A pesquisa desenvolvida no programa CLG-R representa um dos esforços analíticos mais refinados dos últimos anos na intersecção entre complexidade computacional e geometria de paisagens contínuas. A formulação do Teorema 7B (Contração Centrípeta Universal) e a resolução do Teorema 8 via desigualdade de Jensen constituem contribuições matemáticas definitivas.

Para que o trabalho atinja o padrão irrefutável exigido por periódicos do primeiro escalão, a Versão 4.1 deve incorporar imediatamente:
1. A **substituição do argumento folha-raiz do Teorema 10**, reconhecendo a existência de armadilhas locais em árvores ramificadas e delimitando o resultado à classe analítica rigorosamente controlada;
2. A **formalização em cascata (cascaded monotone systems)** no Teorema 9 para redes acíclicas, sanando o conflito com a irredutibilidade de Hirsch;
3. A fundamentação estratificada para a aplicação do escape de selas de Lee et al. em variedades com bordo poliédrico.

Com esses três ajustes, a arquitetura teórica do CLG-R estará blindada contra qualquer investida da comunidade internacional de análise e sistemas dinâmicos.
