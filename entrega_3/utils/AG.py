from utils import np
from utils.Individuo import Individuo
import copy
import itertools
from sys import float_info
import random

MAX_FLOAT = float_info.max
MIN_FLOAT = float_info.min

class AlgoritmoGenetico:

    def __init__(self, pop_size, pc, pm, pv, n_ger, n_elite, seed, items, max_capacity):

        self.seed = seed
        np.random.seed(self.seed) # Setting seed

        self.pc = pc
        self.pm = pm
        self.pv = pv
        self.n_ger = n_ger
        self.items = items
        self.max_capacity = max_capacity
        self.pop_size = pop_size
        self.pop = self.generate_random_population()
        self.n_elite = n_elite


    def fitness(self, solutions):
        return [self.get_solution_value(solution) for solution in solutions]
    
    def weights(self, solutions):
        return [self.get_solution_weight(solution) for solution in solutions]   

    def get_solution_value(self, solution, type = 1):
        if type == 0: # Inviável penalizada
            weight = self.get_solution_weight(solution)

            if weight <= self.max_capacity:
                value = 0
                for i in range(len(solution)):
                    if solution[i] == 1:
                        value += int(self.items[i][0])
                return value
            
            else:
                value = 0
                weight_acc = 0
                for i in range(len(solution)):
                    if solution[i] == 1:
                        value += int((value + self.items[i][0]) * ((1 - ((weight_acc + self.items[i][1]) - self.max_capacity)) / self.max_capacity))
                        weight_acc += self.items[i][1]
                return value

        elif type == 1: # Severa
            weight = self.get_solution_weight(solution)
            if weight <= self.max_capacity:
                value = 0
                for i in range(len(solution)):
                    if solution[i] == 1:
                        value += int(self.items[i][0])
                return value
            
            else:
                value = 0
                weight_acc = 0
                for i in range(len(solution)):
                    if solution[i] == 1:
                        value += int((value + self.items[i][0]) - ((value + self.items[i][0]) * ((weight_acc + self.items[i][1]) - self.max_capacity)))
                        weight_acc += self.items[i][1]
                return value

    def get_solution_weight(self, solution):

        weight = 0
        for i in range(len(solution)):
            if solution[i] == 1:
                weight += self.items[i][1]
        return weight

    def get_best_individual(self):
        fits = self.fitness(self.pop)
        weights = self.weights(self.pop)
        maximum = 0
        idx = -1
        for j in range(len(self.pop)):
            if fits[j] > maximum and weights[j] <= self.max_capacity:
                maximum = fits[j]
                idx = j

        print(f"Best Individual")
        print(idx)
        print(f"Solution: {self.pop[idx]}")
        print(f"Fitness: {round(fits[idx])}")
        print(f"Weight: {weights[idx]}")

        return self.pop[idx]

    def generate_random_population(self):
        return np.random.randint(0, 2, size=(self.pop_size, len(self.items))).tolist()
    
    def roulette_rank(self):
        fits = self.fitness(self.pop)
        n = len(fits)

        sorted_idxs = sorted(range(n), key=lambda i: fits[i])

        ranks = [0] * n
        for rank, idx in enumerate(sorted_idxs, start=1):
            ranks[idx] = rank

        total = n * (n + 1) / 2  # soma de 1..n
        probs = [r / total for r in ranks]

        chosen = [list(ind) for ind in random.choices(self.pop, weights=probs, k=self.pop_size)]
        return chosen

    def tournament(self):
        vpais = []

        winner: list

        for iterator in range(self.pop_size):
            p1 = np.random.choice(range(0, self.pop_size))
            p2 = np.random.choice(range(0, self.pop_size))

            while (p1 == p2):
                p2 = np.random.choice(range(0, self.pop_size))

            r = np.random.random()

            if (self.get_solution_value(self.pop[p2]) < self.get_solution_value(self.pop[p1])):
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
                p1 = pais[i]
                p2 = pais[i+1]

                filho_1 = list(p1[:cut] + p2[cut:])
                filho_2 = list(p2[:cut] + p1[cut:])



                intermed_population.append(filho_1)
                intermed_population.append(filho_2)

        return intermed_population
    
    def mutation(self, intermed_population):

        for i in range(len(intermed_population) - 1):
            r = np.random.random()

            if (r < self.pm):
                random_pos = np.random.randint(0, (len(self.pop[0])))

                intermed_population[i][random_pos] = 0 if intermed_population[i][random_pos] == 1 else 1

    def elitism(self, n_elite, intermed_pop):
        fits = self.fitness(self.pop)
        wts  = self.weights(self.pop)
        
        feasible_idxs = [i for i in range(len(self.pop)) if wts[i] <= self.max_capacity]
        
        sorted_by_fit = sorted(feasible_idxs, key=lambda i: fits[i], reverse=True)
        
        elites = sorted_by_fit[:n_elite]
        
        for rank, idx in enumerate(elites):
            intermed_pop[rank] = copy.deepcopy(self.pop[idx])

    def solve(self):

        iterator = 0
        while (iterator < self.n_ger):
            result = self.roulette_rank()
            intermed_population = self.cross(result, 4)
            self.mutation(intermed_population)
            self.elitism(self.n_elite, intermed_population)
            self.pop = copy.deepcopy(intermed_population)

            iterator += 1

        return self.get_best_individual()
    
    def tests(self):
        import pandas as pd
        # 1) Inicializa histórico
        history = []

        # 2) Loop de gerações
        for gen in range(self.n_ger):
            parents = self.tournament()
            children = self.cross(parents, cut=len(self.items)//2)
            self.mutation(children)
            self.elitism(self.n_elite, children)
            self.pop = [copy.deepcopy(ind) for ind in children]

            # avalia fitness e pesos
            fits = self.fitness(self.pop)
            wts  = self.weights(self.pop)

            # encontra índice do melhor viável (ou global se nenhum viável)
            feasible = [i for i, w in enumerate(wts) if w <= self.max_capacity]
            if feasible:
                best_idx = max(feasible, key=lambda i: fits[i])
            else:
                best_idx = max(range(len(fits)), key=lambda i: fits[i])

            # índice do pior (fitness mínimo)
            worst_idx = min(range(len(fits)), key=lambda i: fits[i])

            # média de fitness
            avg_fit = sum(fits) / len(fits)

            # registra no histórico
            history.append({
                'generation':    gen,
                'best_fitness':  fits[best_idx],
                'best_ind':      self.pop[best_idx].copy(),
                'worst_fitness': fits[worst_idx],
                'worst_ind':     self.pop[worst_idx].copy(),
                'avg_fitness':   avg_fit
            })

        # 3) Salva histórico em CSV
        df_hist = pd.DataFrame(history)
        # Se preferir não salvar a coluna inteira de cromossomos como lista,
        # você pode omitir best_ind e worst_ind:
        # df_hist = df_hist.drop(columns=['best_ind','worst_ind'])
        df_hist.to_csv("results/best_params_iterattions.csv", index=False)
