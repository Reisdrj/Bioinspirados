from typing import Final
from utils.AG import AlgoritmoGenetico
from utils.utils import get_env, load_knapsack_data
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

POP_SIZE = get_env("POP_SIZE", int)
N_GER = get_env("N_GER", int)
PC = get_env("PC", float)
PM = get_env("PM", float)
PV = get_env("PV", float)
N_ELITE = get_env("N_ELITE", int)
SEED = get_env("SEED", int)
WEIGHTS_PATH = get_env("WEIGHTS_PATH", str)
VALUES_PATH = get_env("VALUES_PATH", str)
CAPACITY_PATH = get_env("CAPACITY_PATH", str)

items, capacity = load_knapsack_data(VALUES_PATH, WEIGHTS_PATH, CAPACITY_PATH)

ag = AlgoritmoGenetico(POP_SIZE, PC, PM, PV, N_GER, N_ELITE, SEED, items, capacity)

ag.tests()
ag.get_best_individual()
