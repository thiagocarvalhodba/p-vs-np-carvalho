# Memória do Projeto: Pesquisa P vs NP - Neuro-Meta-Heurística de Carvalho (Max-Cut)

**Autor:** Thiago Carvalho  
**Ano/Data:** 2026  
**Ambiente de Execução:** Python 3.13 / 3.14 | PyTorch | CPU/CUDA  
**Diretório Raiz Oficial:** `C:\MathDoCarvalho\P_NP`  

---

## 📌 Diretriz de Desenvolvimento e Governança
> **Regra Mandatória:** Qualquer arquivo gerado, teste, script de treinamento, modelo serializado (`.pth`), logs de benchmark ou documentação relativa a este projeto **deve** ser criado, executado e mantido exclusivamente dentro deste diretório (`C:\MathDoCarvalho\P_NP`) e seus subdiretórios.

---

## 1. Visão Geral e Fundamentação Científica

O projeto investiga a fronteira entre problemas tratáveis (**P**) e problemas intratáveis (**NP-Difícil**), com ênfase na abordagem de **Neural Combinatorial Optimization (NCO)** aplicada ao problema clássico do **Max-Cut** em grafos densos e esparsos com escalas progressivas ($N=30$, $N=100$, $N=1000$).

### Tese Central
Um algoritmo estocástico por si só é cego à topologia global e sofre de estagnação em mínimos locais ou instabilidade caótica. Uma **Graph Neural Network (GNN)**, computada estritamente em **tempo polinomial ($P$)**, pode operar como um **Meta-Manager (IA Gerente de Hiperparâmetros)**, inspecionando a topologia latente do grafo e parametrizando dinamicamente o solver contínuo-relaxado (definindo número de iterações, ruído estocástico de recozimento e taxa de aprendizado ideal).

---

## 2. Formulação Matemática

### A. Max-Cut via Matriz Laplaciana Combinatória
Dado um grafo não direcionado $G = (V, E)$ com matriz de adjacência simétrica $A \in \{0, 1\}^{N \times N}$ e matriz diagonal de graus $D$:
- **Laplaciana:** $L = D - A$
- **Formulação Contínua do Corte:**
  $$f(s) = \frac{1}{4} s^T L s$$
- **Relaxação Contínua:** $s = \tanh(x) \in (-1, 1)^N$, onde $x \in \mathbb{R}^N$ é o vetor de potenciais de partição otimizado via gradiente.
- **Função de Perda da Descida de Gradiente:**
  $$\mathcal{L}_{\text{cut}} = -f(s) = -\frac{1}{4} s^T L s$$
- **Discretização Final:**
  $$s_{\text{bin}} = \text{sign}(\tanh(x)) \in \{-1, +1\}^N$$
- **Valor Discreto do Corte:**
  $$\text{Cut}(s_{\text{bin}}) = \frac{1}{2} \sum_{i < j} A_{ij} \cdot \mathbb{I}(s_{\text{bin}, i} \neq s_{\text{bin}, j})$$

### B. Arquitetura da GNN Meta-Manager (`MetaGNN`)
- **Node Embedding:** Mapeia atributos iniciais do nó para dimensão oculta $d=64$:
  $$h_i^{(0)} = W_{\text{init}} \mathbf{1} + b_{\text{init}}$$
- **Message Passing Vetorizado (4 camadas):**
  $$h_i^{(l+1)} = h_i^{(l)} + \frac{1}{N} \sum_{j=1}^N \text{MLP}\left([h_i^{(l)}, h_j^{(l)}, A_{ij}]\right)$$
- **Readout / Strategy Head (3 saídas sigmoides):**
  $$\pi(A) = \sigma\left(W_2 \cdot \text{ReLU}(W_1 \bar{h} + b_1) + b_2\right) \in (0, 1)^3$$
  1. $p_{\text{steps}} \rightarrow \text{steps} = \text{int}(100 + 250 \cdot p_{\text{steps}})$
  2. $p_{\text{noise}} \rightarrow \eta = 0.01 + 0.03 \cdot p_{\text{noise}}$
  3. $p_{\text{lr}} \rightarrow \alpha = 0.01 + 0.04 \cdot p_{\text{lr}}$

### C. Função de Recompensa e Policy Gradient
- **Ganho Diferencial sobre a Heurística Base:**
  $$\text{Gain} = \text{Cut}_{\text{IA}} - \text{Cut}_{\text{Base}}$$
  $$\text{Reward} = \frac{\text{Gain}}{N}$$
- **Função de Perda Meta-Heurística com Penalidade de Complexidade:**
  $$\mathcal{L}_{\text{meta}} = -\text{Reward} \cdot \sum_{k=1}^3 \log(\pi_k + \epsilon) + \lambda \|\pi\|_2^2$$
  onde $\lambda = 0.05$ desencoraja o modelo a inflar parâmetros sem retorno justificável de corte.

---

## 3. Linha do Tempo e Evolução dos Experimentos

| Fase | Escala ($N$) | Espaço de Busca | Desafios & Soluções | Resultado Chave |
| :--- | :--- | :--- | :--- | :--- |
| **Fase 1** | $N=30$ | $\approx 10^9$ | Erro de Autograd (`element 0 does not require grad`). Resolvido com `with torch.enable_grad()` e álgebra linear explícita. | Loss convergiu para $0.0001$; Ganhos de $+10.0$. |
| **Fase 2** | $N=100$ | $\approx 1.26 \times 10^{30}$ | Volatilidade em topologias caóticas com quedas de $-30.0$. Aumento da capacidade oculta da GNN para $d=64$. | Ganhos adaptativos de até $+36.0$. |
| **Fase 3.1** | $N=1000$ | $\approx 10^{301}$ | Regras fixas de decisão apresentavam oscilações de $-228.0$ a $+392.0$. | Necessidade de governança contínua. |
| **Fase 3.2** | $N=1000$ | $\approx 10^{301}$ | IA livre iniciou com perdas agudas ($-740.0$), aprendendo com o tempo e fechando em $+170.0$. | Convergência adaptativa confirmada. |
| **Fase 3.3** | $N=1000$ | $\approx 10^{301}$ | **Meta-Estabilidade & Governador:** Freio no teto de learning rate e ruído estocástico. | **Pico recorde de $+489.0$** (Época 55). Média móvel final de **$+34.3$**. |

---

## 4. Mapa dos Arquivos Locais no Workspace

