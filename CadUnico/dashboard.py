import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import joblib
import altair as alt
import folium
import requests
import plotly.express as px
from shapely.geometry import shape, Point
import os
from dotenv import load_dotenv

st.markdown("""
    <style>
        .block-container {
            padding-top: 4rem;
            padding-bottom: 4rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 100%;
        }
        .main {
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)


load_dotenv()
model_path = os.getenv("MODEL_PATH")

# Seletor de estado
st.sidebar.title("👪 Painel de Informações Bolsa Família")
estado = st.sidebar.selectbox("Selecione o estado", ["RN", "PB"])

if estado == "RN":
    data_path = os.getenv("DATA_PATH_RN")
    geojson_url = 'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-24-mun.json'
elif estado == "PB":
    data_path = os.getenv("DATA_PATH_PB")
    geojson_url = 'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-25-mun.json'

# Dados
cadunico = pd.read_csv(data_path, sep=';', low_memory=False)
cadunico = cadunico[cadunico['ano'].isin(range(2012, 2019))]
geojson = requests.get(geojson_url).json()

nomes_cidades = sorted([feature['properties']['name'] for feature in geojson['features']])
nomes_cidades.insert(0, "Todos os municípios")

selected_year = st.sidebar.selectbox('Selecione o ano', list(range(2012, 2019)), index=6)
selected_city = st.sidebar.selectbox('Selecione a cidade', nomes_cidades, index=0)
pagina = st.sidebar.radio("Selecione a página", ["Mapa e Indicadores", "Características Domiciliares", "Predição com ML"])

if selected_city != "Todos os municípios":
    cd_ibge_selected_sidebar = next(
        (f['properties']['id'] for f in geojson['features'] if f['properties']['name'] == selected_city),
        None
    )
else:
    cd_ibge_selected_sidebar = None

def encontrar_municipio(lat, lon, geojson):
    point = Point(lon, lat)
    for feature in geojson['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            return feature['properties']['name'], feature['properties']['id']
    return None, None

def exibir_mapa():
    dados_agrupados = cadunico.groupby(['cd_ibge', 'ano'], as_index=False)['marc_pbf'].sum()
    df_selected_year = dados_agrupados[dados_agrupados.ano == selected_year]
    df_selected_year['cd_ibge'] = df_selected_year['cd_ibge'].astype(str)
    marc_pbf_dict = df_selected_year.set_index('cd_ibge')['marc_pbf'].to_dict()

    for feature in geojson['features']:
        cd_ibge = feature['properties']['id']
        valor = marc_pbf_dict.get(cd_ibge, 0)
        feature['properties']['marc_pbf'] = valor

    m = folium.Map(location=[-7, -36.5], zoom_start=7)
    choropleth = folium.Choropleth(
        geo_data=geojson,
        name='choropleth',
        data=df_selected_year,
        columns=['cd_ibge', 'marc_pbf'],
        key_on='feature.properties.id',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Famílias Beneficiárias do Bolsa Família'
    ).add_to(m)

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['name', 'marc_pbf'], 
            aliases=['Município:', 'Famílias Beneficiárias: '],
            sticky=True
        )
    )

    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        mapa = st_folium(m, use_container_width=True, height=500)
    with col2:
        st.markdown("""
        ### Sobre o Bolsa Família
        O **Bolsa Família** é o principal programa de transferência de renda do Brasil, 
        destinado a apoiar famílias em situação de pobreza e extrema pobreza. 
        Ele busca garantir a elas acesso a direitos fundamentais, como saúde, educação, 
        alimentação e segurança alimentar.

        #### Beneficiários
        O programa atende milhões de famílias em todo o país. Ao interagir com o mapa, 
        você pode explorar como o programa está distribuído e qual o impacto em cada município.
        """)

        st.markdown("""
        ### Como funciona o programa?
        - **Critérios de elegibilidade**: Famílias com renda per capita abaixo de um determinado valor.
        - **Objetivos**: Erradicação da pobreza, inclusão social e melhoria nas condições de vida das famílias vulneráveis.
        """)
    return mapa

def get_municipio_selecionado(mapa, selected_city, cd_ibge_selected_sidebar):
    click_data = mapa.get('last_clicked')
    if click_data:
        municipio_nome, cd_ibge_final = encontrar_municipio(click_data['lat'], click_data['lng'], geojson)
    else:
        municipio_nome = selected_city if selected_city != "Todos os municípios" else None
        cd_ibge_final = cd_ibge_selected_sidebar
    return municipio_nome, cd_ibge_final

CB_color_cycle = ['#377eb8', '#4daf4a', '#e41a1c', '#dede00', '#a65628','#999999']

# Página 1 - Mapa e Indicadores
if pagina == "Mapa e Indicadores":
    mapa = exibir_mapa()
    municipio_nome, cd_ibge_final = get_municipio_selecionado(mapa, selected_city, cd_ibge_selected_sidebar)
    if municipio_nome:
        st.subheader(f"Município selecionado: {municipio_nome}")

    if cd_ibge_final:
        cadunico_filtrado = cadunico[cadunico['cd_ibge'].astype(str) == str(cd_ibge_final)]
    else:
        cadunico_filtrado = cadunico

    dados_ano = cadunico_filtrado.groupby('ano').agg(
        total_familias=('id_familia', 'nunique'),
        renda_media=('vlr_renda_media_fam', 'mean'),
        familias_beneficiadas=('marc_pbf', 'sum'),
        total_pessoas=('qtde_pessoas', 'sum')
    ).reset_index()

    dados_selecionados = dados_ano[dados_ano['ano'] == selected_year]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de famílias", f"{int(dados_selecionados['total_familias'].values[0]):,}".replace(",", "."))
    col2.metric("Beneficiários Bolsa Família", f"{int(dados_selecionados['familias_beneficiadas'].values[0]):,}".replace(",", "."))
    col3.metric("Renda Média (R$)", f"{dados_selecionados['renda_media'].values[0]:,.2f}".replace(",", "."))
    col4.metric("Total de Pessoas", f"{int(dados_selecionados['total_pessoas'].values[0]):,}".replace(",", "."))

    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.line(dados_ano, x='ano', y=['total_familias', 'familias_beneficiadas'], markers=True)
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.line(dados_ano, x='ano', y='renda_media', markers=True)
        st.plotly_chart(fig2, use_container_width=True)

# Página 2 - Gráficos de Características Domiciliares
if pagina == "Características Domiciliares":
    mapa = exibir_mapa()
    municipio_nome, cd_ibge_final = get_municipio_selecionado(mapa, selected_city, cd_ibge_selected_sidebar)
    if municipio_nome:
        st.subheader(f"Município selecionado: {municipio_nome}")

    st.subheader(f"Características dos Domicílios - {selected_year}")

    if cd_ibge_final:
        cad_filtro = cadunico[(cadunico['cd_ibge'] == int(cd_ibge_final)) & (cadunico['ano'] == selected_year)]
    else:
        cad_filtro = cadunico[cadunico['ano'] == selected_year]

    colunas_categorias = {
        "Forma de coleta de lixo": 'cod_destino_lixo_domic_fam',
        "Tipo de Iluminação": 'cod_iluminacao_domic_fam',
        "Calçamento": 'cod_calcamento_domic_fam',
        "Forma de Abastecimento de Água": 'cod_abaste_agua_domic_fam',
        "Forma de Escoamento": 'cod_escoa_sanitario_domic_fam',
        "Espécie do domicílio": 'cod_especie_domic_fam'
    }

    for coluna in colunas_categorias.values():
        cad_filtro[coluna] = cad_filtro[coluna].astype(str)

    col1, col2, col3 = st.columns(3)
    for i, (titulo, coluna) in enumerate(colunas_categorias.items()):
        graf = px.histogram(cad_filtro, x=coluna, title=titulo, color=coluna)
        graf.update_layout(height=400, width=500, margin=dict(t=50, b=40), legend_title_text="")
        [col1, col2, col3][i % 3].plotly_chart(graf, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_comodos = px.histogram(cad_filtro, x='qtd_comodos_domic_fam', title='Qtd. de cômodos do domicílio')
        st.plotly_chart(fig_comodos, use_container_width=True)
    with col2:
        banheiros = cad_filtro['cod_banheiro_domic_fam'].value_counts().rename({1: 'Sim', 2: 'Não'})
        fig_banheiro = px.pie(names=banheiros.index, values=banheiros.values, title="Distribuição de domicílios com banheiro")
        st.plotly_chart(fig_banheiro, use_container_width=True)

# Página 3 - Predição com ML
if pagina == "Predição com ML":
    st.subheader("Predição com Modelo de Machine Learning")

    st.markdown("Preencha os dados abaixo para prever se tem acesso ou não ao Bolsa Família:")

    classf_options = {
    'Capital': 1,
    'Região Metropolitana (RM) ou Região Integrada de Desenvolvimento (RIDE)': 2,
    'Outros': 3
    }

    cod_local_domic_fam_options = {
        'Urbanas': 1,
        'Rurais': 2
    }

    cod_material_piso_fam_options = {
        'Terra': 1,
        'Cimento': 2,
        'Madeira aproveitada': 3,
        'Madeira aparelhada': 4,
        'Cerâmica, lajota ou pedra': 5,
        'Carpete': 6,
        'Outro material': 7
    }

    cod_material_domic_fam_options = {
        'Alvenaria/tijolo com revestimento': 1,
        'Alvenaria/tijolo sem revestiment': 2,
        'Madeira aparelhada': 3,
        'Taipa revestida': 4,
        'Taipa não revestida': 5,
        'Madeira aproveitada': 6,
        'Palha': 7,
        'Outro material': 8
    }

    cod_agua_canalizada_fam_options = {
        'Sim': 1,
        'Não': 2,
    }

    cod_abaste_agua_domic_fam_options = {
        'Rede geral de distribuição': 1,
        'Poço ou nascente': 2,
        'Cisterna': 3,
        'Outra forma': 4
    }

    cod_banheiro_domic_fam_options = {
        'Sim': 1,
        'Não': 2,
    }

    cod_destino_lixo_domic_fam_options = {
        'É coletado diretamente': 1,
        'É coletado indiretamente': 2,
        'É queimado ou enterrado na propriedade': 3,
        'É jogado em terreno baldio ou logradouro (rua, avenida, etc.)': 4,
        'É jogado em rio ou mar': 5,
        'Tem outro destino': 6
    }

    cod_iluminacao_domic_fam_options = {
        'Elétrica com medidor próprio': 1,
        'Elétrica com medidor comunitário': 2,
        'Elétrica sem medidor': 3,
        'Óleo, querosene ou gás': 4,
        'Vela': 5,
        'Outra forma': 6
    }

    cod_calcamento_domic_fam_options = {
        'Total': 1,
        'Parcial': 2,
        'Não existe': 3,
    }

    ind_familia_quilombola_fam_options = {
        'Sim': 1,
        'Não': 2,
    }

    col1, col2, col3 = st.columns(3)
    with col1:
        classf = st.selectbox("Classificação da Localização", options=list(classf_options.keys()))
        vlr_renda_media_fam = st.number_input("Valor da renda média (per capita) da família", min_value=0.0, step=0.1)
        cod_local_domic_fam = st.selectbox("Características do local onde está situado o domicílio", options=list(cod_local_domic_fam_options.keys()))
        qtd_comodos_domic_fam = st.number_input('Quantidade de comodos do domicilio', min_value=0, max_value=30, value=4)
        qtd_comodos_dormitorio_fam = st.number_input('Quantidade de comodos servindo como dormitório do domicilio', min_value=0, max_value=30, value=1)
    with col2:
        cod_material_piso_fam = st.selectbox("Material predominante no piso do domicílio", options=list(cod_material_piso_fam_options.keys()))
        cod_material_domic_fam = st.selectbox("Material predominante nas paredes externas do domicílio", options=list(cod_material_domic_fam_options.keys()))
        cod_agua_canalizada_fam = st.selectbox("Domicílio tem água encanada", options=list(cod_agua_canalizada_fam_options.keys()))
        cod_abaste_agua_domic_fam = st.selectbox("Forma de abastecimento de água", options=list(cod_abaste_agua_domic_fam_options.keys()))
        cod_banheiro_domic_fam = st.selectbox("Existência de banheiro", options=list(cod_banheiro_domic_fam_options.keys()))
    with col3:
        cod_destino_lixo_domic_fam = st.selectbox("Forma de coleta do lixo", options=list(cod_destino_lixo_domic_fam_options.keys()))
        cod_iluminacao_domic_fam = st.selectbox("Tipo de iluminação", options=list(cod_iluminacao_domic_fam_options.keys()))
        cod_calcamento_domic_fam = st.selectbox("Calçamento", options=list(cod_calcamento_domic_fam_options.keys()))
        ind_familia_quilombola_fam = st.selectbox("Família quilombola", options=list(ind_familia_quilombola_fam_options.keys()))
        qtde_pessoas = st.number_input('Quantidade de pessoas utilizada no cálculo da renda per capita familiar', min_value=0, max_value=30, value=4)


    if st.button("Fazer Predição"):
        modelo = joblib.load(model_path)

        entrada = [[
            classf_options[classf],
            vlr_renda_media_fam,
            cod_local_domic_fam_options[cod_local_domic_fam],
            qtd_comodos_domic_fam,
            qtd_comodos_dormitorio_fam,
            cod_material_piso_fam_options[cod_material_piso_fam],
            cod_material_domic_fam_options[cod_material_domic_fam],
            cod_agua_canalizada_fam_options[cod_agua_canalizada_fam],
            cod_abaste_agua_domic_fam_options[cod_abaste_agua_domic_fam],
            cod_banheiro_domic_fam_options[cod_banheiro_domic_fam],
            cod_destino_lixo_domic_fam_options[cod_destino_lixo_domic_fam],
            cod_iluminacao_domic_fam_options[cod_iluminacao_domic_fam],
            cod_calcamento_domic_fam_options[cod_calcamento_domic_fam],
            ind_familia_quilombola_fam_options[ind_familia_quilombola_fam],
            qtde_pessoas
        ]]
        predicao = modelo.predict(entrada)[0]
        probas = modelo.predict_proba(entrada)[0]

        st.success(f"Resultado da Predição: **{'Não apto a receber' if predicao == 0 else 'Apto a receber'}**")
        st.info(f"Probabilidade: {probas[predicao]:.2%}")
