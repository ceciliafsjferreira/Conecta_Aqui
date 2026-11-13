import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


plt.style.use('dark_background')
cor_principal = '#111184'
cor_secundaria = '#00a8ff'

df_pessoas = pd.read_csv('idosos_sp_idade.csv', sep=';')
df_domicilios = pd.read_csv('idosos_sp_internet.csv', sep=';')
df_familia = pd.read_csv('idosos_sp_familia.csv', sep=';')

for nome, df in [('Pessoas', df_pessoas), ('Domicílios', df_domicilios), ('Famílias', df_familia)]:
    print(f"=== {nome} ({len(df):,} linhas) ===")
    print("Colunas:", list(df.columns), "\n")

mapa_idade = {
    13: '60 a 64 anos',
    14: '65 a 69 anos',
    15: '70 a 74 anos',
    16: '75 a 79 anos',
    17: '80 anos ou mais'
}


print("=" * 60)
print("1. DOMICÍLIOS: ACESSO À INTERNET POR FAIXA ETÁRIA (%)")
print("=" * 60)

df_domicilios['faixa_etaria'] = df_domicilios['idade'].map(mapa_idade)
ct_internet = pd.crosstab(df_domicilios['faixa_etaria'], df_domicilios['resultado'], normalize='index') * 100
print(ct_internet.round(2), "\n")


ax1 = ct_internet[['Sim', 'Não']].plot(kind='bar', stacked=True, figsize=(10, 5), color=[cor_principal, '#4a4a4a'])
plt.title('Acesso à Internet nos Domicílios de Idosos por Faixa Etária (SP)', fontweight='bold')
plt.ylabel('Percentual (%)')
plt.xlabel('')
plt.xticks(rotation=0)

