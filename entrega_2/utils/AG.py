from utils import np
from utils.Individuo import Individuo
import copy
import itertools
from sys import float_info
import random

MAX_FLOAT = float_info.max
MIN_FLOAT = float_info.min

class AlgoritmoGenetico:

    def __init__(self, pop_size, pc, pm, min_interval, max_interval, alfa, beta: 0, n_ger, n_elite, n_parameters, seed, cruzamento= 0):
        self.seed = seed
        self.alfa = alfa
        self.beta = beta
        self.pc = pc
        self.pm = pm
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.n_ger = n_ger
        self.pop_size = pop_size
        self.n_parameters = n_parameters
        self.pop = self.generate_random_population()
        self.n_elite = n_elite
        self.cruzamento = cruzamento

    def get_best_individual(self):
        minimum = self.pop[0].fitness
        idx = -1
        for j in range(len(self.pop)):
            if self.pop[j].fitness < minimum:
                minimum = self.pop[j].fitness
                idx = j

        print(f"Best Individual")
        print(f"Parameters: {self.pop[idx].parameters}")
        print(f"Fitness: {round(self.pop[idx].fitness, 20)}")

        return self.pop[idx]

    def generate_random_population(self):
        pop = []

        for _ in range(self.pop_size):
            pop.append(self.generate_random_individual())

        return pop
    
    def generate_random_individual(self):
        params = [np.random.uniform(-10, 10) for _ in range(self.n_parameters)]
        return Individuo(params, self.min_interval, self.max_interval)
    
    def get_fitness_list(self):
        fitness = []

        for i in range(self.pop_size):
            fitness.append((1 / self.pop[i].fitness))

        return fitness
    
    def roulette(self):
        fitness = self.get_fitness_list()
        pais = random.choices(self.pop, weights=fitness, k=self.pop_size)
        return pais

    def cross_BLX_a(self, pais):
        intermed_population = []

        n = len(pais)

        for i in range(0, n - 1, 2):
            p1 = pais[i]
            p2 = pais[i+1]

            for _ in range(2):
                filho_params = []
                for j in range(self.n_parameters):
                    v1 = p1.parameters[j]
                    v2 = p2.parameters[j]
                    d  = abs(v1 - v2)
                    low  = v1 - self.alfa * d
                    high = v2 + self.alfa * d
                    filho_params.append(np.random.uniform(low, high))

                intermed_population.append(
                    Individuo(filho_params,
                            self.min_interval,
                            self.max_interval)
                )

        if n % 2 == 1:
            intermed_population.append(
                copy.deepcopy(pais[-1])
            )

        return intermed_population

    def cross_BLX_ab(self, pais):
        intermed_population = []
        n = len(pais)

        for i in range(0, n - 1, 2):
            p1 = pais[i]
            p2 = pais[i+1]

            for _ in range(2):
                filho_params = []
                for j in range(self.n_parameters):
                    v1 = p1.parameters[j]
                    v2 = p2.parameters[j]
                    d  = abs(v1 - v2)

                    if p1.fitness < p2.fitness:
                        low  = v1 - self.alfa * d
                        high = v2 + self.beta * d
                    else:
                        low  = v1 - self.beta * d
                        high = v2 + self.alfa * d

                    filho_params.append(np.random.uniform(low, high))

                intermed_population.append(
                    Individuo(filho_params,
                            self.min_interval,
                            self.max_interval)
                )

        if n % 2 == 1:
            intermed_population.append(copy.deepcopy(pais[-1]))

        return intermed_population
    
    def mutation(self, intermed_population):

        for i in range(len(intermed_population) - 1):
            r = np.random.random()

            if (r < self.pm):
                random_pos = np.random.randint(0, self.n_parameters)

                intermed_population[i].parameters[random_pos] = np.random.uniform(-2, 2)

    def elitism(self, n_elite, intermed_pop):

        if n_elite == 0: return 
        
        else:
            copy_pop = copy.deepcopy(self.pop)
            best_idx = 0
            minimum = copy_pop[0].fitness

            for j in range(1, len(copy_pop)):
                if copy_pop[j].fitness < minimum:
                    minimum = copy_pop[j].fitness
                    best_idx = j

            intermed_pop[0] = copy.deepcopy(self.pop[best_idx])

    

    def get_avg_fitness(self):

        avg = 0

        for i in self.pop:
            avg += i.fitness

        avg = avg / self.pop_size

        return avg
    
    def get_awful_individual(self):
        maximum = self.pop[0].fitness
        idx = -1
        for j in range(len(self.pop)):
            if self.pop[j].fitness > maximum:
                maximum = self.pop[j].fitness
                idx = j

        return self.pop[idx].fitness

    def solve(self):

        np.random.seed(self.seed) # Setting seed

        best_fitness = []
        avg_fitness = []
        awful_fitnes = []

        iterator = 0
        while (iterator < self.n_ger):
            result = self.roulette()
            if self.cruzamento == 0:
                intermed_population = self.cross_BLX_a(result)
            else:
                intermed_population = self.cross_BLX_ab(result)
            self.mutation(intermed_population)
            self.elitism(self.n_elite, intermed_population)
            self.pop = copy.deepcopy(intermed_population)
            best_fitness.append(self.get_best_individual().fitness)
            avg_fitness.append(self.get_avg_fitness())
            awful_fitnes.append(self.get_awful_individual())
            iterator += 1

        return best_fitness, avg_fitness, awful_fitnes

    def tests(self):

        np.random.seed(self.seed) # Setting seed

        pops = []

        for i in range(20):
            iterator = 0
            while (iterator < self.n_ger):
                result = self.roulette()
                if self.cruzamento == 0:
                    intermed_population = self.cross_BLX_a(result)
                else:
                    intermed_population = self.cross_BLX_ab(result)
                self.mutation(intermed_population)
                if self.n_elite != 0:
                    self.elitism(self.n_elite, intermed_population)
                self.pop = copy.deepcopy(intermed_population)

                iterator += 1

            pops.append(self.get_best_individual())

        return pops
