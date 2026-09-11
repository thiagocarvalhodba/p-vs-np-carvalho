# PROMPT DE AUDITORIA PROFUNDA PARA O CLAUDE CODE
# Projeto: Framework CLG-R (Computational Landscape Geometry & Representation)
# Diretório do Repositório: C:\MathDoCarvalho\P_NP
# Branch: master

Você é um Lead Research Scientist & Senior Principal Engineer, especialista de classe mundial em Teoria da Complexidade Computacional (STOC/FOCS/JACM), Topologia Diferencial e Teoria de Morse (Annals of Mathematics), Física Estatística de Vidros de Spin (Franz-Parisi / TAP / Spin Glasses) e Otimização Combinatória Contínua.

Sua missão é realizar uma auditoria completa, crítica, impiedosa e construtiva de todo o código-fonte, manuscritos matemáticos e pipelines do repositório em `C:\MathDoCarvalho\P_NP` antes da submissão final ao avaliador externo e ao arXiv.

Execute as seguintes etapas sequenciais dentro do terminal e do repositório:

---

## ETAPA 1: Inspeção dos Arquivos do Repositório

Inspecione profundamente os seguintes arquivos centrais:

1. **Código Matemático Central:**
   - `Fontes/clg_framework.py`: Implementação das três representações canônicas (Hinge Quadrático $\Phi_{\text{quad}}$, Multilinear $\Phi_{\text{mult}}$, Softplus $\Phi_{\text{soft}}$), gradientes analíticos, matriz de incidência $V$, Hessianas $\nabla^2 \Phi = V^T W V$, fluxo gradiente projetado no hipercubo $[-1, 1]^N$ e simulação dinâmica de bacias de atração.
   - `Fontes/generate_arxiv_tex.py`: Gerador automatizado do artigo diamante em LaTeX (`Publicacoes/CLG_FOUNDATIONS_ARXIV.tex`).
   - `Fontes/generate_resposta11_deliverables.py`: Gerador dos entregáveis técnicos em Word (DOCX), Markdown e TXT com conversão Unicode rigorosa.
   - Scripts experimentais e de escalabilidade: `Fontes/fase3_op1_max_sat.py`, `Fontes/fase3_op2_hybrid_gnn.py`, `Fontes/fase3_op3_extreme_scale.py`, `Fontes/trilha1_scaled_gat.py`, `Fontes/trilha2_goemans_williamson_benchmark.py`.

2. **Manuscritos Teóricos e Demonstrações:**
   - `Publicacoes/ESTUDO_ANALITICO_DO_CONJUNTO_CRITICO.md`: Monografia analítica Versão 3.0 contendo as provas dos Teoremas 1 a 6, Teoremas Construtivos 7A e 7B, e a Conjectura Central CLG-R.
   - `Publicacoes/RespostaAoProfessor_Analise11.md`: Resposta formal detalhada ao Parecer nº 11 do avaliador externo.
   - `Publicacoes/CLG_FOUNDATIONS_ARXIV.tex`: Manuscrito final para submissão oficial ao arXiv.
   - `Publicacoes/CLG_FOUNDATIONS.md`: Monografia mestre teórico-experimental de 80 páginas.
   - `Publicacoes/clg_references.bib`: Base de dados bibliográfica atualizada.

---

## ETAPA 2: Questões Técnicas Críticas para sua Auditoria

Responda com profundidade matemática e rigor de engenharia:

