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
from shapely.geometry import shape
import gdown
import unicodedata

@st.cache_data
def load_data(data_path, filename):
    # Se data_path é um caminho local existente, usa diretamente
    if os.path.exists(data_path):
        return pd.read_csv(data_path, sep=';', low_memory=False, index_col=0)
    
    # Se é uma URL, faz o download
    if not os.path.exists(filename):
        gdown.download(data_path, filename, quiet=False)
    return pd.read_csv(filename, sep=';', low_memory=False, index_col=0)

if 'cd_ibge_mapa' not in st.session_state:
    st.session_state['cd_ibge_mapa'] = None

st.markdown("""
<style>
.block-container { padding-top: 4rem; padding-left: 2rem; padding-right: 2rem; max-width: 100%; }
            
.main { 
    padding-left: 2rem; 
    padding-right: 2rem; 
}
            
.st-emotion-cache-1r1cntt {
    padding-bottom: 0rem !important;
}

/* Entire sidebar */
section[data-testid="stSidebar"] > div:first-child {
    height: 100%;
}

/* Main sidebar block */
section[data-testid="stSidebar"] .stVerticalBlock {
    flex: 1;
    display: flex;
    flex-direction: column;
}
            
/* Main sidebar content */
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    height: 100%;
    display: flex;
    flex-direction: column;
}

/* Footer pushed to bottom */
.sidebar-footer-card {
    margin-top: auto;
    padding-top: 1rem;
    padding-bottom: 0rem;
}

/* Logo styling */
.logo-card {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 15px;
}

.logo-card img {
    width: 42px;
    height: auto;
}

.footer-title {
    font-weight: bold;
    margin-bottom: 0px;
}

</style>
""", unsafe_allow_html=True)



load_dotenv()
model_path = os.getenv("MODEL_PATH")
model_path_reduced = os.getenv("MODEL_PATH_REDUCED")

# Seletor de estado
st.sidebar.title("👪 Painel de Informações Bolsa Família")
estado = st.sidebar.selectbox("Selecione o estado", ["RN", "PB", "BA", "CE", "PI"])

if estado == "RN":
    data_path = os.getenv("DATA_PATH_RN")
    filename = "cadunico_RN.csv"
    geojson_url = 'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-24-mun.json'
elif estado == "PB":
    data_path = os.getenv("DATA_PATH_PB")
    filename = "cadunico_PB.csv"
    geojson_url = 'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-25-mun.json'
elif estado == "BA":
    data_path = os.getenv("DATA_PATH_BA")
    filename = "cadunico_BA.csv"
    geojson_url = 'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-29-mun.json'
elif estado == "CE":
    data_path = os.getenv("DATA_PATH_CE")
    filename = "cadunico_CE_clean.csv"
    geojson_url = 'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-23-mun.json'
elif estado == "PI":
    data_path = os.getenv("DATA_PATH_PI") or os.path.join(os.path.dirname(__file__), "BaesesPI", "cadunico_pi_clean.csv")
    filename = "cadunico_PI_clean.csv"
    geojson_url = 'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-22-mun.json'    

# Dados
cadunico = load_data(data_path, filename)
cadunico = cadunico[cadunico['ano'].isin(range(2012, 2019))]
geojson = requests.get(geojson_url).json()

def normalize_str(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    ).lower()

nomes_cidades = sorted(
    [feature['properties']['name'] for feature in geojson['features']],
    key=normalize_str
)
nomes_cidades.insert(0, "Todos os municípios")

selected_year = st.sidebar.selectbox('Selecione o ano', list(range(2012, 2019)), index=6)

if "update_city_from_map" in st.session_state and st.session_state.update_city_from_map:
    # Atualize o valor do dropdown antes de criar o widget
    selected_city = st.session_state.city_from_map
    st.session_state.update_city_from_map = False
else:
    selected_city = st.session_state.get("selected_city", "Todos os municípios")

selected_city = st.sidebar.selectbox(
    'Selecione a cidade',
    nomes_cidades,
    index=nomes_cidades.index(selected_city) if selected_city in nomes_cidades else 0,
    key="selected_city"
)

