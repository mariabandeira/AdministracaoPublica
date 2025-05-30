import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import altair as alt
import folium
import requests
import plotly.express as px
from shapely.geometry import shape, Point

st.set_page_config(
    page_title="Painel de Informações Bolsa Família",
    page_icon="👪",
    layout="wide",
    initial_sidebar_state="expanded")

alt.theme.enable("dark")

cadunico_rn = pd.read_csv("C:/Users/luizf/Desktop/AdministracaoPublica/CadUnico/BasesRN/cadunico_rn_clean.csv", sep=';', low_memory=False)

url = 'https://raw.githubusercontent.com/tbrugz/geodata-br/refs/heads/master/geojson/geojs-24-mun.json'
response = requests.get(url)
rn_geojson = response.json()

dados_agrupados = cadunico_rn.groupby(['cd_ibge', 'ano'], as_index=False)['marc_pbf'].sum()

with st.sidebar:
    st.title('👪 Painel de Informações Bolsa Família')
    
    year_list = [2012, 2013, 2014, 2015, 2016, 2017, 2018]
    selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)
    df_selected_year = dados_agrupados[dados_agrupados.ano == selected_year]

# MAPA
m = folium.Map(location=[-5.8, -36.5], zoom_start=3)
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

def encontrar_municipio(lat, lon, geojson):
    point = Point(lon, lat)
    for feature in geojson['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            return feature['properties']['name']
    return None

# MAPA E MÉTRICAS
col_mapa, col_info = st.columns([2, 1])

with col_mapa:
    mapa = st_folium(m, width=700, height=500)
    click_data = mapa.get('last_clicked')
    if click_data:
        lat = click_data['lat']
        lon = click_data['lng']
        municipio_nome = encontrar_municipio(lat, lon, rn_geojson)
    else:
        municipio_nome = None

if municipio_nome:
    st.write(f"Município selecionado: {municipio_nome}")
    cd_ibge_clicked = None
    for feature in rn_geojson['features']:
        if feature['properties']['name'] == municipio_nome:
            cd_ibge_clicked = feature['properties']['id']
            break
    cadunico_filtrado = cadunico_rn[cadunico_rn['cd_ibge'] == int(cd_ibge_clicked)]
else:
    cadunico_filtrado = cadunico_rn

anos = [2012, 2013, 2014, 2015, 2016, 2017, 2018]
cadunico_rn = cadunico_rn[cadunico_rn['ano'].isin(anos)]

dados_ano = cadunico_filtrado.groupby('ano').agg(
    total_familias=('id_familia', 'nunique'),
    renda_media=('vlr_renda_media_fam', 'mean'),
    familias_beneficiadas=('marc_pbf', 'sum'),
    total_beneficiarios=('marc_pbf', 'sum'),
    total_pessoas=('qtde_pessoas', 'sum')
).reset_index()

dados_selecionados = dados_ano[dados_ano['ano'] == selected_year]

with col_info:
    st.metric("Total de famílias", f"{int(dados_selecionados['total_familias'].values[0]):,}".replace(',', '.'))
    st.metric("Beneficiários Bolsa Família", f"{int(dados_selecionados['total_beneficiarios'].values[0]):,}".replace(',', '.'))
    st.metric("Renda Média (R$)", f"{dados_selecionados['renda_media'].values[0]:,.2f}".replace(',', '.'))
    st.metric("Total de Pessoas", f"{int(dados_selecionados['total_pessoas'].values[0]):,}".replace(',', '.'))

# GRÁFICO
fig = px.line(
    dados_ano,
    x='ano',
    y=['total_familias', 'familias_beneficiadas', 'renda_media'],
    markers=True,
    labels={'value': 'Quantidade', 'ano': 'Ano'},
    title='Famílias beneficiadas por ano'
)

st.plotly_chart(fig, use_container_width=True)
