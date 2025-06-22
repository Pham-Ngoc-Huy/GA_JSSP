from src.data_3 import *
from processing import GeneticAlgorithm

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
    print("Operation Sequence:", best_solution.details["executed_sequence"])
    print("Assembly Priority:", best_solution.details["assembly_sequence"])
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
