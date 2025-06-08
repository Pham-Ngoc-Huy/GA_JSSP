import pandas as pd
import numpy as np
from src.data import *

class GeneticAlgorithm:
    def __init__(self, 
                    n_population: int, 
                    interation: int, 
                    n_elitism: int, 
                    n: int, 
                    m: int, 
                    Q: np.ndarray, 
                    Tp: np.ndarray):
        self.n_population = n_population
        self.iteration = interation
        self.n_elitism = n_elitism
        self.n = n
        self.m = m
        self.P = np.arange(1, self.n + 1)
        # range for machine m
        self.M = np.arange(1, self.m + 1)
        #number of operations for each part
        self.Q = np.array(Q)
        # max of operations
        self.MaxOps = np.max(self.Q)
        # range for operations
        self.O = np.arange(1, self.MaxOps + 1)
        # Processing time of operation 𝑗 of part 𝑝 on machine 𝑘
        self.Tp = Tp
    def initialization(self):
        pop = []
        for i in range(1, n_population + 1):
            machine_init = np.random.permutation(np.arange(1, (MaxOps * m) + 1))
            part_init = np.random.permutation(np.arange(1, n + 1))
            assembly_init = np.random.permutation(np.arange(1, n + 1))
            init = np.concatenate((machine_init, part_init, assembly_init), axis=0)
            
            pop.append(init)
        return pop

    def decode_schedule(self,individual):
        machine_schedule = individual[:self.MaxOps * self.m].reshape((self.m, self.MaxOps))
        part_schedule = individual[self.MaxOps * self.m:self.MaxOps * self.m + self.n]
        assembly_schedule = individual[self.MaxOps * self.m + self.n:]
        
        return machine_schedule, part_schedule, assembly_schedule