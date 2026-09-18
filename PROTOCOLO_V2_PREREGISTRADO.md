# Protocolo Experimental Pré-Registrado V2 (CLG-R v4.0.2)
**Status:** Congelado e Pré-Registrado antes de Reexecução  
**Data de Congelamento:** 18 de Setembro de 2026  
**Repositório Oficial:** `C:\MathDoCarvalho\P_NP`  
**Padrão Metodológico:** Padrão STOC/FOCS e SIAM Journal on Optimization  

---

## 1. Princípios Metodológicos e Justificativa da V2

O Protocolo V1 continha divergências e inconsistências entre código e texto apontadas pela auditoria externa:
1. **Contaminação de Potencial:** Scripts anteriores (`exp_clg04_representation_invariance.py` e `strict_audit.py`) continham uma penalidade quadrática de caixa `0.2 * sum((x^2 - 1)^2)` e o otimizador Adam (`lr=0.08`), o que alterava o fluxo analítico contínuo original.
2. **Pseudo-Replicação Amostral:** 15 reinícios em 5 instâncias eram agrupados como 75 amostras independentes, enviesando intervalos de confiança.
3. **Rotulagem Imprecisa:** Amostras com solução plantada eram chamadas de "Random-3-SAT (NP-C)", confundindo benchmark com problema de decisão estocástico.
4. **Hipótese de Horn Superada:** A alegação de que Horn monótono admitia separação dinâmica por Hirsch foi superada pelo contraexemplo do Parecer 19 e pelo colapso do politopo LP sob fatos unitários.

O **Protocolo V2** estabelece a disciplina estrita de execução:
- **Fluxo puro:** Discretização pura de Euler sem penalidades de caixa e sem momentos (Adam).
- **Hierarquia:** Instância lógica como unidade amostral primária.
- **Transparência:** Nomes exatos para instâncias plantadas vs. aleatórias.
- **Reprodutibilidade:** Três sementes globais independentes e exportação de dados brutos completos.

---

## 2. Desenho Experimental e Famílias de Instâncias

### 2.1 Ensemble 1: Horn Monótono com Fato Unitário vs. DAG Geral ($\mathcal{E}_{\text{Horn}}$)
- **Objetivo:** Avaliar o comportamento dinâmico quando $J_{ij} \le 0$ está presente em cláusulas negativas e testar o efeito do colapso do politopo LP quando fatos unitários são adicionados.
- **Tamanho:** $N = 25$ variáveis, $M = 40$ cláusulas.
- **Instâncias independentes:** $N_{\text{inst}} = 15$.
- **Reinícios aninhados por instância:** $R = 10$.

### 2.2 Ensemble 2: 3-SAT Aleatório Subcrítico ($\mathcal{E}_{\text{sub}}, \alpha < 1/6$)
- **Objetivo:** Investigar a taxa de sucesso e resíduo contínuo abaixo do limiar de percolação de hipergrafos ($\alpha = 0.12 < 0.1667$).
- **Tamanho:** $N = 50$ variáveis, $M = 6$ cláusulas.
- **Instâncias independentes:** $N_{\text{inst}} = 15$.
- **Reinícios por instância:** $R = 10$.

### 2.3 Ensemble 3: 3-SAT Plantado ($\mathcal{E}_{\text{plant}}$ — Benchmark Controlado)
- **Objetivo:** Comparar $\rho_{\text{quad}}$ vs $\rho_{\text{mult}}$ na presença de solução garantida $s^* \in \{-1, +1\}^N$ sob densidades crescentes.
- **Densidades:** $\alpha \in \{3.0, 3.86, 4.26\}$.
- **Tamanho:** $N = 30$ e $N = 50$ variáveis.
- **Instâncias independentes:** $N_{\text{inst}} = 15$ por densidade.
- **Reinícios por instância:** $R = 10$.

### 2.4 Ensemble 4: 3-XOR-SAT ($\mathcal{E}_{\text{XOR}}$ — Controle Epistemológico Negativo)
- **Objetivo:** Confirmar o desacoplamento epistemológico: o problema pertence a $\mathbf{P}$ (resolvível em $\mathcal{O}(N^3)$ via Eliminação Gaussiana), mas exibe colapso vítreo completo sob relaxação contínua ($R_{\text{dyn}} = 0\%$).
- **Tamanho:** $N = 30$ variáveis, densidade de equações $\alpha = 1.0$ (gerando $M = 4 \times 30 = 120$ cláusulas CNF).
- **Instâncias independentes:** $N_{\text{inst}} = 15$.
- **Reinícios por instância:** $R = 10$.

