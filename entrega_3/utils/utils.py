import os

def get_env(var_name: str, cast_func, default=None):
    value = os.getenv(var_name, default)
    if value is None:
        raise ValueError(f"Missing environment variable: {var_name}")
    try:
        return cast_func(value)
    except ValueError as e:
        raise ValueError(f"Error converting {var_name}: {e}")

def load_knapsack_data(values_file, weights_file, capacity_file):
    items = []
    
    with open(values_file, 'r') as vf:
        values = [int(line.strip()) for line in vf if line.strip()]
    
    with open(weights_file, 'r') as wf:
        weights = [int(line.strip()) for line in wf if line.strip()]

    with open(capacity_file, 'r') as cf:
        knapsack_capacity = int(cf.read().strip())
    
    if len(values) != len(weights):
        raise ValueError("The number of values and weights must be the same.")
    
    for v, w in zip(values, weights):
        items.append([v, w])
    
    return items, knapsack_capacity

def read_input(filename):
    with open(filename, "r") as file:
        length, weight = [int(i) for i in file.readline().strip().split()]
        items = []
        for _ in range(0, length):
            items.append([int(i) for i in file.readline().split()])
    return items, weight