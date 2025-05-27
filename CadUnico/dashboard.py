import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import altair as alt
import folium
import requests
import plotly.express as px

st.set_page_config(
    page_title="Painel de Informações Bolsa Família",
    page_icon="👪",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

cadunico_rn = pd.read_csv("C:/Users/User/Downloads/duda/AdmPublica/AdministracaoPublica/CadUnico/BasesRN/cadunico_rn_clean.csv", sep=';', low_memory=False)

# mapa interativo
url = 'https://raw.githubusercontent.com/tbrugz/geodata-br/refs/heads/master/geojson/geojs-24-mun.json'

response = requests.get(url)
rn_geojson = response.json()

# Agrupar os dados por código do município e somar os valores de marc_pbf
dados_agrupados = cadunico_rn.groupby(['cd_ibge', 'ano'], as_index=False)['marc_pbf'].sum()

with st.sidebar:
    st.title('👪 Painel de Informações Bolsa Família')
    
    year_list = [2012, 2013, 2014, 2015, 2016, 2017, 2018]
    
    selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)
    df_selected_year = dados_agrupados[dados_agrupados.ano == selected_year]

# Criar o mapa base
m = folium.Map(location=[-5.8, -36.5], zoom_start=3)
#Criar a camada Choroplet
folium.Choropleth(
    geo_data=rn_geojson,
    name='choropleth',
    data=dados_agrupados,
    columns=['cd_ibge', 'marc_pbf'],
    key_on='feature.properties.id',
    range_color=(0, max(df_selected_year.marc_pbf)),
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Famílias Beneficiárias do Bolsa Família'
).add_to(m)
# Visualizar
m

mapa = st_folium(m, width=700, height=500)

