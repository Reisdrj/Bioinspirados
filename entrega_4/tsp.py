from itertools import permutations
import copy, numpy as np, random
from utils.Individuo import Individuo
from sys import float_info
import csv, os
from itertools import product

MAX_FLOAT = float_info.max

class TSP:

    def __init__(self, pop_size, pc, pm, pv, n_ger, matrix_path):
        self.n_ger = n_ger
        self.pop_size = pop_size
        self.pm = pm
        self.pv = pv
        self.pc = pc
        self.matrix, self.n_cities = self.read_matrix_from_file(matrix_path)
        self.matrix_path = matrix_path
        self.pop = self.generate_random_population()

    def get_best_individual(self):
        maximum = MAX_FLOAT
        idx = -1
        for j in range(len(self.pop)):
            if self.pop[j].get_fitness(self.matrix) < maximum:
                maximum = self.pop[j].get_fitness(self.matrix)
                idx = j

        print(f"Best Individual")
        print(f"Parameters: {self.pop[idx].path}")
        print(f"Fitness: {round(self.pop[idx].get_fitness(self.matrix), 20)}")
        
        return self.pop[idx].get_fitness(self.matrix)

    def read_matrix_from_file(self, filename):
        matrix = []
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                row = list(map(int, line.split()))
                matrix.append(row)
        
        size = len(matrix[0]) if matrix else 0
        return matrix, size
    
    def generate_random_population(self):

        source_path = list(range(self.n_cities))
        pop = []

        while len(pop) < self.pop_size:
            permutation = random.sample(source_path, len(source_path))
            individuo = Individuo(permutation, len(permutation))
            pop.append(individuo)

        return pop

    def tournament(self):
        vpais = []

        winner: list

        for iterator in range(self.pop_size):
            p1 = np.random.choice(range(0, self.pop_size))
            p2 = np.random.choice(range(0, self.pop_size))

            while (p1 == p2):
                p2 = np.random.choice(range(0, self.pop_size))

            r = np.random.random()

            if (self.pop[p2].get_fitness(self.matrix) > self.pop[p1].get_fitness(self.matrix)):
                winner = copy.deepcopy(self.pop[p1])
                if (r  > self.pv): winner = copy.deepcopy(self.pop[p2])
            else:
                winner = copy.deepcopy(self.pop[p2])
                if (r  > self.pv): winner = copy.deepcopy(self.pop[p1])

            vpais.append(winner)
            iterator += 1

        return vpais

    def ox_crossover(self, parents):
        new_population = []

        for i in range(0, len(parents), 2):
            parent1 = parents[i].path
            parent2 = parents[i+1].path

            r1 = random.randint(0, self.n_cities - 2)
            r2 = random.randint(r1 + 1, self.n_cities - 1)

            child1 = [None] * self.n_cities
            child2 = [None] * self.n_cities

            child1[r1:r2] = parent1[r1:r2]
            child2[r1:r2] = parent2[r1:r2]

            def fill_remaining(child, donor):
                current_pos = r2 % self.n_cities
                donor_pos = r2 % self.n_cities
                while None in child:
                    gene = donor[donor_pos]
                    if gene not in child:
                        child[current_pos] = gene
                        current_pos = (current_pos + 1) % self.n_cities
                    donor_pos = (donor_pos + 1) % self.n_cities
                return child

            child1 = fill_remaining(child1, parent2)
            child2 = fill_remaining(child2, parent1)
            new_population.extend([Individuo(path=child1, n_cities=self.n_cities), Individuo(path=child2, n_cities=self.n_cities)])

        self.pop = new_population

    def mutation(self):

        for i in range(0, len(self.pop)):
            rand = random.uniform(0, 1)

            if rand < self.pm:
                r1 = random.randint(0, self.n_cities - 2)
                r2 = random.randint(r1 + 1, self.n_cities - 1)

                aux = self.pop[i].path[r1]
                self.pop[i].path[r1] = self.pop[i].path[r2]
                self.pop[i].path[r2] = aux


    def solve(self):
        
        for i in range(self.n_ger):
            parents = self.tournament()
            self.ox_crossover(parents)
            self.mutation()


        self.get_best_individual()

    def tests(self, n_runs=10):
        # build output path
        test_name = self.matrix_path.split('/')[1]
        output_file = f'results/{test_name}/tsp_results.csv'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # parameter grids
        pc_vals      = [0.5, 0.7, 1.0]
        pv_vals      = [0.5, 0.7, 0.9]
        pm_vals      = [0.01, 0.05, 0.1]
        pop_size_vals= [100, 200]
        n_ger_vals   = [100, 200]

        # write header
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'pc', 'pv', 'pm', 'pop_size', 'n_ger',
                'run', 'best_fitness'
            ])

            # loop over every combination
            for pc, pv, pm, pop_sz, n_ger in product(
                    pc_vals, pv_vals, pm_vals, pop_size_vals, n_ger_vals):

                # set GA parameters for this experiment
                self.pc        = pc
                self.pv        = pv
                self.pm        = pm
                self.pop_size  = pop_sz
                self.n_ger     = n_ger

                for run in range(n_runs):
                    # fresh population each run
                    self.pop = self.generate_random_population()

                    # evolve
                    for _ in range(self.n_ger):
                        parents = self.tournament()
                        self.ox_crossover(parents)
                        self.mutation()

                    # record best fitness
                    best_fit = min(
                        self.pop,
                        key=lambda ind: ind.get_fitness(self.matrix)
                    ).get_fitness(self.matrix)

                    writer.writerow([
                        pc, pv, pm, pop_sz, n_ger,
                        run, best_fit
                    ])

        print(f"Finished all experiments. Results saved to '{output_file}'")