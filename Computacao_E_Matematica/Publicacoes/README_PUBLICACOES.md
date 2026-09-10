# Acervo de Publicações Científicas e Apresentações Executivas

**Pesquisa:** Neuro-Meta-Heurística de Carvalho (Otimização Combinatória em Grafos e Problema P vs NP)  
**Autor:** Thiago Carvalho  
**Ano:** 2026  
**Localização:** `C:\MathDoCarvalho\P_NP\Publicacoes`  

> [!IMPORTANT]
> ### 🛡️ AVISO DE PROPRIEDADE INTELECTUAL E DIREITOS AUTORAIS
> **Copyright © 2026 Thiago Carvalho. Todos os direitos reservados.**
> 
> Todos os artigos científicos, teoremas, demonstrações e apresentações contidos neste acervo são de **autoria e titularidade intelectual exclusiva de Thiago Carvalho**.
> É estritamente vedada a reprodução total ou parcial, tradução, republicação, inclusão em bases de dados sem autorização ou utilização em pipelines de treinamento de IA sem autorização formal expressa.
> Termos completos de licença: [LICENSE](../../LICENSE).

Este diretório reúne todos os artigos científicos publicáveis, monografias temáticas, slide decks para bancas avaliadoras e conferências, além dos ativos gráficos em alta resolução gerados durante a pesquisa.

---

## 1. Artigos em Modelo Publicável para Periódicos Internacionais (2026)

Os quatro artigos abaixo foram redigidos e estruturados especificamente para submissão aos periódicos internacionais de maior fator de impacto em suas respectivas áreas:

1. 📐 **Paper I - Matemática Pura e Otimização Discreta:**
   - **Arquivo:** [PAPER_I_MATHEMATICS_MAXCUT_LAPLACIAN_UGC.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/PAPER_I_MATHEMATICS_MAXCUT_LAPLACIAN_UGC.md)
   - **Título:** *Continuous Laplacian Relaxations and the Scale-Free Hub Effect: An Analytical Framework for Graph Bipartitioning and the Asymptotic Goemans-Williamson Gap*
   - **Periódico Alvo:** *SIAM Journal on Discrete Mathematics (SIDMA)* / *Discrete Applied Mathematics*
   - **Contribuições:** Relaxação laplaciana analítica no hipercubo contínuo, prova do Teorema do Efeito Hub em redes com lei de potência (Barabási-Albert), análise espectral hessiana e posicionamento frente ao teto assintótico da Unique Games Conjecture (UGC) / Goemans-Williamson ($\alpha_{\text{GW}} \approx 0.87856$).

2. 💻 **Paper II - Ciência da Computação, Redes Complexas & Escala Extrema:**
   - **Arquivo:** [PAPER_II_COMPUTER_SCIENCE_EXTREME_SCALE_SPARSE_GNN.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/PAPER_II_COMPUTER_SCIENCE_EXTREME_SCALE_SPARSE_GNN.md)
   - **Título:** *Linear-Time Graph Partitioning via Sparse Neural Differential Operators: Extreme-Scale Max-Cut Convergence on Arbitrary Topologies*
   - **Periódico Alvo:** *IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)* / *ACM Transactions on Computer Systems (TOCS)*
   - **Contribuições:** Complexidade estritamente linear $\mathcal{O}(|E|)$ via indexação esparsa atômica (`index_add_`). Prova do Princípio da Parcimônia Espectral (quebra do teto histórico de $80\%$ de corte com $80.01\%$). Benchmarks em grafos gigantes de $N=10.000$ nós e $40.000$ arestas ($10^{3010}$ combinações): convergência em $0.79\text{s}$ em CPU com apenas $1.26\text{ MB RAM}$ ($50.288\text{ arestas/s}$).

