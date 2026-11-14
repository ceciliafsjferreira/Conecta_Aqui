import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# Preparando a base de dados para a formação dos clusters

df = pd.read_csv('idosos_sp_idade.csv', sep = ';')

cols_def = ['deficiencia visual', 'deficiencia auditiva', 'deficiencia motora']
for col in cols_def:
    def_col = pd.to_numeric(df[col], errors = 'coerce')
    df = df[def_col.isin([1,2, 3, 4])]

mapa_severidade = { 4:0, 3:1, 2:2, 1:3}
for col in cols_def:
    df[col] = df[col].map(mapa_severidade)

regiao_num = pd.to_numeric(df['regiao do domicilio'], errors = 'coerce')
df['eh_rural'] = regiao_num.apply(lambda x: 1 if x == 2 else 0)

colunas_cluster = ['idade', 'deficiencia visual', 'deficiencia auditiva',
                  'deficiencia motora', 'eh_rural' ]

df_cluster = df[colunas_cluster].dropna()
df_cluster.to_csv('base_pronta_cluster.csv', sep=';', index=False)
print(f"Pronto! Tabela salva com {len(df_cluster):,} idosos prontos para o modelo.")

# Metodo do cotovelo para definir o número de clusters

df = pd.read_csv('base_pronta_cluster.csv', sep=';')

scaler = StandardScaler()
dados_padronizados = scaler.fit_transform(df)

inercia = []
quantidades = [2, 3, 4, 5, 6]

for k in quantidades:
    modelo = KMeans(n_clusters=k, random_state=42, n_init=10)
    modelo.fit(dados_padronizados)
    inercia.append(modelo.inertia_)

plt.style.use('dark_background')
plt.figure(figsize=(8, 4))
plt.plot(quantidades, inercia, marker='o', color='#00a8ff', linewidth=2)
plt.title('Método do Cotovelo - Escolha da Quantidade de Clusters', fontweight='bold')
plt.xlabel('Número de Grupos (Clusters)')
plt.ylabel('Dispersão Interna (Inércia)')
plt.xticks(quantidades)
plt.grid(alpha=0.2)

plt.tight_layout()
plt.savefig('grafico_cotovelo.png', dpi=300)
plt.close()

print("Gráfico salvo como 'grafico_cotovelo.png'! Abra a imagem para vermos onde a linha dobra.")

# Tamanho dos Clusters

scaler = StandardScaler()
dados_padronizados = scaler.fit_transform(df)

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(dados_padronizados)

print("=== TAMANHO DE CADA CLUSTER (%) ===")
print((df['cluster'].value_counts(normalize=True) * 100).round(2), "\n")

print("=== PERFIL MÉDIO DE CADA CLUSTER ===")
resumo = df.groupby('cluster').mean().round(2)
print(resumo)

df.to_csv('idosos_com_clusters.csv', sep=';', index=False)
print("\nArquivo 'idosos_com_clusters.csv' salvo com sucesso!")

