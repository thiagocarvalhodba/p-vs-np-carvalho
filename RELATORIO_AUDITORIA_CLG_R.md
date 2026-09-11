# Relatório de Auditoria Profunda — Framework CLG-R (Versão 3.0)

**Escopo:** código-fonte (`Fontes/`), manuscritos (`Publicacoes/`), entregáveis do Parecer 11 e pacote arXiv.
**Data da auditoria:** 11 de setembro de 2026.
**Auditor:** Claude (Fable 5.1), atuando como revisor adversarial nos padrões Annals/JACM/STOC.
**Método:** leitura integral dos arquivos listados na Etapa 1; verificação numérica independente (NumPy/PyTorch, precisão dupla) de cada teorema; suíte `tests/test_clg_theorems.py` (26 testes, executável com `venv\Scripts\python.exe -m pytest tests -q`).

---

## 1. Sumário Executivo e Veredito Geral

### Nota global: **5,0 / 10** — *não pronto para submissão* (arXiv ou periódico) sem correções obrigatórias.

| Dimensão | Nota | Justificativa em uma linha |
| :--- | :---: | :--- |
| Correção matemática dos enunciados | 6,5 | Teoremas 1, 2, 3, 5, 6 e 7B corretos; 4A vazio na prática (H4 quase nunca vale); 7A com prova inválida. |
| Correção das demonstrações | 5,0 | Prova do 7A é falsa (regime linear não persiste); 7B contém afirmação falsa na Resposta 11; definições de bacia incoerentes. |
| Novidade / contribuição | 3,0 | Núcleo dos resultados é folclore (folga LP em $y=1/2$; extensão multilinear tem mínimos em vértices; $\Phi_{\text{mult}}$ é campo médio ingênuo). |
| Ligação teoria ↔ experimentos | 3,5 | Experimentos usam Adam + penalidade de caixa não-convexa + inicialização em $[-0,5;0,5]^N$; nenhum teorema descreve esse sistema. |
| Engenharia de software científico | 5,0 | Gradientes/Hessianas corretos; mas `clg_framework.py` não implementa o que o prompt e o README afirmam; sementes ausentes em CLG-03/04-Fase I; sem testes. |
| Bibliografia e apresentação | 4,0 | Erros bibliográficos verificáveis; referência provavelmente inexistente; omissão de Ercsey-Ravasz & Toroczkai; figuras no zip não referenciadas no `.tex`. |
| Firewall P vs NP | 8,0 | Retratação explícita e correta; resta *overclaim* residual em `README_FONTES.md` e nomes de arquivos/repositório. |

**Maturidade para publicação internacional.** A homologação interna "10/10, zero defeitos" registrada em `MEMORIA_CHECKPOINT_SESSAO.md` **não se sustenta**. Com as correções da Seção 6 o material pode virar uma nota técnica sólida de arXiv (math.OC / cs.CC, cross-list cond-mat.dis-nn) de nível **6,5–7,0**. Não há, no estado atual nem no corrigido, resultado com peso para *Annals of Mathematics*, *JACM* ou STOC/FOCS: os teoremas são exercícios corretos de cálculo e análise convexa sobre relaxações clássicas, e a única questão profunda (Conjectura Central) está aberta e mal formulada.

### Os sete achados que bloqueiam a submissão

1. **Teorema 7A — prova inválida.** A solução $u(t)=e^{-tH_N}u(0)$ só descreve o fluxo enquanto *todas* as cláusulas estão ativas. Para $u(0)$ genérico, as coordenadas abaixo da média cruzam $1/3$ em tempo finito ($t^*=-\ln(1-u_i(0)/\bar u)/(bN)$), a trajetória **abandona** $A_N$, cláusulas desativam e o limite **não** é $\frac13\mathbf 1$. Verificado: 200/200 trajetórias ($N=6$) saem de $A_N$; 0/200 convergem a $\frac13\mathbf 1$. A *conclusão* $A_N\subseteq\mathcal B_{\text{spur}}$ resistiu numericamente (200/200 espúrias), mas está **sem prova**.
2. **Resposta ao Parecer 11 (MD e DOCX) contém afirmação falsa.** Item 3 do Teorema 7B: "$\mathcal M_{\text{spur}}(\Phi_{\text{quad}})-\mathcal M_{\text{spur}}(\Phi_{\text{mult}})\ge 1-0=1$" para UNSAT. Para fórmula UNSAT, *todo* $x$ tem $E_{\text{disc}}(\text{sign}(x))\ge 1$, logo $\mathcal M_{\text{spur}}=1$ para **qualquer** representação e **qualquer** dinâmica; a diferença é $0$. O Corolário 4B não implica $\mathcal M_{\text{spur}}(\Phi_{\text{mult}})=0$: os vértices atratores de uma fórmula UNSAT são todos espúrios.
3. **Teorema 7B é trivial no seu enunciado-manchete.** "$\mathcal M_{\text{spur}}\equiv 1$ para UNSAT" vale por definição para toda relaxação. O conteúdo real (e correto) do 7B é: *$\Phi_{\text{quad}}$ não tem equilíbrios projetados fora do politopo LP $Z$; toda trajetória alcança $Z$*. O resumo do arXiv vende a versão trivial como resultado principal.
4. **Hipótese (H4) não é "genérica": é quase nunca satisfeita.** $b_i(s_{-i})=\tfrac12[E_{\text{disc}}(s_{-i},+1)-E_{\text{disc}}(s_{-i},-1)]$, logo (H4) $\iff$ **nenhuma aresta do hipercubo booleano liga dois vértices de energia igual**. Em 3-SAT aleatório ($N=12$, $M=51$, contagem exaustiva) **24,0 % das $N2^{N-1}$ arestas violam (H4)**; a própria família $F_N$ do Teorema 7A viola (H4) em $s=-\mathbf 1$. O Teorema 4A é portanto vazio para todas as instâncias estudadas. **Boa notícia:** o Corolário 4B **não precisa de (H4)** (prova na §2.4) e o 4A admite um substituto verdadeiro sem (H4).
5. **Definições dos quatro níveis são incompatíveis com 7A/7B.** Nível 2 exige "atrator assintoticamente estável", mas nenhum ponto de um platô plano (Teorema 1) é assintoticamente estável (todo vizinho em $Z$ também é equilíbrio). Pelas definições do próprio manuscrito, $\mathcal S_{\text{spur}}(\Phi_{\text{quad}})=\varnothing$ e $\mathcal M_{\text{spur}}(\Phi_{\text{quad}})=0$, contradizendo 7A e 7B.
6. **Experimentos não testam a teoria.** Todas as três representações recebem `box_penalty = 0.2*sum((x²-1)²)` (não-convexa, cria $2^N$ atratores, destrói a convexidade do Teorema 5 e o platô do Teorema 1), otimização por Adam (não é fluxo gradiente), inicialização em $[-0,5;0,5]^N$ (não uniforme no cubo) e *clamp* (não é projeção do fluxo contínuo). O resultado-manchete "Softplus 69,3 % vs Multilinear 9,3 %" (Fase I, Adam) **desaparece** na auditoria estrita (GD, $N=60$): 0/75 para as três representações.
7. **Bibliografia com erros verificáveis** e ausência de trabalhos essenciais (Ercsey-Ravasz & Toroczkai 2011; Molnár et al. 2018; Calinescu–Chekuri–Pál–Vondrák 2011; Mézard–Ricci-Tersenghi–Zecchina 2003). Detalhes na §2.9.

---

## 2. Auditoria Linha por Linha dos Teoremas 1 a 7B e da Conjectura Central

Notação: $g_c(x)=-\tfrac12(1+\sigma^{(c)}\!\cdot x)$; $\Phi_{\text{quad}}$, $\Phi_{\text{mult}}$, $\Phi_{\text{soft}}$ como em `ESTUDO_ANALITICO_DO_CONJUNTO_CRITICO.md` (doravante ESTUDO) e `CLG_FOUNDATIONS_ARXIV.tex` (doravante TEX). Verificações numéricas referem-se a `tests/test_clg_theorems.py`.

### 2.1 Teorema 1 (Caixa Fracionária Central e Folga LP) — **CORRETO, mas frouxo e de novidade nula**

- **Prova (ESTUDO §3, passos 1–4; TEX ll. 113–124):** correta. Em $\mathcal U_N$, $\sigma\cdot x>-1\Rightarrow g_c<0\Rightarrow\Phi_{\text{quad}}=0$, $\nabla\Phi_{\text{quad}}=0$. Verificado em 2 500 pontos aleatórios (`test_theorem1_plateau_zero_energy_and_gradient`). O raio $1/3$ é justo: com $x_j=-\sigma_j/3$ obtém-se $g_c=0$.
- **Passo 5 ("sob (H3') existe ortante violador"):** (H3') é desnecessário. Qualquer fórmula com $M\ge1$ e (H1) tem um vértice violador (a atribuição que falsifica os três literais da cláusula 1). O teorema vale sob (H1) apenas; listar (H1)–(H3') é inflacionar hipóteses.
- **Cota $\text{Vol}(Z)\ge(2/3)^N$:** verdadeira e muito frouxa. $Z=\{x: g_c(x)\le 0\ \forall c\}$ é o **politopo da relaxação LP** inteiro, que contém $\mathcal U_N$, todos os vértices satisfatórios (se SAT) e muito mais. Medição Monte Carlo ($N=12$, $M=51$): $\mu_{\text{norm}}(Z)\approx 1{,}9\times10^{-3}$ contra $(1/3)^{12}=1{,}9\times10^{-6}$ — três ordens de grandeza de folga (`test_theorem1_measure_bound_is_valid_but_loose`).
- **"Blindagem" da quantificação:** sim, as contas $(2/3)^N$, $(1/3)^N$, $(1/6)^N$ estão certas. Mas a apresentação alterna medida euclidiana e normalizada em cada parágrafo (ESTUDO ll. 46–49; TEX l. 105–110), o que já causou confusão no Parecer 10. Recomenda-se fixar **uma** medida ($\mu_{\text{norm}}$) no manuscrito inteiro.
- **Conteúdo:** o teorema afirma que $y=\mathbf{1}/2$ é ponto interior da relaxação LP de MAX-3-SAT com folga $0{,}5$ e que a penalidade quadrática da LP é nula nesse politopo. Isso é folclore de otimização combinatória (é a razão pela qual a relaxação LP de MAX-SAT é inútil sem arredondamento aleatório — Goemans & Williamson 1994, *SIAM J. Disc. Math.*). O que a redação chama de "conjunto crítico espúrio" é o conjunto dos **mínimos globais** da relaxação (valor 0) cujo arredondamento falha — não são mínimos locais espúrios no sentido da literatura de paisagens. A terminologia deve ser corrigida.
- **§3.2 (deriva média, 96 %)** ainda aparece no ESTUDO (l. 65) apesar de a Resposta 11 afirmar que foi "completamente retirada". Inconsistência documental.