O repositório está estruturado em duas pastas principais para organização e publicação no Git:

| Diretório / Arquivo | Função / Descrição |
| :--- | :--- |
| **`Publicacoes/`** | Acervo de artigos para periódicos internacionais, monografias, slides Marp e figuras em 300 DPI. |
| `Publicacoes/README_PUBLICACOES.md` | Catálogo explicativo e índice do acervo de publicações. |
| `Publicacoes/PAPER_I_*.md` a `IV_*.md` | 4 artigos científicos para periódicos internacionais (SIAM, IEEE, JMLR, JACM). |
| `Publicacoes/apresentacao_p_vs_np_carvalho.*` | Slide deck em PDF (818 KB, 300 DPI), HTML interativo e Markdown. |
| **`Fontes/`** | Códigos-fonte validados, modelos treinados (`.pth`), suítes de benchmark e logs. |
| `Fontes/README_FONTES.md` | Guia detalhado de cada script, execução, parâmetros e reprodutibilidade. |
| `Fontes/fase3_op1_max_sat.py` | SATMetaGNN no limiar crítico de Cook-Levin ($m/n=4.267$). |
| `Fontes/fase3_op2_hybrid_gnn.py` | Prova empírica da Parcimônia Espectral (SparseGNN quebrando 80%). |
| `Fontes/fase3_op3_extreme_scale.py` | Solver $\mathcal{O}(\\vert E \\vert)$ para grafos gigantes de $N=10.000$ nós em sub-segundo ($1.26\text{ MB RAM}$). |
| `Fontes/trilha1_*.py` a `trilha4_*.py` | Scaled GAT, Goemans-Williamson UGC, TSP MCMC e gerador de gráficos. |
| `Fontes/model_*.pth` | Pesos treinados de todos os modelos neurais. |
| `Fontes/Framework_UGC_Carvalho/` | Framework de testes para jogos únicos. |
| `PROJECT_MEMORY.md` | Este documento de memória persistente e especificações técnicas. |
| `README.md` | Portal de navegação do repositório no Git. |
| `.gitignore` | Higienização de caches, venv e temporários para versionamento limpo. |

---

## 5. Código de Referência Consolidado

O código abaixo consolida o estado da arte do experimento com escala $N=1000$ e governança meta-heurística:

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import time

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def generate_graph(n):
    p = np.random.uniform(0.2, 0.7)
    A = (torch.rand(n, n, device=device) < p).float()
    A = torch.triu(A, 1)
    A = A + A.T
    return A

def get_cut_value(A, s_bin):
    diff = (s_bin.unsqueeze(1) != s_bin.unsqueeze(0)).float()
    return torch.sum(A * diff) / 2

def solve_managed(A, lr, steps, noise_level, restarts=1):
    n = A.shape[0]
    D = torch.diag(A.sum(dim=1))
    L = D - A
    best_cut = 0.0
    
    with torch.enable_grad():
        for _ in range(restarts):
            x = torch.randn(n, device=device).detach().requires_grad_(True)
            optimizer = torch.optim.Adam([x], lr=lr)
            for t in range(steps):
                s = torch.tanh(x)
                cut_cont = 0.25 * torch.dot(s, torch.mv(L, s))
                loss = -cut_cont
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                with torch.no_grad():
                    x.data.add_(noise_level * (1 - t/steps) * torch.randn_like(x))
            
            s_final = torch.sign(torch.tanh(x)).detach()
            best_cut = max(best_cut, get_cut_value(A, s_final).item())
    return best_cut

class MetaGNN(nn.Module):
    def __init__(self, dim=64):
        super().__init__()
        self.node_init = nn.Linear(1, dim)
        self.message_mlp = nn.Sequential(
            nn.Linear(dim*2+1, dim), nn.ReLU(), nn.Linear(dim, dim)
        )
        self.strategy_head = nn.Sequential(
            nn.Linear(dim, 32),
            nn.ReLU(),
            nn.Linear(32, 3),
            nn.Sigmoid()
        )
    
    def forward(self, A):
        n = A.shape[0]
        h = self.node_init(torch.ones(n, 1, device=device))
        for _ in range(4):
            h_i = h.unsqueeze(1).expand(-1, n, -1)
            h_j = h.unsqueeze(0).expand(n, -1, -1)
            combined = torch.cat([h_i, h_j, A.unsqueeze(-1)], dim=-1)
            h = h + self.message_mlp(combined).mean(dim=1)
        return self.strategy_head(h.mean(dim=0))

if __name__ == "__main__":
    N_NODES = 1000
    model = MetaGNN().to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.0005)

    print(f"--- META-ESTABILIDADE P vs NP (N={N_NODES}) ---")
    running_gain = 0.0

    for epoch in range(61):
        A = generate_graph(N_NODES)
        strategy = model(A)
        
        ia_steps = int(100 + strategy[0].item() * 250)
        ia_noise = 0.01 + strategy[1].item() * 0.03
        ia_lr    = 0.01 + strategy[2].item() * 0.04
        
        cut_base = solve_managed(A, lr=0.04, steps=150, noise_level=0.03)
        cut_ia   = solve_managed(A, lr=ia_lr, steps=ia_steps, noise_level=ia_noise)
        
        gain = cut_ia - cut_base
        reward = gain / N_NODES
        
        complexity_penalty = 0.05 * torch.mean(strategy**2)
        loss_meta = -reward * torch.sum(torch.log(strategy + 1e-6)) + complexity_penalty
        
        optimizer.zero_grad()
        loss_meta.backward()
        optimizer.step()
        
        running_gain = 0.9 * running_gain + 0.1 * gain
        if epoch % 5 == 0:
            print(f"E{epoch:2d} | Gain: {gain:+.1f} (Média: {running_gain:+.1f}) | IA_LR: {ia_lr:.3f} | IA_Noise: {ia_noise:.3f} | IA_Steps: {ia_steps}")
