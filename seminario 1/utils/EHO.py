from utils import np
from utils.Individuo import Individuo
from sys import float_info

MAX_FLOAT = float_info.max

class EHO:

    def __init__(self, pop_size, min_interval, max_interval, n_ger, n_parameters, alpha, beta, nClan, seed):
        self.seed = seed

        self.min_interval = min_interval
        self.max_interval = max_interval
        self.n_ger = n_ger
        self.pop_size = pop_size
        self.n_parameters = n_parameters
        self.alpha = alpha
        self.beta = beta
        self.nClan = nClan
        self.pop = self.generate_random_population()
        self.clans = self.create_random_clans()
        

    def create_random_clans(self):
        indices = np.random.permutation(self.pop_size)
        clans = [[] for _ in range(self.nClan)]
        for i, idx in enumerate(indices):
            clans[i % self.nClan].append(self.pop[idx])
        return clans

    def generate_random_population(self):
        pop = []

        for _ in range(self.pop_size):
            pop.append(self.generate_random_individual())

        return pop

    def get_best_individual(self):
        best = None

        for clan in self.clans:
            for ind in clan:
                if best is None or ind.fitness < best.fitness:
                    best = ind

        print("Best Individual")
        print(f"Parameters: {best.parameters}")
        print(f"Fitness: {round(best.fitness, 20)}")

        return best

    def generate_random_individual(self):
        params = [np.random.uniform(self.min_interval, self.max_interval) for _ in range(self.n_parameters)]
        return Individuo(params, self.min_interval, self.max_interval)

    def sort_clans_by_fitness(self):
        for i, clan in enumerate(self.clans):
            self.clans[i] = sorted(clan, key=lambda ind: ind.fitness)

    def separating_operator(self):
        for clan in self.clans:
            clan[-1].parameters = [self.min_interval + (self.max_interval - self.min_interval + 1) * np.random.random() for _ in range(self.n_parameters)]
        
    def updating_operator(self):
        for clan in self.clans:
            best_ind = clan[0] 
            best_params = best_ind.parameters

            for ind in clan:
                if ind is not best_ind:
                    for index in range(len(ind.parameters)):
                        ind.parameters[index] += self.alpha * (best_params[index] - ind.parameters[index]) * np.random.random()
                else:
                    for index in range(len(ind.parameters)):
                        param_sum = sum(other_ind.parameters[index] for other_ind in clan)
                        avg = param_sum / len(clan)
                        ind.parameters[index] = self.beta * avg

    def solve(self):
        # np.random.seed(self.seed) # Setting seed
        iterator = 0
        while iterator < self.n_ger:
            self.sort_clans_by_fitness()
            self.updating_operator()
            self.separating_operator()
            iterator += 1