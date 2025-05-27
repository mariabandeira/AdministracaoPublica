import pandas as pd

cadUnico_rn_2012 = pd.read_csv("cadunico_rn_2012.csv", sep=';', low_memory=False)
cadUnico_rn_2013 = pd.read_csv("cadunico_rn_2013.csv", sep=';', low_memory=False)
cadUnico_rn_2014 = pd.read_csv("cadunico_rn_2014.csv", sep=';', low_memory=False)
cadUnico_rn_2015 = pd.read_csv("cadunico_rn_2015.csv", sep=';', low_memory=False)
cadUnico_rn_2016 = pd.read_csv("cadunico_rn_2016.csv", sep=';', low_memory=False)
cadUnico_rn_2017 = pd.read_csv("cadunico_rn_2017.csv", sep=';', low_memory=False)
cadUnico_rn_2018 = pd.read_csv("cadunico_rn_2018.csv", sep=';', low_memory=False)

# Mesclando os arquivos CSV em um único DataFrame
cadunico_rn_combined = pd.concat([cadUnico_rn_2012, cadUnico_rn_2013, cadUnico_rn_2014, 
                              cadUnico_rn_2015, cadUnico_rn_2016, cadUnico_rn_2017, cadUnico_rn_2018], 
                              ignore_index=True)


cadunico_rn_combined.to_csv('cadunico_rn_combined.csv', index=False, sep=';')