```

---

## 6. Documentos e Artefatos Associados

- **Artigo Científico 3 (Cook-Levin SAT, Parcimônia & Escala 10K - 2026):** [ARTIGO_CIENTIFICO_FRONTEIRAS_SAT_PARCIMONIA_ESCALA10K_2026.md](file:///C:/MathDoCarvalho/P_NP/ARTIGO_CIENTIFICO_FRONTEIRAS_SAT_PARCIMONIA_ESCALA10K_2026.md) (*Neuro-Meta-Heurística de Carvalho: O Núcleo de Cook-Levin (Max-3-SAT), O Princípio da Parcimônia Espectral e Escalação Linear em Grafos de 10.000 Nós*).
- **Artigo Científico 2 (Avanços & Universalidade - 2026):** [ARTIGO_CIENTIFICO_AVANCOS_ESCALABILIDADE_UGC_TSP_2026.md](file:///C:/MathDoCarvalho/P_NP/ARTIGO_CIENTIFICO_AVANCOS_ESCALABILIDADE_UGC_TSP_2026.md) (*Neuro-Meta-Heurística de Carvalho: Resolução da Anomalia de Atenção via Scaled Dot-Product, Posicionamento Frente ao Limiar de Goemans-Williamson (UGC) e Universalidade no Problema do Caixeiro Viajante (TSP)*).
- **Artigo Científico 1 (Fundamentos & Cross-Topology - 2026):** [ARTIGO_CIENTIFICO_DESCOBERTAS_NEURO_META_HEURISTICA_2026.md](file:///C:/MathDoCarvalho/P_NP/ARTIGO_CIENTIFICO_DESCOBERTAS_NEURO_META_HEURISTICA_2026.md) (*Neuro-Meta-Heurística de Carvalho: Governança Adaptativa em Grafos via Relaxação Laplaciana, Generalização Cross-Topology e Limites da Atenção Local para Max-Cut*).
- **Artigo Acadêmico Anterior:** *Neuro-Meta-Heurística de Carvalho: Gestão Adaptativa de Hiperparâmetros via Aprendizado em Grafos para Otimização de Larga Escala* (Google Docs / PDF V3).
- **Figuras Vetoriais e Raster Geradas (300 DPI):**
  - `fig1_cross_topology_hub_effect.png` / `.svg` (Efeito Hub em redes Scale-Free)
  - `fig2_tradeoff_qualidade_latencia.png` / `.svg` (Fronteira de Pareto de Latência vs Corte)
  - `fig3_benchmarks_multiescala.png` / `.svg` (Benchmarking Multiescala)
  - `fig4_convergencia_meta_governador.png` / `.svg` (Trajetória de Auto-Estabilização do Governador)

---

## 7. Roteiro de Continuidade e Próximos Passos
1. **Generalização Cross-Topology:** Avaliação zero-shot do modelo em grafos Watts-Strogatz e Barabási-Albert - *[Concluído]*.
2. **Cura do Mecanismo de Atenção (Scaled Dot-Product GAT):** Resolução da anomalia de saturação - *[Concluído]*.
3. **Benchmarking contra o Limiar UGC (Goemans-Williamson):** Avaliação de distância assintótica - *[Concluído]*.
4. **Generalização Universal para o TSP (Caixeiro Viajante):** Prova de universalidade em problemas geométricos - *[Concluído]*.
5. **O Núcleo de Cook-Levin (Max-3-SAT):** Validação em lógica proposicional no limiar crítico $m/n=4.26$ - *[Concluído]*.
6. **Princípio da Parcimônia Espectral:** Quebra da barreira dos $80\%$ de corte com a SparseGNN pura - *[Concluído]*.
7. **Escalação Linear em Grafos Gigantes ($N=10.000$ nós):** Throughput de $50.000$ arestas/s com consumo de $1.26\text{ MB}$ - *[Concluído]*.
8. **Slide Deck e Apresentação Executiva em PDF (Marp):** Síntese para bancas e conferências - *[Próxima Fase]*.

---

## 8. Resultados dos Experimentos de Generalização e Baseline (Fase 1)
*(Consulte Seção 8 anterior e o Artigo Científico 1 para os dados completos de Cross-Topology, GAT antigo e Baterias de solvers).*

---

## 9. Resultados das 4 Trilhas Avançadas (Fase 2 - 2026)

### A. Trilha 1: Cura da Anomalia de Atenção via Scaled Dot-Product GAT
- **Arquivo:** `trilha1_scaled_gat.py` | **Modelo:** `model_maxcut_scaled_gat.pth`
- **Resultados:** No regime denso crítico ($N=200, p=0.05$), onde o GAT tradicional colapsava em $0.00\%$, o novo `ScaledDotProductGNN` atingiu **$41.27\%$ de corte** (+41.27 p.p.). No regime esparso, avançou de $51.52\%$ para **$65.82\%$**, reduzindo a latência de inferência em mais de $10\times$ (para $146\text{ ms}$).

### B. Trilha 2: Confronto Teórico com Goemans-Williamson (UGC)
- **Arquivo:** `trilha2_goemans_williamson_benchmark.py` | **Relatório:** `trilha2_gw_benchmark_report.txt`
- **Resultados:** Confrontado com o solver semidefinido ótimo (SDP via Burer-Monteiro e arredondamento por hiperplano aleatório), o solver de Carvalho operou com **$76.30\%$ da eficiência do SDP de Goemans-Williamson**, mantendo um gap assintótico estritamente estável de $\approx 30.5$ p.p. em relação ao limite ótimo analítico da UGC ($\alpha_{\text{GW}} \approx 87.856\%$).

### C. Trilha 3: Generalização Universal para o Caixeiro Viajante (TSP)
- **Arquivo:** `trilha3_tsp_meta_manager.py` | **Modelo:** `model_tsp_meta_manager.pth`
- **Resultados:** Em instâncias euclidianas de $N=100$ cidades, a `TSPMetaGNN` superou o Simulated Annealing base em **$80.0\%$ das instâncias**, reduzindo o comprimento do tour em média em $+1.52$ unidades e atingindo $50.38\%$ de encurtamento em relação a rotas aleatórias.

### D. Trilha 4: Catálogo Gráfico Completo
- Geradas 4 figuras acadêmicas em PNG (300 DPI) e SVG vetorial: `fig1_cross_topology_hub_effect.*`, `fig2_tradeoff_qualidade_latencia.*`, `fig3_benchmarks_multiescala.*` e `fig4_convergencia_meta_governador.*`.

---

## 10. Inventário Consolidado de Ativos e Estado da Arte da Pesquisa

Em 2026, o projeto atingiu maturidade teórica e empírica com 54 arquivos gerados e validados, agora organizados nas pastas `Publicacoes/` e `Fontes/`:

### A. Artigos Científicos Publicados no Repositório (`Publicacoes/`)
1. **[ARTIGO_CIENTIFICO_FRONTEIRAS_SAT_PARCIMONIA_ESCALA10K_2026.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/ARTIGO_CIENTIFICO_FRONTEIRAS_SAT_PARCIMONIA_ESCALA10K_2026.md):**  
   *O Núcleo de Cook-Levin (Max-3-SAT), O Princípio da Parcimônia Espectral e Escalação Linear em Grafos de 10.000 Nós.*
2. **[ARTIGO_CIENTIFICO_AVANCOS_ESCALABILIDADE_UGC_TSP_2026.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/ARTIGO_CIENTIFICO_AVANCOS_ESCALABILIDADE_UGC_TSP_2026.md):**  
   *Avanços e Universalidade:* Cura da atenção via Scaled Dot-Product GAT, confronto assintótico com Goemans-Williamson (UGC) e transição para o Caixeiro Viajante (TSP).
3. **[ARTIGO_CIENTIFICO_DESCOBERTAS_NEURO_META_HEURISTICA_2026.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/ARTIGO_CIENTIFICO_DESCOBERTAS_NEURO_META_HEURISTICA_2026.md):**  
   *Fundamentos e Cross-Topology:* Formulação laplaciana contínua, o Efeito Hub em redes Scale-Free (Barabási-Albert) e a anomalia de saturação do GAT ingênuo.

### B. Modelos Neurais Pré-Treinados Serializados (`Fontes/`)
- `Fontes/model_maxcut.pth` (36.9 KB): Solver neural de convolução espectral esparsa (`SparseGNN` - Campeão de 80.01%).
- `Fontes/model_maxcut_hybrid.pth` (74.2 KB): Modelo híbrido neuro-simbólico espectral + atenção gated.
- `Fontes/model_maxcut_scaled_gat.pth` (105.9 KB): Modelo curado com Scaled Dot-Product Multi-Head Attention.
- `Fontes/model_sat_meta_manager.pth` (48.1 KB): IA Gerente em grafo bipartido para Max-3-SAT.
- `Fontes/model_tsp_meta_manager.pth` (63.9 KB): IA Gerente de hiperparâmetros de recozimento para o Caixeiro Viajante.
- `Fontes/model_maxcut_gat.pth` (21.6 KB): Modelo de atenção em arestas original (baseline do diagnóstico).

### C. Suítes Experimentais e Scripts de Benchmark (`Fontes/`)
- **Fase 1 (Generalização):** `exp1_cross_topology.py`, `exp2_gat_comparison.py`, `exp3_benchmark_solvers.py`.
- **Fase 2 (Avanços Teóricos):** `trilha1_scaled_gat.py`, `trilha2_goemans_williamson_benchmark.py`, `trilha3_tsp_meta_manager.py`, `trilha4_gerador_graficos_cientificos.py`.
- **Fase 3 (Fronteiras Finais):** `fase3_op1_max_sat.py`, `fase3_op2_hybrid_gnn.py`, `fase3_op3_extreme_scale.py`.
- **Scripts de Escala e Governança:** `math_p_np_carvalho_consolidado_n1000.py`, `math_p_np_carvalho_IA_gerente_hiperparametros_01.py` até `06.py`.
- **Framework UGC:** `Framework_UGC_Carvalho/` (testes de jogos únicos).

---

## 11. Resultados da Fase 3: Cook-Levin SAT, Parcimônia e Grafos Gigantes (2026)

### A. Opção 1: Max-3-SAT no Limiar Crítico de Transição de Fase ($\alpha = 4.26$)
- **Arquivo:** `Fontes/fase3_op1_max_sat.py` | **Modelo:** `Fontes/model_sat_meta_manager.pth`
- **Resultados:** A `SATMetaGNN` atingiu **$99.25\%$ de cláusulas satisfeitas** em $N=50$ variáveis (com instâncias atingindo $100\%$), **$98.92\%$** em $N=100$ e **$98.44\%$** em $N=150$, com taxa de vitória de **$60.0\%$** sobre a heurística padrão.

### B. Opção 2: O Princípio da Parcimônia Espectral
- **Arquivo:** `Fontes/fase3_op2_hybrid_gnn.py` | **Modelo:** `Fontes/model_maxcut_hybrid.pth`
- **Resultados:** O modelo híbrido obteve $73.86\%$ de corte com $265\text{ ms}$ de latência. Em contrapartida, a **`SparseGNN` pura bateu o teto histórico de $80.01\%$ de corte** em grafos esparsos ($N=200, p=0.02$, com picos de $81.1\%$), provando que convoluções espectrais amortecidas puras evitam a suavização excessiva (*oversmoothing*) induzida por atenção densa.

### C. Opção 3: Escalação Linear em Grafos Gigantes ($N=10.000$ Nós)
- **Arquivo:** `Fontes/fase3_op3_extreme_scale.py` | **Relatório:** `Fontes/fase3_op3_extreme_scale_report.txt`
- **Resultados:** Em instâncias com $10.000$ nós e $\approx 40.000$ arestas (espaço $2^{10000} \approx 10^{3010}$), o solver esparso laplaciano convergiu em **$0.79\text{ segundos}$** consumindo apenas **$1.26\text{ MB}$ de memória RAM** (Throughput: $50.288\text{ arestas/segundo}$), superando o Greedy ($28.04\%$) e o Random ($24.80\%$) com $34.37\%$ de corte.

### D. Opção 4: Apresentação Executiva em Marp (PDF & HTML)
- **Arquivo Fonte:** [apresentacao_p_vs_np_carvalho.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/apresentacao_p_vs_np_carvalho.md)
- **Slide Deck Compilado (PDF):** [apresentacao_p_vs_np_carvalho.pdf](file:///C:/MathDoCarvalho/P_NP/Publicacoes/apresentacao_p_vs_np_carvalho.pdf) (818 KB, 300 DPI)
- **Slide Deck Compilado (HTML Interativo):** [apresentacao_p_vs_np_carvalho.html](file:///C:/MathDoCarvalho/P_NP/Publicacoes/apresentacao_p_vs_np_carvalho.html)
- **Conteúdo:** 20 slides acadêmicos estruturados para bancas e conferências internacionais, cobrindo o problema P vs NP, a relaxação laplaciana, governança por GNN, benchmarks de $N=30$ a $N=10.000$, parcimônia espectral, Cook-Levin SAT, TSP e roadmap.

---

## 12. Coleção de 4 Artigos Científicos para Periódicos Internacionais (2026)

Para submissão a periódicos internacionais de alto impacto em Matemática Aplicada, Estatística e Ciência da Computação, foram produzidos 4 artigos completos e modulares dentro de `Publicacoes/`:

1. **Paper I (Matemática Pura & Otimização Concreta):**
   - **Arquivo:** [PAPER_I_MATHEMATICS_MAXCUT_LAPLACIAN_UGC.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/PAPER_I_MATHEMATICS_MAXCUT_LAPLACIAN_UGC.md)
   - **Título:** *Continuous Laplacian Relaxations and the Scale-Free Hub Effect: An Analytical Framework for Graph Bipartitioning and the Asymptotic Goemans-Williamson Gap*
   - **Periódico Alvo:** *SIAM Journal on Discrete Mathematics (SIDMA)* / *Discrete Applied Mathematics*
   - **Foco:** Formulação contínua no hipercubo $[-1, 1]^N$, gradientes analíticos, análise hessiana, Teorema 1 (Scale-Free Hub Distortion) e distância assintótica ao limitante da UGC ($\alpha_{\text{GW}} \approx 0.87856$).

2. **Paper II (Informática Aplicada, Redes Complexas & Escala Extrema):**
   - **Arquivo:** [PAPER_II_COMPUTER_SCIENCE_EXTREME_SCALE_SPARSE_GNN.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/PAPER_II_COMPUTER_SCIENCE_EXTREME_SCALE_SPARSE_GNN.md)
   - **Título:** *Linear-Time Graph Partitioning via Sparse Neural Differential Operators: Extreme-Scale Max-Cut Convergence on Arbitrary Topologies*
   - **Periódico Alvo:** *IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)* / *ACM Transactions on Computer Systems (TOCS)*
   - **Foco:** Complexidade estrita $\mathcal{O}(|E|)$ via indexação esparsa (`index_add_`), convergência sub-segundo ($0.793\text{ s}$) em grafos de $N=10.000$ nós ($|E| \approx 40.000$, espaço $10^{3010}$), consumo de $1.26\text{ MB RAM}$ e formalização do Princípio da Parcimônia Espectral (quebra da barreira de $80\%$ de corte).

3. **Paper III (Estatística Aplicada, MCMC & Física Estatística):**
   - **Arquivo:** [PAPER_III_APPLIED_STATISTICS_TSP_ANNEALING.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/PAPER_III_APPLIED_STATISTICS_TSP_ANNEALING.md)
   - **Título:** *Non-Equilibrium Annealing and Neural Adaptive Gibbs-Boltzmann Dynamics: A Statistical Mechanics Approach to the Euclidean Traveling Salesperson Problem*
   - **Periódico Alvo:** *Journal of Machine Learning Research (JMLR)* / *Journal of the Royal Statistical Society: Series B (Methodological)*
   - **Foco:** Dinâmica MCMC não-equilibrada, transição de fase tipo vidro de spin (*spin glass*) de $N=30$ para $N=100$ cidades, taxa de vitória de $80.0\%$ da `TSPMetaGNN` sobre recozimento fixo e controle de entropia $d\mathcal{S}/dt$.

4. **Paper IV (Lógica Computacional & Inteligência Artificial Simbólica):**
   - **Arquivo:** [PAPER_IV_COMPUTATIONAL_LOGIC_COOK_LEVIN_MAX3SAT.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/PAPER_IV_COMPUTATIONAL_LOGIC_COOK_LEVIN_MAX3SAT.md)
   - **Título:** *Continuous Differentiable Relaxation of the Cook-Levin Satisfiability Core: Meta-Governed Neural Message Passing across the Critical Phase Transition ($m/n \approx 4.267$)*
   - **Periódico Alvo:** *Journal of the ACM (JACM)* / *Artificial Intelligence (AIJ)*
   - **Foco:** Redução de Cook-Levin, relaxação probabilística multilinear $\mathcal{L}_{\text{SAT}}(v)$, grafo bipartido de fatores, dinâmica de Langevin para transposição de barreiras de Hamming e alcance de até $99.25\%$ de cláusulas satisfeitas no limiar crítico $m/n \approx 4.267$.

---

## 14. O Programa CLG (Computational Landscape Geometry) e a Trilogia de Benchmarks (2026)

Para investigar se a não-linearidade geométrica de relaxações contínuas poderia mapear a fronteira P vs NP, foi estruturada a 5-tupla CLG $\mathcal{L}(I) = (\mathcal{M}, \Phi, \mathcal{H}, \Omega_{\text{curv}}, \mathcal{G}(I))$:

1. **Benchmark CLG-01 (`Fontes/exp_clg01_p_vs_np.py`):**
   - Comparou 2-SAT (Classe P, $\deg=2$) com Random-3-SAT (NP-Completo, $\deg=3$).
   - Demonstrou curvatura estática nula para 2-SAT ($\Omega_{\text{curv}} = 0.0000$) e anarmonicidade para 3-SAT ($\Omega_{\text{curv}} \approx 1.86$), com separação de rigidez estatística ($p = 1.53 \times 10^{-6}$).
   - **Objeção do Professor Avaliador:** Apontou que a diferença observada poderia ser um artefato do grau polinomial da penalidade ($\deg=2$ vs $\deg=3$), atuando como variável oculta confundidora.

2. **Benchmark CLG-02 (`Fontes/exp_clg02_degree_control.py`):**
   - Implementou o teste de controle estrito de grau ($\deg=3$ mantido constante em todas as famílias).
   - Comparou Horn-3-SAT (Classe P, $\deg=3$) com Random-3-SAT (NP-Completo, $\deg=3$).
   - **Resultado do Controle:** Curvatura estática e norma tensorial $\Gamma = \|\nabla^3 \Phi\|_F$ foram praticamente idênticas ($\Omega \approx 1.81$ vs $1.90$), confirmando que a curvatura estática mede apenas o grau algébrico.
   - **Métrica Dinâmica de Bacias:** Horn-3-SAT apresentou **100.0% de Reachability e 0.00 armadilhas**, enquanto Random-3-SAT no ponto crítico caiu para **6.0% de Reachability com 2.23 armadilhas**.

350: 3. **Benchmark CLG-03 (`Fontes/exp_clg03_xorsat_and_ogp.py`):**
   - O teste canônico e definitivo: introdução da família **3-XOR-SAT** (sistemas de paridade em $\text{GF}(2)$).
   - **Propriedades:** 3-XOR-SAT está estritamente em **Classe P** (solvível em tempo polinomial cúbico no pior caso $\mathcal{O}(N^3)$ por Eliminação Gaussiana em $\text{GF}(2)$) e possui grau algébrico $\deg=3$.
   - **Esclarecimento Variacional:** A relaxação multilinear no hipercubo contínuo $[-1, 1]^N$ conecta-se a Hamiltonianos de 3-spin glass, mas não deve ser identificada automaticamente com o modelo esférico $p$-spin (que impõe $\sum x_i^2 = N$).
   - **Resultados Empíricos ($N=30$ e $N=60$):**
     - Eliminação Gaussiana em $\text{GF}(2)$: **100.0% de sucesso em 3.6 a 4.8 ms**.
     - Relaxação Contínua Diferencial: **Reachability $R_{\text{dyn}} = 0.0\%$ (colapso total) e severidade de armadilha $\bar{E}_{\text{trap}} = 8.81$ cláusulas**.
   - **Conclusão:** O 3-XOR-SAT exibe paisagem mais vítrea do que o próprio Random-3-SAT. Isso refuta experimentalmente a hipótese de que a geometria contínua separa P de NP, provando que:
     $$\boxed{ \text{Geometric Hardness} \not\Rightarrow \text{Computational Hardness} }$$
     para dinâmicas de descida contínua.

4. **Benchmark CLG-04 (`Fontes/exp_clg04_representation_invariance.py`):**
   - **O Experimento Decisivo (Ensemble $\mathcal{E}_{\text{equiv}}$):** Teste das *exatas mesmas fórmulas booleanas* sob três relaxações contínuas distintas no hipercubo: Multilinear ($\Phi_{\text{mult}}$), Quadrática Hinge ($\Phi_{\text{quad}}$) e Softplus Log-Sum-Exp ($\Phi_{\text{soft}}$ com $\beta=5.0$).
   - **Métricas Avançadas:** Intervalos de confiança de Wilson a 95% e distância de Hamming normalizada $d_H(s_{\text{final}}, s^*) \in [0, 1]$.
   - **Descoberta:** Em Random-3-SAT ($N=60$), mudar de $\Phi_{\text{mult}}$ para $\Phi_{\text{soft}}$ elevou a alcançabilidade dinâmica de **$9.3\%$ para $69.3\%$** ($IC_{95\%} [58.2\%, 78.6\%]$) e reduziu armadilhas de $2.71$ para $0.45$ cláusulas. Em contrapartida, no 3-XOR-SAT ($N=60$), a alcançabilidade permaneceu em **$0.0\%$ ($0/75$, $IC_{95\%} [0.0\%, 4.9\%]$)** com $d_H \approx 0.50$ (ortogonal à solução plantada) sob todas as três relaxações suaves.
   - **Impacto:** Demonstrou que a geometria contínua $\mathcal{G}(\Phi(I))$ **não é intrínseca** ao problema discreto $I$, abrindo o problema variacional da Geometria Canônica $\Phi^*(I) = \arg\min_{\Phi} \text{Glassiness}(\Phi)$.


---

## 15. Auditorias Adversariais Independentes

O framework foi submetido a análises adversariais independentes orientadas estritamente pelos critérios da literatura de teoria da complexidade e otimização combinatória:

### A. Análise de Física Estatística e Otimização
- Identificou a dualidade do 3-XOR-SAT como controle negativo canônico.
- Forneceu as rotas analíticas: Horn-3-SAT via **Sistemas Dinâmicos Cooperativos (Condições de Kamke-Müller / Teorema de Hirsch)** com matrizes Jacobianas Z; e Random-3-SAT via **Fórmula de Kac-Rice** com complexidade topológica $\Sigma(\alpha) > 0$.
- Confirmou a validade metodológica da `SparseGNN` ($N=10.000$ nós em $0.79\text{s}$ com $1.26\text{ MB RAM}$).

### B. Análise de Teoria da Complexidade e Análise Funcional
- Revelou quatro identidades algébricas e metodológicas fundamentais:
  1. **Identidade de Curvatura:** $\Omega_{\text{curv}} = \frac{1}{\sqrt{3}} \|\mathcal{T}\|_F$ em amostragem uniforme $[-1, 1]$, demonstrando que $\Omega$ re-amostrava o desvio da distribuição uniforme e contava cláusulas.
  2. **Cancelamento em Equi-3-SAT:** $[(1-z) + (1+z)] = 2$, provando que a variável auxiliar se cancela na extensão multilinear, colapsando o grau efetivo para 2.
  3. **Atrator all-FALSE em Horn:** A atribuição all-negative satisfaz trivialmente qualquer fórmula Horn aleatória com $\le 1$ literal positivo.
  4. **Confundidor UNSAT e Viés de Plantação:** No limiar crítico, ~50% das fórmulas são insatisfatíveis por definição; enquanto o Planted SAT elimina o viés de UNSAT, introduz viés estatístico de plantação, exigindo avaliação em três ensembles independentes ($\mathcal{E}_{\text{random|SAT}}$, $\mathcal{E}_{\text{planted}}$, $\mathcal{E}_{\text{controlled}}$).

---

## 16. A Tríade Estrutural do CLG e o Reposicionamento Teórico

O projeto adota a arquitetura de três níveis proposta pelo Professor Avaliador:

```
                            PROGRAMA CLG (REVISADO)
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         ▼                             ▼                             ▼
       CLG-L                         CLG-G                         CLG-A
 (Local Landscape)             (Global Landscape)           (Algorithmic Landscape)
 - Hessiana H(x)               - Bacias de atração          - Estabilidade de GNNs
 - Espectro e traço            - Barreiras de energia       - Langevin e gradiente
 - Curvatura Omega_curv        - Overlap q(x, y)            - Limites locais (OGP)
 - Tensor T = grad^3 Phi       - Fragmentação vítrea        - Desacoplamento vs. Álgebra
 [Falsificado como             [Conexão com física          [Teoremas de limites
  invariante de complexidade]   estatística e OGP]           para classes de solvers]
