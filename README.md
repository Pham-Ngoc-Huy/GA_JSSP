# Pseudo code
n: Number of parts

q: Part quantities

m: Number of assemblies

d: Dependencies between assemblies

mach: Machines for each operation

proc: Processing time for each operation

asm: Assembly time for each assembly

pop_size: Population size

elite_size: Number of elite chromosomes in each generation

mutation_rate: Probability of mutation

gen: Number of generations

```
Begin
    Repeat
        Generate initial gene population (Randomly create chromosomes with operation sequence and assembly priority)
        
        For each generation from 1 to `gen`:
            For each chromosome in the population:
                If chromosome is feasible:
                    Evaluate fitness based on Cmax (using simulate function)
                Else:
                    Set fitness to infinity
                
            Sort population by fitness (ascending)
            Select the best `elite_size` chromosomes as elites

            If best fitness (Cmax) found is better than previous, update the best solution
            
            Create new population:
                Initialize new population with elites
                While size of new population < `pop_size`:
                    Randomly select two parents from elites
                    Randomly select 2 positions for crossover
                        Apply crossover operator to generate two new offspring
                    Randomly select a mutation operator position:
                        If random value < mutation_rate:
                            Randomly select 2 positions to swap in the offspring
                                Apply mutation operator to the offspring
                    Calculate the fitness function for each new offspring in the children set
                    Elitism: Select the top 30% best chromosomes from the children set
                    Add selected offspring to new population
                
            Replace the old population with the new population            
        
        Until (termination criteria met, e.g., maximum generations or best fitness reached)
End
```     


# Genetic Algorithm for Job Shop Scheduling with Assembly and Part Sequence (JSSPASP)

## Solution Representation (Encoding)

In this approach, each solution (chromosome) is represented by two main components:

1. **Operation Sequence**: A permutation of all operations, represented as tuples `(part_index, operation_index)`.
2. **Assembly Priority**: A list of assembly indices that indicates the order in which assemblies should be processed.

### Example Encoding

```python
operation_sequence = [(2, 2), (1, 0), (0, 1), (2, 0), (1, 1), (0, 0)]
assembly_priority = [0, 1]
```

- **Operation Sequence**: Defines the order in which operations should be scheduled.
- **Assembly Priority**: Specifies that Assembly 0 should be processed before Assembly 1.

---

## Decoding: Translating Chromosome to Schedule

The decoding process transforms the encoded chromosome into a feasible schedule. The process involves:

1. **Scheduling Operations**: Operations are scheduled based on the order defined by `operation_sequence`.
2. **Handling Dependencies**: Operations are scheduled only when all their prerequisites are met, such as the completion of previous operations and machine availability.
3. **Assembly Scheduling**: Assemblies are scheduled based on the order specified in `assembly_priority`, ensuring that parts required for each assembly are ready.

### Example Decoding

Given the encoding:

```python
operation_sequence = [(2, 0), (1, 1), (0, 0)]
assembly_priority = [1, 0]
```

The decoding process works as follows:

1. Schedule `(2, 0)` first, as long as its machine is available.
2. Wait for `(1, 0)` to finish before starting `(1, 1)`.
3. Process Assembly 1 before Assembly 0, as specified in the assembly priority list.

---

## Initialization

The initialization step generates a population consisting of multiple candidate solutions. Each individual in the population is represented by a solution encoded as an operation sequence and assembly priority. Over time, the population size will evolve to find the most suitable configuration for the problem.

---

## Feasibility Check

Feasibility is ensured throughout the decoding process by:

- **Operation Scheduling**: Ensuring operations are scheduled only after their prerequisites are completed.
- **Machine Availability**: Verifying that machines are available for each scheduled operation.
- **Assembly Readiness**: Ensuring that all required parts are available before starting assembly operations.

These checks guarantee that the resulting schedule is valid, though not necessarily optimal.

---

## Fitness Function

The fitness function evaluates the quality of a solution based on the makespan (Cmax), which is calculated from various scheduling components. The fitness function is designed to minimize the total time taken to complete all operations and assemblies.

### Breakdown of the Fitness Function

1. **Operation Scheduling**:
   - Operations are scheduled based on the `operation_sequence`.
   - Each operation is assigned to a machine, and its start and end times are computed sequentially.
   - The machine's readiness time is updated after each operation to reflect when it will be free for the next task.

2. **Assembly Operations**:
   - Once all operations are scheduled, the assembly operations are handled according to the `assembly_priority`.
   - The start time for each assembly is calculated by finding the maximum finish time of all required parts.
   - The end time for the assembly is determined by adding the processing time for the assembly to its start time.

