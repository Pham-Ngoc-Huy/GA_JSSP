import random
import copy
from src.data import *

class Schedule:
    def __init__(self, num_parts, qp, num_assemblies, depend, machine, proc_time, asm_time):
        self.num_parts = num_parts
        self.qp = qp
        self.num_assemblies = num_assemblies
        self.depend = depend
        self.machine = machine
        self.proc_time = proc_time
        self.asm_time = asm_time

    def simulate_schedule(self, chromosome):
        scheduled_ops = []
        op_sequence = chromosome.operation_sequence
        asm_priority = chromosome.assembly_priority

        machine_ready = [0.0 for _ in range(self.num_parts)]
        op_start = [[-1.0] * self.qp[i] for i in range(self.num_parts)]
        op_end = [[-1.0] * self.qp[i] for i in range(self.num_parts)]

        remaining_ops = {(i, o): True for i in range(self.num_parts) for o in range(self.qp[i])}
        
        while remaining_ops:
            for (i, o) in op_sequence:
                if (i, o) not in remaining_ops:
                    continue
                if o > 0 and op_end[i][o - 1] < 0:
                    continue  # Wait for previous op to finish

                m_id = self.machine[i][o]
                if m_id == 0:
                    del remaining_ops[(i, o)]
                    continue
                p_time = self.proc_time[i][o]
                earliest_start = 0.0
                if o > 0:
                    earliest_start = max(earliest_start, op_end[i][o - 1])
                earliest_start = max(earliest_start, machine_ready[m_id - 1])
                start = earliest_start
                end = start + p_time
                op_start[i][o] = start
                op_end[i][o] = end
                machine_ready[m_id - 1] = end
                del remaining_ops[(i, o)]
                scheduled_ops.append((i, o))
                break

        part_done = [op_end[i][self.qp[i] - 1] for i in range(self.num_parts)]
        asm_start = [0.0 for _ in range(self.num_assemblies)]
        asm_end = [0.0 for _ in range(self.num_assemblies)]
        inventory_time = [0.0 for _ in range(self.num_parts)]

        for a in asm_priority:
            wait_parts = [i for i in range(self.num_parts) if self.depend[a][i]]
            start = max(part_done[i] for i in wait_parts)
            end = start + self.asm_time[a]
            asm_start[a] = start
            asm_end[a] = end
            for i in wait_parts:
                inventory_time[i] = start - part_done[i]

        Cmax = max(asm_end)

        return {
            "Cmax": Cmax,
            "op_start": op_start,
            "op_end": op_end,
            "asm_start": asm_start,
            "asm_end": asm_end,
            "inventory_time": inventory_time
        }


class Chromosome:
    def __init__(self, operation_sequence, assembly_priority):
        self.operation_sequence = operation_sequence
        self.assembly_priority = assembly_priority

    def mutate(self, mutation_rate):
        new_chrom = copy.deepcopy(self)
        if random.random() < mutation_rate:
            i, j = random.sample(range(len(new_chrom.operation_sequence)), 2)
            new_chrom.operation_sequence[i], new_chrom.operation_sequence[j] = new_chrom.operation_sequence[j], new_chrom.operation_sequence[i]
        if len(new_chrom.assembly_priority) > 1 and random.random() < mutation_rate:
            i, j = random.sample(range(len(new_chrom.assembly_priority)), 2)
            new_chrom.assembly_priority[i], new_chrom.assembly_priority[j] = new_chrom.assembly_priority[j], new_chrom.assembly_priority[i]
        return new_chrom


