from typing import Final
from utils.AG import AlgoritmoGenetico
from utils.utils import get_env, load_knapsack_data
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

# POP_SIZE = get_env("POP_SIZE", int)
# N_GER = get_env("N_GER", int)
# PC = get_env("PC", float)
# PM = get_env("PM", float)
# PV = get_env("PV", float)
# N_ELITE = get_env("N_ELITE", int)
# SEED = get_env("SEED", int)
WEIGHTS_PATH = get_env("WEIGHTS_PATH", str)
VALUES_PATH = get_env("VALUES_PATH", str)
CAPACITY_PATH = get_env("CAPACITY_PATH", str)

items, capacity = load_knapsack_data(VALUES_PATH, WEIGHTS_PATH, CAPACITY_PATH)

# ag = AlgoritmoGenetico(POP_SIZE, PC, PM, PV, N_GER, N_ELITE, SEED, items, capacity)

# ag.solve()
# ag.get_best_individual()

import pandas as pd
import random
from utils.AG import AlgoritmoGenetico
from utils.utils import load_knapsack_data

# — Parâmetros fixos —
pc = 0.8
pm = 0.02
pv = 0.5
n_elite = 2

# — Variações solicitadas —
selections    = ['roulette_rank', 'tournament']
penalty_types = [0, 1]
n_gens        = [100, 200]
pop_sizes     = [200, 100]

# Índices dos arquivos (0 a 8)
file_ids = list(range(1, 9))

for file_id in file_ids:
    # Monte aqui os caminhos para cada arquivo com base em file_id:
    values_path   = f"tests/test_0{file_id}/p0{file_id}_p.txt"
    weights_path  = f"tests/test_0{file_id}/p0{file_id}_w.txt"
    capacity_path = f"tests/test_0{file_id}/p0{file_id}_c.txt"

    # Carrega dados da mochila
    items, capacity = load_knapsack_data(values_path, weights_path, capacity_path)

    # Lista local para este file_id
    results = []

    # Gera 10 testes para cada configuração
    for sel in selections:
        for penalty_type in penalty_types:
            for n_ger in n_gens:
                for pop_size in pop_sizes:
                    for run_id in range(10):
                        seed = run_id
                        ag = AlgoritmoGenetico(
                            pop_size=pop_size,
                            pc=pc, pm=pm, pv=pv,
                            n_ger=n_ger, n_elite=n_elite,
                            seed=seed,
                            items=items,
                            max_capacity=capacity
                        )

                        # Seleção de pais
                        parents = ag.roulette_rank() if sel == 'roulette_rank' else ag.tournament()

                        # Executa o AG
                        ag.pop = parents
                        best_solution = ag.solve()

                        # Avalia com o tipo de penalidade
                        best_value  = ag.get_solution_value(best_solution, type=penalty_type)
                        best_weight = ag.get_solution_weight(best_solution)

                        penalty_str = "inviavel_penalizada" if penalty_type == 0 else "penalidade_severa"

                        results.append({
                            'selection': sel,
                            'penalty': penalty_str,
                            'n_gen': n_ger,
                            'pop_size': pop_size,
                            'run_id': run_id,
                            'best_value': best_value,
                            'best_weight': best_weight
                        })

    # Monta DataFrame e salva CSV específico para este file_id
    df = pd.DataFrame(results)
    out_path = f'results/test_0{file_id}/experiments_results_test.csv'
    df.to_csv(out_path, index=False)
    print(f"Resultados do teste {file_id} salvos em: {out_path}")