```

### Taxonomia Operacional de Famílias em P:
Não são criadas falsas classes de complexidade. A distinção analítica é estritamente de compatibilidade algorítmica:
- **Famílias em P favoráveis à dinâmica contínua:** Instâncias (2-SAT, Horn monótono) cujo fluxo gradiente preserva ordem parcial ou convexidade efetiva, permitindo que a física contínua escoe para o ótimo global.
- **Famílias em P com estrutura algébrica não capturada pela dinâmica:** Instâncias (3-XOR-SAT) cuja paisagem contínua sofre fraturamento vítreo, mas cujo algoritmo algébrico opera em uma representação estrutural diferente (eliminação sobre corpos finitos $\mathbb{F}_2$) daquela explorada pela dinâmica métrica contínua.

---

## 17. Reorganização Estratégica das Publicações Internacionais

1. **Retirada Definitiva de Reivindicações sobre P vs NP:**
   Canceladas formalmente submissões pretendidas a Annals of Mathematics e JACM.
2. **Papers I e II (Max-Cut, HISAC e Escala Extrema $N=10.000$):**
   - **Periódicos:** *SIAM Journal on Optimization (SIOPT)*, *IEEE TPAMI* ou *ACM TOCS*.
   - **Destaque:** Desempenho linear comprovado de $N=10.000$ em $0.79\text{s}$ com $1.26\text{ MB RAM}$, recorde de $80.01\%$ de corte e respeito estrito aos limites da Unique Games Conjecture (UGC) e Goemans-Williamson.
3. **Monografia e Paper Teórico CLG:**
   - **Título Definitivo:** *"Computational Landscape Geometry: Why Glassiness Does Not Imply Computational Hardness"*.
   - **Alvo:** *Journal of Machine Learning Research (JMLR)* / *NeurIPS*.
   - **Contribuição Inédita:** Caracterização quantitativa da interação entre a relaxação contínua no hipercubo $[-1, 1]^N$ e os limites de algoritmos locais e GNNs sob a Overlap Gap Property (OGP).
4. **Documento Formal para a Banca:**
   - [RESPOSTA_FORMAL_AO_PARECER_DO_PROFESSOR.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/RESPOSTA_FORMAL_AO_PARECER_DO_PROFESSOR.md) consolidado com todos os agradecimentos, formalizações matemáticas e o protocolo dos três ensembles.

---

## 18. Diretriz Permanente e Conclusão
Toda a base matemática, empírica, modelos treinados, artigos científicos publicáveis, relatórios de benchmark (CLG-01, CLG-02, CLG-03), cartas de resposta técnica e apresentações executivas foram consolidadas integralmente dentro deste ecossistema (`C:\MathDoCarvalho\P_NP`) e sincronizadas no GitHub (`https://github.com/thiagocarvalhodba/p-vs-np-carvalho`).