for container in ax1.containers:
    ax1.bar_label(container, fmt='%.1f%%', label_type='center', color='white', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('eda_internet_idade.png', dpi=300)
plt.close()


print("=" * 60)
print("2. FAMÍLIAS: ESCOLARIDADE POR TIPOLOGIA FAMILIAR (%)")
print("=" * 60)

ct_familia = pd.crosstab(df_familia['tipologia_desc'], df_familia['instrucao_desc'], normalize='index') * 100
print(ct_familia.round(2), "\n")


top_tipologias = df_familia['tipologia_desc'].value_counts().head(6).index
ct_familia_top = ct_familia.loc[top_tipologias]

ax2 = ct_familia_top.plot(
    kind='barh',
    stacked=True,
    figsize=(12, 6),
    color=['#111184', '#00a8ff', '#5c7cfa', '#7f8c8d']
)
plt.title('Escolaridade dos Idosos nas Principais Tipologias Familiares (SP)', fontweight='bold')
plt.xlabel('Percentual (%)')
plt.ylabel('')
plt.legend(title='Nível de Instrução', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.savefig('eda_familia_instrucao.png', dpi=300)
plt.close()


print("=" * 60)
print("3. PESSOAS: PERFIL INDIVIDUAL, DEFICIÊNCIAS E REGIÃO")
print("=" * 60)

if pd.api.types.is_numeric_dtype(df_pessoas['idade']):
    df_pessoas['faixa_etaria'] = df_pessoas['idade'].map(mapa_idade)
else:
    df_pessoas['faixa_etaria'] = df_pessoas['idade']

cols_def = [c for c in df_pessoas.columns if 'defic' in c.lower()]
for col in cols_def:
    print(f"--- Prevalência de {col} por Faixa Etária (%) ---")
    ct_def = pd.crosstab(df_pessoas['faixa_etaria'], df_pessoas[col], normalize='index') * 100
    print(ct_def.round(2), "\n")

mapa_regiao = {
    1: 'Área urbana de alta densidade',
    2: 'Área urbana de baixa densidade',
    3: 'Núcleo urbano',
    5: 'Povoado',
    6: 'Núcleo rural',
    7: 'Lugarejo',
    8: 'Área rural (exclusive aglomerados)'
}

df_pessoas['regiao_desc'] = pd.to_numeric(df_pessoas['regiao do domicilio'], errors='coerce').map(mapa_regiao)
dist_regiao = (df_pessoas['regiao_desc'].value_counts(normalize=True) * 100).round(2)

# 2. Plota o gráfico horizontal correto (Texto no Y, Percentual no X)
plt.figure(figsize=(11, 5))
ax_reg = sns.barplot(x=dist_regiao.values, y=dist_regiao.index, orient='h', color=cor_secundaria)
plt.title('Distribuição dos Idosos por Situação do Setor (SP)', fontweight='bold')
plt.xlabel('Percentual (%)')
plt.ylabel('')
plt.xlim(0, 98)  # Dá folga na direita para o rótulo 84.78% não cortar

for container in ax_reg.containers:
    ax_reg.bar_label(container, fmt='%.2f%%', padding=5, color='white', fontweight='bold')

plt.tight_layout()
plt.savefig('eda_regiao_domicilio.png', dpi=300)
plt.close()

contagem_idade = df_pessoas['faixa_etaria'].value_counts().reindex(mapa_idade.values())

plt.figure(figsize=(9, 5))
ax4 = sns.barplot(x=contagem_idade.index, y=contagem_idade.values, color=cor_secundaria)
plt.title('Distribuição da População Idosa por Faixa Etária (SP)', fontweight='bold')
plt.xlabel('')
plt.ylabel('Quantidade de Idosos')

for container in ax4.containers:
    ax4.bar_label(container, fmt='{:,.0f}', padding=3, color='white', fontweight='bold')

plt.tight_layout()
plt.savefig('eda_distribuicao_etaria.png', dpi=300)
plt.close()


# ==============================================================================
# 5. GRÁFICO DE DEFICIÊNCIAS POR FAIXA ETÁRIA (DICIONÁRIO P0420, P0430, P0440)
# ==============================================================================
cols_def = [c for c in df_pessoas.columns if 'defic' in c.lower()]
dados_def = {}

for col in cols_def:
    serie_valida = pd.to_numeric(df_pessoas[col], errors='coerce')
    serie_valida = serie_valida[serie_valida.isin([1, 2, 3, 4])]

    ct = pd.crosstab(df_pessoas.loc[serie_valida.index, 'faixa_etaria'], serie_valida, normalize='index') * 100
    

    codigos_com_dificuldade = [c for c in [1, 2, 3] if c in ct.columns]
    
    nome_limpo = col.replace('_', ' ').title()
    dados_def[nome_limpo] = ct[codigos_com_dificuldade].sum(axis=1)

df_plot_def = pd.DataFrame(dados_def).reindex(mapa_idade.values())

ax_def = df_plot_def.plot(
    kind='bar',
    figsize=(12, 6),
    width=0.8,
    color=['#111184', '#00a8ff', '#5c7cfa'][:len(cols_def)]
)

plt.title('Idosos com Algum Grau de Dificuldade Visual, Auditiva ou Motora por Idade (SP)', fontweight='bold', fontsize=12, pad=15)
plt.xlabel('')
plt.ylabel('Percentual de Idosos (%)', fontsize=11)
plt.xticks(rotation=0)
plt.legend(title='Tipo de Deficiência', bbox_to_anchor=(1.01, 1), loc='upper left')

for container in ax_def.containers:
    ax_def.bar_label(container, fmt='%.1f%%', padding=3, color='white', fontweight='bold', fontsize=8)

plt.tight_layout()
plt.savefig('eda_deficiencias_idade.png', dpi=300)
plt.close()

print("Gráfico de deficiências atualizado salvo com sucesso!")

print("Gráfico de deficiências salvo como 'eda_deficiencias_idade.png'!")



print("Análise Exploratória concluída! Os 4 gráficos (.png) foram salvos na pasta.")