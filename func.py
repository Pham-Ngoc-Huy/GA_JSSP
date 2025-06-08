import numpy as np
from src.data import *
import random

class GeneticAlgorithm:
    def __init__(self, 
                    n_population: int, 
                    interation: int, 
                    n_elitism: int, 
                    n: int, 
                    m: int, 
                    Q: np.ndarray, 
                    machine_matrix: np.ndarray,
                    number_of_assemblies: int):
        self.machine_matrix = machine_matrix
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
        # number of assemblies
        self.num_assemblies = number_of_assemblies
        
    def generate_feasible_chromosome(self):
        part_seq = random.sample(range(1, self.n + 1), self.n)
        machine_seq = []
        for p in part_seq:
            for o in range(self.Qp[p-1]):
                valid_machine = self.machine_matrix[p-1][o]
                machine_seq.append(valid_machine)
        assembly_seq = random.sample(range(1, self.num_assemblies + 1), self.num_assemblies)
        return {
            "part_seq": part_seq,
            "machine_seq": machine_seq,
            "assembly_seq": assembly_seq
        }
        
    def decode_chromosome(self, chromosome):
        part_seq = chromosome["part_seq"]
        machine_seq = chromosome["machine_seq"]

        schedule = []
        op_counter = {p: 0 for p in part_seq}  # track which op we're on for each part
        machine_index = 0

        for p in part_seq:
            for o in range(1, self.Qp[p - 1] + 1):
                if machine_index >= len(machine_seq):
                    return None  # malformed chromosome
                assigned_machine = machine_seq[machine_index]
                schedule.append((p, o, assigned_machine))
                machine_index += 1

        return schedule

    def check_feasibility(self,schedule):
        for (p, o, m) in schedule:
            valid_machine = self.machine_matrix[p - 1][o - 1]
            if m != valid_machine:
                return False
        return True
    