pagina = st.sidebar.radio(
    "Selecione a página",
    ["Mapa e Indicadores", "Características Domiciliares", "Predição com ML", "Piauí - Visão Geral"]
)

st.sidebar.markdown("""
<div class="sidebar-footer-card">                    
<div class="footer-title">Desenvolvimento</div><br>
<div class="logo-card">
    <img src="https://www.ufpb.br/aci/contents/imagens/diversos/logoufpb.png/@@images/8e95c80b-dae1-489d-b384-52e1d08f2d13.png">
    <div>
        <b>UFPB</b><br>
        <small>Universidade Federal da Paraíba</small>
    </div>
</div>
<div class="logo-card">
    <img src="https://assecom.ufersa.edu.br/wp-content/uploads/sites/24/2014/09/PNG-bras%C3%A3o-Ufersa.png">
    <div>
        <b>UFERSA</b><br>
        <small>Universidade Federal Rural do Semi-Árido</small>
    </div>
</div>
</div>                    
""", unsafe_allow_html=True)

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

def filtrar_geojson_por_cidade(geojson, cd_ibge):
    if not cd_ibge:
        return geojson
    features = [f for f in geojson['features'] if f['properties']['id'] == cd_ibge]
    return {'type': 'FeatureCollection', 'features': features}

def get_centro_municipio(geojson, cd_ibge):
    for feature in geojson['features']:
        if feature['properties']['id'] == cd_ibge:
            geom = shape(feature['geometry'])
            lon, lat = geom.centroid.xy
            return [lat[0], lon[0]]
    # Valor padrão por estado
    if estado == "BA":
        return [-13, -55]
    elif estado == "PB":
        return [-7.5, -37]
    elif estado == "CE":
        return [-5.5, -39.5]
    elif estado == "PI":
        return [-7.2, -42.7]
    else:  # RN
        return [-7, -36.5]


