import pandas as pd

cadunico_rn = pd.read_csv("cadunico_rn_combined.csv", sep=';', low_memory=False)

# removendo colunas que não se encontram em um formato adequado para o treinamento de ML
cadunico_rn = cadunico_rn.drop(columns=['dat_cadastramento_fam', 'dat_alteracao_fam', 'dat_atualizacao_familia', 'nom_estab_assist_saude_fam', 'cod_eas_fam', 'nom_centro_assist_fam', 'cod_centro_assist_fam', 'ind_parc_mds_fam'])

# colunas que precisam de tratamento de tipos
columns_to_convert = ['vlr_renda_media_fam', 'peso.fam']

for column in columns_to_convert:
    cadunico_rn[column] = cadunico_rn[column].replace(',', '.', regex=True).astype(float)

repetidos_por_ano = (
    cadunico_rn.groupby(['ano', 'id_familia'])
    .size()
    .reset_index(name='contagem')
)

# removendo linhas com valores ausentes
cadunico_rn = cadunico_rn.dropna()

# identificando colunas com apenas um valor
single_value_columns = [col for col in cadunico_rn.columns if cadunico_rn[col].nunique() == 1 | 0]

# Colunas com um único valor: ['cod_especie_domic_fam', 'cod_banheiro_domic_fam', 'cod_familia_indigena_fam']

# cadunico_rn = cadunico_rn.drop(columns=single_value_columns)

print(cadunico_rn.shape)

cadunico_rn.to_csv('cadunico_rn_clean.csv', sep=';')