import pandas as pd

df = pd.read_csv('idosos_com_clusters.csv', sep=';')


mapa_idade = {
    13: '60 a 64 anos',
    14: '65 a 69 anos',
    15: '70 a 74 anos',
    16: '75 a 79 anos',
    17: '80 anos ou mais'
}
df['faixa_etaria'] = df['idade'].map(mapa_idade)

print("=== DISTRIBUIÇÃO DE IDADE POR CLUSTER (%) ===")
pct_idade = pd.crosstab(df['cluster'], df['faixa_etaria'], normalize='index') * 100
print(pct_idade.round(1), "\n")

print("=== PERCENTUAL COM DEFICIÊNCIA POR CLUSTER (%) ===")
cols_score = [c for c in df.columns if 'defic' in c.lower()]

tabela_def = pd.DataFrame()
for col in cols_score:
    nome_limpo = col.replace('_score', '').replace('_', ' ').title()
    tabela_def[nome_limpo + ' (%)'] = (df.groupby('cluster')[col].apply(lambda x: (x > 0).mean() * 100)).round(1)

print(tabela_def, "\n")

print("=== PERCENTUAL EM ÁREA RURAL POR CLUSTER (%) ===")
pct_rural = (df.groupby('cluster')['eh_rural'].mean() * 100).round(1)
print(pct_rural)