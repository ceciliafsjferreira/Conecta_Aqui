import pandas as pd

df_pessoas = pd.read_csv('idosos_sp_idade.csv', sep=';')
df_familia = pd.read_csv('idosos_sp_familia.csv', sep=';')

total_geral = len(df_pessoas)
total_em_familia = len(df_familia)
sem_familia = total_geral - total_em_familia

pct_sem_familia = (sem_familia / total_geral) * 100

print(f"Total geral de idosos: {total_geral:,}")
print(f"Idosos em arranjos familiares (códigos 1 a 10): {total_em_familia:,}")
print(f"Idosos sem família / unipessoais: {sem_familia:,} ({pct_sem_familia:.2f}%)")
