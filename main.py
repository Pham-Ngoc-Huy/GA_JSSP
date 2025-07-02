from src.large_scale import *
from staging import GeneticAlgorithm
import time
import pandas as pd
def main():
    start_time = time.perf_counter()
    algorithm = GeneticAlgorithm(
        num_parts=num_parts,
        qp=qp[0],
        num_assemblies=num_assemblies,
        depend=depend,
        machine=machine,
        proc_time=proc_time,
        asm_time=asm_time[0],
        generations=generations,
        pop_size=pop_size,
        elite_size=elite_size,
        mutation_rate=mutation_rate,
        children_size=children_size
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

    operation_data =[]
    for i in range(len(op_start)):
        for o in range(len(op_start[i])):
            operation_data.append({
                "Part": i,
                "Operation": o,
                "Start": op_start[i][o],
                "End": op_end[i][o]
            })
            

    operation_df = pd.DataFrame(operation_data)
    
    operation_df.to_excel("operation_times.xlsx", index=False)
    
    assembly_data = []
    for a in range(len(asm_start)):
        assembly_data.append({
            "Assembly": a,
            "Start": asm_start[a],
            "End": asm_end[a]
        })
    assembly_df = pd.DataFrame(assembly_data)
    
    assembly_df.to_excel("assembly_times.xlsx", index=False)
    
    print("=== Part Processing Times ===")
    for i in range(num_parts):
        for o in range(qp[0][i]):
            print(f"Part {i} - Op {o}: Start = {op_start[i][o]:.2f}, End = {op_end[i][o]:.2f}")
        print(f"  Last operation ends at: {op_end[i][qp[0][i]-1]:.2f}")
        print(f"  Inventory time before assembly: {inventory_time[i]:.2f}\n")

    print("=== Assembly Times ===")
    for a in range(num_assemblies):
        print(f"Assembly {a}: Start = {asm_start[a]:.2f}, End = {asm_end[a]:.2f}")

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    
    print(f"Elapsed time for calculation: {elapsed_time:.6f} seconds")
    
if __name__ == "__main__":
    main()
