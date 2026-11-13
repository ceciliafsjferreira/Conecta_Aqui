import pandas as pd

df_familia = pd.read_csv('Familia_35_publico.csv', sep=';')

df_familia = df_familia.rename(columns={'F0180': 'idade','F0190': 'instrucao', "F0210": 'familia_tipologia'})

df_familia.dropna(subset=['instrucao', 'familia_tipologia', 'idade'], inplace=True)

df_familia[['idade', 'instrucao', 'familia_tipologia']] = df_familia[['idade', 'instrucao', 'familia_tipologia']].apply(pd.to_numeric, errors='coerce')


df_idosos_familia = df_familia[
    (df_familia['idade'].isin([13, 14, 15, 16, 17])) &
    (df_familia['instrucao'].isin([1, 2, 3, 4])) &
    (df_familia['familia_tipologia'].isin([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
].dropna(subset=['idade', 'instrucao', 'familia_tipologia']).copy()


mapa_instrucao = {
    1: 'sem instrução e ensino fundamental incompleto',
    2: 'ensino fundamental completo e médio incompleto',
    3: 'médio completo e superior incompleto',
    4: 'superior completo'
}

mapa_tipologia = {
    1: 'casal sem filhos',
    2: 'casal sem filhos e com parentes',
    3: 'casal com filhos',
    4: 'casal com filhos e com parentes',
    5: 'mulher sem conjuge e com filhos',
    6: 'mulher sem conjuge e com filhos e com parentes',
    7: 'homem sem conjuge e com filhos',
    8: 'homem sem conjuge e com filhos e com parentes',
    9: 'mulher ou homem com dois ou mais conjuges',
    10: 'outras tipologias de familia'
}

df_idosos_familia['instrucao_desc'] = df_idosos_familia['instrucao'].map(mapa_instrucao)
df_idosos_familia['tipologia_desc'] = df_idosos_familia['familia_tipologia'].map(mapa_tipologia)

df_idosos_familia = df_idosos_familia[['idade', 'instrucao_desc', 'tipologia_desc']]

print(df_idosos_familia['instrucao_desc'].value_counts())
print("\n", df_idosos_familia['tipologia_desc'].value_counts())

df_idosos_familia.to_csv('idosos_familia_sp_tratado.csv', sep=';', index=False, encoding='utf-8-sig')

total_antes = df_familia['idade'].isin([13, 14, 15, 16, 17]).sum()
total_depois = len(df_idosos_familia)

print(f"Total de idosos na base Família (geral): {total_antes}")


