from typing import Final
from utils.AG import AlgoritmoGenetico
from utils.utils import get_env
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

MIN_INTERVAL: Final[int] = get_env("MIN_INTERVAL", int)
MAX_INTERVAL: Final[int] = get_env("MAX_INTERVAL", int)
POP_SIZE = get_env("POP_SIZE", int)
N_GER = get_env("N_GER", int)
PC = get_env("PC", float)
PM = get_env("PM", float)
ALFA = get_env("ALFA", float)
BETA = get_env("BETA", float)
N_ELITE = get_env("N_ELITE", int)
N_PARAMETERS = get_env("N_PARAMETERS", int)
SEED = get_env("SEED", int)

with open("tests/tests.csv", "a") as file:
    file.write("Taxa_Cruzamento,Elitismo,Mutacao,Cruzamento,Geracoes,Populacao,Best_Fitness")


for mutacao in [0.01, 0.05, 0.1]:
    for tx_cruzamento in [0.6, 0.8, 1]:
        for pop_size in [25, 50, 100]:
            for geracoes in [25, 50, 100]:
                for elitismo in [0, 1]:
                    for cruzamento in [0, 1]:
                        ag = AlgoritmoGenetico(pop_size, tx_cruzamento, mutacao, MIN_INTERVAL, MAX_INTERVAL, ALFA, BETA, geracoes, elitismo, N_PARAMETERS, SEED, cruzamento)
                        genes = ag.tests()

                        cruzamento = "BLX-α" if cruzamento == 0 else "BLX-αβ"

                        elitismo = "False" if elitismo == 0 else "True"

                        with open("tests/tests.csv", "a") as file:
                            for i in genes:
                                file.write(f"\n{tx_cruzamento},{elitismo},{mutacao},{cruzamento},{geracoes},{pop_size},{i.fitness}")
