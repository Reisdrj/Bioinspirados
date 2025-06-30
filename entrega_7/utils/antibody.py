class Antibody:

    def __init__(self, path):
        self.path = path

    def fget_cost(self, adjacency_matrix):
        cost = 0

        if len(self.path) > 1:
            for i in range(len(self.path)):
                cost += adjacency_matrix[self.path[i] - 1][(self.path[(i + 1) % len(self.path)] - 1)]

            return cost
        else: return cost