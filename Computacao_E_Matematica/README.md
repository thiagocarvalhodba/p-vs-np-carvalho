# Pesquisa P vs NP: Neuro-Meta-Heurística de Carvalho (Max-Cut)

**Autor:** Thiago Carvalho  
**Ano/Data:** 2026  
**Ambiente:** Python 3.13 / 3.14 | PyTorch | CPU/CUDA  
**Diretório do Projeto:** `C:\MathDoCarvalho\P_NP`  

---

## Sobre o Projeto

Este projeto investiga a intersecção entre problemas de classe **P** e **NP-Difícil** por meio de **Neural Combinatorial Optimization (NCO)**.

A tese central avalia como uma **Graph Neural Network (GNN)**, computada estritamente em tempo polinomial ($P$), pode atuar como um **Meta-Manager (IA Gerente de Hiperparâmetros)** para controlar e otimizar um solver matemático baseado em relaxação contínua via **Matriz Laplaciana** e recozimento estocástico para o problema do **Max-Cut** em larga escala ($N=30, 100, 1000$) e escala extrema ($N=10.000$).

---

## Estrutura do Repositório (Organização para Git)

O projeto está organizado em duas pastas principais, além dos documentos de governança raiz:

```
├── Publicacoes/           # Coleção de artigos científicos, monografias, slides e figuras
│   ├── README_PUBLICACOES.md
│   ├── PAPER_I_MATHEMATICS_MAXCUT_LAPLACIAN_UGC.md
│   ├── PAPER_II_COMPUTER_SCIENCE_EXTREME_SCALE_SPARSE_GNN.md
│   ├── PAPER_III_APPLIED_STATISTICS_TSP_ANNEALING.md
│   ├── PAPER_IV_COMPUTATIONAL_LOGIC_COOK_LEVIN_MAX3SAT.md
│   ├── ARTIGO_CIENTIFICO_*.md
│   ├── apresentacao_p_vs_np_carvalho.pdf (.html, .md)
│   └── fig*.png / fig*.svg (300 DPI)
├── Fontes/                # Códigos-fonte validados, modelos (.pth), benchmarks e testes
│   ├── README_FONTES.md   # Guia detalhado de cada script, execução e dependências
│   ├── fase3_op1_max_sat.py
│   ├── fase3_op2_hybrid_gnn.py
│   ├── fase3_op3_extreme_scale.py
│   ├── trilha1_scaled_gat.py / trilha2_*.py / trilha3_*.py / trilha4_*.py
│   ├── math_p_np_carvalho_*.py
│   ├── model_*.pth        # Pesos treinados e validados
│   └── Framework_UGC_Carvalho/
├── PROJECT_MEMORY.md      # Memória persistente e especificações técnicas
├── README.md              # Este documento guia
└── .gitignore             # Higienização de cache, venv e temporários para Git
```

---

## 📚 Publicações e Apresentações (`/Publicacoes`)

Consulte o catálogo detalhado em **[`Publicacoes/README_PUBLICACOES.md`](file:///C:/MathDoCarvalho/P_NP/Publicacoes/README_PUBLICACOES.md)**:

### Artigos para Periódicos Internacionais (2026)
1. 📐 **Matemática Aplicada & Otimização Concreta (SIAM / DAM):**  
   👉 **[`Publicacoes/PAPER_I_MATHEMATICS_MAXCUT_LAPLACIAN_UGC.md`](file:///C:/MathDoCarvalho/P_NP/Publicacoes/PAPER_I_MATHEMATICS_MAXCUT_LAPLACIAN_UGC.md)**
2. 💻 **Ciência da Computação & Escala Extrema (IEEE TPAMI / ACM TOCS):**  
   👉 **[`Publicacoes/PAPER_II_COMPUTER_SCIENCE_EXTREME_SCALE_SPARSE_GNN.md`](file:///C:/MathDoCarvalho/P_NP/Publicacoes/PAPER_II_COMPUTER_SCIENCE_EXTREME_SCALE_SPARSE_GNN.md)**
3. 📊 **Estatística Aplicada & Aprendizado de Máquina (JMLR / JRSS-B):**  
   👉 **[`Publicacoes/PAPER_III_APPLIED_STATISTICS_TSP_ANNEALING.md`](file:///C:/MathDoCarvalho/P_NP/Publicacoes/PAPER_III_APPLIED_STATISTICS_TSP_ANNEALING.md)**
4. 🧠 **Lógica Computacional & Inteligência Artificial (JACM / AIJ):**  
   👉 **[`Publicacoes/PAPER_IV_COMPUTATIONAL_LOGIC_COOK_LEVIN_MAX3SAT.md`](file:///C:/MathDoCarvalho/P_NP/Publicacoes/PAPER_IV_COMPUTATIONAL_LOGIC_COOK_LEVIN_MAX3SAT.md)**

### Apresentação Executiva para Bancas e Conferências (Marp)
- 📊 **Slide Deck Executivo em PDF (818 KB, 300 DPI):** 👉 **[`Publicacoes/apresentacao_p_vs_np_carvalho.pdf`](file:///C:/MathDoCarvalho/P_NP/Publicacoes/apresentacao_p_vs_np_carvalho.pdf)**
- 🌐 **Slide Deck Interativo em HTML:** 👉 **[`Publicacoes/apresentacao_p_vs_np_carvalho.html`](file:///C:/MathDoCarvalho/P_NP/Publicacoes/apresentacao_p_vs_np_carvalho.html)**
- 📝 **Código-Fonte Marp Markdown:** 👉 **[`Publicacoes/apresentacao_p_vs_np_carvalho.md`](file:///C:/MathDoCarvalho/P_NP/Publicacoes/apresentacao_p_vs_np_carvalho.md)**

---

## 💻 Códigos-Fonte e Modelos (`/Fontes`)

Consulte a documentação técnica e instruções de execução em **[`Fontes/README_FONTES.md`](file:///C:/MathDoCarvalho/P_NP/Fontes/README_FONTES.md)**:

- `fase3_op1_max_sat.py`: SATMetaGNN no limiar crítico de Cook-Levin ($m/n=4.267$).
- `fase3_op2_hybrid_gnn.py`: Prova da Parcimônia Espectral (SparseGNN batendo recorde de 80.01%).
- `fase3_op3_extreme_scale.py`: Solver diferencial esparso $\mathcal{O}(|E|)$ em grafos de $N=10.000$ nós ($0.79\text{s}$, $1.26\text{ MB RAM}$).
- `trilha1_scaled_gat.py`: Scaled Dot-Product Multi-Head Attention curando o colapso do GAT.
- `trilha2_goemans_williamson_benchmark.py`: Solver ótimo SDP (Goemans-Williamson) e teste UGC.
- `trilha3_tsp_meta_manager.py`: Meta-governador de recozimento no Caixeiro Viajante (80% vitórias).
- `trilha4_gerador_graficos_cientificos.py`: Gerador das figuras científicas em alta resolução.
- Modelos serializados `.pth`: `model_maxcut.pth`, `model_maxcut_hybrid.pth`, `model_maxcut_scaled_gat.pth`, `model_sat_meta_manager.pth`, `model_tsp_meta_manager.pth`, `model_maxcut_gat.pth`.
