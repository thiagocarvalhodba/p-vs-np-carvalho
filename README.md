# Pesquisa P vs NP: Neuro-Meta-Heurística de Carvalho

**Autor:** Thiago Carvalho  
**Ano/Data:** 2026  
**Ambiente:** Python 3.13 / 3.14 | PyTorch | CPU/CUDA  
**Diretório do Projeto:** `C:\MathDoCarvalho\P_NP`  

> [!IMPORTANT]
> ### 🛡️ AVISO DE PROPRIEDADE INTELECTUAL E DIREITOS AUTORAIS
> **Copyright © 2026 Thiago Carvalho. Todos os direitos reservados.**
> 
> Todo o conteúdo intelectual, científico, matemático e computacional contido neste repositório — incluindo formulações analíticas, provas de teoremas, arquiteturas de Redes Neurais em Grafos (GNN), pesos pré-treinados (`.pth`), códigos-fonte, artigos científicos e apresentações — é de **propriedade intelectual exclusiva de Thiago Carvalho**.
> 
> - ❌ **Proibida a reprodução ou cópia:** É estritamente vedada a cópia, reprodução, redistribuição, modificação, engenharia reversa, sublicenciamento ou comercialização, total ou parcial, sem autorização prévia, expressa e formal por escrito do autor.
> - ❌ **Proibido treinamento de IA de terceiros:** Não é permitida a incorporação destes ativos para o treinamento ou ajuste fino de modelos de Inteligência Artificial sem autorização formal expressa.
> - 📖 **Licença de Leitura Pública:** O acesso público constitui tão somente licença de leitura e apreciação científica pessoal por pares acadêmicos e pela comunidade científica.
> 
> Consulte os termos legais completos no arquivo [LICENSE](LICENSE).

---

## 🎯 Sobre o Projeto

Este repositório reúne os desenvolvimentos, formulações teóricas, benchmarks computacionais e publicações da pesquisa em **Neural Combinatorial Optimization (NCO)** voltada a instâncias de alta complexidade da classe **NP-Difícil** (Max-Cut, Caixeiro Viajante - TSP e Max-3-SAT).

### A Tese Central
Demonstra-se analítica e computacionalmente que uma **Graph Neural Network (GNN)**, computada estritamente em tempo polinomial ($P$), pode atuar como um **Meta-Manager (IA Gerente de Hiperparâmetros)** para controlar e otimizar um solver matemático baseado em relaxação contínua via **Matriz Laplaciana** e recozimento estocástico para o problema do **Max-Cut** em larga escala ($N=30, 100, 1000$) e escala extrema ($N=10.000$).

---