def exibir_mapa(cd_ibge=None):
    dados_agrupados = cadunico.groupby(['cd_ibge', 'ano'], as_index=False)['marc_pbf'].sum()
    df_selected_year = dados_agrupados[dados_agrupados.ano == selected_year]
    df_selected_year['cd_ibge'] = df_selected_year['cd_ibge'].astype(str)
    marc_pbf_dict = df_selected_year.set_index('cd_ibge')['marc_pbf'].to_dict()

    geojson_filtrado = filtrar_geojson_por_cidade(geojson, cd_ibge)
    if cd_ibge:
        df_selected_year = df_selected_year[df_selected_year['cd_ibge'] == str(cd_ibge)]
        centro = get_centro_municipio(geojson, cd_ibge)
        zoom = 10  # Ajuste o nível de zoom conforme necessário
    else:
        if estado == "BA":
            centro = [-13, -55]
        elif estado == "PB":
            centro = [-7.5, -37]
        elif estado == "CE":
            centro = [-5.5, -39.5]
        elif estado == "PI":
            centro = [-7.2, -42.7]
        else:  # RN
            centro = [-7, -36.5]
        zoom = 7

    for feature in geojson_filtrado['features']:
        cd_ibge_f = feature['properties']['id']
        valor = marc_pbf_dict.get(cd_ibge_f, 0)
        feature['properties']['marc_pbf'] = valor

    m = folium.Map(location=centro, zoom_start=zoom)
    choropleth = folium.Choropleth(
        geo_data=geojson_filtrado,
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
        #### Como funciona o programa?
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
    st.subheader(f"Mapa e Indicadores - {selected_year}") 

    # Atualiza o cd_ibge_mapa conforme o dropdown
    if st.session_state.selected_city != "Todos os municípios":
        cd_ibge_selected = next(
            (f['properties']['id'] for f in geojson['features'] if f['properties']['name'] == st.session_state.selected_city),
            None
        )
        st.session_state['cd_ibge_mapa'] = cd_ibge_selected
    else:
        st.session_state['cd_ibge_mapa'] = None

    # Exibe o mapa filtrado
    mapa = exibir_mapa(st.session_state['cd_ibge_mapa'])

    # Se clicou no mapa, atualize o session_state e o dropdown
    click_data = mapa.get('last_clicked')
    if click_data:
        municipio_nome, cd_ibge_final = encontrar_municipio(click_data['lat'], click_data['lng'], geojson)
        if cd_ibge_final:
            st.session_state['cd_ibge_mapa'] = cd_ibge_final
            # Atualiza o dropdown para o nome da cidade clicada, usando flags auxiliares
            st.session_state.city_from_map = municipio_nome
            st.session_state.update_city_from_map = True
            st.rerun()
    else:
        municipio_nome = st.session_state.selected_city if st.session_state.selected_city != "Todos os municípios" else None
        cd_ibge_final = st.session_state['cd_ibge_mapa']

    #  cd_ibge_final para filtrar os dados
    if municipio_nome:
        st.subheader(f"Município selecionado: {municipio_nome} ({cd_ibge_final}) - {estado}")

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
    st.subheader(f"Características dos Domicílios - {selected_year}")

    # Atualiza o cd_ibge_mapa conforme o dropdown
    if st.session_state.selected_city != "Todos os municípios":
        cd_ibge_selected = next(
            (f['properties']['id'] for f in geojson['features'] if f['properties']['name'] == st.session_state.selected_city),
            None
        )
        st.session_state['cd_ibge_mapa'] = cd_ibge_selected
    else:
        st.session_state['cd_ibge_mapa'] = None

    # Exibe o mapa filtrado
    mapa = exibir_mapa(st.session_state['cd_ibge_mapa'])

    # Se clicou no mapa, atualize o session_state e o dropdown
    click_data = mapa.get('last_clicked')
    if click_data:
        municipio_nome, cd_ibge_final = encontrar_municipio(click_data['lat'], click_data['lng'], geojson)
        if cd_ibge_final:
            st.session_state['cd_ibge_mapa'] = cd_ibge_final
            # Atualiza o dropdown para o nome da cidade clicada, usando flags auxiliares
            st.session_state.city_from_map = municipio_nome
            st.session_state.update_city_from_map = True
            st.rerun()
    else:
        municipio_nome = st.session_state.selected_city if st.session_state.selected_city != "Todos os municípios" else None
        cd_ibge_final = st.session_state['cd_ibge_mapa']


    if municipio_nome:
        st.subheader(f"Município selecionado: {municipio_nome} - {estado}")

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

    mapeamentos = {
        'cod_destino_lixo_domic_fam': {
            1: "Coletado diretamente",
            2: "Coletado indiretamente",
            3: "Queimado ou enterrado",
            4: "Jogado em terreno baldio",
            5: "Jogado em rio ou mar",
            6: "Outro destino"
        },
        'cod_iluminacao_domic_fam': {
            1: "Elétrica com medidor próprio",
            2: "Elétrica com medidor comunitário",
            3: "Elétrica sem medidor",
            4: "Óleo, querosene ou gás",
            5: "Vela",
            6: "Outra forma"
        },
        'cod_calcamento_domic_fam': {
            1: "Total",
            2: "Parcial",
            3: "Não existe"
        },
        'cod_abaste_agua_domic_fam': {
            1: "Rede geral",
            2: "Poço ou nascente",
            3: "Cisterna",
            4: "Outra forma"
        },
        'cod_escoa_sanitario_domic_fam': {
            1: "Rede coletora",
            2: "Fossa séptica",
            3: "Fossa rudimentar",
            4: "Vala a céu aberto",
            5: "Direto para um rio, lago ou mar",
            6: "Outra forma"
        },
        'cod_especie_domic_fam': {
            1: "Particular Permanente",
            2: "Particular improvisado",
            3: "Coletivo"
        }
    }

    for coluna, mapeamento in mapeamentos.items():
        if coluna in cad_filtro.columns:
            cad_filtro[coluna] = cad_filtro[coluna].replace(mapeamento)

    col1, col2, col3 = st.columns(3)
    for i, (titulo, coluna) in enumerate(colunas_categorias.items()):
        graf = px.histogram(cad_filtro, x=coluna, title=titulo, color=coluna)
        graf.update_layout(height=400, width=500, margin=dict(t=50, b=40), legend_title_text="")
        graf.update_xaxes(title=None)
        graf.update_yaxes(title=None) 
        [col1, col2, col3][i % 3].plotly_chart(graf, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_comodos = px.histogram(cad_filtro, x='qtd_comodos_domic_fam', title='Qtd. de cômodos do domicílio')
        fig_comodos.update_layout(legend_title_text="")
        fig_comodos.update_xaxes(title=None)
        fig_comodos.update_yaxes(title=None)
        st.plotly_chart(fig_comodos, use_container_width=True)
    with col2:
        banheiros = cad_filtro['cod_banheiro_domic_fam'].value_counts().rename({1: 'Sim', 2: 'Não'})
        fig_banheiro = px.pie(names=banheiros.index, values=banheiros.values, title="Distribuição de domicílios com banheiro")
        st.plotly_chart(fig_banheiro, use_container_width=True)  

# Página 3 - Predição com ML reduzido
if pagina == "Predição com ML":
    st.subheader("Predição com Modelo de Machine Learning")

    st.markdown("Preencha os dados abaixo para prever se tem acesso ou não ao Bolsa Família:")

    st.markdown("""
    <span style='font-size:14px; user-select:none;'><em>
    O modelo de Machine Learning utilizado foi o xgboost, treinado com dados do Cadastro Único (CadÚnico) dos anos entre 2016 e 2018.
    </em></span>
    """, unsafe_allow_html=True)

    cod_material_piso_fam_options = {
        'Terra': 1,
        'Cimento': 2,
        'Madeira aproveitada': 3,
        'Madeira aparelhada': 4,
        'Cerâmica, lajota ou pedra': 5,
        'Carpete': 6,
        'Outro material': 7
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

    cod_calcamento_domic_fam_options = {
        'Total': 1,
        'Parcial': 2,
        'Não existe': 3,
    }

    col1, col2, col3 = st.columns(3)
    with col1:
        vlr_renda_media_fam = st.number_input("Valor da renda média (per capita) da família", min_value=0.0, step=0.1)
        qtd_comodos_domic_fam = st.number_input('Quantidade de comodos do domicilio', min_value=0, max_value=30, value=4)
        cod_material_piso_fam = st.selectbox("Material predominante no piso do domicílio", options=list(cod_material_piso_fam_options.keys()))
    with col2:
        cod_agua_canalizada_fam = st.selectbox("Domicílio tem água encanada", options=list(cod_agua_canalizada_fam_options.keys()))
        cod_abaste_agua_domic_fam = st.selectbox("Forma de abastecimento de água", options=list(cod_abaste_agua_domic_fam_options.keys()))
    with col3:
        cod_calcamento_domic_fam = st.selectbox("Calçamento", options=list(cod_calcamento_domic_fam_options.keys()))
        qtde_pessoas = st.number_input('Quantidade de pessoas utilizada no cálculo da renda per capita familiar', min_value=0, max_value=30, value=4)


    if st.button("Fazer Predição"):
        modelo = joblib.load(model_path_reduced)

        entrada = [[
            vlr_renda_media_fam,
            qtd_comodos_domic_fam,
            cod_material_piso_fam_options[cod_material_piso_fam],
            cod_agua_canalizada_fam_options[cod_agua_canalizada_fam],
            cod_abaste_agua_domic_fam_options[cod_abaste_agua_domic_fam],
            cod_calcamento_domic_fam_options[cod_calcamento_domic_fam],
            qtde_pessoas
        ]]
        predicao = modelo.predict(entrada)[0]
        probas = modelo.predict_proba(entrada)[0]


        st.success(f"Resultado da Predição: **{'Não apto a receber' if predicao == 0 else 'Apto a receber'}**")

st.markdown("""
<style>
.block-container {
    padding-top: 4rem;
    padding-bottom: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-footer", style="text-align: center; font-size: 16px;">
    © 2025 Universidade Federal da Paraíba • Universidade Federal Rural do Semi-Árido • Todos os direitos reservados
</div>
""", unsafe_allow_html=True)