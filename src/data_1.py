# Dataset 1: Base Case
num_parts = 3
qp = [3, 2, 3]
num_assemblies = 1
depend = [[1, 1, 1]]  # Dependencies for assembly tasks
machine = [
    [1, 2, 3],  # Part 1 operations
    [3, 2, 0],  # Part 2 operations
    [3, 1, 2]   # Part 3 operations
]
proc_time = [
    [3.0, 2.0, 2.0],  # Part 1 processing times
    [2.0, 4.0, 0.0],  # Part 2 processing times
    [4.0, 3.0, 2.0]   # Part 3 processing times
]
asm_time = [5.0]  # Time required for the assembly task

# Genetic algorithm parameters
generations = 100
pop_size = 100
elite_size = 20
mutation_rate = 0.1
