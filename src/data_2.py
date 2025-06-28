# Dataset 2: More Assembly Tasks and Parts
num_parts = 5
qp = [2, 3, 4, 2, 3]  # Number of operations per part
num_assemblies = 3
depend = [
    [1, 1, 0, 1, 0],  # Task 1 depends on parts 1, 2, and 4
    [0, 1, 1, 0, 1],  # Task 2 depends on parts 2, 3, and 5
    [1, 0, 1, 0, 1]   # Task 3 depends on parts 1, 3, and 5
]
machine = [
    [1, 4, 0, 0],  # Part 1 operations
    [2, 3, 1, 0],  # Part 2 operations
    [3, 1, 2, 4],  # Part 3 operations
    [4, 3, 0, 0],  # Part 4 operations
    [3, 2, 1, 0]   # Part 5 operations
]
proc_time = [
    [3.0, 5.0, 0.0, 0.0],  # Part 1 processing times
    [2.0, 4.0, 1.0, 0.0],  # Part 2 processing times
    [4.0, 3.0, 2.0, 4.0],  # Part 3 processing times
    [5.0, 3.5, 0.0, 0.0],  # Part 4 processing times
    [6.0, 2.5, 3.0, 0.0]   # Part 5 processing times
]
asm_time = [6.0, 4.5, 7.0]  # Assembly task times

# Genetic algorithm parameters
generations = 50
pop_size = 100
elite_size = 20
mutation_rate = 0.1
