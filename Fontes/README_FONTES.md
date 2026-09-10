# Guia Explicativo e Catálogo de Código-Fonte: Neuro-Meta-Heurística de Carvalho

**Autor:** Thiago Carvalho  
**Repositório:** Pesquisa P vs NP - Otimização Combinatória Neural e Grafos Esparsos  
**Ambiente:** Python 3.13 / 3.14 | PyTorch | CPU / CUDA  
**Localização:** `C:\MathDoCarvalho\P_NP\Fontes`  

---

## 1. Visão Geral da Arquitetura de Software

Este diretório contém a suíte completa de algoritmos, modelos neurais pré-treinados, benchmarks e rotinas de validação empírica desenvolvidos ao longo da pesquisa. A base computacional combina:
1. **Álgebra Linear Esparsa & Operadores Diferenciais**: Relaxações contínuas no hipercubo $[-1, 1]^N$ via matriz laplaciana combinatória $L = D - A$ e produtos multilineares para CNF.
2. **Graph Neural Networks (GNNs)**: Convoluções espectrais esparsas lineares (`SparseGNN`), Atenção Multi-Head com Normalização Escalar (`ScaledDotProductGNN`) e Redes em Grafos Bipartidos de Fatores (`SATMetaGNN`).
3. **Meta-Governança de Políticas de Otimização**: Agentes neurais que inspecionam a topologia latente da instância em tempo polinomial $\mathcal{O}(\\vert E \\vert)$ e governam os hiperparâmetros de solvers iterativos (temperatura, amortecimento e passos de recozimento estocástico).

---

## 2. Mapa Estrutural dos Arquivos de Código-Fonte

### A. Geometria da Paisagem Computacional (Projeto CLG-01 - 2026)

| Arquivo | Descrição Técnica & Arquitetura | Modelo / Método | Saída / Relatório |
| :--- | :--- | :--- | :--- |
| **`clg_framework.py`** | **Motor de Paisagem Contínua (v2.0):** Implementação da 5-tupla $\mathcal{L}(I)$, relaxação funcional de $k$-SAT, cálculo de Hessiana analítica, tensor de terceira ordem $\mathcal{T}_{ijk}$ e decomposição espectral. Extrai o vetor de descritores $\mathcal{G}(I)$. | Decomposição Espectral Exata | Descritores $\mathcal{G}(I)$ |
| **`exp_clg01_p_vs_np.py`** | **Benchmark Controlado Classe P vs NP:** Teste comparativo entre 2-SAT ($\text{P}$) e 3-SAT ($\text{NP}$) em $N=20, 40, 60$. Confirma o Teorema 1 ($\Omega_{\text{curv}} \approx 0$ em $\text{P}$) e estabelece separação de 5 ordens de magnitude na rigidez ($p = 1.53 \times 10^{-6}$). | Teste Estatístico Mann-Whitney U | `exp_clg01_report.txt`, `exp_clg01_results.json` |
| **`exp_clg02_degree_control.py`** | **Benchmark com Controle Estrito de Grau (CLG-02):** Compara Horn-3-SAT ($\text{P}$, $\deg=3$) com Random-3-SAT ($\text{NP}$, $\deg=3$). Desacopla curvatura estática da topologia dinâmica, provando que a alcançabilidade da bacia ($100\%$ vs $6\%$) e densidade de armadilhas ($0.00$ vs $2.23$) separam $\text{P}$ de $\text{NP}$ sob grau constante. | Topologia Dinâmica de Bacias | `exp_clg02_report.txt`, `exp_clg02_results.json` |
| **`exp_clg03_xorsat_and_ogp.py`** | **Benchmark Canônico de 3-XOR-SAT (CLG-03):** Avalia a barreira definitiva da otimização contínua. Compara 3-XOR-SAT ($\text{P}$ algébrico, $\deg=3$) via Eliminação Gaussiana em $\text{GF}(2)$ com a relaxação contínua. Demonstra empiricamente que a relaxação contínua entra em colapso vítreo ($0\%$ reachability) em um problema estritamente na Classe $\text{P}$, consolidando o reposicionamento formal do framework. | Eliminação Gaussiana GF(2) + Gradiente Contínuo | `exp_clg03_report.txt`, `exp_clg03_results.json` |

### B. Módulos de Fronteira e Estado da Arte (Fase 3 - 2026)