### 2.2 Teorema 2 (Medida Nula dos Críticos) — **CORRETO**

- **Multilinear:** $\Phi_{\text{mult}}\not\equiv$ const $\Rightarrow\exists k:\partial_k\Phi\not\equiv0\Rightarrow\mu(Z(\partial_k\Phi))=0$. Correto. O lema "zeros de polinômio não nulo têm medida nula" é elementar (indução em $N$ + Fubini); citar Okamoto/Caron–Traynor é aceitável, mas a **citação de Okamoto no `.bib` tem título errado** (ver §2.9).
- **Parseval / (H3'):** $\sum_{S\ne\varnothing}\hat\Phi(S)^2=\text{Var}(E_{\text{disc}})$ está correto e a implicação "SAT com $M\ge1\Rightarrow\text{Var}>0$" também. O contraexemplo das 8 cláusulas completas ($\Phi_{\text{mult}}\equiv1$) foi verificado (`test_theorem2_h3prime_counterexample_is_constant`). Portanto (H3') **só** exclui fórmulas UNSAT "isotrópicas"; isto deveria ser dito explicitamente.
- **Softplus:** correto. Observação mais forte e mais simples que a do manuscrito: $\Phi_{\text{soft}}(x)$ depende de $x$ apenas via $Vx$, logo o conjunto crítico, se não vazio, é $x^*+\ker V$ — um subespaço afim de dimensão $N-\text{rank}(V)\le N-1$ (pois $M\ge1$), de medida nula sem invocar o Teorema da Identidade. Com $\text{rank}(V)=N$ o crítico é **um único ponto**.
- **Ressalva conceitual:** "$\mu(\mathcal C_0)=0$" não diz nada sobre dinâmica. O Teorema 6 mostra que, para $\beta$ moderado, $\|\nabla\Phi_{\text{soft}}\|\le \tfrac M2 e^{-\beta(1-3\rho)/2}$ em $\mathcal U_N(\rho)$: em FP32 o *update* $\eta\,\nabla\Phi$ já é menor que um ulp de $x\approx0{,}1$ para $\beta\gtrsim36$ (calculado), muito antes do *underflow* em $\beta\approx175$. O platô "some" em medida mas persiste numericamente.

### 2.3 Teorema 3 (Harmonicidade e Milnor) — **CORRETO; Milnor é decorativo**

