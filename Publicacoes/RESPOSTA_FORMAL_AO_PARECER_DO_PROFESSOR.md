# Carta de Resposta Técnica e Reposicionamento Científico do Programa de Pesquisa

**Destinatário:** Ilustre Professor e Comitê de Avaliação  
**Autor:** Thiago Carvalho  
**Data:** 10 de Setembro de 2026  
**Ambiente & Repositório:** `C:\MathDoCarvalho\P_NP` | [GitHub Repository](https://github.com/thiagocarvalhodba/p-vs-np-carvalho)  
**Assunto:** Resposta Detalhada ao Parecer 07, Estatística Hierárquica, Desacoplamento CLG-04A/B, Controle de Unicidade em 3-XOR-SAT, Diagnóstico de Condicionamento (CLG-04C) e Transição para CLG-04 Fase II

---

## 1. Considerações Iniciais e Acolhimento das Seis Objeções do Parecer 07

Prezado Professor,

Sua sétima leitura crítica (`AnaliseReportadaPeloProfessor07`) estabelece o padrão mais elevado de rigor experimental e epistemológico. Reconhecemos integralmente que a frase "blindados contra qualquer objeção editorial" foi prematura. Acolhemos todas as suas seis objeções centrais e implementamos imediatamente os protocolos analíticos e experimentais necessários para superá-las.

As ações tomadas foram:
1. **Estatística Hierárquica:** Desagregamos formalmente a análise entre o nível da trajetória ($R_{\text{traj}}$) e o nível da instância ($R_{\text{inst}} = \text{Média} \pm \text{SEM}$ e dispersão inter-instâncias), eliminando a vulnerabilidade de pseudorreplicamento amostral.
2. **Separação de Protocolos (CLG-04A vs. CLG-04B):** Estruturamos o programa em **CLG-04A** (dinâmicas de 1ª ordem puras: GD determinístico e Langevin estocástico com passo fixo) e **CLG-04B** (dinâmica adaptativa com re-escalonamento de momentos: Adam), garantindo rastreabilidade experimental absoluta.
3. **O Resultado Central Realçado:** Colocamos no centro da teoria o fato de que a representação contínua altera dramaticamente a qualidade da solução aproximada e a distância de Hamming ao ótimo ($d_H$) mesmo quando todas as taxas de sucesso colapsam para zero ($R_{\text{dyn}} = 0$).
4. **Controle de Condicionamento (CLG-04C):** Medimos empiricamente $\|\nabla \Phi\|$, $\lambda_{\min}(H)$, $\lambda_{\max}(H)$ e o número de condicionamento $\kappa(H)$, explicando analiticamente por que a Quadrática sofre de colapso numérico ($\kappa > 360.000$) enquanto Softplus mantém estabilidade suave ($\kappa \approx 8.8$).
5. **Correção de Convexidade do Softplus:** Retificamos a formulação para indicar convexidade restrita às variáveis ativas de cada cláusula, sem alegações infundadas de estrita convexidade global em $\mathbb{R}^N$.
6. **Controle Estrito de Unicidade no 3-XOR-SAT:** Comprovamos analítica e computacionalmente que $\text{rank}_{\mathbb{F}_2}(A) = N$ ($|S| = 1$), legitimando a distância $d_H(s_{\text{final}}, s^*)$ como a distância exata ao espaço global de soluções.
7. **Precisão de Vocabulário:** Substituímos "completamente ortogonal" pela formulação precisa de física estatística: **overlap aproximadamente nulo** ($q(s, s^*) \approx 0$).
8. **Conjectura CLG-R Generalizada:** Reformulamos a conjectura sobre um funcional geral de qualidade algorítmica $\mathcal{Q}$, e não apenas sobre $\liminf R_{\text{dyn}}$.
9. **Transição Metodológica para Fase II:** Abandonamos o termo "auditoria final" e adotamos **CLG-04 Fase I (Auditoria Pareada Base)** e **CLG-04 Fase II (Representação $\times$ Condicionamento $\times$ Dinâmica)**.

---

## 2. Estatística Hierárquica: Nível Trajetória vs. Nível Instância

Acolhendo sua advertência sobre independência amostral, reprocessamos o conjunto de 1.800 trajetórias em dois níveis hierárquicos:
- **Nível Trajetória ($R_{\text{traj}}$):** Sucessos totais / 75 trajetórias.
- **Nível Instância ($R_{\text{inst}}$):** Média entre as 5 instâncias independentes $\bar{R} = \frac{1}{5}\sum_{i=1}^5 R_i \pm \text{SEM}$ (onde $\text{SEM} = s / \sqrt{5}$).

### Tabela Hierárquica Consolidada:

| Problema | Escala | Dinâmica | Representação | $R_{\text{traj}}$ ($75$ runs) | $R_{\text{inst}}$ (Média $\pm$ SEM) | Distância de Hamming $d_H$ (Média $\pm$ SEM) |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: |
| **Random-3-SAT** | $N=30$ | GD Puro | Multilinear | 13.3% | 13.3% $\pm$ 4.7% | 0.352 $\pm$ 0.030 |
| Random-3-SAT | $N=30$ | GD Puro | Quadrática Hinge | 0.0% | 0.0% $\pm$ 0.0% | 0.473 $\pm$ 0.013 |
| Random-3-SAT | $N=30$ | GD Puro | Softplus Log-Sum-Exp | 9.3% | 9.3% $\pm$ 4.0% | 0.322 $\pm$ 0.033 |
| Random-3-SAT | $N=30$ | Langevin | Multilinear | 16.0% | 16.0% $\pm$ 5.8% | 0.352 $\pm$ 0.025 |
| Random-3-SAT | $N=30$ | Langevin | Quadrática Hinge | 0.0% | 0.0% $\pm$ 0.0% | 0.465 $\pm$ 0.016 |
| Random-3-SAT | $N=30$ | Langevin | Softplus Log-Sum-Exp | 16.0% | 16.0% $\pm$ 6.9% | 0.322 $\pm$ 0.036 |
| **Random-3-SAT** | $N=60$ | GD Puro | Multilinear | 0.0% | 0.0% $\pm$ 0.0% | 0.327 $\pm$ 0.016 |
| Random-3-SAT | $N=60$ | GD Puro | Quadrática Hinge | 0.0% | 0.0% $\pm$ 0.0% | 0.476 $\pm$ 0.008 |
| Random-3-SAT | $N=60$ | GD Puro | Softplus Log-Sum-Exp | 0.0% | 0.0% $\pm$ 0.0% | 0.284 $\pm$ 0.022 |
| Random-3-SAT | $N=60$ | Langevin | Multilinear | 0.0% | 0.0% $\pm$ 0.0% | 0.326 $\pm$ 0.015 |
| Random-3-SAT | $N=60$ | Langevin | Quadrática Hinge | 0.0% | 0.0% $\pm$ 0.0% | 0.473 $\pm$ 0.005 |
| Random-3-SAT | $N=60$ | Langevin | Softplus Log-Sum-Exp | 0.0% | 0.0% $\pm$ 0.0% | 0.292 $\pm$ 0.020 |
| **3-XOR-SAT** | $N=30, 60$ | GD / Lang | Todas as 3 | 0.0% | 0.0% $\pm$ 0.0% | 0.490 a 0.508 $\pm$ 0.012 |

---

## 3. Rastreabilidade Experimental: CLG-04A vs. CLG-04B

A separação dos protocolos resolve a inconsistência apontada:
- **CLG-04A (Baseline de Primeira Ordem):** Gradient Descent determinístico e Langevin estocástico com passo fixo ($\eta = 0.02$, $T = 200$ passos). Sob este regime estrito, $N=60$ resulta em $R_{\text{dyn}} = 0.0\%$ em todas as formulações.
- **CLG-04B (Dinâmica Adaptativa de Segunda Ordem):** Otimizador Adam ($\eta = 0.08$, $T = 120$ épocas). Neste regime com momentos normalizados ($\frac{g_t}{\sqrt{v_t}}$), o Softplus atinge **$69.3\%$** de alcançabilidade, contra $9.3\%$ da Multilinear e $4.0\%$ da Quadrática.

Essa diferenciação comprova que a alcançabilidade é uma propriedade da interação $\Phi \times \mathcal{D}$ ($	ext{CLG}_R \times \text{CLG}_A$).

---

## 4. O Resultado Central: Qualidade da Solução sob Colapso de Sucesso

Mesmo quando $R_{\text{dyn}} = 0.0\%$ para todas as representações em $N=60$, a representação contínua governa deterministamente a proximidade métrica ao ótimo global:
- **Softplus Log-Sum-Exp:** $d_H = 0.284 \pm 0.022$ (Overlap $q = +0.432$, $4.6$ cláusulas violadas)
- **Multilinear Cúbica:** $d_H = 0.327 \pm 0.016$ (Overlap $q = +0.346$, $4.5$ cláusulas violadas)
- **Quadrática Hinge:** $d_H = 0.476 \pm 0.008$ (Overlap $q = +0.048$, $20.4$ cláusulas violadas)

A distância ao ótimo sob a relaxação Quadrática é quase $70\%$ superior à do Softplus (teste $t$ pareado inter-instâncias: $p < 10^{-4}$). A representação dita a qualidade do atrator assintótico mesmo sob colapso da convergência exata.

---

## 5. Controle de Condicionamento (CLG-04C): Diagnóstico Numérico

O rastreamento temporal das métricas hessianas ao longo de trajetórias pareadas (`Fontes/exp_clg04_conditioning_and_phase2.py`) revelou:
1. **Colapso Numérico da Quadrática Hinge:** Cláusulas satisfeitas geram gradiente zero no interior (platôs com $\|\nabla \Phi\| = 0.0$). Quando ativada, a Hessiana gera autovalores nulos nas direções satisfeitas e positivos nas violadas, explodindo o número de condicionamento para **$\kappa(H) > 360.000$**.
2. **Instabilidade de Gradiente na Multilinear:** Embora $\kappa(H) \approx 1.3$, os produtos cruzados multiplicativos ($x_i x_j x_k$) provocam aceleração caótica de $\|\nabla \Phi\|$ (subindo de $2.74$ para $3.73$).
3. **Estabilidade Numérica do Softplus:** Mantém o gradiente suave e decrescente ($2.54 \to 0.85$) com condicionamento hessiano estável (**$\kappa(H) \approx 8.8$**).

---

## 6. Controle Rigoroso de Unicidade no 3-XOR-SAT

Garantimos via eliminação gaussiana completa sobre $\mathbb{F}_2$ que:
$$\text{rank}_{\mathbb{F}_2}(A) = N \implies |S(I)| = 1 \iff S(I) = \{ s^* \}$$
Pelo Teorema de Rouché-Capelli, o conjunto de soluções é estritamente unitário. A distância de Hamming $d_H(s_{\text{final}}, s^*)$ mede exatamente a distância à única solução existente na fórmula. Como o overlap observado é $q \approx 0.0$ ($d_H \approx 0.50$), comprova-se que a busca contínua estagna em estados sem qualquer correlação informacional com o estado fundamental.

---

## 7. Conjectura CLG-R Generalizada (Funcional de Qualidade Algorítmica $\mathcal{Q}$)

> **Conjectura CLG-R (Não-Invariância da Qualidade Algorítmica sob Representações Booleanas Equivalentes).**  
> *Seja $\mathcal{Q}(I, \Phi, \mathcal{D})$ um funcional de desempenho algorítmico (distância de Hamming assintótica $d_H$, energia residual discreta $E_{\text{disc}}$ ou tempo de escape). Existem famílias infinitas de instâncias booleanas $I_N$ e pares de representações admissíveis $\Phi_N^{(1)} \sim_I \Phi_N^{(2)} \in \mathcal{F}(I_N)$ tais que, para uma classe fixada de dinâmicas $\mathcal{D}$:*
> $$\limsup_{N \to \infty} \left| \mathcal{Q}(I_N, \Phi_N^{(1)}, \mathcal{D}) - \mathcal{Q}(I_N, \Phi_N^{(2)}, \mathcal{D}) \right| > 0$$

---

## 8. A Pergunta Central do Artigo Consagrada

Adotamos em definitivo a formulação epistemológica consagrada por Vossa Senhoria:

> ### *"Qual representação torna determinada classe de algoritmos capaz de explorar a paisagem?"*

Agradeço mais uma vez ao Professor por esta tutoria de altíssimo nível, que transformou uma investigação empírica em um programa de pesquisa teórica rigoroso e publicável.

Respeitosamente,

**Thiago Carvalho**  
Pesquisador Principal  
Vitória, ES, 2026
