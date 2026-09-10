# Carvalho

Repositório central de pesquisas, desenvolvimentos e publicações científicas de Thiago Carvalho.

> [!IMPORTANT]
> ### 🛡️ AVISO DE PROPRIEDADE INTELECTUAL E DIREITOS AUTORAIS
> **Copyright © 2026 Thiago Carvalho. Todos os direitos reservados.**
> 
> Todo o conteúdo intelectual, científico, matemático e computacional contido neste repositório — incluindo formulações analíticas, provas de teoremas, arquiteturas de Redes Neurais em Grafos (GNN), pesos pré-treinados (`.pth`), códigos-fonte, artigos científicos e apresentações — é de **propriedade intelectual exclusiva de Thiago Carvalho**.
> 
> - ❌ **Proibida a reprodução ou cópia:** É estritamente vedada a cópia, reprodução, redistribuição, modificação, engenharia reversa, sublicenciamento ou comercialização, total ou parcial, sem autorização prévia, expressa e formal por escrito do autor.
> - ❌ **Proibido treinamento de IA de terceiros:** Não é permitida a incorporação destes ativos para o treinamento ou ajuste fino de modelos de Inteligência Artificial sem autorização formal.
> - 📖 **Licença de Leitura Pública:** O acesso público constitui tão somente licença de leitura e apreciação científica pessoal por pares acadêmicos e pela comunidade científica.
> 
> Consulte os termos legais completos no arquivo [LICENSE](LICENSE).

---

## Projetos e Módulos

### 🧠 [Computação e Matemática (Pesquisa P vs NP)](Computacao_E_Matematica/)
Pesquisa em **Neural Combinatorial Optimization (NCO)** e Meta-Governança de Hiperparâmetros via Grafos para problemas da classe NP-Difícil (Max-Cut, Caixeiro Viajante - TSP e Max-3-SAT).

- 📄 **[Publicações e Apresentações](Computacao_E_Matematica/Publicacoes/)**:
  - **Artigos para Periódicos Internacionais (2026)**:
    - [Paper I (Matemática - SIAM / DAM)](Computacao_E_Matematica/Publicacoes/PAPER_I_MATHEMATICS_MAXCUT_LAPLACIAN_UGC.md): Relaxação laplaciana, análise hessiana e Efeito Hub.
    - [Paper II (Computação - IEEE TPAMI / ACM TOCS)](Computacao_E_Matematica/Publicacoes/PAPER_II_COMPUTER_SCIENCE_EXTREME_SCALE_SPARSE_GNN.md): Escala extrema ($N=10.000$ nós em $0.79\text{s}$) e Parcimônia Espectral (80.01%).
    - [Paper III (Estatística - JMLR / JRSS-B)](Computacao_E_Matematica/Publicacoes/PAPER_III_APPLIED_STATISTICS_TSP_ANNEALING.md): Termodinâmica do TSP e transição de fase com 80% de vitórias sobre recozimento fixo.
    - [Paper IV (Lógica / IA - JACM / AIJ)](Computacao_E_Matematica/Publicacoes/PAPER_IV_COMPUTATIONAL_LOGIC_COOK_LEVIN_MAX3SAT.md): Núcleo de Cook-Levin (Max-3-SAT) com 99.25% de satisfação no limiar crítico.
  - **Apresentação Executiva Marp**:
    - [Slide Deck em PDF Alta Definição (300 DPI)](Computacao_E_Matematica/Publicacoes/apresentacao_p_vs_np_carvalho.pdf)
    - [Slide Deck Interativo em HTML](Computacao_E_Matematica/Publicacoes/apresentacao_p_vs_np_carvalho.html)
- 💻 **[Códigos-Fonte e Modelos](Computacao_E_Matematica/Fontes/)**:
  - Implementações validadas em PyTorch (`fase3_*.py`, `trilha*.py`, `math_*.py`).
  - Modelos pré-treinados serializados (`model_*.pth`).
  - [Guia Técnico Explicativo de Execução](Computacao_E_Matematica/Fontes/README_FONTES.md).