- $\Delta\Phi_{\text{mult}}\equiv0$: correto e verificado ($|\text{Tr}\,H|<10^{-14}$; diagonal nula).
- Princípio do Mínimo Forte: correto, com a observação de que se aplica primeiro à bola $B_\delta(x^*)$ (conexa) e depois se estende a $\mathbb R^N$ por ser polinômio. A redação salta essa etapa.
- Item 2: correto (traço nulo + não-degenerado $\Rightarrow$ autovalores de ambos os sinais). Verificado numa fórmula polaridade-balanceada $F\cup\bar F$, onde $x=0$ é crítico interior e a Hessiana tem $\lambda_1<0<\lambda_N$ (`test_theorem3_interior_critical_point_is_saddle`). **Observação relevante:** para 3-SAT aleatório ($N=6,8,12$) a minimização de $\|\nabla\Phi_{\text{mult}}\|^2$ por LBFGS (30 partidas) **não encontrou nenhum ponto crítico interior**; é provável que o Teorema 3 seja vazio para instâncias típicas (os críticos vivem no bordo do cubo), o que enfraquece a narrativa "selas interiores de Morse" como mecanismo da dinâmica. Vale investigar se $\Phi_{\text{mult}}$ de fórmulas genéricas admite algum crítico em $(-1,1)^N$.
- Item 3 e Lema de Seleção de Curvas (Milnor 1968, Lema 3.1): a hipótese se aplica ($\{\Phi<\Phi(x^*)\}$ é semialgébrico aberto com $x^*$ na aderência), a conclusão é correta, mas **não acrescenta nada** ao item "não é mínimo local", que já é a definição. Na Resposta 11 (l. 76) escreve-se "todo ponto crítico interior **isolado** é sela de Morse" — errado: isolado $\ne$ não-degenerado (sela de macaco é isolada e degenerada, sem índice de Morse). O ESTUDO e o TEX estão corretos ("não-degenerado").
- **Novidade:** o fato de a extensão multilinear ser harmônica e de seus extremos no cubo estarem em vértices é clássico (método das esperanças condicionais; Calinescu–Chekuri–Pál–Vondrák, *SIAM J. Comput.* 2011, extensão multilinear de funções submodulares; O'Donnell, *Analysis of Boolean Functions*, 2014). **Mais importante:** $\Phi_{\text{mult}}(m)=\mathbb E_{s\sim\prod\text{Bern}(m_i)}[E_{\text{disc}}(s)]$ — é exatamente a energia de **campo médio ingênuo** da física estatística. O gradiente em $\Phi_{\text{mult}}$ é a dinâmica de campo médio ingênuo a $T=0$; as equações TAP acrescentam o termo de reação de Onsager; BP/SP são as correções de Bethe no grafo de fatores. O manuscrito não identifica esse vínculo, que é o mais relevante para o diálogo com vidros de spin (ver §4).

### 2.4 Teorema 4A e Corolário 4B — **4A VAZIO na prática; 4B CORRETO e demonstrável sem (H4)**

**Equivalência combinatória de (H4).** Na aresta $x_i\in[-1,1]$ com $x_{-i}=s_{-i}$, $\Phi_{\text{mult}}$ é afim e vale $E_{\text{disc}}$ nos extremos, logo
$$b_i(s_{-i})=\tfrac12\big[E_{\text{disc}}(s_{-i},+1)-E_{\text{disc}}(s_{-i},-1)\big].$$
(H4) exige $b_i\neq0$ para **todo** $i$ e **todo** $s_{-i}$: nenhum par de vértices adjacentes pode ter a mesma energia discreta. Consequências:

| Instância | Arestas com $b_i=0$ | Fonte |
| :--- | :---: | :--- |
| 3-SAT aleatório $N=12$, $M=51$ (exaustivo, 49 152 arestas) | **24,0 %** | `verify_clg.py` §G |
| 3-SAT aleatório $N=30$, $M=128$ (amostragem) | ~22,9 % | idem |
| 3-SAT aleatório $N=60$, $M=256$ (amostragem) | ~25,1 % | idem |
| Família $F_N$ do Teorema 7A, em $s=-\mathbf 1$, flip de $x_1$ | $E: 0\to0$ | `test_h4_fails_on_random_3sat_and_on_F_N` |
| Qualquer fórmula SAT com duas soluções a distância de Hamming 1 | viola | trivial |

Chamar (H4) de "conjunto de fórmulas genericamente bem-comportadas" (Resposta 11 §4.3) é **falso**; a condição caracteriza fórmulas cuja paisagem discreta não tem nenhuma aresta plana — essencialmente nenhuma instância de interesse.

**Prova do 4A sob (H4):** correta (a passagem "(H4) $\Rightarrow\Phi_{\mathcal F}$ não constante em toda face de $\dim\ge1$" está implícita e é verdadeira: se $\Phi_{\mathcal F}$ fosse constante, alguma aresta contida em $\mathcal F$ teria $b_i=0$). Mas o teorema é inaplicável.

**Substituto verdadeiro sem (H4) (recomendado):**
> *Teorema 4A′.* Sob (H1), todo mínimo local $x^*$ de $\Phi_{\text{mult}}|_{[-1,1]^N}$ situado no interior relativo de uma face $\mathcal F$ satisfaz $\Phi_{\text{mult}}(x^*)=E_{\text{disc}}(v)$ para **todo** vértice $v$ de $\mathcal F$. Em particular, arredondar as coordenadas livres de $x^*$ de qualquer maneira produz uma atribuição de energia $\Phi_{\text{mult}}(x^*)$.

*Prova.* $x^*$ é mínimo local de $\Phi|_{\mathcal F}$, que é multilinear (harmônica) nas coordenadas livres; pelo Princípio do Mínimo Forte, $\Phi|_{\mathcal F}$ é constante numa vizinhança e, sendo polinômio, em toda a $\mathcal F$; os vértices de $\mathcal F$ são vértices do cubo, onde $\Phi=E_{\text{disc}}$. $\square$ (Verificado em `test_theorem4_local_minima_value_equals_vertex_value`.)

**Corolário 4B sem (H4):**
> Sob (H1) e (H3'), todo equilíbrio isolado assintoticamente estável do fluxo projetado é um vértice.

*Prova.* Estabilidade assintótica + $V=\Phi$ não-crescente dão $\Phi(x)\ge\Phi(x^*)$ numa vizinhança; se $\Phi(x)=\Phi(x^*)$ para $x\ne x^*$ próximo, a trajetória de $x$ tem $\dot V\equiv0$, logo $\Pi_T(-\nabla\Phi)\equiv0$, i.e. $x$ é equilíbrio — contradição com isolamento. Logo $x^*$ é mínimo local **estrito**. Se $x^*$ estivesse no interior relativo de uma face de $\dim\ge1$, o Teorema 4A′ daria $\Phi$ constante na face, contradizendo a estritude. $\square$

Ou seja: (H4) pode ser **eliminada** do manuscrito. Rigor adicional exigido em nível Annals: o fluxo projetado $\dot x=\Pi_{T_{\mathcal X}(x)}(-\nabla\Phi)$ tem lado direito descontínuo; existência/unicidade e a fórmula $\dot V=-\|\Pi_T(-\nabla\Phi)\|^2$ (q.t.p.) devem ser referenciadas (Nagurney & Zhang 1996, *Projected Dynamical Systems*; Brogliato–Daniilidis–Lemaréchal–Acary 2006). A identidade $\langle v,\Pi_K v\rangle=\|\Pi_K v\|^2$ para cone convexo fechado (Moreau) está correta.

### 2.5 Teorema 5 (Hessiana Softplus e Condicionamento) — **CORRETO**

- $\nabla^2\Phi_{\text{soft}}=V^TW(x)V$, $w_c=\beta\,\varsigma(\beta g_c)(1-\varsigma(\beta g_c))$: verificado contra a Hessiana por autodiferenciação (erro $<10^{-10}$, `test_theorem5_hessian_factorization_and_bounds`); $\text{Tr}=\tfrac34\sum_c w_c$ confirmado; $\ker H=\ker V$ confirmado com $M<N$.
- Cotas de Rayleigh e $\kappa(H)\le\kappa(W)\kappa(V^TV)$: corretas.
- **Utilidade limitada:** perto de um vértice com $\beta=20$, $\kappa(W)\approx5{,}7\times10^{16}$ (calculado). A cota é correta e inútil nesse regime; o manuscrito deveria dizê-lo e restringir a $\beta$ moderado.
- **Ressalva de interpretação (tabela de síntese, ESTUDO l. 246 e TEX l. 311):** "mínimo único se $\text{rank}(V)=N$" é verdade, mas esse mínimo é um ponto **fracionário** (nunca um vértice: em vértices $\nabla\Phi_{\text{soft}}\ne0$ genericamente). Convexidade global significa que o "funil" leva a um único ponto cujo arredondamento não tem garantia alguma. O ganho experimental do Softplus **não decorre** deste teorema — decorre da penalidade de caixa não-convexa (§3.3).

### 2.6 Teorema 6 (Lipschitz e IEEE 754) — **CORRETO**

- Gershgorin em $V^TV$: diagonal $d_i/4$, soma fora da diagonal $\le d_i/2$, $\|V^TV\|_2\le 3d_{\max}/4$; $w_c\le\beta/4$; $L_\beta\le 3d_{\max}\beta/16$. Cota inferior $3\beta/16$ no hiperplano $g_c=0$ com $\|v_c\|^2=3/4$. Verificado ($N=12$: $0{,}94\le \sup\|H\|\approx5{,}8\le17{,}8$ para $\beta=5$).
- Decaimento em $\mathcal U_N(\rho)$: correto (a cota $L_2$ usa $\sum_i d_i^2\le 3M d_{\max}\le 3M^2$; poderia ser apertada com $d_{\max}$).
- Limiares IEEE 754 para $e^{-\beta/2}$: $2\cdot126\ln2=174{,}7$; $2\cdot149\ln2=206{,}6$; $2\cdot1022\ln2=1416{,}8$; $2\cdot1074\ln2=1488{,}9$. Corretos e confirmados em `float32` real (`test_theorem6_ieee754_underflow_thresholds`). Deve-se explicitar que a quantidade é $e^{\beta g_c(0)}=e^{-\beta/2}$ (fator do gradiente numa implementação estável de $\varsigma$); implementações ingênuas de $1/(1+e^{\beta/2})$ **estouram** (overflow) já em $\beta\approx177$, antes do underflow.
- Como observado em 2.2, o limiar *prático* de platô em FP32 é $\beta\approx30$–$40$ (update abaixo de 1 ulp), o que é mais relevante para o leitor do que $\beta=175$.

### 2.7 Teorema 7A (Família $F_N$) — **ENUNCIADO PLAUSÍVEL, PROVA INVÁLIDA**

Correto: $g_c=\tfrac12(x_i+x_j+x_k-1)$; todas as cláusulas ativas em $A_N$; $H_N=\gamma I+\eta\mathbf 1\mathbf 1^T$ com $\lambda_\perp=\tfrac14(N-2)(N-3)$, $\lambda_\parallel=\tfrac34(N-1)(N-2)$ (verificado por Hessiana numérica, erro $<10^{-10}$, $N=4,6,8$); $\nabla\Phi(\tfrac13\mathbf1)=0$.

**Erro:** escrevendo $H_N=aI+b\mathbf1\mathbf1^T$,
$$u_i(t)=e^{-at}\Big[u_i(0)-\big(1-e^{-bNt}\big)\,\bar u(0)\Big],\qquad \bar u=\tfrac1N\textstyle\sum_j u_j(0).$$
Para toda coordenada com $u_i(0)<\bar u(0)$ o colchete muda de sinal em $t^*=-\ln(1-u_i(0)/\bar u(0))/(bN)<\infty$: $x_i(t^*)=1/3$, a trajetória sai de $A_N$, as cláusulas contendo $i$ com soma $\le1$ desativam e a EDO deixa de ser linear. A afirmação "as trajetórias jamais escapam do ortante" (Resposta 11, l. 219) é falsa. Exemplo numérico ($N=6$, $x(0)=(0{,}34;0{,}95;\dots)$): em $t=0{,}5$ a EDO linear prevê $x_1=0{,}220$ e $x_1\to1/3$; o fluxo real tem $x_1=0{,}061$ e permanece aí. Em 200/200 trajetórias uniformes em $A_N$ o limite está a distância $>10^{-3}$ de $\tfrac13\mathbf1$.

**O que se salva:** em 200/200 ($N=6$), 30/30 ($N=4,6,8$) e 60/60 ($N=10$ e $N=12$) trajetórias o limite está em $Z$, nenhuma coordenada muda de sinal e o arredondamento viola cláusulas, sustentando $A_N\subseteq\mathcal B_{\text{spur}}$. Em todos os casos o fluxo abandona $A_N$ e o ponto-limite tem coordenadas dispersas (ex.: $N=12$, mínimo $0{,}214$ e máximo $0{,}338$), não $\tfrac13\mathbf 1$. Uma prova correta precisa de outro argumento; ingredientes verificáveis: (i) todas as coordenadas são não-crescentes em $A_N$; (ii) a ordem das coordenadas é preservada (para $x_i\ge x_j$, o conjunto de cláusulas ativas contendo $j$ injeta-se no de $i$, logo $\dot x_i\le\dot x_j$); (iii) falta mostrar que ao menos três coordenadas permanecem positivas. **Alternativa imediata e rigorosa:** o Teorema 1 já dá $\mathcal M_{\text{spur}}(\Phi_{\text{quad}})\ge(1/3)^N$ (euclidiano) para *qualquer* fórmula — cada ponto de $\mathcal U_N$ num ortante violador é um equilíbrio cujo arredondamento viola (`test_theorem1_plateau_points_are_spurious_equilibria`). Para $F_N$ os ortantes violadores são $2^N-1-N-\binom N2$, dando volume $\approx(2/3)^N$ sem nenhuma EDO. O valor do 7A estaria em exibir uma bacia *dinâmica* fora do platô; isso permanece a demonstrar.

**Inconsistências:** Resposta 11 enuncia "$N\ge3$" (l. 184) e depois exige $N\ge4$ (l. 214); o ESTUDO e o TEX dizem $N\ge4$. O DOCX enviado contém ambas.

### 2.8 Teorema 7B (Contração Centrípeta) — **IDENTIDADE CORRETA; CONCLUSÃO-MANCHETE TRIVIAL; ITEM 3 DA RESPOSTA 11 FALSO**

- Identidade $\langle-\nabla\Phi_{\text{quad}},x\rangle=-\sum_{\text{act}}(2g_c^2+g_c)$: correta (erro $<10^{-14}$ em 2 500 pontos). Extensão ao fluxo projetado (não escrita no manuscrito, mas verdadeira): $\langle x,\Pi_Tv\rangle=\langle x,v\rangle-\langle x,\Pi_{N}v\rangle\le\langle x,v\rangle$ pois $x_i\nu_i\ge0$.
- Inexistência de equilíbrios projetados com $\Phi>0$ (cone normal): correto. LaSalle $\Rightarrow$ trajetórias $\to Z$: correto; verificado por descida projetada (10/10 chegam a $\Phi<10^{-20}$).
- **"$\mathcal M_{\text{spur}}\equiv1$ para UNSAT":** verdadeiro por definição para **qualquer** $\Phi$ e $\mathcal D$, pois $E_{\text{disc}}\ge1$ em todos os vértices. Não é um teorema sobre o Hinge. O resumo do TEX ("proving that for all UNSAT the spurious basin mass is universally 100 %") deve ser reescrito.
- **Item 3 na Resposta 11 e no DOCX** ("separação $\ge1-0=1$") é **falso** (ver Achado 2; teste `test_theorem7b_unsat_spurious_mass_is_trivially_one_for_every_representation`). Deve ser retratado ao avaliador explicitamente.
- **Enunciado correto e útil do 7B:** "Para toda 3-CNF, $\Phi_{\text{quad}}$ não possui pontos críticos nem equilíbrios projetados em $\{\Phi_{\text{quad}}>0\}$; sob o fluxo projetado, toda trajetória converge para o politopo LP $Z=\{g_c\le0\ \forall c\}$, com $\|x\|_2^2$ estritamente decrescente enquanto $x\notin Z$." Isto sim é um resultado estrutural limpo — e mostra que o Hinge **não tem armadilhas locais**: sua deficiência é a **degenerescência do mínimo global**, não a rugosidade. Essa reinterpretação inverte parte da narrativa do manuscrito (o Hinge não é "vítreo"; é "cego").

### 2.9 Conjectura Central e o roadmap — **MAL FORMULADA; ROADMAP INADEQUADO**

- **Falsa como enunciada para $\alpha>\alpha_s\approx4{,}267$:** ali a fórmula é UNSAT c.q.c., ambas as massas valem 1 e a diferença é $0<c(\alpha)$. Deve-se restringir a $\alpha_d<\alpha<\alpha_s$ ou ao ensemble plantado (usado nos experimentos, mas não na conjectura).
- **Definições:** a conjectura só faz sentido com $\mathcal B_{\text{spur}}$ redefinida via $\omega$-limite $\subseteq\{x:E_{\text{disc}}(\text{sign}(x))>0\}$ (Achado 5) e com a distribuição inicial declarada (uniforme no cubo).
- **Por que a direção pode ser falsa:** pelo 7B, $\Phi_{\text{quad}}$ envia toda trajetória ao politopo LP $Z$; a fração de $Z$ que arredonda para solução, sob fluxo iniciado uniformemente, não é obviamente menor do que a fração de vértices-solução alcançados por $\Phi_{\text{mult}}$ (campo médio ingênuo, sabidamente ruim em 3-SAT acima de $\alpha_d$). Os dados da auditoria estrita (GD, $N=60$) dão $0/75$ para **ambas**, e a Fase I dá $4{,}0\%$ (quad) vs $9{,}3\%$ (mult) — IC de Wilson sobrepostos e amostras agrupadas por instância. Não há evidência empírica robusta para o sinal de $c(\alpha)$.
- **Roadmap:** (1) *McKean–Vlasov* descreve limites de partículas trocáveis em interação densa; 3-SAT aleatório é um hipergrafo **esparso** cujo limite é de convergência local fraca (Aldous–Steele; Bordenave–Caputo) e cuja dinâmica se trata por cavidade dinâmica/DMFT (Agoritsas–Biroli–Urbani–Zamponi 2018). (2) *Azuma–Hoeffding* pressupõe martingale; a aleatoriedade está na fórmula, não no tempo; a ferramenta natural é McDiarmid sobre cláusulas com controle de Gronwall — e a constante de Lipschitz cresce como $e^{L t}$, o que inviabiliza concentração para $t=\Theta(1)$ sem argumentos adicionais. (3) *Eyring–Kramers* aplica-se a Langevin com ruído; para GD determinístico a ferramenta é o teorema da variedade central-estável (Lee–Simchowitz–Jordan–Recht 2016; Panageas–Piliouras 2017): GD evita selas estritas q.t.p., o que aliás **favorece** $\Phi_{\text{mult}}$ (Teorema 3) e deveria estar no manuscrito.
- **Limiar citado:** $\alpha_d\approx3{,}86$ está correto para 3-SAT (Krzakala et al. 2007). No código (`exp_clg03_xorsat_and_ogp.py` l. 279) "$\alpha_d\sim0{,}918$" para 3-XORSAT está **errado**: $0{,}918$ é $\alpha_s$ (Dubois–Mandler 2002; Mézard–Ricci-Tersenghi–Zecchina 2003); o limiar de clustering é $\alpha_d\approx0{,}818$. Os experimentos em $\alpha=1{,}0>\alpha_s$ usam ensemble plantado acima do limiar de satisfatibilidade, o que deve ser dito.

### 2.10 Bibliografia (`clg_references.bib`) — erros verificáveis

| Chave | Problema | Correção |
| :--- | :--- | :--- |
| `okamoto1973distinctness` | Título errado. | "Distinctness of the eigenvalues of a quadratic form in a multivariate sample", *Ann. Statist.* 1(4):763–765, 1973 (o lema de medida nula é o Lema 1). |
| `caron2005zero` | Provavelmente não existe no *Amer. Math. Monthly* 112(8). | Caron & Traynor, "The zero set of a polynomial", nota técnica (Univ. Windsor, 2005). Verificar antes de manter. |
| `gamarnik2014limits` | Volume/ano trocados. | *Ann. Probab.* **45**(4):2353–2376, **2017** (versão de conferência: ITCS 2014). |
| `levin1973universal` | Páginas incorretas. | *Probl. Peredachi Inf.* 9(3):115–116 (1973); trad. *Probl. Inform. Transm.* 9(3):265–266. |
| `ebrahimi2024continuous` | Não localizei este artigo; parece fabricado. | Substituir por Ercsey-Ravasz & Toroczkai, *Nature Physics* 7:966–970 (2011) e Molnár, Molnár, Varga, Toroczkai, Ercsey-Ravasz, *Nature Commun.* 9:4864 (2018). |
| `cook1971complexity`, `khot2002power` | Tipo `@article` com *proceedings* no campo `journal`. | Usar `@inproceedings` + `booktitle`. |
| `carvalho2026clg` | Autocitação a "monograph series" inexistente. | Remover ou apontar para o repositório/DOI. |

Ausências graves para arXiv: Ercsey-Ravasz & Toroczkai 2011 (dinâmica contínua para SAT, "transient chaos"); Calinescu et al. 2011 (extensão multilinear); Mézard–Ricci-Tersenghi–Zecchina 2003 e Franz et al. 2001 (XORSAT/p-spin diluído); Folena–Franz–Zamponi 2020; Lee et al. 2016 (GD evita selas). Além disso, o TEX carrega `graphicx` mas **não contém nenhum `\includegraphics`**: as três figuras do `arxiv_package.zip` (2,1 MB) jamais aparecem no PDF. Não há LaTeX instalado nesta máquina (`pdflatex` ausente), logo o pacote **nunca foi compilado aqui**; a compilação deve ser verificada (Overleaf/TeX Live) antes da submissão.

---

## 3. Análise de Código e Verificação Numérica

### 3.1 O que `Fontes/clg_framework.py` realmente implementa

| Item do prompt / `README_FONTES.md` | Estado real |
| :--- | :--- |
| Três representações canônicas | **Só a multilinear** (`CNFInstance.potential`, l. 83–91). Hinge e Softplus vivem apenas em `exp_clg04_representation_invariance.py` e `exp_clg04_strict_audit.py`. |
| Gradientes analíticos | **Autograd** (`gradient`, l. 93–97); nenhum gradiente fechado. |
| Matriz de incidência $V$ e $\nabla^2=V^TWV$ | **Não implementados.** Hessiana por `torch.autograd.functional.hessian` (densa, $O(N)$ passes reversos). |
| Fluxo gradiente projetado em $[-1,1]^N$ | **Não implementado.** Há `torch.clamp` após passos de Langevin/Adam (projeção do *iterado*, não do campo). |
| Volume de bacia por Monte Carlo com controle de erro | **Não implementado.** Só `wilson_score_interval` sobre alcançabilidade (Bernoulli) nos scripts CLG-04. |
| "Hessiana analítica e decomposição espectral" (README_FONTES l. 25) | Autograd + `np.linalg.eigvalsh`. Descrição enganosa. |

A documentação deve ser alinhada ao código, ou o código elevado à documentação (recomendação na §6).

### 3.2 Correção numérica (verificada nesta auditoria)

| Verificação | Resultado |
| :--- | :--- |
| $\nabla\Phi_{\text{mult}}$ analítico vs diferenças finitas ($N=12$, 20 pontos) | erro máx. $1{,}4\times10^{-9}$ |
| $\nabla\Phi_{\text{soft}}$ vs DF | $1{,}1\times10^{-9}$ |
| $\nabla\Phi_{\text{quad}}$ vs DF (longe de $g_c=0$) | $2{,}9\times10^{-10}$ |
| $V^TWV$ vs Hessiana DF / autograd | $1{,}2\times10^{-7}$ / $6{,}7\times10^{-16}$ |
| `CNFInstance.potential/gradient/compute_hessian` vs referência | $<10^{-4}$ (float32) |
| Tr $\nabla^2\Phi_{\text{mult}}$ | $6\times10^{-15}$ |

Os gradientes e Hessianas usados nos experimentos estão **corretos** (critério $<10^{-6}$ atendido, exceto a tolerância natural $O(h)$ do Hinge sobre um vínculo ativo, onde $\Phi_{\text{quad}}$ é apenas $\mathcal C^1$).

### 3.3 Bugs, imprecisões e problemas metodológicos encontrados

1. **`clg_framework.py` l. 128–137 (`compute_third_order_tensor_norm`):** ramos para índices repetidos usam contribuição $-\tfrac18\prod\sigma$; para uma cláusula $(i,i,i)$ a derivada terceira real de $((1-\sigma x_i)/2)^3$ é $-\tfrac34\sigma^3$. Código morto sob (H1), mas `exp_clg03` gera cláusulas `([i,i,i],[1,1,1])` (l. 195), que violam (H1) e a harmonicidade (Teorema 3 não vale para essas instâncias Horn).
2. **`clg_framework.py` l. 177–182:** "Morse index" e "condition number" em pontos **aleatórios** (não críticos). O índice de Morse só existe em pontos críticos; com traço nulo a fração de autovalores negativos é $\approx1/2$ sempre. $\kappa=|\lambda|_{\max}/(|\lambda|_{\min}+10^{-6})$ é ruído numérico (Hessiana harmônica tem autovalor $\approx0$ frequente). Descritores sem significado; convém removê-los ou renomeá-los ("inércia da Hessiana").
3. **Sementes:** `exp_clg03_xorsat_and_ogp.py` l. 223 e `exp_clg04_representation_invariance.py` l. 169 usam `torch.empty(n).uniform_` sem `torch.manual_seed` → **os resultados publicados da Fase I (inclusive o 69,3 %) não são reproduzíveis bit a bit.** `exp_clg04_strict_audit.py` corrige (pool de $x_0$ com `default_rng`, `manual_seed` por trajetória). `clg_framework.py` usa `random.seed`/`torch.manual_seed` **globais** (efeito colateral); preferir `torch.Generator`.
4. **Penalidade de caixa:** `box_penalty = 0.2*sum((x**2-1)**2)` em todas as trajetórias (CLG-03 l. 230; CLG-04 l. 183; auditoria l. 173). Efeitos: (a) o "Softplus" experimental não é convexo (Teorema 5 inaplicável); (b) o platô do Teorema 1 deixa de ser plano (gradiente da penalidade $0{,}8x(x^2-1)\ne0$); (c) todas as representações ganham $2^N$ atratores de vértice. **Nenhum teorema descreve o sistema experimentado.** É o principal descolamento teoria–experimento.
5. **Otimizador:** Adam (Fase I) vs GD (auditoria) mudam o resultado de 69,3 % para 0,0 % no mesmo ensemble ($N=60$, Softplus). O manuscrito (`CLG_FOUNDATIONS.md` §7.2) reporta só a Fase I como "Theoretical Breakthrough". Isso é *cherry-picking* involuntário; a Tabela deve mostrar ambas, com a interpretação "o efeito de representação **depende** da dinâmica", que aliás é a tese CLG-R.
6. **Inicialização em $[-0,5;0,5]^N$** (CLG-03/04): a "massa de bacia" $\mu$ do manuscrito é sobre o cubo inteiro; a estimativa experimental é sobre outra medida. Declarar ou mudar para uniforme em $[-1,1]^N$.
7. **Intervalos de Wilson sobre 75 trajetórias agrupadas em 5 instâncias:** as tentativas não são i.i.d. (efeito de instância); os ICs são anticonservadores. Usar *bootstrap* por instância ou IC por instância (a Fase II já reporta `per_instance_dh` — bom sinal).
8. **`exp_clg04_representation_invariance.py` l. 195:** `cont_val = energy.item()` é a energia em $x_{T-1}$, não em $x_T$ (após o último `step` e `clamp`). Inconsistência leve entre `mean_cont_energy` e o estado final.
9. **`exp_clg04_strict_audit.py` l. 187–193:** *early stopping* quando o arredondamento intermediário resolve. A métrica passa a ser "tempo de acerto do arredondamento ao longo da trajetória", não $\omega$-limite. Deve ser declarado (é uma métrica válida, diferente).
10. **`generate_random_3xorsat` docstring (l. 330):** "dense 3-spin Sherrington-Kirkpatrick" — é um p-spin **diluído** (Franz et al. 2001), não SK denso. `exp_clg03` l. 279: $\alpha_d$ errado (ver 2.9).
11. **`README_FONTES.md` l. 27:** "provando que a alcançabilidade … separam P de NP sob grau constante" — afirmação já refutada pelo próprio CLG-03. Overclaim residual a expurgar.
12. **Reprodutibilidade de ambiente:** não há `requirements.txt`/`pyproject`, nem `tests/` (até esta auditoria). Torch 2.11 CPU, NumPy 2.4, Python 3.13 no `venv`.

### 3.4 Aceleração

- **Hessiana Softplus/Hinge:** usar a forma fechada $V^TWV$ (esparsa; $V$ tem $3M$ não-nulos) em vez de `autograd.functional.hessian` ($O(N)$ *backward passes*): para $N=1000$, $M=4260$, cai de segundos para milissegundos (`scipy.sparse` ou `torch.sparse`).
- **Multilinear:** gradiente fechado $\partial_i\Phi=\sum_{c\ni i}(-\sigma_i/2)\prod_{j\in c\setminus i}(1-\sigma_jx_j)/2$ vetoriza com `torch.prod` sobre máscaras (já vetorizado no `potential`; falta o gradiente/Hessiana). Hessiana: $H_{ij}=\sum_{c\ni i,j}\tfrac{\sigma_i\sigma_j}{4}\cdot\tfrac{1-\sigma_kx_k}{2}$ — construção esparsa $O(M)$.
- **Trajetórias:** os 75 *restarts* × 3 representações × 2 dinâmicas são independentes → `torch.vmap`/batching em uma dimensão de lote (`x` de forma `[R, N]`) elimina o laço Python; ganho ~50× em CPU.
- **`discrete_evaluation`/`discrete_energy`:** laços Python por cláusula; vetorizar com `np.all(S*s<0, axis=1)` (usado nos testes desta auditoria).
- **`generate_huge_sparse_graph` (`fase3_op3`, l. 31–37):** deduplicação por `set` em Python é o gargalo real para $N=10^4$; usar `np.unique` sobre pares ordenados.
- **`walksat_solver` (`fase3_op1`, l. 73–80):** recomputa `count_satisfied_clauses` para cada *flip* candidato ($O(M)$ por avaliação); manter contadores incrementais de literais verdadeiros por cláusula ($O(\text{grau})$).
- Numba/PyTorch compilado só compensam depois das vetorizações acima.

### 3.5 Suíte de testes entregue (`tests/test_clg_theorems.py`)

26 testes, ~60 s em CPU, **26/26 aprovados** após ajuste da busca de Newton. Cobertura: DF de gradientes/Hessianas; integração com `clg_framework.CNFInstance`; T1 (platô, justeza de $1/3$, cota de medida, equilíbrios espúrios no platô); T2 (pontos aleatórios não críticos, contraexemplo (H3'), Parseval); T3 (Laplaciano, sela interior); T4 (falha de (H4) em 3-SAT aleatório e em $F_N$; versão 4A′ sem (H4)); T5 (fatoração, cotas, núcleo); T6 (sanduíche de Lipschitz, decaimento em $\mathcal U_N(\rho)$, limiares IEEE); T7B (identidade centrípeta, convergência a $Z$, trivialidade em UNSAT); T7A (Hessiana e autovalores; **teste que documenta a lacuna**: o fluxo abandona $A_N$ e não converge a $\tfrac13\mathbf1$, mas termina espúrio).

Execução: `venv\Scripts\python.exe -m pytest tests -q` (o `pytest` foi instalado no `venv` durante a auditoria).

---

## 4. Tabela de Confronto com a Literatura Clássica e de Vidros de Spin

| Referência | O que estabelece | Relação com o CLG-R | Situação no manuscrito |
| :--- | :--- | :--- | :--- |
| **Goemans & Williamson 1994** (LP para MAX-SAT); folclore LP | $y=\mathbf 1/2$ é viável com folga $1/2$ em toda relaxação LP de $k$-SAT. | É exatamente o Teorema 1. | Não citado; apresentado como novo. |
| **Calinescu–Chekuri–Pál–Vondrák 2011**; O'Donnell 2014 | Extensão multilinear é afim por coordenada; extremos em vértices; *pipage rounding*. | Teoremas 3/4A são casos particulares (com o refinamento harmônico para mínimos locais). | Não citado. |
| **Campo médio ingênuo / TAP (Thouless–Anderson–Palmer 1977)** | Energia de produto $\mathbb E_{\prod\text{Bern}(m)}[E]$; TAP adiciona reação de Onsager. | $\Phi_{\text{mult}}(m)$ **é** a energia de campo médio ingênuo; GD em $\Phi_{\text{mult}}$ = dinâmica de campo médio ingênuo a $T=0$. | Não identificado. É a ponte natural com a física. |
| **Franz & Parisi 1995/1997** | Potencial restrito a *overlap* fixo com uma referência; metaestabilidade. | Um potencial de FP para $\Phi_{\text{mult}}$ no cubo, com *overlap* $q=\tfrac1N\sum s_i^* x_i$, daria a versão termodinâmica da "distância de Hamming" reportada em CLG-04. | Só nominalmente em `CLG_FOUNDATIONS.md` §4.2. |
| **Mézard–Parisi–Zecchina 2002; Krzakala et al. 2007** | $\alpha_d\approx3{,}86$, $\alpha_s\approx4{,}267$; clustering/condensação; SP. | Fixam os regimes da Conjectura. | Citados; conjectura mal restringida a $\alpha<\alpha_s$. |
| **Franz–Mézard–Ricci-Tersenghi–Weigt–Zecchina 2001; Mézard–Ricci-Tersenghi–Zecchina 2003; Ricci-Tersenghi 2010** | XORSAT = p-spin diluído; $\alpha_d\approx0{,}818$, $\alpha_s\approx0{,}918$; "vítreo sem ser difícil". | O experimento CLG-03 **replica** este resultado conhecido. | Só Ricci-Tersenghi 2010 citado; $\alpha_d$ errado no código. |
| **Ercsey-Ravasz & Toroczkai 2011; Molnár et al. 2018** | Dinâmica contínua determinística para SAT com variáveis auxiliares; caos transiente; escalonamento do tempo de solução. | Trabalho **mais próximo** de "representação contínua × dinâmica"; usa outra representação (produtos $K_m$) e mostra alcance total com escala exponencial no tempo. | **Ausente.** Omissão grave para arXiv. |
| **Folena–Franz–Zamponi 2020** (PRX) | Em p-spin misto, GD não fica no *threshold* estático; dinâmica e paisagem estática desacoplam. | Mina a narrativa "Kac-Rice ⇒ preso com prob. $1-o(1)$" de `CLG_FOUNDATIONS.md` §4.2. | Não citado. |
| **Ros–Ben Arous–Biroli–Cammarota 2019** (PRX); Ros–Biroli–Cammarota 2019 | Complexidade de mínimos e de barreiras via Kac-Rice; geometria de selas. | Ferramentas para contar críticos de $\Phi_{\text{mult}}$ em ensembles aleatórios (Etapa 3 do roadmap, corretamente formulada). | Não citado. (A referência "Behrens, Cammarota & Ros 2021" do prompt não foi por mim localizada com segurança; sugiro confirmar antes de citá-la.) |
| **Gamarnik & Sudan 2014/2017; Gamarnik 2021** (OGP) | Propriedade do **conjunto de soluções** (independe de representação) que obstrui algoritmos locais/estáveis. | CLG-R é sobre a **paisagem de uma representação**; OGP é sobre a instância. A distinção é real e é a contribuição conceitual mais defensável ("efeito causal da representação"). | Citado; distinção só esboçada. |
| **Lee–Simchowitz–Jordan–Recht 2016; Panageas–Piliouras 2017** | GD evita selas estritas q.t.p. (variedade central-estável). | Combinado com o Teorema 3, dá: GD em $\Phi_{\text{mult}}$ converge q.t.p. a mínimos no bordo — a versão dinâmica *correta* do 4B, sem (H4). | Ausente; substituiria Eyring–Kramers no roadmap. |
| **Nagurney & Zhang 1996; Brogliato et al. 2006** | Sistemas dinâmicos projetados: existência, unicidade, Lyapunov. | Necessários para 4B e 7B (campo descontínuo no bordo). | Ausentes. |
| **Agoritsas–Biroli–Urbani–Zamponi 2018** (DMFT) | Teoria dinâmica de campo médio para GD/Langevin em modelos aleatórios. | Ferramenta correta para a Etapa 1 do roadmap (em vez de McKean–Vlasov). | Ausente. |

**Veredito sobre o "efeito causal da representação":** a formulação (mesma instância $F$, mesma dinâmica $\mathcal D$, mesma $x_0$, três $\Phi$) é um desenho experimental **legítimo e bem controlado** (auditoria estrita), e a distinção conceitual em relação à OGP é correta. Não é, porém, inédita: é a pergunta de Ercsey-Ravasz & Toroczkai (2011) e da literatura de *penalty/continuation methods*. A contribuição metodológica genuína seria o protocolo pareado com IC e ensembles plantados/filtrados, desde que as métricas sejam reportadas com honestidade sobre a dependência da dinâmica (Fase I vs auditoria).

---

## 5. Código de Testes Automatizados

Arquivo entregue: **`tests/test_clg_theorems.py`** (ver §3.5). Auto-contido (NumPy + PyTorch), importa `Fontes/clg_framework.py` para o teste de integração. Dois testes estão marcados no *docstring* como "DOCUMENTA LACUNA" (`test_h4_fails_on_random_3sat_and_on_F_N`, `test_theorem7a_conclusion_holds_but_linear_regime_does_not_persist`): eles **passam** porque asseveram o comportamento real, que contradiz a prova escrita; devem ser revisitados quando o manuscrito for corrigido.

Script auxiliar de verificação usado na auditoria (não versionado): `verify_clg.py` no diretório de rascunho da sessão; sua saída íntegra está resumida nas Seções 2 e 3.

---

## 6. Recomendações Práticas e Roadmap

### 6.1 Correções obrigatórias antes de qualquer envio

1. **Retratar ao avaliador** o item 3 do Teorema 7B da Resposta 11 (MD e DOCX) e a afirmação "trajetórias jamais escapam do ortante" do 7A. Reemitir `RespostaAoProfessor_Analise11.*` via `generate_resposta11_deliverables.py` (l. 610 e vizinhas) com a errata.
2. **Teorema 7A:** (a) rebaixar a "Proposição 7A" com prova numérica e enunciado condicional, ou (b) substituir pelo argumento do platô (Teorema 1 ⇒ $\mathcal M_{\text{spur}}\ge(1/3)^N$ para toda fórmula; $\approx(2/3)^N$ para $F_N$), ou (c) provar de fato que $\ge3$ coordenadas permanecem positivas (ordem preservada + comparação). Unificar "$N\ge4$".
3. **Teorema 4A/4B:** eliminar (H4); adotar 4A′ e a prova de 4B sem (H4) (§2.4). Adicionar referências de sistemas projetados.
4. **Teorema 7B:** reescrever enunciado e resumo do arXiv: "ausência de equilíbrios fora do politopo LP + contração centrípeta"; remover "100 % para UNSAT" como resultado.
5. **Definições dos quatro níveis:** $\mathcal B_{\text{spur}}(\Phi,\mathcal D)=\{x_0:\omega(x_0)\subseteq\{x:E_{\text{disc}}(\text{sign}(x))>0\}\}$; $\mathcal S_{\text{spur}}$ como conjunto de equilíbrios Lyapunov-estáveis (não assintoticamente); declarar $\mu$ = uniforme em $[-1,1]^N$.
6. **Conjectura Central:** restringir a $\alpha\in(\alpha_d,\alpha_s)$ ou ensemble plantado; substituir o roadmap por: (1) convergência local fraca + DMFT/cavidade dinâmica; (2) McDiarmid sobre cláusulas com controle de Gronwall (explicitar a limitação em $t$); (3) variedade central-estável para GD e Kac-Rice (Ros et al.) para contagem de selas de $\Phi_{\text{mult}}$.
7. **Bibliografia:** corrigir as sete entradas da tabela §2.10; incluir as ausências; inserir `\includegraphics` ou retirar as figuras do zip; **compilar o `.tex`** (não há LaTeX nesta máquina) e anexar o PDF ao repositório.
8. **Teorema 1:** unificar a medida; retirar §3.2 (deriva média) do ESTUDO, como prometido na Resposta 11; declarar que $Z$ é o politopo LP e que os pontos de $\mathcal U_N$ são mínimos **globais** da relaxação.
9. **Manuscrito × experimentos:** ou (i) reexecutar CLG-04 **sem** penalidade de caixa, com fluxo projetado explícito (Euler projetado), inicialização uniforme em $[-1,1]^N$, sementes e IC por instância, reportando GD e Adam lado a lado; ou (ii) declarar no manuscrito que os teoremas descrevem $\Phi$ puro e os experimentos $\Phi+0{,}2\sum(x^2-1)^2$ sob Adam, sem inferir um do outro.
10. **Overclaim residual:** `README_FONTES.md` l. 27; considerar renomear o repositório/arquivos "p-vs-np" para "clg-r".

### 6.2 Engenharia (curto prazo)

- Elevar `clg_framework.py` ao que a documentação promete: classe `Relaxation` com `phi/grad/hess` fechados para `quad|mult|soft`, matriz $V$ esparsa, `projected_flow(x0, dt, T)` (Euler projetado ou Moreau), `basin_mass_mc(seed, K)` com IC de Wilson **e** *bootstrap* por instância, `torch.Generator` explícito.
- `requirements.txt` fixando `numpy==2.4.4 torch==2.11.0 pytest==9.1.1`; CI que rode `pytest tests`.
- Vetorizar `discrete_energy` e as trajetórias em lote (§3.4).

### 6.3 Programa científico (médio prazo) — o que de fato poderia render publicação

1. **Curvas de escala** $R_{\text{dyn}}(N)$ para $N\in\{50,\dots,800\}$ nos três ensembles prometidos em `CLG_FOUNDATIONS.md` §7.1 (SAT-filtrado por CaDiCaL, plantado, controlado), sem penalidade, GD projetado e Langevin, com ICs por instância. Sem isso não há evidência de um limite $N\to\infty$.
2. **Identificar $\Phi_{\text{mult}}$ com campo médio ingênuo** e comparar com TAP/BP a $T=0$: é a única via para conectar o 4B a resultados quantitativos de física (limiar de campo médio ingênuo em 3-SAT é conhecido ser muito abaixo de $\alpha_d$).
3. **Provar a Conjectura numa família tratável** (por exemplo, XORSAT plantado, onde $\Phi_{\text{mult}}$ tem simetria de *gauge* e o politopo LP é explícito) antes de atacar 3-SAT aleatório.
4. **Comparar com Ercsey-Ravasz–Toroczkai** na mesma instância: a quarta representação (com variáveis auxiliares) alcança 100 % com tempo exponencial; isso reposiciona a tese ("representação muda alcançabilidade" vira "representação troca prob. de sucesso por tempo de escape").

### 6.4 Sobre o firewall P vs NP

O núcleo (3-XOR-SAT ∈ P com $R_{\text{dyn}}=0$) é correto como demonstração de que dureza geométrica contínua não implica NP-dureza, e a retratação em `CLG_FOUNDATIONS.md` §8 é adequada. Três ressalvas: (i) é uma **replicação** de Ricci-Tersenghi 2010 e Franz et al. 2001 e deve ser apresentada como tal; (ii) o $0{,}0\%$ com IC $[0;4{,}9\%]$ em 75 trajetórias de $N\le60$ não autoriza "colapso total" ou "prova" — apenas "não observado"; (iii) a direção recíproca (NP-dureza ⇒ dureza geométrica) não foi testada e não deve ser sugerida. Nada no material atual constitui alegação sobre $P$ vs $NP$; o risco reputacional está apenas na **nomenclatura** (repositório, README, apresentação).

---

*Fim do relatório. Todos os números citados foram gerados nesta sessão com precisão dupla, sementes fixas (`default_rng(0)`, `default_rng(20260911)`) e estão reproduzíveis via `tests/test_clg_theorems.py`.*


---

## 7. Instruções de Pesquisa para o Gemini (trabalho pesado sob revisão externa)

Orientações iniciais: 
Leia também `tests/test_clg_theorems.py` e as Seções 1 a 6 deste relatório. 
O Gemini fará derivações, código e experimentos; o revisor externo (que pode ser um outro agente do gemini, por enquanto) reexecutará o código, rederivará as recursões e emitirá o parecer final. 
Toda discrepância entre o que o Gemini afirmar e o que o revisor reproduzir será penalizada.

### INÍCIO DO PROMPT

Você é uma equipe de pesquisa em matemática (análise, probabilidade em grafos aleatórios, física estatística de CSPs) encarregada de executar um programa de pesquisa rigoroso. O seu relatório será auditado por um revisor externo hostil que **reexecutará todo o código, rederivará todas as recursões e verificará cada citação**. Afirmações sem prova ou sem verificação numérica serão tratadas como erro. Escreva em português, com matemática em LaTeX. Prefira sempre um enunciado mais fraco e provado a um mais forte e não provado.

#### 1. Objetos matemáticos (use exatamente esta notação)

- Hipercubo $\mathcal X=[-1,1]^N$. Fórmula 3-CNF $F$ com $M$ cláusulas; cada cláusula $c$ tem vetor de polaridades $\sigma^{(c)}\in\{-1,0,+1\}^N$ com exatamente três entradas não nulas (variáveis distintas).
- Função de violação afim $g_c(x)=-\tfrac12\big(1+\sigma^{(c)}\!\cdot x\big)$. Num vértice $s\in\{-1,1\}^N$: $g_c(s)=1$ se a cláusula é violada, $g_c(s)\le 0$ caso contrário.
- Três relaxações: $\Phi_{\text{quad}}(x)=\sum_c\max(0,g_c(x))^2$; $\Phi_{\text{mult}}(x)=\sum_c\prod_{j\in c}\tfrac{1-\sigma^{(c)}_jx_j}{2}$; $\Phi_{\text{soft}}(x)=\sum_c\tfrac1\beta\ln(1+e^{\beta g_c(x)})$ com $\beta=5$.
- Dinâmica: **fluxo gradiente projetado** $\dot x=\Pi_{T_{\mathcal X}(x)}(-\nabla\Phi(x))$, discretizado por Euler projetado $x\leftarrow\text{clip}(x-\eta\nabla\Phi(x),-1,1)$ com $\eta$ pequeno. **Sem penalidade de caixa, sem Adam, sem ruído.** Inicialização $x_0$ uniforme em $[-1,1]^N$.
- Energia discreta $E_{\text{disc}}(s)$ = número de cláusulas violadas por $s$. Arredondamento $\text{sign}(x)$ (com $\text{sign}(0)=+1$).
- Ensemble $\mathcal E(N,\alpha)$: $M=\lfloor\alpha N\rfloor$ cláusulas, cada uma com três variáveis distintas uniformes e polaridades uniformes independentes.
- **Densidade de energia residual:** $\rho_\Phi(\alpha,T)=\lim_{N\to\infty}\mathbb E\big[E_{\text{disc}}(\text{sign}\,x(T))/M\big]$ e $\rho_\Phi(\alpha)=\lim_{T\to\infty}\rho_\Phi(\alpha,T)$, quando existirem.

#### 2. Fatos já estabelecidos (use, não reprove; não os contradiga)

1. **Platô do Hinge (Teorema 1):** em $\mathcal U_N=(-1/3,1/3)^N$, $\Phi_{\text{quad}}\equiv0$ e $\nabla\Phi_{\text{quad}}\equiv0$. O conjunto $Z=\{x:g_c(x)\le0\ \forall c\}$ é o politopo da relaxação LP e é o conjunto dos mínimos globais de $\Phi_{\text{quad}}$.
2. **Harmonicidade (Teorema 3):** $\Delta\Phi_{\text{mult}}\equiv0$; nenhum mínimo local interior se $\Phi_{\text{mult}}\not\equiv$ const.
3. **Teorema 4A-linha (sem hipótese H4):** todo mínimo local de $\Phi_{\text{mult}}|_{\mathcal X}$ no interior relativo de uma face tem valor igual a $E_{\text{disc}}$ de todo vértice dessa face.
4. **Corolário 4B (sem H4):** todo equilíbrio isolado assintoticamente estável do fluxo projetado de $\Phi_{\text{mult}}$ é um vértice.
5. **Teorema 5:** $\nabla^2\Phi_{\text{soft}}=V^TW(x)V\succeq0$, $V$ com linhas $-\sigma^{(c)}/2$, $w_c=\beta\varsigma(\beta g_c)(1-\varsigma(\beta g_c))$.
6. **Teorema 6:** $\tfrac3{16}\beta\le\sup_x\|\nabla^2\Phi_{\text{soft}}\|_2\le\tfrac{3d_{\max}}{16}\beta$.
7. **Teorema 7B (forma correta):** $\langle-\nabla\Phi_{\text{quad}}(x),x\rangle=-\sum_{c:\,g_c>0}(2g_c^2+g_c)<0$ sempre que há cláusula ativa; não existem equilíbrios (interiores ou projetados) com $\Phi_{\text{quad}}>0$; toda trajetória converge para $Z$ e $\|x(t)\|^2$ decresce estritamente fora de $Z$.
8. **Identificações exatas:** $\Phi_{\text{mult}}(x)=\mathbb E_{s\sim\prod_i\text{Bern}((1+x_i)/2)}[E_{\text{disc}}(s)]$ (energia de campo médio ingênuo). Para 3-XORSAT, $\Phi_{\text{mult}}=\tfrac12\sum_e(1-J_ex_ix_jx_k)$ (p-spin diluído).
9. **Fatos negativos a respeitar:** (a) a hipótese "H4" ($b_i(s_{-i})\ne0$ em todas as arestas) é falsa para instâncias típicas e não deve ser usada; (b) a "prova" de que o fluxo de $\Phi_{\text{quad}}$ na família $F_N$ (todas as cláusulas negativas) permanece em $A_N=(1/3,1)^N$ é falsa: o fluxo sai de $A_N$; (c) para fórmulas UNSAT, $E_{\text{disc}}(\text{sign}\,x)\ge1$ para todo $x$, logo qualquer "massa espúria" vale 1 para qualquer representação; (d) acima de $\alpha_s\approx4{,}267$ o ensemble é UNSAT c.q.c.
10. Limiares de 3-SAT aleatório: $\alpha_d\approx3{,}86$ (clustering), $\alpha_s\approx4{,}267$. Componente gigante do hipergrafo 3-uniforme: $\alpha=1/6$.

#### 3. Conjectura a investigar (enunciado corrigido)

> **Conjectura (separação de energia residual).** Para $\alpha$ em $(\alpha_d,\alpha_s)$, sob fluxo gradiente projetado com $x_0$ uniforme, os limites $\rho_{\text{quad}}(\alpha)$ e $\rho_{\text{mult}}(\alpha)$ existem e $\rho_{\text{quad}}(\alpha)>\rho_{\text{mult}}(\alpha)>0$.

Evidência preliminar ($N=60$, GD, $\alpha=4{,}26$ plantado): $20{,}4/256$ cláusulas violadas para o Hinge contra $4{,}5/256$ para a multilinear.

#### 4. Programa de trabalho (execute na ordem; não pule etapas)

**Etapa 1 - Localidade em tempo finito (lema com prova completa).**
Prove: para $T$ fixo e $\Phi\in\{\Phi_{\text{quad}},\Phi_{\text{mult}},\Phi_{\text{soft}}\}$, existe $R=R(T,\alpha,\varepsilon)$ tal que $x_i(T)$ depende da bola de raio $R$ em torno de $i$ no grafo de fatores a menos de erro $\varepsilon$, uniformemente em $N$, com alta probabilidade. Use Gronwall com a constante de Lipschitz do campo e a cota de grau máximo $O(\log N/\log\log N)$ do hipergrafo aleatório. Trate a projeção no bordo explicitamente (o campo é descontínuo no bordo: use a formulação de Moreau/sweeping process ou a versão discreta de Euler projetado e prove o resultado para a versão discreta com $\eta\to0$).

**Etapa 2 - Recursão na árvore de Galton-Watson (o núcleo).**
O grafo de fatores local de $\mathcal E(N,\alpha)$ converge à árvore: variável raiz com $\text{Poisson}(3\alpha)$ cláusulas, cada cláusula com duas variáveis novas, polaridades uniformes, recursivamente. Para cada $\Phi$:
(a) escreva a EDO do fluxo restrita à árvore de profundidade $R$ (variáveis nas folhas com evolução truncada, justifique a truncagem pelo lema da Etapa 1);
(b) derive o operador $\mathcal R_\Phi$ que mapeia a distribuição da trajetória $t\mapsto x_v(t)$ de uma variável filha na distribuição da trajetória da variável pai (uma "population dynamics" sobre trajetórias, não sobre escalares);
(c) implemente $\mathcal R_\Phi$ em Python/NumPy puro (sem PyTorch), com discretização temporal explícita, população $\ge10^4$ trajetórias, sementes fixas, e compute $\rho_\Phi(\alpha,T)$ como a probabilidade de a cláusula raiz estar violada por $\text{sign}(x(T))$;
(d) tabule $\rho_\Phi(\alpha,T)$ para $\alpha\in\{1,2,3,3{,}5,3{,}86,4{,}0,4{,}2,4{,}26,4{,}5,5\}$, $T\in\{1,2,5,10,20,50,100\}$, $R\in\{2,4,6,8\}$, e as três representações; mostre a convergência em $R$ e em tamanho de população com barras de erro.

**Etapa 3 - Validação por simulação direta.**
Implemente o Euler projetado em NumPy para $N\in\{200,1000,5000\}$, $\ge20$ instâncias por ponto, $x_0$ uniforme, $\eta=10^{-2}$, e compare $E_{\text{disc}}(\text{sign}\,x(T))/M$ com a recursão da Etapa 2, com intervalo de confiança **por instância** (não agrupe trajetórias de instâncias diferentes como se fossem i.i.d.). Reporte o escalonamento em $N$ e a discrepância recursão/simulação em cada ponto. Se discordarem além do erro estatístico, a recursão está errada: corrija-a antes de prosseguir.

**Etapa 4 - Limite $T\to\infty$.**
Para o Hinge: use o Teorema 7B para provar que $\text{dist}(x(t),Z)\to0$ com taxa explícita (a energia $\Phi_{\text{quad}}$ é Lyapunov e é quadrática por partes), e conclua que $\rho_{\text{quad}}(\alpha,T)$ converge em $T$; tente provar que os limites em $T$ e em $N$ comutam. Para a multilinear: prove ou refute que $\rho_{\text{mult}}(\alpha,T)$ é monótona em $T$; se não conseguir provar a comutação dos limites, declare o resultado como "teorema em tempo finito" e a comutação como lema condicional, enunciado com precisão.

**Etapa 5 - A desigualdade.**
Com as tabelas da Etapa 2, verifique numericamente $\rho_{\text{quad}}(\alpha,T)>\rho_{\text{mult}}(\alpha,T)$ em toda a faixa; reporte também $\Phi_{\text{soft}}$. Em seguida tente uma prova analítica em pelo menos um regime: (i) $\alpha\to0$ por expansão em $\alpha$ da recursão (ordem 1 e 2); (ii) $T$ pequeno por expansão em $T$; (iii) acoplamento das duas trajetórias no mesmo $x_0$ e mesma árvore. Se algum regime fechar, enuncie o teorema correspondente com prova completa.

**Etapa 6 - Corolários e resultados de apoio (após as Etapas 1 a 5).**
(A) Volume do politopo LP: $\mu_{\text{norm}}(Z)=e^{-Nf(\alpha)+o(N)}$; calcule $f$ por primeiro momento e verifique numericamente para $N\le20$ por Monte Carlo exato.
(B) Separação em famílias Horn monótonas via teoria de sistemas cooperativos (Hirsch): enuncie e prove.
(C) Para $\alpha<1/6$ (componentes árvore de tamanho $O(\log N)$): prove que $\rho_{\text{mult}}(\alpha)=0$ mostrando que fórmulas-árvore não têm vértices que sejam mínimos locais com $E_{\text{disc}}>0$ (indução das folhas), combinado com 4A-linha e com o teorema de que fluxos gradiente evitam selas estritas (Lee, Simchowitz, Jordan, Recht 2016), adaptado ao fluxo projetado.
(D) Família $F_N$: prove que, a partir de $A_N=(1/3,1)^N$, ao menos três coordenadas permanecem positivas ao longo do fluxo de $\Phi_{\text{quad}}$ (ingredientes verificados numericamente: todas as coordenadas são não-crescentes; a ordem entre coordenadas é preservada; nenhuma coordenada muda de sinal em $N\le12$).

**Etapa 7 - Bateria experimental completa (protocolo pré-registrado).**
Antes de rodar, escreva o protocolo (parâmetros, sementes, métricas, critérios de sucesso) em um arquivo `PROTOCOLO.md` e não o altere depois; qualquer desvio deve ser registrado em `DESVIOS.md`.
(a) *Ensembles:* (i) $\mathcal E_{\text{SAT}}$: 3-SAT aleatório em $\alpha\in\{3{,}0;3{,}5;3{,}86;4{,}0;4{,}2\}$ filtrado por um solver completo (use `pysat` com CaDiCaL ou Glucose; registre a versão), descartando instâncias UNSAT; (ii) $\mathcal E_{\text{plant}}$: plantado nos mesmos $\alpha$; (iii) $\mathcal E_{\text{XOR}}$: 3-XORSAT plantado em $\alpha\in\{0{,}5;0{,}7;0{,}818;0{,}9\}$; (iv) $\mathcal E_{\text{Horn}}$: Horn monótono acíclico com fatos iniciais.
(b) *Escalas:* $N\in\{50,100,200,400,800,1600,3200\}$; $\ge30$ instâncias por ponto; $\ge10$ inicializações uniformes por instância.
(c) *Representações:* $\Phi_{\text{quad}}$, $\Phi_{\text{mult}}$, $\Phi_{\text{soft}}$ ($\beta\in\{2,5,20\}$) e, como quarta representação, a dinâmica de Ercsey-Ravasz e Toroczkai (2011) com variáveis auxiliares, implementada a partir das equações do artigo original (verifique a existência do artigo: *Nature Physics* 7, 966–970).
(d) *Dinâmicas:* Euler projetado com $\eta\in\{10^{-2},10^{-3}\}$ até $T=100$ ou até $\|\Pi_T(-\nabla\Phi)\|<10^{-8}$; Langevin projetado com $T_{\text{temp}}\in\{10^{-3},10^{-2}\}$. Sem penalidade de caixa. Sem Adam.
(e) *Métricas por trajetória:* $E_{\text{disc}}(\text{sign}\,x(T))$, $E_{\text{disc}}/M$, tempo de entrada em $Z$ (Hinge), distância de Hamming normalizada à solução plantada quando existir, $\|x(T)\|_2/\sqrt N$, fração de coordenadas em $\{\pm1\}$.
(f) *Estatística:* média e intervalo de confiança **por instância** (bootstrap sobre instâncias, 2000 reamostragens); nunca agrupe trajetórias de instâncias distintas como i.i.d. Reporte curvas $\rho_\Phi(N)$ e extrapole $N\to\infty$ por ajuste em $1/N$ e $1/\sqrt N$, mostrando os dois.
(g) *Critério de sucesso pré-registrado:* a conjectura recebe apoio se, para todo $\alpha\in(\alpha_d,\alpha_s)$ testado, o intervalo de confiança de $\rho_{\text{quad}}-\rho_{\text{mult}}$ excluir zero em $N\ge800$ e a extrapolação concordar com a recursão da Etapa 2 dentro de duas barras de erro.

**Etapa 8 - Rascunho do manuscrito integrado.**
Produza `CLG_R_V4.tex` (artigo, `amsart` ou `article` com `amsthm`) contendo: as identificações exatas (item 8 da Seção 2); os Teoremas 1, 2, 3, 4A-linha, 4B sem H4, 5, 6 e 7B na forma correta; os resultados novos das Etapas 1 a 6 com o status exato de cada um (teorema, teorema em tempo finito, proposição condicional, conjectura); a seção experimental da Etapa 7; a Conjectura na forma corrigida. Regras: nenhum resultado com status inferior a "PROVADO" pode ser chamado de teorema; o resumo só pode listar o que está provado; cada referência com dados completos e verificada; inclua `\includegraphics` para cada figura que citar; forneça também o `.bib` e o comando de compilação. Não escreva agradecimentos, cartas ao avaliador ou texto promocional.

#### 4-bis. Protocolo obrigatório de teste e autovalidação (antes de entregar)

Execute e reporte cada item abaixo; o revisor repetirá todos.

1. **Gradientes e Hessianas:** para cada $\Phi$, compare o gradiente analítico com diferenças finitas centrais ($h=10^{-6}$, precisão dupla) em 50 pontos aleatórios de $N=12$; erro máximo aceitável $10^{-6}$ (para o Hinge, exclua pontos a menos de $10^{-4}$ de um hiperplano $g_c=0$). Verifique $\text{Tr}\,\nabla^2\Phi_{\text{mult}}=0$ e $\nabla^2\Phi_{\text{soft}}=V^TWV$ com erro $<10^{-10}$.
2. **Identidade centrípeta:** verifique $\langle-\nabla\Phi_{\text{quad}},x\rangle=-\sum_{\text{act}}(2g_c^2+g_c)$ em 1000 pontos, erro $<10^{-12}$.
3. **Recursão versus simulação:** para cada $(\alpha,T)$ da Etapa 2, a diferença entre $\rho_\Phi(\alpha,T)$ da recursão e a média da simulação direta em $N=5000$ deve ficar dentro de duas barras de erro; caso contrário, declare a recursão como não validada naquele ponto.
4. **Convergência interna:** mostre que $\rho_\Phi(\alpha,T)$ muda menos de $10^{-3}$ ao dobrar a população, ao aumentar $R$ em 2 e ao reduzir o passo temporal pela metade.
5. **Casos-limite com resposta conhecida:** (i) $\alpha\to0$: $\rho_\Phi\to0$ para as três representações; (ii) fórmula UNSAT explícita (as 8 cláusulas completas sobre 3 variáveis): $E_{\text{disc}}\ge1$ sempre; (iii) família $F_N$ com $N=6$: o fluxo do Hinge a partir de $A_N$ termina em $Z$ com arredondamento violador em 100 % das trajetórias e sai de $A_N$ em 100 % delas; (iv) Horn monótono: $\rho_{\text{mult}}=0$ em todas as instâncias.
6. **Reprodutibilidade:** cada tabela deve ser regenerável por um único comando declarado; rode-o duas vezes e confirme igualdade bit a bit.
7. **Provas:** para cada lema, liste as hipóteses usadas e verifique que nenhuma delas é o item 9 da Seção 2. Para cada desigualdade com constante, cheque numericamente a constante em um exemplo pequeno.
8. **Referências:** para cada citação, informe título, autores, veículo, volume, páginas, ano e a marca "verificada" (você confirmou os dados) ou "não verificada". Referências não verificadas não podem sustentar nenhum passo de prova.
9. **Checklist final:** entregue uma lista com os nove itens acima marcados como "passou", "falhou" ou "não executado", com a razão.

#### 5. Formato obrigatório do relatório final

1. **Tabela de afirmações**, uma linha por resultado, com status em {PROVADO, PROVADO CONDICIONALMENTE A [lema X], CONJECTURA COM EVIDÊNCIA NUMÉRICA, FALHOU} e, para cada um, a localização da prova ou a descrição exata do obstáculo.
2. **Provas completas**, sem "é fácil ver" e sem "por argumento padrão"; toda desigualdade com a constante explícita.
3. **Código** Python/NumPy executável, um arquivo por etapa, sementes fixas, tempo de execução declarado, e o comando exato para reproduzir cada tabela.
4. **Tabelas numéricas** com barras de erro e número de amostras.
5. **Lista de todas as hipóteses** usadas, incluindo as implícitas (por exemplo, comutação de limites).
6. **Referências** apenas às que você efetivamente usou, com dados bibliográficos completos e a marca "verificada" ou "não verificada" para cada uma. Não invente referências. Se não tiver certeza de que um artigo existe, diga.
7. **Seção "Pontos para o revisor"**: os três resultados de que você menos tem certeza e por quê.

#### 6. Regras

- Separe sempre heurística (física) de prova (matemática); rotule cada parágrafo.
- Quando travar, descreva o obstáculo com precisão (qual desigualdade não fecha, qual constante explode) em vez de contornar com prosa.
- Não use as hipóteses ou provas listadas como falsas na Seção 2, item 9.
- Reporte falhas com o mesmo destaque dos sucessos. Um "FALHOU" honesto vale mais do que um "PROVADO" que o revisor derrubará.

### FIM DO PROMPT
