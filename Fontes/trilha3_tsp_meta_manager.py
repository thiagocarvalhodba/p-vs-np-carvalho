import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import torch
import torch.nn as nn
import numpy as np
import time
import json

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def generate_tsp_instance(n):
    # Coordenadas euclidianas 2D no quadrado unitário [0, 1]^2
    coords = np.random.rand(n, 2)
    # Matriz de distâncias
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    dist_matrix = np.sqrt(np.sum(diff**2, axis=-1))
    return coords, dist_matrix

def compute_tour_length(tour, dist_matrix):
    n = len(tour)
    length = 0.0
    for i in range(n):
        length += dist_matrix[tour[i], tour[(i + 1) % n]]
    return length

# 1. Nearest Neighbor Heuristic (Gulosa)
def nearest_neighbor_tsp(dist_matrix):
    n = dist_matrix.shape[0]
    unvisited = set(range(1, n))
    tour = [0]
    current = 0
    while unvisited:
        next_city = min(unvisited, key=lambda c: dist_matrix[current, c])
        tour.append(next_city)
        unvisited.remove(next_city)
        current = next_city
    return tour, compute_tour_length(tour, dist_matrix)

# 2. 2-Opt Solver com Parâmetros Configuráveis
def solve_tsp_2opt_annealing(dist_matrix, initial_temp, cooling_rate, steps, init_tour=None):
    n = dist_matrix.shape[0]
    if init_tour is None:
        tour = list(np.random.permutation(n))
    else:
        tour = list(init_tour)
        
    best_tour = list(tour)
    best_len = compute_tour_length(tour, dist_matrix)
    current_len = best_len
    temp = initial_temp
    
    for t in range(steps):
        # Seleciona 2 índices aleatórios para troca 2-opt
        i = np.random.randint(0, n - 2)
        j = np.random.randint(i + 2, n if i > 0 else n - 1)
        
        # Variação delta no custo ao inverter o segmento tour[i+1 : j+1]
        c_i, c_i1 = tour[i], tour[i+1]
        c_j, c_j1 = tour[j], tour[(j+1) % n]
        
        delta = (dist_matrix[c_i, c_j] + dist_matrix[c_i1, c_j1]) - (dist_matrix[c_i, c_i1] + dist_matrix[c_j, c_j1])
        
        # Critério de Metropolis com recozimento
        if delta < 0 or np.random.rand() < np.exp(-delta / max(temp, 1e-6)):
            tour[i+1 : j+1] = reversed(tour[i+1 : j+1])
            current_len += delta
            if current_len < best_len:
                best_len = current_len
                best_tour = list(tour)
                
        temp *= cooling_rate
        
    return best_tour, best_len

# 3. MetaGNN Adaptada para Grafos Geométricos TSP
class TSPMetaGNN(nn.Module):
    def __init__(self, in_dim=2, d_model=64):
        super().__init__()
        self.coord_embed = nn.Linear(in_dim, d_model)
        self.edge_mlp = nn.Sequential(
            nn.Linear(d_model * 2 + 1, d_model),
            nn.ReLU(),
            nn.Linear(d_model, d_model)
        )
        self.meta_head = nn.Sequential(
            nn.Linear(d_model, 32),
            nn.ReLU(),
            nn.Linear(32, 3),
            nn.Sigmoid()
        )
        
    def forward(self, coords, dist_matrix):
        coords_t = torch.tensor(coords, dtype=torch.float32, device=device)
        dist_t = torch.tensor(dist_matrix, dtype=torch.float32, device=device).unsqueeze(-1)
        n = coords_t.shape[0]
        
        h = self.coord_embed(coords_t)
        for _ in range(3):
            h_i = h.unsqueeze(1).expand(-1, n, -1)
            h_j = h.unsqueeze(0).expand(n, -1, -1)
            combined = torch.cat([h_i, h_j, dist_t], dim=-1)
            h = h + self.edge_mlp(combined).mean(dim=1)
            
        pooled = h.mean(dim=0)
        return self.meta_head(pooled)

