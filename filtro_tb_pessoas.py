import pandas as pd


# analisar colunas do dataset Pessoas_35_publico.csv e excluir as colunas não relevantes para a análise.
df_pessoas = pd.read_csv('Pessoas_35_publico.csv', sep= ';')

df_pessoas = df_pessoas.rename(columns={
                'P0120': "regiao do domicilio",
                'P0180': 'idade',
                'P0420': 'deficiencia visual',
                'P0430': 'deficiencia auditiva',
                'P0440': 'deficiencia motora',
                'P0700': 'curso mais elevado',
                'P0740': 'conclusao do curso mais elevado',
                'P1200': 'diagnostico de autismo',
                'P0370': 'filhos vivos'} )

colunas_para_remover = [ 'P0130', 'P0140', 'P0150', 'P0160', 'P0170', 'P0190', 'P0200', 'P0210', 'P0220', 'P0230', 'P0240',
                         'P0250', 'P0260', 'P0270', 'P0280', 'P0290', 'P0300', 'P0310', 'P0320', "P0330", 'P0340', 'P0350', 
                         'P0360', 'P0380', 'P0390', 'P0400', 'P0410', 'P0450', 'P0460', 'P0470', 'P0480', 'P0490', 
                         'P0500', 'P0510', 'P0520', 'P0530', 'P0540', 'P0550', 'P0560', 'P0570', 'P0580', 'P0590', 'P0600', 
                         'P0610', 'P0620', 'P0630', 'P0640', 'P0650', 'P0660', 'P0670', 'P0680', 'P0690', 'P0700', 'P0710',
                         'P0720', 'P0730', 'P0740', 'P0750', 'P0760', 'P0770', 'P0780', 'P0790', 'P0800', 'P0810', 'P0820',
                         'P0830', 'P0840', 'P0850', 'P0860', 'P0870', 'P0880', 'P0890', 'P0900', 'P0910', 'P0920', 'P0930',
                         'P0940', 'P0950', 'P0960', 'P0970', 'P0980', 'P0990', 'P1000', 'P1010', 'P1020', 'P1030', 'P1040', 
                         'P1050', 'P1060', 'P1070', 'P1080', 'P1090', 'P1100', 'P1110', 'P1120', 'P1130', 'P1140', 'P1150',
                         'P1160', 'P1170', 'P1180', 'P1190', 'P1210', 'P1220''P0690', 
                         'MP0150', 'MP0160', 'MP0170', 'MP0180', 'MP0190', 'MP0200', 'MP0210', 'MP0220', 'MP0230', 'MP0240',
                         'MP0250', 'MP0260', 'MP0270', 'MP0280', 'MP0290', 'MP0300', 'MP0310', 'MP0320', 'MP0330', 'MP0340',
                         'MP0350', 'MP0360', 'MP0370', 'MP0380', 'MP0390', 'MP0400', 'MP0410', 'MP0420', 'MP0430', 'MP0440',
                         'MP0450', 'MP0460', 'MP0470', 'MP0480', 'MP0490', 'MP0500', 'MP0510', 'MP0520', 'MP0530', 'MP0540',
                         'MP0550', 'MP0560', 'MP0570', 'MP0580', 'MP0590', 'MP0600', 'MP0610', 'MP0620', 'MP0630', 'MP0640',
                         'MP0650', 'MP0660', 'MP0670', 'MP0680', 'MP0690', 'MP0700', 'MP0710', 'MP0720', 'MP0730', 'MP0740',
                         'MP0750', 'MP0760', 'MP0770', 'MP0780', 'MP0790', 'MP0800', 'MP0810', 'MP0820', 'MP0830', 'MP0840',
                         'MP0850', 'MP0860', 'MP0870', 'MP0880', 'MP0890', 'MP0900', 'MP0910', 'MP0920', 'MP0930', 'MP0940',
                         'MP0950', 'MP0960', 'MP0970', 'MP0980', 'MP0990', 'MP1000', 'MP1010', 'MP1020', 'MP1030', 'MP1040',
                         'MP1050', 'MP1060', 'MP1070', 'MP1080', 'MP1090', 'MP1100', 'MP1110', 'MP1120', 'MP1130', 'MP1140',
                         'MP1150', 'MP1160', 'MP1170', 'MP1180', 'MP1190', 'MP1200', 'MP1210', 'MP1220'
                        ] 

df_pessoas.drop(columns=colunas_para_remover, errors='ignore', inplace=True)

colunas_uteis = [ 'regiao do domicilio', 'idade', 'deficiencia visual', 'deficiencia auditiva', 'deficiencia motora',
                  'curso mais elevado', 'conclusao do curso mais elevado', 'diagnostico de autismo', 'filhos vivos']
colunas_existentes = [col for col in colunas_uteis if col in df_pessoas.columns]
df_pessoas = df_pessoas[colunas_existentes]

# remover linhas com valores ausentes na coluna 'idade' e filtar idades válidas

df_pessoas.dropna(subset=['idade'], inplace=True)

df_pessoas['idade'] = pd.to_numeric(df_pessoas['idade'], errors = 'coerce')

df_base_demografica = df_pessoas[df_pessoas['idade'].isin(range(1, 18))].dropna(subset=['idade'])


df_idosos = df_pessoas[df_pessoas['idade'].isin ([13,14,15,16,17])]
faixas= {
    13: '60 a 64 anos',
    14: '65 a 69 anos',
    15: '70 a 74 anos',
    16: '75 a 79 anos',
    17: '80 anos ou mais'

}

df_idosos['faixa_etaria'] = df_idosos['idade'].map(faixas)

print(df_idosos['faixa_etaria'].value_counts())

# porcentagem e total de idosos em relação ao total da população do Estado de SP

total_de_idosos = df_pessoas['idade'].isin([13,14,15,16,17]).sum()
percent = (total_de_idosos /len(df_base_demografica))* 100

print(f'Total de idosos: {total_de_idosos}. {percent:.2f}% da população total do Estado de SP.')

# salvar o dataset

df_idosos.to_csv('idosos_sp_idade.csv', sep=';', index=False, encoding='utf-8-sig')