### 1. Auditoria Matemática dos Teoremas (Annals of Mathematics / STOC criteria):
- **Teorema 1 (Caixa Fracionária Central e Folga LP):** A prova de que $g_c(x) < 0$ para todo $x \in \mathcal{U}_N = (-1/3, 1/3)^N$ decorre da folga interior canônica de $0.5$ da relaxação LP em $x=0$ ($y_i = 1/2 \implies \sum z_j = 1.5 \ge 1.0$). A quantificação de $\text{Vol}(Z) \ge (2/3)^N$ e $\text{Vol}(\mathcal{C}_{\text{spur}}) \ge (1/3)^N > 0$ está matematicamente blindada?
- **Teorema 2 (Walsh-Fourier e Medida Nula):** A fundamentação de (H3') via identidade de Parseval $\sum_{S \ne \emptyset} \widehat{\Phi}(S)^2 = \text{Var}(E_{\text{disc}}) > 0$ e o Lema de Okamoto / conjuntos semialgébricos para $\mu(\mathcal{C}_0) = 0$ fecham categoricamente a não-degenerescência?
- **Teorema 3 (Harmonicidade e Milnor):** A aplicação do Princípio do Mínimo Forte ($\Delta \Phi_{\text{mult}} \equiv 0$) e do Lema de Seleção de Curvas de Milnor (1968) para pontos degenerados ($\forall \varepsilon > 0, \exists y: \Phi(y) < \Phi(x^*)$) é irrefutável?
- **Teorema 4A e Corolário 4B (Vértices e LaSalle):** A indução em faces $d \ge 2$ com $\Delta_{\mathcal{F}} \Phi \equiv 0$ e arestas $d=1$ afins ($b_i \ne 0$ sob H4 de Não-Degenerescência de Fronteira) prova que todo mínimo local é um vértice $\{-1, +1\}^N$? A dedução de estabilidade assintótica via função de Lyapunov estrita $V(x) = \Phi(x)$ e Princípio de Invariância de LaSalle possui qualquer brecha?
- **Teorema 5 (Hessiana Softplus e Condicionamento):** A fatoração matricial $\nabla^2 \Phi_{\text{soft}} = V^T W(x) V$ e as cotas $\kappa(\nabla^2 \Phi) \le \kappa(W) \cdot \kappa(V^T V)$ estão corretas?
- **Teorema 6 (Lipschitz do Gradiente e Regimes IEEE 754):** As cotas sanduíche $\frac{3}{16}\beta \le L_\beta \le \frac{3 d_{\max}}{16}\beta$ e os limiares de underflow em FP32 ($\beta \approx 175/207$) e FP64 ($\beta \approx 1417/1489$) estão corretos?
- **Teoremas 7A e 7B (Dinâmica de Bacia e Contração Centrípeta Universal):**
  - No Teorema 7A, para a família simétrica $F_N$ com $M = \binom{N}{3}$ cláusulas negativas, a solução analítica da EDO linear $\dot{u} = -H_N u$ com $H_N \succ 0$ prova formalmente que $A_N = (1/3, 1)^N \subseteq \mathcal{B}_{\text{spur}} \implies \mathcal{M}_{\text{spur}} \ge (1/3)^N > 0$?
  - No Teorema 7B, a identidade $\langle -\nabla \Phi_{\text{quad}}(x), x \rangle = -\sum [2 g_c(x)^2 + g_c(x)] < 0$ prova que $\|x(t)\|_2^2$ é Lyapunov estrito e que $\mathcal{M}_{\text{spur}} \equiv 1$ (100%) para qualquer fórmula UNSAT? A incompatibilidade com o cone normal exterior na fronteira $\langle \nu, x^* \rangle \ge 0$ elimina equilíbrios espúrios com $\Phi > 0$ no bordo?
- **Conjectura Central CLG-R:** O roadmap em 3 etapas (McKean-Vlasov, Azuma-Hoeffding, Eyring-Kramers) está bem estruturado para investigar a separação em ensembles aleatórios acima de $\alpha_d \approx 3.86$?

### 2. Confronto com a Literatura de Vidros de Spin e Física Estatística:
- Como o framework CLG-R se articula com o **Potencial de Franz-Parisi (1995)**, as **Equações TAP**, os modelos $p$-spin esféricos e o threshold de *aging*?
- Como o trabalho dialoga com **Folena & Zamponi (2020)** e **Behrens, Cammarota & Ros (2021)** sobre dinâmicas de gradiente em paisagens rugosas?
- Como o CLG-R se distingue fundamentalmente da **Overlap Gap Property (OGP)** de Gamarnik & Sudan?
- O conceito de **"efeito causal da representação"** (fixando a mesma instância combinatória $F$ e variando $\Phi_{\text{quad}}$ vs $\Phi_{\text{mult}}$ vs $\Phi_{\text{soft}}$ sob a mesma dinâmica) constitui uma contribuição metodológica genuína?

### 3. Auditoria de Código Python e Engenharia de Software Científico:
- `clg_framework.py`: Os gradientes e Hessianas analíticas coincidem numericamente com aproximações por diferenças finitas com erro $< 10^{-6}$?
- A projeção tangencial no hipercubo $\Pi_{[-1, 1]^N}$ está matematicamente correta nos vértices e arestas?
- O cálculo do volume de bacia via integração de Monte Carlo possui controle de erro estatístico e sementes determinísticas?
- Quais rotinas podem ser aceleradas via NumPy vetorizado, PyTorch ou Numba?
- Crie ou recomende testes automatizados com `pytest` para verificar os Teoremas 1 a 7B numericamente.

### 4. Firewall contra Overclaiming em P vs NP:
- A utilização de **3-XOR-SAT** (em P via eliminação Gaussiana sobre $\mathbb{F}_2$, mas com reachability contínua de $0.0\%$) como separador canônico entre complexidade combinatória e geometria contínua está matematicamente sólida? Há qualquer vestígio de alegação temerária sobre P vs NP que deva ser expurgado?

---

## ETAPA 3: Entregáveis Esperados no seu Relatório de Auditoria

Produza um relatório formal estruturado com:

1. **Sumário Executivo e Veredito Geral (com nota de 0 a 10 e maturidade para publicação internacional).**
2. **Auditoria Linha por Linha dos Teoremas 1 a 7B e da Conjectura Central.**
3. **Análise de Código e Verificação Numérica (apontando eventuais bugs ou imprecisões numéricas).**
4. **Tabela de Confronto com a Literatura Clássica e de Vidros de Spin.**
5. **Código de Testes Automatizados (`tests/test_clg_theorems.py`) em pytest para verificar os teoremas.**
6. **Recomendações Práticas e Roadmap para a Conjectura Central.**

Seja rigoroso, detalhista, profundo e construtivo. Não hesite em apontar fragilidades reais se as encontrar.
