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
6. 🔬 **Auditoria Externa e Protocolo de Testes Adversariais (Projeto CLG-02 & Auditoria Independente):**  
   👉 **[`Publicacoes/PROMPT_CLAUDE_CODE_AUDITORIA.md`](Publicacoes/PROMPT_CLAUDE_CODE_AUDITORIA.md)**  
   *Protocolo estruturado de auditoria matemática (Annals/STOC criteria), testes formais de invariância de representação e desacoplamento do grau algébrico ($\deg=3$ fixo: Horn-3-SAT em P vs Random-3-SAT em NP-C).*
7. 📜 **Carta de Resposta Técnica e Reposicionamento Científico (Projeto CLG-03):**  
   👉 **[`Publicacoes/RESPOSTA_FORMAL_AO_PARECER_DO_PROFESSOR.md`](Publicacoes/RESPOSTA_FORMAL_AO_PARECER_DO_PROFESSOR.md)**  
   *Resolução matemática definitiva dos achados dos pareceres e benchmark canônico de 3-XOR-SAT: prova empírica de que a otimização contínua entra em colapso vítreo ($0.0\%$ reachability) em problemas solvíveis em $P$ via Eliminação Gaussiana em $\text{GF}(2)$, refundando a pesquisa sobre os limites de GNNs e a Overlap Gap Property (OGP).*

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
- `exp_clg03_xorsat_and_ogp.py`: Benchmark canônico com 3-XOR-SAT (Classe P, $\deg=3$) via Eliminação Gaussiana em $\text{GF}(2)$ e prova empírica do colapso vítreo ($0.0\%$ reachability) da relaxação contínua.
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

### 3. Execução do Benchmark CLG-03 (Teste Canônico do 3-XOR-SAT e OGP)
```bash
python Fontes/exp_clg03_xorsat_and_ogp.py
```

### 4. Execução do Benchmark de Escala Extrema (Max-Cut $N=10.000$)
```bash
python Fontes/fase3_op3_extreme_scale.py
```

---

## 📄 Licença e Direitos Autorais

Todos os direitos reservados a **Thiago Carvalho (2026)**.  
O uso, redistribuição, cópia ou engenharia reversa sem autorização expressa é estritamente proibido.  
Para mais informações, consulte o arquivo [LICENSE](LICENSE).


---

## 📄 Para "leigo entender":

Artigo 1: Paper_1_M6_Minimal_Obstruction.pdf
Artigo 2: Paper_2_Geometry_Continuous_3SAT_Relaxations
Artigo 3: Paper_3_Random_Horn_Complexity_Firewall


Para entender esses três artigos de forma intuitiva, imagine o seguinte cenário geral:

Você tem um grande quebra-cabeça de lógica pura (o famoso problema **3-SAT**), composto por milhares de interruptores que só podem estar **ligados (Verdadeiro)** ou **desligados (Falso)**, e uma lista de regras que precisam ser satisfeitas ao mesmo tempo.

Como testar todas as combinações de interruptores uma a uma é impraticável, muitos cientistas tentam transformar esse quebra-cabeça discreto numa **paisagem montanhosa contínua** (onde os interruptores viram botões giratórios que deslizam suavemente entre $-1$ e $+1$). A ideia é soltar uma bolinha no topo dessa montanha e deixar a gravidade (o método de gradiente) guiá-la para o vale mais fundo, que corresponderia à solução do quebra-cabeça.

Os três artigos investigam **quando, como e por que essa bolinha fica presa no caminho**.

---

### Artigo 1: O Tamanho Mínimo de uma Armadilha

*(Minimal Positive-Measure Obstructions in Projected Multilinear 3-SAT Dynamics)*

Este artigo responde a uma pergunta fundamental: **qual é a menor estrutura de regras lógicas interligadas capaz de criar um "buraco" onde a bolinha fica presa com certeza e não consegue sair?**

* **A barreira dos 5:** O autor prova matematicamente que, em redes lógicas lineares sem ciclos (árvores), qualquer conjunto com até 5 regras é incapaz de prender a bolinha em uma região real de volume positivo. Nesses casos menores, o relevo força sempre uma ponta solta que escorrega a bolinha em direção à saída ou para a borda.


