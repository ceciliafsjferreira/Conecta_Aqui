import pandas as pd


# analisar colunas do dataset Domicilios_35_publico.csv e excluir as colunas não relevantes para a análise.

df_acesso = pd.read_csv('Domicilios_35_publico.csv', sep= ';')

df_acesso = df_acesso.rename(columns={'D0180': 'idade','D0310': 'acesso_a_internet'})

df_acesso.dropna(subset=['acesso_a_internet', 'idade'], inplace=True)

df_acesso['idade'] = pd.to_numeric(df_acesso['idade'], errors = 'coerce')
df_acesso['acesso_a_internet'] = pd.to_numeric(df_acesso['acesso_a_internet'], errors = 'coerce')

df_idosos_domicilio = df_acesso[df_acesso['idade'].isin ([13,14,15,16,17]) &
                                (df_acesso['acesso_a_internet'].isin([1,2]))
                                ].dropna(subset=['idade', 'acesso_a_internet']).copy()

df_idosos_domicilio['resultado'] = df_idosos_domicilio['acesso_a_internet'].map({1: 'Sim', 2: 'Não'})
print(df_idosos_domicilio['resultado'].value_counts())

percent = (df_idosos_domicilio['resultado'].value_counts(normalize=True) * 100).round(2)
print(f'o percentual de idosos com acesso à internet é: {percent.get("Sim")}%')

df_idosos_domicilio.to_csv('idosos_sp_internet.csv', sep=';', index=False, encoding='utf-8-sig')