---

## 19. Consolidação do Parecer 05 do Professor e Entregáveis

Em resposta ao Parecer 05 (`C:\MathDoCarvalho\AnaliseReportadaPeloProfessor05.docx`), o programa de pesquisa atingiu a maturidade científica plena:
1. **Proposição 1 Formal:** $\Omega_{\text{curv}} = \frac{1}{\sqrt{3}} \|\mathcal{T}\|_F$ demonstrada passo a passo sob amostragem i.i.d. $x_i \sim \mathcal{U}([-1, 1])$, provando a degenerescência algébrica de $\text{CLG}_L$.
2. **Execução do Experimento Decisivo $\mathcal{E}_{\text{equiv}}$ (CLG-04):** Fórmulas idênticas sob relaxações Multilinear, Quadrática e Softplus, com intervalos de confiança de Wilson a 95% e distâncias de Hamming.
3. **Formalização da Geometria Canônica:** Definição do espectro de alcançabilidade $\mathcal{R}(I) = \{ R_{\text{dyn}}(\Phi) : \Phi \sim I \}$ e do problema variacional da representação ótima $\Phi^*(I)$.
4. **Documentos Oficiais Gerados:**
   - Markdown completo: [Publicacoes/RESPOSTA_FORMAL_AO_PARECER_DO_PROFESSOR.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/RESPOSTA_FORMAL_AO_PARECER_DO_PROFESSOR.md)
   - Documento Word formatado para o Professor: `C:\MathDoCarvalho\RespostaAoProfessor05.docx`
   - Fundações teóricas atualizadas: [Publicacoes/CLG_FOUNDATIONS.md](file:///C:/MathDoCarvalho/P_NP/Publicacoes/CLG_FOUNDATIONS.md)
   - Códigos e relatórios: `Fontes/exp_clg04_representation_invariance.py`, `Fontes/exp_clg04_report.txt`, `Fontes/exp_clg04_results.json`.

---

## 20. Parecer 06 do Professor: Auditoria Metodológica e o Eixo CLG-R

Em resposta ao Parecer 06 (`C:\MathDoCarvalho\AnaliseReportadaPeloProfessor06.docx`), o programa de pesquisa foi submetido a uma auditoria metodológica profunda:

1. **Definição Formal de Equivalência de Relaxações:**
   - $\mathcal{F}(I) = \{ \Phi: [-1, 1]^N \to \mathbb{R}_{\ge 0} \mid \text{Zero}_{\mathcal{V}}(\Phi) = S(I) \}$ onde $\mathcal{V} = \{-1, +1\}^N$.
   - Duas relaxações são equivalentes se e somente se $\text{Zero}_{\mathcal{V}}(\Phi_1) = \text{Zero}_{\mathcal{V}}(\Phi_2) = S(I)$.
   - Os gradientes $\nabla \Phi_1, \nabla \Phi_2$ permanecem desvinculados no interior do hipercubo $(-1, 1)^N$.

2. **Auditoria Matemática do Softplus:**
   - Softplus é estritamente $>0$ no contínuo ($\ge \frac{M}{\beta}\ln(1 + e^{-\beta})$). O critério de alcançabilidade dinâmica $R_{\text{dyn}}$ é puramente discreto: $E_{\text{disc}}(s_{\text{round}}) = 0$.

3. **Auditoria Estrita de Pareamento CLG-04 (`exp_clg04_strict_audit.py`):**
   - 1.800 trajetórias estritamente pareadas (mesma instância $I \times$ mesmo ponto inicial $x_0 \times$ mesmo orçamento de passos $T=200$ e $\eta=0.02$).
   - Separação entre Gradient Descent puro (GD) e Langevin com difusão térmica ($T=0.005$).
   - Registros imutáveis salvos em `Fontes/exp_clg04_audit_log.json` e `Fontes/exp_clg04_audit_summary.json`.

4. **Desacoplamento Representação vs. Otimizador:**
   - A alta alcançabilidade no Random-3-SAT ($N=60$) obtida originalmente sob Adam ($69.3\%$) decorre da re-escala adaptativa de coordenadas $\frac{g_t}{\sqrt{v_t}}$, que explora a curvatura suave e monotonicidade do Softplus.
   - Sob SGD com taxa fixa em horizonte finito de 200 passos, as distâncias de Hamming confirmam a hierarquia geométrica: Softplus ($d_H=0.284$) vs Multilinear ($d_H=0.327$) vs Quadrática ($d_H=0.476$).
   - No 3-XOR-SAT, $R_{\text{dyn}} = 0.0\%$ ($0/75$) e $d_H \approx 0.50$ persistem sob todos os otimizadores e relaxações.

5. **A Quádruple CLG e a Conjectura CLG-R:**
   - Adotada a estrutura de quatro eixos: $\text{CLG}_L$ (Local), $\text{CLG}_G$ (Global), $\text{CLG}_A$ (Algorítmico) e $\text{CLG}_R$ (Representação).
   - Conjectura Formal CLG-R:
     $$\liminf_{N \to \infty} R_{\text{dyn}}(I_N, \Phi_N^{(1)}, \mathcal{D}) \;\neq\; \liminf_{N \to \infty} R_{\text{dyn}}(I_N, \Phi_N^{(2)}, \mathcal{D})$$

6. **Entregável Oficial:**
   - Word formatado: `C:\MathDoCarvalho\RespostaAoProfessor06.docx`.
   - Markdown: `Publicacoes/RESPOSTA_FORMAL_AO_PARECER_DO_PROFESSOR.md`.

---

## 21. Parecer 07 do Professor: Estatística Hierárquica, Condicionamento e Transição para CLG-04 Fase II

O Parecer 07 (`C:\MathDoCarvalho\AnaliseReportadaPeloProfessor07.docx`) estabeleceu o padrão analítico definitivo:

1. **Estatística Hierárquica:**
   - Desagregação entre $R_{\text{traj}}$ ($75$ ensaios) e $R_{\text{inst}}$ ($5$ instâncias com $\bar{R} \pm \text{SEM}$), prevenindo pseudorreplicamento.
   - Em $N=60$ (GD puro): $R_{\text{inst}} = 0.0\% \pm 0.0\%$, com $d_H(\Phi_{\text{soft}}) = 0.284 \pm 0.022$ vs. $d_H(\Phi_{\text{quad}}) = 0.476 \pm 0.008$ ($p < 10^{-4}$).

2. **Separação CLG-04A vs. CLG-04B:**
   - **CLG-04A:** Baseline de 1ª ordem pura (GD/Langevin, $\eta=0.02$, $T=200$).
   - **CLG-04B:** Otimização adaptativa (Adam com re-escala de momentos), onde Softplus atinge $69.3\%$.

3. **Diagnóstico de Condicionamento (CLG-04C):**
   - Quadrática Hinge sofre de colapso numérico extremo ($\kappa(H) > 360.000$ e platôs de gradiente nulo).
   - Softplus mantém condicionamento hessiano estável ($\kappa(H) \approx 8.8$) e gradiente decrescente.
   - Multilinear exibe explosão de gradiente próximo às bordas por produtos cruzados.

4. **Controle de Unicidade em 3-XOR-SAT:**
   - Comprovado $\text{rank}_{\mathbb{F}_2}(A) = N$ ($|S| = 1$), garantindo que $d_H(s_{\text{final}}, s^*)$ e overlap $q \approx 0.0$ medem o afastamento da única solução da fórmula.

5. **Conjectura CLG-R Generalizada:**
   $$\limsup_{N \to \infty} | \mathcal{Q}(I_N, \Phi_N^{(1)}, \mathcal{D}) - \mathcal{Q}(I_N, \Phi_N^{(2)}, \mathcal{D}) | > 0$$
   para funcional de qualidade algorítmica $\mathcal{Q}$ (como $d_H$ ou $E_{\text{disc}}$).

6. **A Pergunta Central Consagrada:**
   *"Qual representação torna determinada classe de algoritmos capaz de explorar a paisagem?"*

7. **Entregáveis:**
   - Documento Word: `C:\MathDoCarvalho\RespostaAoProfessor07.docx`.
   - Códigos e dados: `Fontes/compute_hierarchical_stats.py`, `Fontes/exp_clg04_conditioning_and_phase2.py`, `Fontes/exp_clg04_hierarchical_summary.json`, `Fontes/exp_clg04_conditioning_tracking.json`.

---

## 22. Parecer 08 do Professor: Os Quatro Controles Mandatórios do CLG-R

O Parecer 08 (`C:\MathDoCarvalho\AnaliseReportadaPeloProfessor08.docx`) validou a mudança da pergunta para a dependência da dinâmica em relação à representação e estabeleceu quatro controles experimentais rigorosos:

1. **Normalização de Escala de Gradiente:**
   - Potenciais normalizados $\tilde{\Phi} = \Phi / c_\Phi$, com $c_\Phi = \mathbb{E}[\|\nabla \Phi\|]$ ($c_{\text{multi}} = 5.26, c_{\text{quad}} = 5.93, c_{\text{soft}} = 8.65$).
2. **Matriz Fatorial 3x3 Completa:**
   - Avaliadas 3 Representações $\times$ 3 Dinâmicas (GD puro, Langevin, Adam) em $N=60$.
   - A Quadrática Hinge exibe colapso severo de condicionamento ($\kappa_2 > 80.000$), enquanto Softplus permanece estável ($\kappa_2 \approx 25$).
3. **Diferenças Pareadas por Instância:**
   - $\Delta_i = d_{H, i}^{\text{quad}} - d_{H, i}^{	ext{soft}} > 0$ em 100% das instâncias independentes.
4. **Alinhamento Teórico Rigoroso:**
   - Posto-Nulidade no 3-XOR-SAT: $\text{rank}(A) = N \implies \dim \ker(A) = 0 \implies |S(I)| = 1$.
   - Conjectura CLG-R com funcional limitado $\mathcal{Q} \in [0, 1]$.
   - Tese Central: *"A equivalência booleana não determina a acessibilidade algorítmica de uma relaxação contínua: representações equivalentes podem induzir geometrias numéricas e interações representação–dinâmica distintas, produzindo diferentes qualidades de solução sob a mesma classe de algoritmo local."*
5. **Entregável Oficial:**
   - Word: `C:\MathDoCarvalho\RespostaAoProfessor08.docx`.
