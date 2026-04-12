import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

input_file = os.path.join(script_dir, "BasesAno", "cadunico_pi_combined.csv")
cadunico_pi = pd.read_csv(input_file, sep=';', low_memory=False)

# removendo colunas que não se encontram em um formato adequado para o treinamento de ML
cadunico_pi = cadunico_pi.drop(columns=['dat_cadastramento_fam', 'dat_alteracao_fam', 'dat_atualizacao_familia', 'nom_estab_assist_saude_fam', 'cod_eas_fam', 'nom_centro_assist_fam', 'cod_centro_assist_fam', 'ind_parc_mds_fam'])

# colunas que precisam de tratamento de tipos
columns_to_convert = ['vlr_renda_media_fam', 'peso.fam']

for column in columns_to_convert:
    cadunico_pi[column] = cadunico_pi[column].replace(',', '.', regex=True).astype(float)

# repetidos_por_ano = (
#     cadunico_pi.groupby(['ano', 'id_familia'])
#     .size()
#     .reset_index(name='contagem')
# )

# removendo linhas com valores ausentes
cadunico_pi = cadunico_pi.dropna()

# identificando colunas com apenas um valor
single_value_columns = [col for col in cadunico_pi.columns if cadunico_pi[col].nunique() == 1 | 0]

# Colunas com um único valor: ['cod_especie_domic_fam', 'cod_banheiro_domic_fam', 'cod_familia_indigena_fam']

# cadunico_ba = cadunico_ba.drop(columns=single_value_columns)

print(cadunico_pi.shape)

output_file = os.path.join(script_dir, 'cadunico_pi_clean.csv')
cadunico_pi.to_csv(output_file, sep=';')