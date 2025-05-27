import pandas as pd

anos = range(2012, 2019)
bases_rn = {}

for ano in anos:
    df = pd.read_csv(f"cadunico_rn_{ano}.csv", sep=';', low_memory=False)
    df["ano"] = ano
    bases_rn[ano] = df

# Mesclando os arquivos CSV em um único DataFrame
cadunico_rn_combined = pd.concat(bases_rn.values(), ignore_index=True)

cadunico_rn_combined.to_csv('cadunico_rn_combined.csv', index=False, sep=';')