class GeneticAlgorithm:
    def __init__(self, num_parts, qp, num_assemblies, depend, machine, proc_time, asm_time, generations, pop_size, elite_size, mutation_rate):
        self.num_parts = num_parts
        self.qp = qp
        self.num_assemblies = num_assemblies
        self.depend = depend
        self.machine = machine
        self.proc_time = proc_time
        self.asm_time = asm_time
        self.generations = generations
        self.pop_size = pop_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.schedule = Schedule(num_parts, qp, num_assemblies, depend, machine, proc_time, asm_time)

    def generate_initial_population(self):
        population = []
        for _ in range(self.pop_size):
            op_seq = [(i, o) for i in range(self.num_parts) for o in range(self.qp[i])]
            random.shuffle(op_seq)
            asm_prio = list(range(self.num_assemblies))
            random.shuffle(asm_prio)
            population.append(Chromosome(op_seq, asm_prio))
        return population

    def crossover(self, parent1, parent2):
        cut = random.randint(1, len(parent1.operation_sequence) - 2)
        child1_seq = parent1.operation_sequence[:cut] + [x for x in parent2.operation_sequence if x not in parent1.operation_sequence[:cut]]
        child2_seq = parent2.operation_sequence[:cut] + [x for x in parent1.operation_sequence if x not in parent2.operation_sequence[:cut]]

        ap1, ap2 = parent1.assembly_priority, parent2.assembly_priority
        if len(ap1) > 1:
            ap_cut = random.randint(1, len(ap1)-1)
            child1_ap = ap1[:ap_cut] + [x for x in ap2 if x not in ap1[:ap_cut]]
            child2_ap = ap2[:ap_cut] + [x for x in ap1 if x not in ap2[:ap_cut]]
        else:
            child1_ap = ap1[:]
            child2_ap = ap2[:]

        return Chromosome(child1_seq, child1_ap), Chromosome(child2_seq, child2_ap)

    def genetic_algorithm(self):
        population = self.generate_initial_population()
        best_makespan = float("inf")
        best_solution = None

        for gen in range(self.generations):
            scored = [(chrom, self.schedule.simulate_schedule(chrom)) for chrom in population]
            scored.sort(key=lambda x: x[1]["Cmax"])  # Sort by makespan (Cmax)

            elites = [chrom for chrom, _ in scored[:self.elite_size]]

            details = scored[0][1]
            if details["Cmax"] < best_makespan:
                best_makespan = details["Cmax"]
                best_solution = scored[0][0]
                best_solution.details = details

            new_population = elites[:]
            while len(new_population) < self.pop_size:
                p1, p2 = random.sample(elites, 2)
                c1, c2 = self.crossover(p1, p2)
                new_population.append(c1.mutate(self.mutation_rate))
                if len(new_population) < self.pop_size:
                    new_population.append(c2.mutate(self.mutation_rate))

            population = new_population
            print(f"Generation {gen+1}: Best Makespan = {details['Cmax']:.2f}")

        return best_solution, best_makespan


def main():
    algorithm = GeneticAlgorithm(
        num_parts=num_parts,
        qp=qp,
        num_assemblies=num_assemblies,
        depend=depend,
        machine=machine,
        proc_time=proc_time,
        asm_time=asm_time,
        generations=generations,
        pop_size=pop_size,
        elite_size=elite_size,
        mutation_rate=mutation_rate
    )
    best_solution, best_makespan = algorithm.genetic_algorithm()
    print("\n--- Best solution found ---")
    print("Operation Sequence:", best_solution.operation_sequence)
    print("Assembly Priority:", best_solution.assembly_priority)
    print(f"Best Makespan (Cmax): {best_makespan:.2f}\n")

    details = best_solution.details
    op_start = details["op_start"]
    op_end = details["op_end"]
    asm_start = details["asm_start"]
    asm_end = details["asm_end"]
    inventory_time = details["inventory_time"]

    print("=== Part Processing Times ===")
    for i in range(num_parts):
        for o in range(qp[i]):
            print(f"Part {i} - Op {o}: Start = {op_start[i][o]:.2f}, End = {op_end[i][o]:.2f}")
        print(f"  Last operation ends at: {op_end[i][qp[i]-1]:.2f}")
        print(f"  Inventory time before assembly: {inventory_time[i]:.2f}\n")

    print("=== Assembly Times ===")
    for a in range(num_assemblies):
        print(f"Assembly {a}: Start = {asm_start[a]:.2f}, End = {asm_end[a]:.2f}")


if __name__ == "__main__":
    main()
