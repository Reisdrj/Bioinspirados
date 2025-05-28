from typing import Final
from utils.EHO import EHO
from utils.utils import get_env
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

MIN_INTERVAL: Final[int] = get_env("MIN_INTERVAL", int)
MAX_INTERVAL: Final[int] = get_env("MAX_INTERVAL", int)
POP_SIZE = get_env("POP_SIZE", int)
N_GER = get_env("N_GER", int)
N_PARAMETERS = get_env("N_PARAMETERS", int)
ALPHA = get_env("ALPHA", float)
BETA = get_env("BETA", float)
N_CLAN = get_env("N_CLAN", int)
SEED = get_env("SEED", int)

ag = EHO(POP_SIZE, MIN_INTERVAL, MAX_INTERVAL, N_GER, N_PARAMETERS, ALPHA, BETA, N_CLAN, SEED)
ag.solve()
ag.get_best_individual()