3. **Inventory Time**:
   - The inventory time represents the delay each part experiences before it can be used in an assembly.
   - This is calculated as the difference between the time a part finishes and when it is needed for assembly.

4. **Cmax Calculation**:
   - Cmax represents the overall makespan, which is the maximum end time of all assembly operations.
   - The goal is to minimize Cmax, which indicates the time it takes for the entire system to complete.

---

## Genetic Operators

### Selection

Selection is performed by randomly choosing two parents from the elite pool for crossover. The elite pool consists of the best-performing solutions in the population, ensuring that the algorithm favors high-quality solutions.

### Crossover

The crossover operation is based on the Ordered Crossover (OX) method, which is effective for permutation problems. The steps of the crossover process are:

1. **Random Selection of Subsequence**: Two random points (start and end) are selected within the parent chromosomes.
2. **Copy Subsequence**: A subsequence from Parent 1 is directly copied to the offspring.
3. **Maintain Relative Order**: The remaining positions in the offspring chromosome are filled with genes from Parent 2, maintaining their relative order.
4. **Gene Placement**: The genes from Parent 2 that are not already in the offspring (due to being copied from Parent 1) are placed in the remaining positions in the offspring.

This crossover method ensures that the offspring inherit valuable characteristics from both parents while maintaining the integrity of the solution structure.

### Mutation

Mutation introduces small variations in the population to avoid premature convergence and improve diversity. The mutation process is as follows:

- **Mutation Rate**: A mutation rate (`mutation_rate`) determines the probability of mutation occurring for each individual. Typically, this value is between 0 and 1 (e.g., 0.05 or 0.1).
- **Random Mutation**: If a random number generated is less than the mutation rate, a mutation occurs.
- **Mutation Action**: The mutation consists of randomly selecting two positions in the chromosome and swapping their values, introducing small changes that may lead to improved solutions.

### Elitism

Elitism ensures that the best solutions from the current generation are retained in the population. In this method, the best 30% of the children solutions replace the worst 30% of the current population. This strategy preserves diversity in the population, preventing premature convergence to suboptimal solutions. By limiting the number of replacements to 30%, we maintain enough diversity to explore the solution space effectively.

---

By combining these genetic operators, the algorithm seeks to evolve the population toward the optimal solution while balancing exploration and exploitation. The iterative process of selection, crossover, mutation, and elitism allows the algorithm to progressively improve the scheduling solution.

---
# Validation

**Scalable_1**:
>3 parts - 3 operations - 3 machines - 1 assembly task

This scalable stands for the Base Case - which is the simpliest one


**Schedule_in_exact_solution**

**Schedule_in_algorithm**


| **Objective**                    | **Exact Solution** | **Genetics Algorithm** |
| ------------------------------- | ------------------ | ----------------------|
| **Makespan**                   | 21.5                 | 21.5           |
| **Time elapsed**              | 0.41 seconds             | 0.426641 seconds|
|**Scalable**| 5 parts, 4 operations, 3 machines, 3 assembly tasks| 5 parts, 4 operations, 3 machines, 3 assembly tasks


**Scalable_2**: 
>5 parts - 4 operations - 3 machines - 3 assembly tasks

This scalable stands for more complicate that i increase the the number of parts, operations, and tasks.

**Schedule_in_exact_solution**

**Schedule_in_algorithm**


| **Objective**                    | **Exact Solution** | **Genetics Algorithm** |
| ------------------------------- | ------------------ | ----------------------|
| **Makespan**                   | 21.5                 | 21.5           |
| **Time elapsed**              | 0.41 seconds             | 0.426641 seconds|
|**Scalable**| 5 parts, 4 operations, 3 machines, 3 assembly tasks| 5 parts, 4 operations, 3 machines, 3 assembly tasks


Schedule

**Scalable_3**: 
>4 parts - 3 operations - 3 machines - 2 assembly tasks

This scalable stands for varying operations and processing times

**Schedule_in_exact_solution**

**Schedule_in_algorithm**


| **Objective**                    | **Exact Solution** | **Genetics Algorithm** |
| ------------------------------- | ------------------ | ----------------------|
| **Makespan**                   | 21.5                 | 21.5           |
| **Time elapsed**              | 0.41 seconds             | 0.426641 seconds|
|**Scalable**| 4 parts, 3 operations, 3 machines, 2 assembly tasks| 4 parts, 3 operations, 3 machines, 2 assembly tasks



Through 3 scales of calculations, we can say that the genetic algorithms in the Job Shop Schedule Planning and Assembly Schedule Planning is realiable.

So we can continue using this algorith to adapt larger scale in calculation where the exact solution take too much time to explore the optimal ones, with the algorithm, we can get near to the optimal solution.


---

