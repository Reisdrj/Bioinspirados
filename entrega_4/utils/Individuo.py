import numpy as np
import math

class Individuo:

    def __init__(self, path, n_cities):
        self.path = path
        self.n_cities = n_cities
        
    def get_fitness(self, adjacency_matrix):
        fitness = 0
        for i in range(len(self.path)):
            fitness += adjacency_matrix[self.path[i]][self.path[(i + 1) % self.n_cities]]

        return fitness