def run_experiment():
    print("==================================================================")
    print(" TRILHA 3: GENERALIZAÇÃO UNIVERSAL PARA O CAIXEIRO VIAJANTE (TSP)")
    print(f" Dispositivo: {device} | Python / PyTorch")
    print("==================================================================")
    
    # 1. Instanciar MetaGNN para TSP
    print("\n[1/3] Treinando MetaGNN para inferência de parâmetros do TSP...")
    model = TSPMetaGNN().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    # Treino rápido com gradiente da política (recompensa = redução no comprimento do tour)
    t_start = time.time()
    for ep in range(1, 21):
        _, D_train = generate_tsp_instance(50)
        coords_train, _ = generate_tsp_instance(50)
        strat = model(coords_train, D_train)
        
        # Parâmetros governados
        init_t = 0.1 + strat[0].item() * 0.9
        cooling = 0.95 + strat[1].item() * 0.049
        steps = int(200 + strat[2].item() * 400)
        
        # Tour base vs tour IA
        _, len_base = solve_tsp_2opt_annealing(D_train, initial_temp=0.5, cooling_rate=0.98, steps=300)
        _, len_ia   = solve_tsp_2opt_annealing(D_train, initial_temp=init_t, cooling_rate=cooling, steps=steps)
        
        # Recompensa positiva se o comprimento diminuiu (ganho = len_base - len_ia)
        reward = (len_base - len_ia) / 50.0
        loss = -reward * torch.sum(torch.log(strat + 1e-6)) + 0.05 * torch.mean(strat**2)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
    print(f"Treinamento concluído em {time.time() - t_start:.1f}s.")
    torch.save(model.state_dict(), "model_tsp_meta_manager.pth")
    print("Modelo salvo em model_tsp_meta_manager.pth")
    
    # 2. Bateria de testes comparativos
    test_scales = [30, 60, 100]
    results = {}
    print("\n[2/3] Executando benchmark comparativo de rotas (5 instâncias por escala)...")
    
    for n_cities in test_scales:
        label = f"N={n_cities} cidades"
        print(f"\n--- Escala: {label} ---")
        
        rand_lens = []
        nn_lens = []
        base_lens = []
        ia_lens = []
        gains = []
        strategies = []
        
        for trial in range(5):
            coords, dist_matrix = generate_tsp_instance(n_cities)
            
            # 1. Random Tour
            rand_tour = list(np.random.permutation(n_cities))
            l_rand = compute_tour_length(rand_tour, dist_matrix)
            rand_lens.append(l_rand)
            
            # 2. Nearest Neighbor
            _, l_nn = nearest_neighbor_tsp(dist_matrix)
            nn_lens.append(l_nn)
            
            # 3. Base Simulated Annealing (hiperparâmetros fixos)
            _, l_base = solve_tsp_2opt_annealing(dist_matrix, initial_temp=0.5, cooling_rate=0.98, steps=500)
            base_lens.append(l_base)
            
            # 4. MetaGNN Governed Annealing
            with torch.no_grad():
                strat = model(coords, dist_matrix)
                ia_temp = 0.1 + strat[0].item() * 0.9
                ia_cooling = 0.95 + strat[1].item() * 0.049
                ia_steps = int(200 + strat[2].item() * 600)
                
            _, l_ia = solve_tsp_2opt_annealing(dist_matrix, initial_temp=ia_temp, cooling_rate=ia_cooling, steps=ia_steps)
            ia_lens.append(l_ia)
            
            gain = l_base - l_ia  # positivo = IA encontrou rota mais curta
            gains.append(gain)
            strategies.append({"temp": ia_temp, "cooling": ia_cooling, "steps": ia_steps})
            
            print(f"  Instância {trial+1}: Random={l_rand:.2f} | NearestNeighbor={l_nn:.2f} | Base={l_base:.2f} | MetaGNN={l_ia:.2f} | Ganho={gain:+.2f}")
            
        results[label] = {
            "mean_random_len": float(np.mean(rand_lens)),
            "mean_nn_len": float(np.mean(nn_lens)),
            "mean_base_len": float(np.mean(base_lens)),
            "mean_ia_len": float(np.mean(ia_lens)),
            "mean_gain": float(np.mean(gains)),
            "ia_win_rate_vs_base": float(np.mean([1 if g > 0 else 0 for g in gains])) * 100,
            "ia_improvement_over_random": float((np.mean(rand_lens) - np.mean(ia_lens)) / np.mean(rand_lens)) * 100,
            "mean_predicted_temp": float(np.mean([s["temp"] for s in strategies])),
            "mean_predicted_steps": float(np.mean([s["steps"] for s in strategies]))
        }
        
    print("\n[3/3] Resumo Final da Generalização Universal para TSP:")
    report_lines = [
        "=== RESULTADOS: TRILHA 3 (GENERALIZAÇÃO UNIVERSAL PARA TSP) ===",
        f"Data/Hora: {time.ctime()}\n"
    ]
    for lbl, dat in results.items():
        block = (
            f"Cenário: {lbl}\n"
            f"  - Random Tour:                {dat['mean_random_len']:.2f}\n"
            f"  - Nearest Neighbor (Gulosa):  {dat['mean_nn_len']:.2f}\n"
            f"  - Base Annealing (Fixo):      {dat['mean_base_len']:.2f}\n"
            f"  - MetaGNN Carvalho (IA):      {dat['mean_ia_len']:.2f}\n"
            f"  - Redução Médio de Rota (IA): {dat['mean_gain']:+.2f} unidades\n"
            f"  - Taxa de Vitória IA vs Base: {dat['ia_win_rate_vs_base']:.1f}%\n"
            f"  - Redução vs Rota Aleatória:  {dat['ia_improvement_over_random']:.2f}%\n"
            f"  - Temperatura Média Predita:  {dat['mean_predicted_temp']:.3f} | Passos: {dat['mean_predicted_steps']:.0f}\n"
        )
        print(block)
        report_lines.append(block)
        
    with open("trilha3_tsp_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    with open("trilha3_tsp_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Resultados salvos em trilha3_tsp_report.txt e trilha3_tsp_results.json")

if __name__ == "__main__":
    run_experiment()
