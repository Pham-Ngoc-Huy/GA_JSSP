import numpy as np
n_population = 10
interation = 100
n_elitism = 2

# number of part
n = 4
# number of machines
m = 3
# range for part n
P = np.arange(1, n + 1)
# range for machine m
M = np.arange(1, m + 1)
#number of operations for each part
Q = np.array([2, 3, 2, 3])
# max of operations
MaxOps = np.max(Q)
# range for operations
O = np.arange(1, MaxOps + 1)
# Processing time of operation 𝑗 of part 𝑝 on machine 𝑘
Tp = np.random.randint(1, 10, size=(n, MaxOps, m))

Ta = np.array([5, 6, 4, 7])     # Base assembly time per part
nd = np.array([1, 0, 1, 1])     # Orientation change
td = 2                          # Time penalty per orientation change
no = np.array([0, 1, 1, 0])     # Operation type change
to = 3                          # Time penalty per op type change
nt = np.array([1, 1, 0, 1])     # Tool change
tt = 1  