---

## 3. Especificação Numérica do Fluxo Contínuo

### 3.1 Potenciais
1. **Multilinear Harmônico:**
   $$\Phi_{\text{mult}}(x) = \sum_{c=1}^M \prod_{j \in c} \frac{1 - \sigma_j^{(c)} x_j}{2}$$
2. **Quadrático Hinge (LP Penalty):**
   $$\Phi_{\text{quad}}(x) = \sum_{c=1}^M \left[\max\left(0, -\frac{1}{2}(1 + \sigma^{(c)} \cdot x)\right)\right]^2$$
3. **Softplus Convexa:**
   $$\Phi_{\text{soft}}(x) = \frac{1}{\beta}\sum_{c=1}^M \ln\left(1 + \exp\left(-\frac{\beta}{2}(1 + \sigma^{(c)} \cdot x)\right)\right), \quad \beta = 5.0$$

### 3.2 Dinâmica Temporal (Sem Penalidade de Caixa e Sem Adam)
- **Algoritmo:** Euler Projetado Puro no hipercubo $[-1, 1]^N$:
  $$x^{(t+1)} = \text{clip}\left(x^{(t)} - \eta \nabla \Phi(x^{(t)}), -1.0, 1.0\right)$$
- **Passo temporal:** $\eta = 0.01$.
- **Tempo máximo:** $T = 40.0$ ($4000$ passos).
- **Critério de Parada:** $\|\nabla \Phi(x)\|_2 < 10^{-10}$ ou $\|x^{(t+1)} - x^{(t)}\|_\infty < 10^{-8}$.
- **Inicialização:** $x_0 \sim \text{Unif}([-1, 1]^N)$ gerada com sementes fixadas.
- **Pareamento:** Para cada par $(I, r)$ (instância $I$, reinício $r$), exatamente o mesmo vetor $x_0$ é fornecido às três representações.

---

## 4. Métricas e Análise Estatística Hierárquica

### 4.1 Métricas Primárias e Secundárias
1. **Violação Residual Normalizada ($\rho$):**
   $$\rho = \frac{1}{M} E_{\text{disc}}(\text{sign}(x^*))$$
2. **Taxa de Alcance Satisfatível ($R_{\text{dyn}}$):**
   $$\mathbb{I}(E_{\text{disc}}(\text{sign}(x^*)) = 0)$$
3. **Tamanho de Efeito Pré-Registrado ($\Delta \rho$):**
   $$\Delta \rho = \rho_{\text{quad}} - \rho_{\text{mult}}$$

### 4.2 Análise Hierárquica por Instância
1. Para cada instância $i \in \{1, \dots, N_{\text{inst}}\}$, calcula-se a média sobre os $R$ reinícios:
   $$\bar{\rho}_i^{\text{rep}} = \frac{1}{R}\sum_{r=1}^R \rho_{i, r}^{\text{rep}}, \quad \Delta \bar{\rho}_i = \bar{\rho}_i^{\text{quad}} - \bar{\rho}_i^{\text{mult}}$$
2. O intervalo de confiança de 95% para $\Delta \rho$ é obtido via **bootstrap de instâncias** (2.000 reamostragens com reposição do vetor $(\Delta \bar{\rho}_1, \dots, \Delta \bar{\rho}_{N_{\text{inst}}})$).
3. Teste de hipótese não-paramétrico pareado: **Teste dos Postos Sinalizados de Wilcoxon** sobre as instâncias.

---

## 5. Sementes Globais e Sensibilidade

- **Semente Primária:** `20260911`
- **Sementes Secundárias de Validação:** `20260918`, `20260925`
- **Análise de Sensibilidade:** Variação do passo $\eta \in \{0.005, 0.01, 0.02\}$ e horizonte $T \in \{20.0, 40.0, 60.0\}$.

*Protocolo V2 aprovado e congelado em 18 de Setembro de 2026.*
