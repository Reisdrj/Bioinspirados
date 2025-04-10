import numpy as np
import math

class Individuo:

    def __init__(self, n_bits, parameters, min_interval, max_interval):
        self.n_bits = n_bits
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
        sum = 0

        for i in parameters:
            sum += pow(self.mapping(i), 2)

        return sum
    
    def get_cos_sum(self, parameters):
        sum = 0

        for i in parameters:
            sum += math.cos(2 * math.pi * self.mapping(i))

        return sum

    def mapping(self, binary):
        return (self.min_interval + ((self.max_interval - self.min_interval) / (pow(2, self.n_bits) - 1)) * self.get_bin_value(binary))
    
    def get_bin_value(self, binary):
        value = 0
        max_pow = (self.n_bits - 1) # Highest power of 2

        for i in range(self.n_bits):
            value += binary[i] * pow(2, (max_pow - i))

        return value