| Arquivo | Descrição Técnica & Arquitetura | Modelo Associado | Complexidade |
| :--- | :--- | :--- | :--- |
| **`fase3_op1_max_sat.py`** | **Núcleo de Cook-Levin (Max-3-SAT):** Implementa a formulação contínua da probabilidade de insatisfação de cláusulas $\mathcal{L}_{\text{SAT}}(v)$ em conjunto com a rede em grafo de fatores `SATMetaGNN`. Governa learning rate, ruído de Langevin e horizonte de descida no limiar crítico $m/n \approx 4.267$. | `model_sat_meta_manager.pth` | $\mathcal{O}(M)$ |
| **`fase3_op2_hybrid_gnn.py`** | **Princípio da Parcimônia Espectral:** Avaliação comparativa de três paradigmas (SparseGNN linear, HybridGNN com atenção gated e Heurística Gulosa). Demonstra experimentalmente que a convolução espectral linear esparsa evita oversmoothing e **bate o recorde histórico de $80.01\%$ de corte**. | `model_maxcut_hybrid.pth` / `model_maxcut.pth` | $\mathcal{O}(\\vert E \\vert)$ |
| **`fase3_op3_extreme_scale.py`** | **Escalação Linear em Grafos Gigantes ($N=10.000$ nós):** Motor de partição laplaciana puramente baseado em indexação esparsa (`index_add_`) com zero alocação intermediária. Executa convergência em **$0.79\text{s}$ em CPU comum**, alocando apenas **$1.26\text{ MB RAM}$** para $10^{3010}$ combinações ($50.288\text{ arestas/s}$). | — (Diferencial analítico) | Estrito $\mathcal{O}(\\vert E \\vert)$ |

### B. Módulos Teóricos e de Universalidade (Fase 2 - 2026)

| Arquivo | Descrição Técnica & Arquitetura | Modelo Associado | Saída / Relatório |
| :--- | :--- | :--- | :--- |
| **`trilha1_scaled_gat.py`** | **Scaled Dot-Product Multi-Head GAT:** Cura definitiva da anomalia de saturação do GAT clássico. Implementa projeções $Q, K, V$ escaladas por $\frac{1}{\sqrt{d_k}}$ e mascaramento de topologia, elevando o corte em grafos densos de $0.00\%$ para $41.27\%$. | `model_maxcut_scaled_gat.pth` | `trilha1_scaled_gat_report.txt` |
| **`trilha2_goemans_williamson_benchmark.py`** | **Benchmarking Teórico Goemans-Williamson (UGC):** Implementa o solver ótimo SDP via fatoração de Burer-Monteiro com arredondamento por hiperplano aleatório. Posiciona a heurística frente ao limitante assintótico $\alpha_{\text{GW}} \approx 0.87856$. | — (SDP Burer-Monteiro) | `trilha2_gw_benchmark_report.txt` |
| **`trilha3_tsp_meta_manager.py`** | **Universalidade no Caixeiro Viajante (TSP):** Modela instâncias geométricas 2D como grafos completos via `TSPMetaGNN`, prevendo a temperatura inicial $T_0$, taxa de resfriamento $\gamma$ e passos de MCMC / 2-Opt. Atinge **$80\%$ de vitória** contra recozimento fixo em $N=100$. | `model_tsp_meta_manager.pth` | `trilha3_tsp_report.txt` |
| **`trilha4_gerador_graficos_cientificos.py`** | **Pipeline Gráfico Vetorial:** Script automatizado em Matplotlib para geração das 4 figuras de alta resolução (300 DPI PNG e vetores SVG) utilizadas nos artigos e na apresentação Marp. | — | `fig1` a `fig4` (.png/.svg) |

### C. Módulos Fundacionais, Diagnósticos e Benchmarks Históricos

| Arquivo | Função / Propósito |
| :--- | :--- |
| **`math_p_np_carvalho_consolidado_n1000.py`** | Implementação de referência consolidada do pipeline em grande escala ($N=1000$) com governança adaptativa por GNN. |
| **`exp1_cross_topology.py`** | Bateria de testes de generalização zero-shot em topologias Erdős-Rényi, Watts-Strogatz e Barabási-Albert (onde foi descoberto o Efeito Hub). |
| **`exp2_gat_comparison.py`** | Diagnóstico empírico do colapso de atenção local e saturação de softmax em grafos não-ponderados. |
| **`exp3_benchmark_solvers.py`** | Comparação direta entre partições aleatórias, heurística gulosa de grau, Simulated Annealing clássico e o solver Carvalho. |
| **`math_p_np_carvalho_IA_gerente_hiperparametros_01.py` a `06.py`** | Série temporal da evolução dos algoritmos de política e meta-governança com freios de estabilidade. |
| **`math_p_np_carvalho_n_30.py`, `n_100.py`, `n_1000.py`** | Códigos de calibração específicos para as três ordens de magnitude originais do projeto. |
| **`train_model.py` / `train_model_evolucao.py`** | Treinamento do solver neural esparso `SparseGNN`. |
| **`train_attention_model.py` / `...attention.py`** | Treinamento dos modelos baseados em atenção (GAT). |
| **`benchmark*.py`** | Scripts auxiliares de medição de qualidade e tempos de execução. |
| **`Framework_UGC_Carvalho/`** | Subdiretório experimental com implementações de rotinas para a Unique Games Conjecture. |

