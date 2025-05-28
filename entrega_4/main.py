from typing import Final
from utils.AG import AlgoritmoGenetico
from tsp import TSP
from utils.utils import get_env
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

POP_SIZE = get_env("POP_SIZE", int)
N_GER = get_env("N_GER", int)
PC = get_env("PC", float)
PM = get_env("PM", float)
PV = get_env("PV", float)
SEED = get_env("SEED", int)
MATRIX_PATH = get_env("MATRIX_PATH", str)

ag = TSP(POP_SIZE, PC, PM, PV, N_GER, MATRIX_PATH)
ag.tests()
# ag.solve()