## 🗂️ Estrutura do Repositório

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
├── LICENSE                # Termos de Propriedade Intelectual e Direitos Autorais
├── README.md              # Este documento guia
└── .gitignore             # Higienização de cache, venv e temporários para Git
```

---

## 📚 Acervo de Publicações Internacionais (`/Publicacoes`)

Consulte o catálogo detalhado em **[`Publicacoes/README_PUBLICACOES.md`](Publicacoes/README_PUBLICACOES.md)**:

### Artigos para Periódicos Internacionais (2026)
1. 📐 **Matemática Pura e Otimização Discreta (SIAM / DAM):**  
   👉 **[`Publicacoes/PAPER_I_MATHEMATICS_MAXCUT_LAPLACIAN_UGC.md`](Publicacoes/PAPER_I_MATHEMATICS_MAXCUT_LAPLACIAN_UGC.md)**  
   *Relaxação laplaciana contínua, análise hessiana e prova do Teorema do Efeito Hub.*
2. 💻 **Ciência da Computação & Escala Extrema (IEEE TPAMI / ACM TOCS):**  
   👉 **[`Publicacoes/PAPER_II_COMPUTER_SCIENCE_EXTREME_SCALE_SPARSE_GNN.md`](Publicacoes/PAPER_II_COMPUTER_SCIENCE_EXTREME_SCALE_SPARSE_GNN.md)**  
   *Escala extrema ($N=10.000$ nós em $0.79\text{s}$) e Princípio da Parcimônia Espectral ($80.01\%$).*
3. 📊 **Estatística Aplicada & Aprendizado de Máquina (JMLR / JRSS-B):**  
   👉 **[`Publicacoes/PAPER_III_APPLIED_STATISTICS_TSP_ANNEALING.md`](Publicacoes/PAPER_III_APPLIED_STATISTICS_TSP_ANNEALING.md)**  
   *Termodinâmica do TSP e transição vítrea com 80% de vitórias sobre recozimento fixo.*
4. 🧠 **Lógica Computacional & Inteligência Artificial (JACM / AIJ):**  
   👉 **[`Publicacoes/PAPER_IV_COMPUTATIONAL_LOGIC_COOK_LEVIN_MAX3SAT.md`](Publicacoes/PAPER_IV_COMPUTATIONAL_LOGIC_COOK_LEVIN_MAX3SAT.md)**  
   *Núcleo de Cook-Levin (Max-3-SAT) com 99.25% de cláusulas satisfeitas no limiar crítico.*
5. 🌐 **Monografia Teórica - Geometria da Paisagem Computacional (Projeto CLG-01):**  
   👉 **[`Publicacoes/CLG_FOUNDATIONS.md`](Publicacoes/CLG_FOUNDATIONS.md)**  
   *Fundamentação da 5-tupla CLG, prova da Invariância de Curvatura em 2-SAT (Classe P) vs Anarmonicidade em 3-SAT (Classe NP), e validação empírica da Hipótese de Separabilidade ($p = 1.53 \times 10^{-6}$).*
6. 🔬 **Dossiê de Auditoria Externa e Teste de Controle de Grau (Projeto CLG-02):**  
   👉 **[`Publicacoes/DOSSIE_AUDITORIA_CLAUDE_OPUS.md`](Publicacoes/DOSSIE_AUDITORIA_CLAUDE_OPUS.md)**  
   *Protocolo completo de auditoria por pares (Claude Opus / Gemini Pro) e desacoplamento formal do grau algébrico ($\deg=3$ fixo: Horn-3-SAT em P vs Random-3-SAT em NP-C) via bacias de atração e densidade de armadilhas metaestáveis.*

### Apresentação Executiva para Bancas e Conferências (Marp)
- 📊 **Slide Deck Executivo em PDF (Alta Resolução, 300 DPI):** 👉 **[`Publicacoes/apresentacao_p_vs_np_carvalho.pdf`](Publicacoes/apresentacao_p_vs_np_carvalho.pdf)**
- 🌐 **Slide Deck Interativo em HTML:** 👉 **[`Publicacoes/apresentacao_p_vs_np_carvalho.html`](Publicacoes/apresentacao_p_vs_np_carvalho.html)**
- 📝 **Código-Fonte dos Slides:** 👉 **[`Publicacoes/apresentacao_p_vs_np_carvalho.md`](Publicacoes/apresentacao_p_vs_np_carvalho.md)**

---

## 💻 Códigos-Fonte, Modelos e Benchmarks (`/Fontes`)

Consulte a documentação técnica completa em **[`Fontes/README_FONTES.md`](Fontes/README_FONTES.md)**:

- `clg_framework.py`: Framework de Geometria da Paisagem Computacional (CLG), cálculo de Hessianas e invariantes $\mathcal{G}(I)$.
- `exp_clg01_p_vs_np.py`: Benchmark comparativo Classe P (2-SAT) vs NP-Completo (3-SAT) provando separação estatística de 5 ordens de magnitude.
- `exp_clg02_degree_control.py`: Benchmark com controle rigoroso de grau algébrico ($\deg=3$: Horn-3-SAT em P vs Random-3-SAT em NP-C), medindo Reachability dinâmico e densidade de armadilhas.
- `fase3_op1_max_sat.py`: SATMetaGNN no limiar crítico de Cook-Levin ($m/n=4.267$).
- `fase3_op2_hybrid_gnn.py`: Prova da Parcimônia Espectral (SparseGNN batendo recorde de 80.01%).
- `fase3_op3_extreme_scale.py`: Solver diferencial esparso $\mathcal{O}(|E|)$ em grafos de $N=10.000$ nós ($0.79\text{s}$, $1.26\text{ MB RAM}$).
- `trilha1_scaled_gat.py`: Scaled Dot-Product Multi-Head Attention curando o colapso do GAT.
- `trilha2_goemans_williamson_benchmark.py`: Solver ótimo SDP (Goemans-Williamson) e teste UGC.
- `trilha3_tsp_meta_manager.py`: Meta-governador de recozimento no Caixeiro Viajante (80% vitórias).
- `trilha4_gerador_graficos_cientificos.py`: Gerador das figuras científicas em alta resolução.
- **Modelos Treinados `.pth`:** `model_maxcut.pth`, `model_maxcut_hybrid.pth`, `model_maxcut_scaled_gat.pth`, `model_sat_meta_manager.pth`, `model_tsp_meta_manager.pth`, `model_maxcut_gat.pth`.

---

## 🚀 Como Executar e Replicar

### Pré-requisitos
- Python 3.10+ (validado em 3.13 / 3.14)
- Bibliotecas: `torch`, `networkx`, `numpy`, `matplotlib`

```bash
pip install torch networkx numpy matplotlib
```

### 1. Execução do Benchmark CLG-01 (Classe P vs NP-Completo)
```bash
python Fontes/exp_clg01_p_vs_np.py
```

### 2. Execução do Benchmark CLG-02 (Controle de Grau Algébrico deg=3)
```bash
python Fontes/exp_clg02_degree_control.py
```

### 3. Execução do Benchmark de Escala Extrema (Max-Cut $N=10.000$)
```bash
python Fontes/fase3_op3_extreme_scale.py
```

---

## 📄 Licença e Direitos Autorais

Todos os direitos reservados a **Thiago Carvalho (2026)**.  
O uso, redistribuição, cópia ou engenharia reversa sem autorização expressa é estritamente proibido.  
Para mais informações, consulte o arquivo [LICENSE](LICENSE).
