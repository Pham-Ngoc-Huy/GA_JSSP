import random
import copy
import logging
# import itertools import count
import matplotlib.pyplot as plt
# from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


plt.style.use('fivethirtyeight')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

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
        self.fitness = None
        self.details = None

    def mutate(self, mutation_rate):
        new_chrom = copy.deepcopy(self)
        if random.random() < mutation_rate:
            i, j = random.sample(range(len(new_chrom.operation_sequence)), 2)
            new_chrom.operation_sequence[i], new_chrom.operation_sequence[j] = new_chrom.operation_sequence[j], new_chrom.operation_sequence[i]
        if len(new_chrom.assembly_priority) > 1 and random.random() < mutation_rate:
            i, j = random.sample(range(len(new_chrom.assembly_priority)), 2)
            new_chrom.assembly_priority[i], new_chrom.assembly_priority[j] = new_chrom.assembly_priority[j], new_chrom.assembly_priority[i]
        # Reset fitness after mutation
        new_chrom.fitness = None
        new_chrom.details = None
        return new_chrom


class GeneticAlgorithm:
    def __init__(self, num_parts, qp, num_assemblies, depend, machine, proc_time, asm_time, generations, pop_size, elite_size, mutation_rate, children_size):
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
        self.children_size = children_size
        self.schedule = Schedule(num_parts, qp, num_assemblies, depend, machine, proc_time, asm_time)

    def generate_initial_population(self):
        population = []
        
        while len(population) < self.pop_size:
            op_seq = []
            asm_prio = []
            for i in range(self.num_parts):
                for o in range(self.qp[i]):
                    op_seq.append((i, o))
            random.shuffle(op_seq)  
            asm_prio = list(range(self.num_assemblies))
            random.shuffle(asm_prio) 
            new_chromosome = Chromosome(op_seq, asm_prio)
            if new_chromosome not in population:
                if self.schedule.is_feasible(new_chromosome):
                    fitness, details = self.schedule.evaluate_fitness(new_chromosome)
                    new_chromosome.fitness = fitness
                    new_chromosome.details = details
                else:
                    continue 
            population.append(new_chromosome)
        return population


    def evaluate_population(self, population):
        for chromosome in population:
            if chromosome.fitness is None:  # Only evaluate if not already evaluated
                if self.schedule.is_feasible(chromosome):
                    fitness, details = self.schedule.evaluate_fitness(chromosome)
                    chromosome.fitness = fitness
                    chromosome.details = details
                else:
                    chromosome.fitness = float("inf")
                    chromosome.details = {}

    def selection(self, population):
        random_n1 = 0
        random_n2 = 0
        while random_n1 == random_n2: 
            random_n1 = random.randint(0, len(population) - 1)
            random_n2 = random.randint(0, len(population) - 1)
        
        return population[random_n1], population[random_n2]

    def crossover(self, parent1, parent2):
        cut1 = random.randint(0, len(parent1.operation_sequence) - 1)
        cut2 = random.randint(cut1 + 1, len(parent1.operation_sequence))

        child1_seq = [None] * len(parent1.operation_sequence)
        child1_seq[cut1:cut2] = parent1.operation_sequence[cut1:cut2]
        
        parent2_remaining = [x for x in parent2.operation_sequence if x not in child1_seq]
        child1_seq = [item if item is not None else parent2_remaining.pop(0) for item in child1_seq]
        
        child2_seq = [None] * len(parent2.operation_sequence)
        child2_seq[cut1:cut2] = parent2.operation_sequence[cut1:cut2]
        
        parent1_remaining = [x for x in parent1.operation_sequence if x not in child2_seq]
        child2_seq = [item if item is not None else parent1_remaining.pop(0) for item in child2_seq]

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
        fitness_history = []
        
        logger.info("Stage 1: Initializing population...")
        population = self.generate_initial_population()
        
        if len(population) == 0:
            logger.error("Failed to generate any feasible solutions!")
            return None, float("inf")
        
        logger.info("Stage 2: Evaluating initial fitness...")
        self.evaluate_population(population)
        
        # Log initial population fitness
        for i, chromosome in enumerate(population):
            logger.info(f"Chromosome {i + 1}: Fitness = {chromosome.fitness}")
        
        population.sort(key=lambda x: x.fitness)
        best_chromosome = copy.deepcopy(population[0])
        best_makespan = best_chromosome.fitness
        logger.info(f"Initial best fitness: {best_makespan:.2f}")
        
        for generation in range(self.generations):
            logger.info(f"\n--- Generation {generation + 1} ---")
            
            fitness_history.append(best_makespan)
            child_population = []
            
            # Generate children
            while len(child_population) < self.children_size:
                parent1, parent2 = self.selection(population)
                child1, child2 = self.crossover(parent1, parent2)
                
                # Apply mutation
                child1 = child1.mutate(self.mutation_rate)
                child2 = child2.mutate(self.mutation_rate)
                
                child_population.append(child1)
                # if len(child_population) < self.children_size:
                    # child_population.append(child2)
            
            logger.info(f"Evaluating {len(child_population)} offspring...")
            self.evaluate_population(child_population)
            
            child_population.sort(key=lambda x: x.fitness)
            
            population.sort(key=lambda x: x.fitness)
            
            for etil in range(self.elite_size):
                if child_population[etil].fitness < population[-1].fitness:  
                    population[-1] = copy.deepcopy(child_population[etil])
                    logger.info(f"Replaced worst (fitness: {population[-1].fitness:.2f}) with child {etil}")
            
                population = population[:self.pop_size - self.elite_size] + child_population[:self.elite_size]    
            population.sort(key=lambda x: x.fitness)
                  
            current_best = population[0]
            if current_best.fitness < best_makespan:
                best_makespan = current_best.fitness
                best_chromosome = copy.deepcopy(current_best)
                logger.info(f"*** New best solution found: {best_makespan:.2f} ***")
            
            # Log generation statistics
            fitnesses = [chrom.fitness for chrom in population if chrom.fitness != float("inf")]
            if fitnesses:
                avg_fitness = sum(fitnesses) / len(fitnesses)
                logger.info(f"Best: {population[0].fitness:.2f}, Avg: {avg_fitness:.2f}, Worst: {population[-1].fitness:.2f}")
            else:
                logger.error("No feasible solutions in population!")
        
        logger.info(f"\nFinal best makespan: {best_makespan:.2f}")
        
        # Plot fitness evolution
        if fitness_history:
            plt.figure(figsize=(10, 6))
            plt.plot(range(1, len(fitness_history) + 1), fitness_history, 'b-', linewidth=2)
            plt.xlabel('Generation')
            plt.ylabel('Best Fitness (Makespan)')
            plt.title('Genetic Algorithm Convergence')
            plt.grid(True)
            plt.show()
        
        return best_chromosome, best_makespan