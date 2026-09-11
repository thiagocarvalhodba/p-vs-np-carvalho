# Protocolo Pré-Registrado de Avaliação Experimental CLG-R
**Versão:** 1.0 (Pré-Registrado)  
**Data:** 11 de Setembro de 2026  
**Status:** Protocolo Congelado (Pre-registered Protocol)  
**Repositório:** C:\MathDoCarvalho\P_NP

---

## 1. Objetivos do Protocolo
Este protocolo estabelece o desenho experimental pré-registrado para a validação empírica das predições do framework **Computational Landscape Geometry and Representation (CLG-R)**, em estrita conformidade com as diretrizes da auditoria independente e padrões dos periódicos *STOC/FOCS*, *SIAM Journal on Optimization* e *Annals of Mathematics*.

O princípio norteador é o **desacoplamento causal da representação**: fixada a mesma fórmula booleana $ e a mesma condição inicial  \sim \text{Unif}([-1, 1]^N)$, avalia-se o comportamento do fluxo contínuo sob representações distintas.

---

## 2. Famílias de Instâncias e Ensembles

### 2.1 Ensemble $\mathcal{E}_{\text{Horn}}$ (Horn Monótono Acíclico — Classe P)
- **Estrutura:** Cadeias acíclicas de implicações {i_1} \land x_{i_2} \to x_{i_3}$ com fatos unitários iniciais.
- **Predição Teórica (Teorema 9):**
  - Sob $\Phi_{\text{mult}}$, o campo é cooperativo de Hirsch $\implies \mathcal{M}_{\text{spur}}(\Phi_{\text{mult}}) = o(1)$ e $\rho_{\text{mult}} = 0$.
  - Sob $\Phi_{\text{quad}}$, o politopo LP aprisiona as trajetórias $\implies \mathcal{M}_{\text{spur}}(\Phi_{\text{quad}}) \ge 1 - o(1)$ e $\rho_{\text{quad}} > 0$.

### 2.2 Ensemble $\mathcal{E}_{\text{plant}}$ (3-SAT Plantado — Benchmark Controlado)
- **Estrutura:** Fórmulas aleatórias geradas a partir de uma solução escondida ^* \in \{-1, +1\}^N$, garantindo satisfatibilidade estrita para qualquer $\alpha = M/N$.
- **Parâmetros:** $\alpha \in \{3.0, 3.5, 3.86, 4.26\}$.
- **Predição Teórica:** Separação estrita de energia residual $\rho_{\text{quad}}(\alpha) > \rho_{\text{mult}}(\alpha)$.

### 2.3 Ensemble $\mathcal{E}_{\text{sub}}$ (3-SAT Aleatório Subcrítico $\alpha < 1/6$)
- **Estrutura:** 3-SAT aleatório com $\alpha < 0.1667$.
- **Predição Teórica (Teorema 10):**
  - Hipergrafo é floresta de componentes-árvore de tamanho $\mathcal{O}(\log N)$.
  - Toda árvore tem zero mínimos espúrios $\implies \rho_{\text{mult}}(\alpha) = 0$ via Lee et al. (2016).
  - O Hinge aprisiona no platô LP com $\mathbb{E}[\mu(Z)] = (5/6)^{\alpha N} > 0 \implies \rho_{\text{quad}}(\alpha) > 0$.

### 2.4 Ensemble $\mathcal{E}_{\text{XOR}}$ (3-XOR-SAT / Paridade — Vidro de Spin em P)
- **Estrutura:** Equações de paridade de 3 variáveis sobre $\mathbb{F}_2$.
- **Complexidade:** Solúvel em $\mathcal{O}(N^3)$ via Gauss (em P).
- **Predição Teórica (Firewall P vs NP):** Colapso vítreo de gradiente em ambas as representações contínuas ({\text{dyn}} = 0.0\%$), demonstrando que dureza contínua não reflete complexidade de Turing.

---

## 3. Representações e Dinâmicas Avaliadas

1. **Quadrática Hinge ($\Phi_{\text{quad}}$):** $\sum_{c=1}^M \max(0, g_c(x))^2$.
2. **Multilinear Harmônica ($\Phi_{\text{mult}}$):** $\sum_{c=1}^M \prod_{j \in c} \frac{1 - \sigma_j^{(c)} x_j}{2}$.
3. **Softplus Convexa ($\Phi_{\text{soft}}$):** $\frac{1}{\beta} \sum_{c=1}^M \ln(1 + e^{\beta g_c(x)})$, com $\beta = 5.0$.
4. **Dinâmica ERT (Ercsey-Ravasz & Toroczkai, 2011):** Sistema determinístico contínuo com variáveis auxiliares  \ge 1$.

### Dinâmica e Parâmetros Numéricos:
- **Fluxo:** Euler projetado puro ^{(t+1)} = \text{clip}(x^{(t)} - \eta \nabla \Phi(x^{(t)}), -1, 1)$.
- **Passo temporal:** $\eta = 0.01$.
- **Tempo máximo:**  = 40.0$ (4000 passos).
- **Sem penalidade de caixa artificial, sem otimizador Adam, sem ruído térmico.**
- **Inicialização:**  \sim \text{Unif}([-1, 1]^N)$.

---

## 4. Métricas e Rigor Estatístico

Para cada execução pareada:
1. **Energia Residual Discreta:** {\text{disc}}(\text{sign}(x(T)))$.
2. **Densidade de Violação Residual:** $\rho = E_{\text{disc}}/M$.
3. **Taxa de Sucesso / Reachability:** $\mathbb{I}(E_{\text{disc}} = 0)$.
4. **Entrada no Politopo LP ($):** $\mathbb{I}(\max_c g_c(x(T)) \le 10^{-6})$.
5. **Estatística Inferencial:**
   - Intervalos de confiança de 95% calculados **por instância** via bootstrap não-paramétrico (2000 reamostragens).
   - Intervalo de Wilson para taxas de sucesso proporcionais.
   - Teste de hipóteses pareado (teste de postos de Wilcoxon) para a diferença $\rho_{\text{quad}} - \rho_{\text{mult}}$.

---

## 5. Critérios de Sucesso Pré-Registrados

A hipótese de separação dinâmica causal de representação do CLG-R é considerada **confirmada** se:
1. Em Horn Monótono: $\rho_{\text{mult}} = 0.000$ em 100% das instâncias, enquanto $\rho_{\text{quad}} > 0$ com  < 0.001$.
2. Em 3-SAT Subcrítico ($\alpha < 1/6$): $\rho_{\text{mult}} = 0.000$, enquanto $\rho_{\text{quad}} > 0$.
3. Em 3-SAT Plantado no limiar crítico: O intervalo de confiança de $\rho_{\text{quad}} - \rho_{\text{mult}}$ exclui zero com 95% de confiança.
4. Em 3-XOR-SAT: O algoritmo contínuo falha em encontrar soluções ({\text{dyn}} = 0.0\%$), confirmando o firewall contra overclaiming em P vs NP.

---
*Protocolo registrado e congelado em 11 de Setembro de 2026.*