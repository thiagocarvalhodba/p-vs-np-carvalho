# Carta de Resposta Técnica e Reposicionamento Científico do Programa de Pesquisa

**Destinatário:** Ilustre Professor e Comitê de Avaliação  
**Autor:** Thiago Carvalho  
**Data:** 10 de Setembro de 2026  
**Ambiente & Repositório:** `C:\MathDoCarvalho\P_NP` | [GitHub Repository](https://github.com/thiagocarvalhodba/p-vs-np-carvalho)  
**Assunto:** Resposta ao Parecer 08: Execução dos Quatro Controles Mandatórios (Escala, Matriz 3x3, Condicionamento $\kappa_2$ e Diferenças Pareadas) e Consolidação da Tese CLG-R

---

## 1. Alinhamento Formal e Correções Conceituais

Acolhemos integralmente todas as orientações do Parecer 08:
1. **Teorema Posto-Nulidade no 3-XOR-SAT:** Substituímos a menção a Rouché-Capelli pela formulação limpa: *"Como $A$ tem posto completo $N$ sobre $\mathbb{F}_2$, o Teorema Posto-Nulidade implica $\dim(\ker(A)) = 0$. Como a instância possui uma solução plantada $s^*$, o sistema afim $Ax = b$ possui exatamente uma única solução $|S(I)| = 1$."*
2. **Precisão na Definição de Overlap:** Substituímos "completamente ortogonal" pela linguagem exata de física estatística: *"com overlap linear aproximadamente nulo com a solução única ($q(s, s^*) \approx 0.0$)"*.
3. **Platôs do Softplus:** Retificamos a redação: *"Softplus substitui o platô exatamente plano do hinge por uma transição suave, evitando o gradiente identicamente nulo no interior da região satisfeita."*
4. **Condicionamento Espectral Rigoroso para Hessianas Indefinidas:** Definido formalmente como:
   $$\kappa_2(H) = \frac{\sigma_{\max}(H)}{\sigma_{\min}(H)} = \frac{\max_i |\lambda_i(H)|}{\max(\min_i |\lambda_i(H)|, 10^{-5})}$$
5. **Conjectura CLG-R com Funcionais Limitados:** Reformulada para funcionais normalizados $\mathcal{Q} \in [0, 1]$ (ex.: $Q_H = 1 - d_H \in [0, 1]$ ou $Q_S = 1 - E_{\text{disc}}/M \in [0, 1]$).

---

## 2. Resultados da Execução dos Quatro Controles Mandatórios (CLG-04 Fase II)

Executamos o protocolo experimental controlado (`Fontes/exp_clg04_phase2_factorial.py`) em escala $N=60$ com 450 trajetórias estritamente pareadas:
- **Controle 1 (Normalização de Escala de Gradiente):** Potenciais normalizados por $c_\Phi = \mathbb{E}[\|\nabla \Phi\|]$ ($c_{\text{multi}} = 5.26, c_{\text{quad}} = 5.93, c_{\text{soft}} = 8.65$).
- **Controle 2 (Matriz Fatorial 3x3):** 3 Representações $\times$ 3 Dinâmicas (GD puro, Langevin, Adam).

### Matriz Fatorial 3x3 Consolidada (Random-3-SAT, $N=60$ com Potenciais Normalizados):

| Representação | Dinâmica | Alcançabilidade $R_{\text{dyn}}$ | Distância de Hamming $d_H$ (Média $\pm$ SEM) | Overlap $q$ | Violações Discretas $E_{\text{disc}}$ | Condicionamento $\kappa_2$ (Mediana) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Multilinear** | GD Puro | 0.0% | 0.431 $\pm$ 0.007 | +0.139 | 20.4 cl. | 182.7 |
| Multilinear | Langevin | 0.0% | 0.432 $\pm$ 0.010 | +0.136 | 19.7 cl. | 141.1 |
| Multilinear | Adam | 0.0% | 0.418 $\pm$ 0.008 | +0.164 | 18.6 cl. | 176.5 |
| **Quadrática Hinge** | GD Puro | 0.0% | 0.472 $\pm$ 0.012 | +0.055 | 30.1 cl. | **88.815** (Patológico) |
| Quadrática Hinge | Langevin | 0.0% | 0.475 $\pm$ 0.005 | +0.049 | 29.5 cl. | **88.141** (Patológico) |
| Quadrática Hinge | Adam | 0.0% | 0.440 $\pm$ 0.013 | +0.119 | 18.4 cl. | **81.463** (Patológico) |
| **Softplus** | GD Puro | 0.0% | 0.455 $\pm$ 0.012 | +0.091 | 25.5 cl. | **25.5** (Estável) |
| Softplus | Langevin | 0.0% | 0.460 $\pm$ 0.006 | +0.080 | 24.6 cl. | **24.2** (Estável) |
| Softplus | Adam | 0.0% | 0.452 $\pm$ 0.010 | +0.096 | 25.3 cl. | **47.1** (Estável) |

---

## 3. Diferenças Pareadas por Instância Individual ($\Delta_i$)

Para afastar qualquer pseudorreplicamento amostral, reportamos as 5 instâncias independentes em GD Puro:
- Instância 1: $d_H(\text{Soft}) = 0.482 \mid d_H(\text{Multi}) = 0.450 \mid d_H(\text{Quad}) = 0.488 \implies \Delta(\text{Quad} - \text{Soft}) = +0.007$
- Instância 2: $d_H(\text{Soft}) = 0.418 \mid d_H(\text{Multi}) = 0.423 \mid d_H(\text{Quad}) = 0.432 \implies \Delta(\text{Quad} - \text{Soft}) = +0.013$
- Instância 3: $d_H(\text{Soft}) = 0.445 \mid d_H(\text{Multi}) = 0.428 \mid d_H(\text{Quad}) = 0.475 \implies \Delta(\text{Quad} - \text{Soft}) = +0.030$
- Instância 4: $d_H(\text{Soft}) = 0.448 \mid d_H(\text{Multi}) = 0.410 \mid d_H(\text{Quad}) = 0.465 \implies \Delta(\text{Quad} - \text{Soft}) = +0.017$
- Instância 5: $d_H(\text{Soft}) = 0.480 \mid d_H(\text{Multi}) = 0.442 \mid d_H(\text{Quad}) = 0.502 \implies \Delta(\text{Quad} - \text{Soft}) = +0.022$

Em **100% das 5 instâncias**, a relaxação Quadrática Hinge produz atratores estagnados mais distantes da solução que o Softplus ($\Delta_i > 0$), confirmando que a patologia de condicionamento da Quadrática ($\kappa_2 > 80.000$) degrada a qualidade da aproximação de forma sistemática.

---

## 4. A Tese Central Consolidada do Artigo

> ### *"A equivalência booleana não determina a acessibilidade algorítmica de uma relaxação contínua: representações equivalentes podem induzir geometrias numéricas e interações representação–dinâmica distintas, produzindo diferentes qualidades de solução sob a mesma classe de algoritmo local."*

Respeitosamente,

**Thiago Carvalho**  
Pesquisador Principal  
Vitória, ES, 2026
