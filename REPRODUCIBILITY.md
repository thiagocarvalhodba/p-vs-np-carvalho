# Guia de Reprodutibilidade Científica — CLG-R v4.0.2

Este documento descreve a sequência canônica e automatizada de comandos para reproduzir integralmente:
1. As figuras teóricas e diagramas topológicos do manuscrito;
2. Os experimentos computacionais pré-registrados no Protocolo V2;
3. As tabelas analíticas e dados estatísticos consolidados;
4. A suíte completa de testes de regressão e integridade.

---

## 1. Pré-Requisitos e Ambiente

- **Sistema Operacional:** Windows 11 / Linux Ubuntu 22.04+ / macOS 14+
- **Python:** 3.14+ (compatível com 3.10+)
- **Instalação das dependências exatas:**
  ```powershell
  python -m pip install -r requirements.lock
  ```

---

## 2. Sequência de Execução Única (One-Liner / Script de Execução Total)

Para reproduzir todos os artefatos, tabelas, figuras e validações a partir do ambiente limpo, execute na raiz do repositório (`C:\MathDoCarvalho\P_NP`):

```powershell
# 1. Executar a suíte de testes de integridade matemática e regressão
python -m pytest tests -v

# 2. Executar o inventário criptográfico de hashes (Fase 0)
python Fontes/inventory_fase0.py

# 3. Gerar os diagramas topológicos e figuras do manuscrito
python Fontes/generate_topological_diagrams.py

# 4. Executar os experimentos congelados do Protocolo V2 (3 sementes + sensibilidade)
python Fontes/run_protocol_v2_clean.py
```

---

## 3. Descrição dos Artefatos Gerados

### 3.1 Figuras Científicas (em `Publicacoes/`)
- `fig_clg_teorema1_caixa_fracionaria.png`: Visualização geométrica da caixa central $\mathcal{U}_N = (-1/3, 1/3)^N$, do hipercubo $[-1, 1]^N$ e da folga fracionária $0.5$ do politopo LP.
- `fig_clg_teorema3_4_harmonic_saddles_vertices.png`: Demonstração da harmonicidade ($\Delta \Phi_{\text{mult}} \equiv 0$), selas de Morse no interior e confinamento de atratores estáveis aos vértices discretos $\{-1, 1\}^N$.
- `fig_clg_teorema5_6_softplus_convexity_bifurcation.png`: Fatoração da Hessiana Softplus $V^T W V \succeq 0$, funil estritamente convexo e underflow exponencial IEEE 754.

### 3.2 Dados Experimentais e Relatórios (em `Fontes/`)
- `exp_protocol_v2_raw_data.json`: Registro JSON de todas as trajetórias individuais, com valores de $\rho$, energia contínua, passos até convergência, sementes e metadados de hardware.
- `relatorio_experimentos_protocolo_v2.txt`: Relatório textual consolidado com intervalos de confiança de 95% via bootstrap por instância e testes pareados de Wilcoxon.

### 3.3 Pacote de Submissão arXiv (em `Publicacoes/`)
- `arxiv_package.zip`: Contém estritamente:
  - `CLG_FOUNDATIONS_ARXIV.tex` (código-fonte LaTeX sincronizado)
  - `CLG_FOUNDATIONS_ARXIV.bbl` (bibliografia pré-compilada padrão arXiv)
  - `clg_references.bib` (base de dados BibTeX)
  - 3 figuras PNG em alta resolução
