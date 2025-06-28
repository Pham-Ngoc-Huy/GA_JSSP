import pandas as pd
import numpy as np

num_parts = 14
num_assemblies = 6

df_machine = pd.read_excel('src/data_large.xlsx', header=None, sheet_name="machine")
df_qp = pd.read_excel('src/data_large.xlsx', header=None, sheet_name="qp")
df_proc=pd.read_excel('src/data_large.xlsx', header=None, sheet_name="proc")
df_asm_time=pd.read_excel('src/data_large.xlsx', header=None, sheet_name="asm_time")
df_depend=pd.read_excel('src/data_large.xlsx', header=None, sheet_name="depend")

machine = np.array(df_machine)
qp = np.array(df_qp)
proc_time = np.array(df_proc)
asm_time=np.array(df_asm_time)
depend=np.array(df_depend)

# print(machine)
# print(qp)
# print(proc_time)
# print(asm_time)
# print(depend)


generations = 1000
pop_size = 150
elite_size = 20 
mutation_rate = 1