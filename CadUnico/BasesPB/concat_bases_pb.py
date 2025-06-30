import pandas as pd

anos = range(2012, 2019)
bases_pb = {}

for ano in anos:
    df = pd.read_csv(f"cadunico_pb_{ano}.csv", sep=';', low_memory=False)
    df["ano"] = ano
    bases_pb[ano] = df

# Mesclando os arquivos CSV em um único DataFrame
cadunico_pb_combined = pd.concat(bases_pb.values(), ignore_index=True)

cadunico_pb_combined.to_csv('cadunico_pb_combined.csv', index=False, sep=';')