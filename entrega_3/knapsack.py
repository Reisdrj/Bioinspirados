from copy import deepcopy
import numpy as np
import random
import math

class Knapsack:

    def __init__(
        self,
        max_iterations,
        items,
        max_weight,
    ):


        self.knapsack_length = len(items)
        self.max_weight = max_weight
        self.max_iterations = max_iterations
        self.items = items

    def flip(self, pos):
        if pos == 1:
            return 0
        else:
            return 1

    def get_solution_value(self, solution):
        weight = self.get_solution_weight(solution)

        if weight <= self.max_weight:
            value = 0
            for i in range(len(solution)):
                if solution[i] == 1:
                    value += self.items[i][0]
            return value
        
        else:
            value = 0
            for i in range(len(solution)):
                if solution[i] == 1:
                    value += (self.items[i][0] * (1 - (self.items[i][1] - self.max_weight) / self.max_weight))
            return value

    def get_solution_weight(self, solution):
        weight = 0
        for i in range(len(solution)):
            if solution[i] == 1:
                weight += self.items[i][1]
        return weight

    def get_initial_solution(self):
        solution = [0] * self.knapsack_length
        solution_weight = 0
        solution_value = 0
        while True:
            rand_int = random.randint(0, self.knapsack_length - 1)
            if (solution_weight + self.items[rand_int][1]) <= self.max_weight:
                solution[rand_int] = 1
                solution_weight += self.items[rand_int][1]
                solution_value += self.items[rand_int][0]
            else:
                break
            
        return solution, solution_weight, solution_value