* **A armadilha mínima (M6):** O trabalho descobre que a menor armadilha possível exige exatamente **6 regras interligadas** num desenho específico de 13 variáveis chamado $M6$. Nesse formato, cria-se um vale plano falso onde a bolinha para, e, ao tentar arredondar a posição da bolinha para "ligado" ou "desligado", pelo menos uma regra é violada.


* **Presença no mundo real:** O artigo demonstra que essa armadilha de 6 regras não é uma raridade teórica; ela surge com frequência previsível em fórmulas aleatórias grandes, provando que o método da bolinha sempre vai errar uma fração das vezes em problemas reais esparsos.



---

### Artigo 2: O Formato da Montanha Muda Tudo

*(Geometry of Continuous 3-SAT Relaxations: Hinge Plateaus, Harmonic Multilinear Landscapes, and Softplus Convexity)*

Este artigo mostra que **a maneira matemática como você desenha a montanha altera completamente o relevo**, mesmo que no final todos os topos e vales de interruptores ligados/desligados representem exatamente o mesmo quebra-cabeça. O autor compara três tipos de relevo:

* **O Relevo Hinge (Quadrático):** Cria um **platô central gigantesco e perfeitamente plano**. Quando a bolinha entra nessa região central neutra (onde os interruptores estão no meio-termo), a inclinação é zero absoluto. A bolinha simplesmente estagna sem saber para onde ir, resultando em respostas indecisas.


* **O Relevo Multilinear:** Funciona como uma superfície cheia de curvas no estilo "sela de cavalo" ou batata frita *Pringles* (uma superfície harmônica). Por definição geométrica, esse relevo não tem buracos ou poços no meio do terreno; a bolinha nunca fica presa no interior, mas pode ficar retida nas quinas e paredes da caixa.


* **O Relevo Softplus:** Uma tentativa de arredondar o terreno para que ele se torne uma "tigela" com um único fundo (convexo). O artigo revela o preço dessa escolha: para a tigela ser fiel às regras lógicas, as encostas tornam-se paredes verticais e o fundo fica tão plano que os computadores perdem a precisão numérica (acontece o chamado *underflow*, em que os números viram zero na memória da máquina).



---

### Artigo 3: Cadeias de Causa e Efeito e o "Alarme Falso" da Complexidade

*(Random and Structured Continuous SAT Dynamics: LP-Volume Bounds, Horn Chains, Subcritical Hinge Residuals, and a Complexity Firewall)*

Este terceiro artigo investiga problemas com encadeamento lógico (como "se A, então B; se B, então C") e faz um alerta essencial para a ciência da computação:

* **Cadeias lógicas de Horn:** O artigo estuda o que acontece em correntes de causa e efeito. Ele mostra que a bolinha move as variáveis em bloco, como uma média que se equilibra. Mas basta introduzir uma única certeza factual no início da cadeia ("A é verdadeiro com certeza") para todo o platô desaparecer e a bolinha correr direto para a resposta correta.


* **Regras isoladas falham sozinhas:** O autor calcula que, no modelo Hinge, mesmo uma regra simples e totalmente isolada do resto do quebra-cabeça tem uma probabilidade exata de $3/32$ (cerca de $9{,}4\%$) de fazer a bolinha parar num ponto que resulta em erro.


* **O "Firewall" (O Alarme Falso):** É a mensagem epistemológica mais importante do trabalho. Muitas vezes, ao ver uma bolinha rolando ficar presa num labirinto montanhoso hipercomplexo, pesquisadores concluem precipitadamente que o problema original é intrinsecamente "impossível" ou insolúvel rapidamente para computadores ($P \neq NP$). O artigo usa o problema **3-XOR-SAT** para desmentir isso: o relevo contínuo dele é um pesadelo intransponível para a bolinha, mas qualquer computador de bolso resolve o mesmo problema em milissegundos usando eliminação simples de matrizes (álgebra linear de colégio). O fato de a bolinha se perder diz respeito apenas às limitações do método contínuo, e não à verdadeira dificuldade do problema lógico.



---

### Resumo em Uma Frase
O **Artigo 2** mostra como diferentes fórmulas criam paisagens montanhosas completamente distintas; o **Artigo 1** encontra o menor buraco possível nessas paisagens que consegue capturar o algoritmo; e o **Artigo 3** demonstra como regras em cadeia se comportam e adverte que a bolinha ficar presa não significa que o problema seja computacionalmente impossível de resolver.



