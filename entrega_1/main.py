from typing import Final
from utils.AG import AlgoritmoGenetico
from utils.utils import get_env
from dotenv import load_dotenv


load_dotenv(dotenv_path=".env")

MIN_INTERVAL: Final[int] = get_env("MIN_INTERVAL", int)
MAX_INTERVAL: Final[int] = get_env("MAX_INTERVAL", int)
POP_SIZE = get_env("POP_SIZE", int)
N_GER = get_env("N_GER", int)
N_BITS = get_env("N_BITS", int)
PC = get_env("PC", float)
PM = get_env("PM", float)
PV = get_env("PV", float)
N_ELITE = get_env("N_ELITE", int)

ag = AlgoritmoGenetico(POP_SIZE, PC, PM, PV, MIN_INTERVAL, MAX_INTERVAL, N_BITS, N_GER, N_ELITE)
ag.solve()
ag.get_best_individual()