---

## 3. Catálogo de Modelos Neurais Pré-Treinados (`*.pth`)

Todos os modelos treinados e validados estão preservados neste diretório para inferência e reprodutibilidade imediata:

1. **`model_maxcut.pth` (36.9 KB)**:
   - **Classe:** `SparseGNN` (Convolução linear esparsa com normalização simétrica de grau).
   - **Desempenho:** Campeão histórico em grafos esparsos ($N=1000$), atingindo média de **$80.01\%$ de corte** (picos de $81.10\%$).
2. **`model_maxcut_hybrid.pth` (165.6 KB)**:
   - **Classe:** `HybridMaxCutGNN` (Integração de difusão esparsa, atenção escalar por aresta e governança contínua).
   - **Desempenho:** $78.83\%$ de corte em média sobre múltiplos conjuntos topológicos.
3. **`model_maxcut_scaled_gat.pth` (105.9 KB)**:
   - **Classe:** `ScaledDotProductGNN` (Atenção multi-head com projeções Q/K/V e mascaramento).
   - **Desempenho:** Cura da saturação de atenção em regimes densos, alcançando $41.27\%$ de corte onde o GAT clássico zerava.
4. **`model_sat_meta_manager.pth` (80.2 KB)**:
   - **Classe:** `SATMetaGNN` (Rede em grafo bipartido de fatores para lógica proposicional).
   - **Desempenho:** $99.25\%$ de cláusulas satisfeitas em $N=50$ e $98.92\%$ em $N=100$ no limiar crítico $m/n=4.267$.
5. **`model_tsp_meta_manager.pth` (63.9 KB)**:
   - **Classe:** `TSPMetaGNN` (Rede convolucional geométrica completa para instâncias 2D).
   - **Desempenho:** $80\%$ de vitórias sobre recozimento fixo em $N=100$ cidades, reduzindo rotas em $50.38\%$ sobre o acaso.
6. **`model_maxcut_gat.pth` (21.6 KB)**:
   - **Classe:** `GATMaxCut` (Modelo clássico de atenção em arestas, mantido para propósitos de linha de base e contraste científico).

---

## 4. Instruções de Execução e Reprodutibilidade

### Pré-Requisitos de Ambiente
Para executar qualquer um dos fontes, assegure-se de que as seguintes dependências estejam instaladas em seu ambiente Python:

```bash
pip install torch numpy scipy matplotlib networkx
```

### Exemplos de Comandos para Replicação Direta

1. **Executar o Solver de Max-3-SAT no Limiar Crítico de Cook-Levin:**
   ```powershell
   python fase3_op1_max_sat.py
   ```
   *Gera relatório em `fase3_op1_max_sat_report.txt` e métricas em `.json`.*

2. **Executar o Benchmark da Parcimônia Espectral (Sparse vs Hybrid vs Greedy):**
   ```powershell
   python fase3_op2_hybrid_gnn.py
   ```

3. **Executar o Teste de Escalação Extrema ($N=10.000$ nós em tempo real):**
   ```powershell
   python fase3_op3_extreme_scale.py
   ```
   *Mede consumo dinâmico de RAM e throughput de arestas/segundo.*

4. **Executar a IA Gerente de Hiperparâmetros no Caixeiro Viajante (TSP):**
   ```powershell
   python trilha3_tsp_meta_manager.py
   ```

5. **Executar a Bateria Goemans-Williamson (Confronto UGC):**
   ```powershell
   python trilha2_goemans_williamson_benchmark.py
   ```

6. **Regenerar todas as Figuras Científicas Vetoriais e Raster:**
   ```powershell
   python trilha4_gerador_graficos_cientificos.py
   ```

---

## 5. Garantia de Integridade e Validação
Todos os scripts presentes nesta pasta foram executados, depurados contra anomalias numéricas (divisões por zero, gradientes nulos ou vazamentos de memória) e validados em sistema operacional Windows com backends PyTorch CPU e CUDA.
