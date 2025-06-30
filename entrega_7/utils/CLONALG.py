from utils.antibody import Antibody
import math, random
from copy import deepcopy

class CLONALG:
    def __init__(self, filename, n, d, beta, rho, N=100, n_gen=100):
        self.adjacency_matrix, self.n_cities = self.read_matrix_from_file(filename)
        self.n = n      # número de indivíduos a selecionar para clonar
        self.d = d      # tamanho da memória (elitismo)
        self.beta = beta
        self.rho = rho
        self.N = N      # tamanho da população
        self.n_gen = n_gen
        self.antibodies = []
        self.memory = []

    def read_matrix_from_file(self, filename):
        matrix = []
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                matrix.append(list(map(int, line.split())))
        return matrix, len(matrix[0]) if matrix else 0

    def generate_antibodies(self):
        cities = list(range(self.n_cities))
        self.antibodies = []
        for _ in range(self.N):
            path = cities[:]
            random.shuffle(path)
            self.antibodies.append(Antibody(path))

    def select_best(self, k):
        return sorted(self.antibodies, key=lambda a: a.fget_cost(self.adjacency_matrix))[:k]

    def clone(self, selected):
        num_clones = [round(self.beta * (self.N / (i+1))) for i in range(len(selected))]
        clones = []
        for indiv, n_clones in zip(selected, num_clones):
            clones.extend(deepcopy(indiv) for _ in range(n_clones))
        return clones

    def hypermutate(self, clones):
        costs = [clone.fget_cost(self.adjacency_matrix) for clone in clones]
        Dmax = max(costs) + 1e-9
        for i, clone in enumerate(clones):
            D_star = costs[i] / Dmax
            alpha = math.exp(-self.rho * D_star)
            if random.random() > alpha:
                p1, p2 = random.sample(range(self.n_cities), 2)
                clone.path[p1], clone.path[p2] = clone.path[p2], clone.path[p1]
        return clones

    def update_memory(self):
        combined = self.memory + self.antibodies
        combined.sort(key=lambda a: a.fget_cost(self.adjacency_matrix))
        self.memory = deepcopy(combined[:self.d])

    def insert_memory(self):
        self.antibodies[-self.d:] = deepcopy(self.memory)

    def solve(self):
        self.generate_antibodies()
        self.update_memory()

        for gen in range(self.n_gen):
            selected = self.select_best(self.n)
            clones = self.clone(selected)
            clones = self.hypermutate(clones)
            self.antibodies.extend(clones)
            self.antibodies.sort(key=lambda a: a.fget_cost(self.adjacency_matrix))
            self.antibodies = self.antibodies[:self.N]
            self.update_memory()
            self.insert_memory()

        self.update_memory()
        best = self.memory[0]
        print("\nBest solution found:")
        print(f"Path: {best.path}")
        print(f"Cost: {best.fget_cost(self.adjacency_matrix)}")