3. 📊 **Paper III - Estatística Aplicada, MCMC & Física Estatística:**
   - **Arquivo:** [PAPER_III_APPLIED_STATISTICS_TSP_ANNEALING.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/PAPER_III_APPLIED_STATISTICS_TSP_ANNEALING.md)
   - **Título:** *Non-Equilibrium Annealing and Neural Adaptive Gibbs-Boltzmann Dynamics: A Statistical Mechanics Approach to the Euclidean Traveling Salesperson Problem*
   - **Periódico Alvo:** *Journal of Machine Learning Research (JMLR)* / *Journal of the Royal Statistical Society: Series B (Methodological)*
   - **Contribuições:** Termodinâmica fora do equilíbrio aplicada ao Caixeiro Viajante Euclidiano (TSP). Identificação empírica da transição vítrea (*spin-glass fracturing*) entre $N=30$ e $N=100$. A rede `TSPMetaGNN` alcançou $80.0\%$ de vitórias contra o recozimento simulado tradicional, reduzindo o comprimento de rota em $50.38\%$ em relação a permutações aleatórias.

4. 🧠 **Paper IV - Lógica Computacional & Inteligência Artificial Simbólica:**
   - **Arquivo:** [PAPER_IV_COMPUTATIONAL_LOGIC_COOK_LEVIN_MAX3SAT.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/PAPER_IV_COMPUTATIONAL_LOGIC_COOK_LEVIN_MAX3SAT.md)
   - **Título:** *Continuous Differentiable Relaxation of the Cook-Levin Satisfiability Core: Meta-Governed Neural Message Passing across the Critical Phase Transition ($m/n \approx 4.267$)*
   - **Periódico Alvo:** *Journal of the ACM (JACM)* / *Artificial Intelligence (AIJ)*
   - **Contribuições:** Formulação contínua e diferenciável do núcleo da NP-completude (redução de Cook-Levin). A `SATMetaGNN` em grafo bipartido de fatores alcançou **$99.25\%$ de satisfação de cláusulas** no ponto crítico de transição de fase ($m/n \approx 4.267$), superando com folga o limite de inaproximabilidade de Håstad ($87.5\%$).

---

## 2. Apresentação Executiva em Marp (PDF & HTML)

- 📕 **Slide Deck em Alta Definição (PDF, 818 KB, 300 DPI):** [apresentacao_p_vs_np_carvalho.pdf](file:///C:/MathDoCarvalho/P_NP/Publicacoes/apresentacao_p_vs_np_carvalho.pdf)
- 🌐 **Slide Deck Standalone Interativo (HTML):** [apresentacao_p_vs_np_carvalho.html](file:///C:/MathDoCarvalho/P_NP/Publicacoes/apresentacao_p_vs_np_carvalho.html)
- 📝 **Código-Fonte em Markdown Marp:** [apresentacao_p_vs_np_carvalho.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/apresentacao_p_vs_np_carvalho.md)

---

## 3. Monografias Temáticas Anteriores (Em Português)

- 📄 **Artigo 3 (Fronteiras Finais):** [ARTIGO_CIENTIFICO_FRONTEIRAS_SAT_PARCIMONIA_ESCALA10K_2026.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/ARTIGO_CIENTIFICO_FRONTEIRAS_SAT_PARCIMONIA_ESCALA10K_2026.md)
- 📄 **Artigo 2 (Avanços Teóricos):** [ARTIGO_CIENTIFICO_AVANCOS_ESCALABILIDADE_UGC_TSP_2026.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/ARTIGO_CIENTIFICO_AVANCOS_ESCALABILIDADE_UGC_TSP_2026.md)
- 📄 **Artigo 1 (Fundamentos e Descobertas):** [ARTIGO_CIENTIFICO_DESCOBERTAS_NEURO_META_HEURISTICA_2026.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/ARTIGO_CIENTIFICO_DESCOBERTAS_NEURO_META_HEURISTICA_2026.md)

---

## 4. Catálogo de Figuras Científicas (300 DPI & SVG Vetorial)

- `fig1_cross_topology_hub_effect.png` / `.svg`: Evidência empírica do Efeito Hub em redes sem escala.
- `fig2_tradeoff_qualidade_latencia.png` / `.svg`: Fronteira de Pareto comparando qualidade de partição e tempo de convergência.
- `fig3_benchmarks_multiescala.png` / `.svg`: Comparativo multiescala ($N=30$ a $N=10.000$).
- `fig4_convergencia_meta_governador.png` / `.svg`: Curvas de estabilização da IA Gerente de Hiperparâmetros.
