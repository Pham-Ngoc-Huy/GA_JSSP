# Dataset 3: Varying Operations and Processing Times
num_parts = 4
qp = [3, 2, 3, 1]  # Number of operations per part
num_assemblies = 2
depend = [
    [1, 0, 1, 0],  # Task 1 depends on parts 1 and 3
    [0, 1, 0, 1]   # Task 2 depends on parts 2 and 4
]
machine = [
    [1, 2, 3],  # Part 1 operations
    [2, 3, 0],  # Part 2 operations
    [3, 1, 2],  # Part 3 operations
    [1, 0, 0]   # Part 4 operations
]
proc_time = [
    [5.0, 3.0, 2.5],  # Part 1 processing times
    [4.5, 2.0, 0.0],  # Part 2 processing times
    [3.0, 4.0, 3.5],  # Part 3 processing times
    [7.0, 0.0, 0.0]   # Part 4 processing times
]
asm_time = [8.0, 5.5]  # Assembly task times

# Genetic algorithm parameters
generations = 100
pop_size = 100
elite_size = 20
mutation_rate = 0.1
