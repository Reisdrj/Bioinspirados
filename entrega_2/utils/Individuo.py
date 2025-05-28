import numpy as np
import math

class Individuo:

    def __init__(self, parameters, min_interval, max_interval):
        self.parameters = parameters
        self.max_interval = max_interval
        self.min_interval = min_interval
        
    @property
    def fitness(self):
        return self.get_fitness()

    def get_fitness(self):
        sum_x = self.get_real_values_sum(self.parameters)
        sum_cos_x = self.get_cos_sum(self.parameters)
        return -20 * pow(math.e, (-0.2 * math.sqrt((1/len(self.parameters)) * sum_x))) - pow(math.e, (1/len(self.parameters)) * sum_cos_x) + 20 + math.e

    def get_real_values_sum(self, parameters):
        sum_x = 0
        for i in parameters:
            sum_x += i ** 2
        return sum_x
    
    def get_cos_sum(self, parameters):
        sum = 0

        for i in parameters:
            sum += math.cos(2 * math.pi * i)
        return sum