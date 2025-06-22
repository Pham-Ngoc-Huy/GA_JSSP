import random
import copy

class Schedule:
    def __init__(self, num_parts, qp, num_assemblies, depend, machine, proc_time, asm_time):
        self.num_parts = num_parts
        self.qp = qp
        self.num_assemblies = num_assemblies
        self.depend = depend
        self.machine = machine
        self.proc_time = proc_time
        self.asm_time = asm_time

    def _simulate(self, chromosome):
        scheduled_ops = []
        op_sequence = chromosome.operation_sequence
        asm_priority = chromosome.assembly_priority

        machine_ready = [0.0 for _ in range(self.num_parts)]
        op_start = [[-1.0] * self.qp[i] for i in range(self.num_parts)]
        op_end = [[-1.0] * self.qp[i] for i in range(self.num_parts)]

        remaining_ops = {(i, o): True for i in range(self.num_parts) for o in range(self.qp[i])}
        attempts = 0
        max_attempts = len(op_sequence) * 10

        while remaining_ops and attempts < max_attempts:
            progress = False
            for (i, o) in op_sequence:
                if (i, o) not in remaining_ops:
                    continue
                if o > 0 and op_end[i][o - 1] < 0:
                    continue

                m_id = self.machine[i][o]
                if m_id == 0:
                    del remaining_ops[(i, o)]
                    progress = True
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
                progress = True
                break
            if not progress:
                break
            attempts += 1

        feasible = (len(remaining_ops) == 0)

        if not feasible:
            return {"feasible": False}

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
            "feasible": True,
            "Cmax": Cmax,
            "op_start": op_start,
            "op_end": op_end,
            "asm_start": asm_start,
            "asm_end": asm_end,
            "inventory_time": inventory_time,
            "assembly_sequence": asm_priority,
            "executed_sequence": scheduled_ops
        }

    def is_feasible(self, chromosome):
        result = self._simulate(chromosome)
        return result["feasible"]

    def evaluate_fitness(self, chromosome):
        result = self._simulate(chromosome)
        if not result["feasible"]:
            return float("inf"), {}
        return result["Cmax"], result


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
            op_seq = []
            for i in range(self.num_parts):
                for o in range(self.qp[i]):
                    op_seq.append((i, o))
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
            scored = []
            for chrom in population:
                if self.schedule.is_feasible(chrom):
                    fitness, details = self.schedule.evaluate_fitness(chrom)
                else:
                    fitness, details = float("inf"), {}
                scored.append((chrom, fitness, details))

            scored.sort(key=lambda x: x[1])
            elites = [chrom for chrom, _, _ in scored[:self.elite_size]]

            if scored[0][1] < best_makespan:
                best_makespan = scored[0][1]
                best_solution = scored[0][0]
                best_solution.details = scored[0][2]

            new_population = elites[:]
            while len(new_population) < self.pop_size:
                p1, p2 = random.sample(elites, 2)
                c1, c2 = self.crossover(p1, p2)
                new_population.append(c1.mutate(self.mutation_rate))
                if len(new_population) < self.pop_size:
                    new_population.append(c2.mutate(self.mutation_rate))

            population = new_population
            print(f"Generation {gen+1}: Best Makespan = {scored[0][1]:.2f}")

        return best_solution, best_makespan
