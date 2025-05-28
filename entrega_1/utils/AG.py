from utils import np
from utils.Individuo import Individuo
import copy
import itertools
from sys import float_info

MAX_FLOAT = float_info.max

class AlgoritmoGenetico:

    def __init__(self, pop_size, pc, pm, pv, min_interval, max_interval, n_bits, n_ger, n_elite, n_parameters, seed):
        self.seed = seed
        self.n_bits = n_bits
        self.pc = pc
        self.pm = pm
        self.pv = pv
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.n_ger = n_ger
        self.pop_size = pop_size
        self.n_parameters = n_parameters
        self.pop = self.generate_random_population()
        self.n_elite = n_elite

    def get_best_individual(self):
        minimum = MAX_FLOAT
        idx = -1
        for j in range(len(self.pop)):
            if self.pop[j].fitness < minimum:
                minimum = self.pop[j].fitness
                idx = j

        print(f"Best Individual")
        print(f"Parameters: {self.pop[idx].parameters}")
        print(f"Fitness: {round(self.pop[idx].fitness, 20)}")

    def generate_random_population(self):
        pop = []

        for i in range(self.pop_size):
            pop.append(self.generate_random_individual())

        return pop
    
    def generate_random_individual(self):
        params = [list(np.random.randint(0, 2, size=self.n_bits)) for _ in range(self.n_parameters)]
        return Individuo(self.n_bits, params, self.min_interval, self.max_interval)

    def tournament(self): #  Minimização
        vpais = []

        winner: Individuo

        for iterator in range(self.pop_size):
            p1 = np.random.choice(range(0, self.pop_size))
            p2 = np.random.choice(range(0, self.pop_size))

            while (p1 == p2):
                p2 = np.random.choice(range(0, self.pop_size))

            r = np.random.random()

            if (self.pop[p2].fitness > self.pop[p1].fitness):
                winner = copy.deepcopy(self.pop[p1])
                if (r  > self.pv): winner = copy.deepcopy(self.pop[p2])
            else:
                winner = copy.deepcopy(self.pop[p2])
                if (r  > self.pv): winner = copy.deepcopy(self.pop[p1])

            vpais.append(winner)
            iterator += 1

        return vpais
    
    def cross(self, pais, cut):
        intermed_population = []

        i = 0
        
        for i in range(0, self.pop_size, 2):
            r = np.random.random()

            if (r > self.pc):
                p1 = copy.deepcopy(pais[i])
                p2 = copy.deepcopy(pais[i + 1])

                intermed_population.append(p1)
                intermed_population.append(p2)

            else:
                # concatenar os "n" parâmetros do individuo em uma coisa só
                p1 = list(itertools.chain.from_iterable(pais[i].parameters))
                p2 = list(itertools.chain.from_iterable(pais[i + 1].parameters)) 

                filho_1_aux = list(p1[:cut] + p2[cut:])
                filho_2_aux = list(p2[:cut] + p1[cut:])

                params_1 = [filho_1_aux[i * self.n_bits : (i + 1) * self.n_bits] for i in range(self.n_parameters)]
                params_2 = [filho_2_aux[i * self.n_bits : (i + 1) * self.n_bits] for i in range(self.n_parameters)]

                filho_1 = Individuo(self.n_bits, params_1, self.min_interval, self.max_interval)
                filho_2 = Individuo(self.n_bits, params_2, self.min_interval, self.max_interval)

                intermed_population.append(filho_1)
                intermed_population.append(filho_2)

            i += 1

        return intermed_population
    
    def mutation(self, intermed_population):

        for i in range(len(intermed_population) - 1):
            r = np.random.random()

            if (r < self.pm):
                random_pos = np.random.randint(0, (self.n_bits * self.n_parameters))

                parameter = int((random_pos / self.n_bits))

                idx = random_pos % self.n_bits

                intermed_population[i].parameters[parameter][idx] = 0 if intermed_population[i].parameters[parameter][idx] == 1 else 1

    def elitism(self, n_elite, intermed_pop):
        minimum = MAX_FLOAT
        idxs = []

        copy_pop = copy.deepcopy(self.pop)

        for i in range(n_elite):
            idx = -1
            for j in range(len(copy_pop)):
                if copy_pop[j].fitness < minimum:
                    minimum = copy_pop[j].fitness
                    idx = j

            idxs.append(idx)
            copy_pop.pop(idx)

        intermed_pop[0] = copy.deepcopy(self.pop[idxs[0]])
        intermed_pop[1] = copy.deepcopy(self.pop[idxs[1]])

    def solve(self):

        np.random.seed(self.seed) # Setting seed

        iterator = 0
        while (iterator < self.n_ger):
            result = self.tournament()
            intermed_population = self.cross(result, 6)
            self.mutation(intermed_population)
            self.elitism(self.n_elite, intermed_population)
            self.pop = copy.deepcopy(intermed_population)

            iterator += 1

