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
    initial_sidebar_state="expanded"
)

alt.theme.enable("dark")

cadunico_rn = pd.read_csv("/workspaces/AdministracaoPublica/CadUnico/BasesRN/cadunico_rn_clean.csv", sep=';', low_memory=False)
cadunico_rn = cadunico_rn[cadunico_rn['ano'].isin(range(2012, 2019))]

url = 'https://raw.githubusercontent.com/tbrugz/geodata-br/refs/heads/master/geojson/geojs-24-mun.json'
rn_geojson = requests.get(url).json()

# Extrai os nomes das cidades do GeoJSON
nomes_cidades = sorted([feature['properties']['name'] for feature in rn_geojson['features']])
nomes_cidades.insert(0, "Todos os municípios")

with st.sidebar:
    st.title('👪 Painel de Informações Bolsa Família')
    selected_year = st.selectbox('Selecione o ano', list(range(2012, 2019)), index=6)
    selected_city = st.selectbox('Selecione a cidade', nomes_cidades, index=0)
    pagina = st.radio("Selecione a página", ["Mapa e Indicadores", "Características Domiciliares"])

# Pegamos o código IBGE da cidade selecionada (a menos que seja "Todos os municípios")
if selected_city != "Todos os municípios":
    cd_ibge_selected_sidebar = next(
        (f['properties']['id'] for f in rn_geojson['features'] if f['properties']['name'] == selected_city),
        None
    )
else:
    cd_ibge_selected_sidebar = None

dados_agrupados = cadunico_rn.groupby(['cd_ibge', 'ano'], as_index=False)['marc_pbf'].sum()
df_selected_year = dados_agrupados[dados_agrupados.ano == selected_year]

# Garante que o código IBGE seja string
df_selected_year['cd_ibge'] = df_selected_year['cd_ibge'].astype(str)

# Cria dicionário de valores
marc_pbf_dict = df_selected_year.set_index('cd_ibge')['marc_pbf'].to_dict()

# Adicionar campo `marc_pbf` às propriedades do GeoJSON
for feature in rn_geojson['features']:
    cd_ibge = feature['properties']['id']
    valor = marc_pbf_dict.get(cd_ibge, 0)  # Padrão: 0 se não encontrado
    feature['properties']['marc_pbf'] = valor

# Mapa
m = folium.Map(location=[-5.8, -36.5], zoom_start=8)

choropleth = folium.Choropleth(
    geo_data=rn_geojson,
    name='choropleth',
    data=df_selected_year,
    columns=['cd_ibge', 'marc_pbf'],
    key_on='feature.properties.id',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Famílias Beneficiárias do Bolsa Família'
).add_to(m)

# Adicionar tooltip diretamente à camada do choropleth
choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(
        fields=['name', 'marc_pbf'], 
        aliases=['Município:', 'Famílias Beneficiárias: '],
        sticky=True
    )
)

# Função para encontrar município
def encontrar_municipio(lat, lon, geojson):
    point = Point(lon, lat)
    for feature in geojson['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            return feature['properties']['name'], feature['properties']['id']
    return None, None

# Exibir mapa e capturar clique
mapa = st_folium(m, use_container_width=True, height=500)

# Clique no mapa tem prioridade
click_data = mapa.get('last_clicked')
if click_data:
    municipio_nome, cd_ibge_final = encontrar_municipio(click_data['lat'], click_data['lng'], rn_geojson)
else:
    municipio_nome = selected_city if selected_city != "Todos os municípios" else None
    cd_ibge_final = cd_ibge_selected_sidebar


# Página 1 - Mapa e Indicadores
if pagina == "Mapa e Indicadores":
    if municipio_nome:
        st.subheader(f"Município selecionado: {municipio_nome}")

    # Filtragem dos dados conforme município clicado
    if cd_ibge_final:
        cadunico_filtrado = cadunico_rn[cadunico_rn['cd_ibge'].astype(str) == str(cd_ibge_final)]
    else:
        cadunico_filtrado = cadunico_rn  

    # Agrupamento dos dados por ano
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

    # Gráficos de evolução
    st.markdown("### 📈 Evolução Anual dos Indicadores")
    
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.line(
            dados_ano,
            x='ano',
            y=['total_familias', 'familias_beneficiadas'],
            markers=True,
            labels={'value': 'Quantidade', 'ano': 'Ano'},
            title='Famílias'
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.line(
            dados_ano,
            x='ano',
            y=['renda_media'],
            markers=True,
            labels={'value': 'Valor (R$)', 'ano': 'Ano'},
            title='Renda Média'
        )
        st.plotly_chart(fig2, use_container_width=True)

# Página 2 - Gráficos de Características Domiciliares
if pagina == "Características Domiciliares":
    if municipio_nome:
        st.subheader(f"Município selecionado: {municipio_nome}")

    st.subheader(f"Características dos Domicílios - {selected_year}")
    if cd_ibge_clicked:
        cad_filtro = cadunico_rn[(cadunico_rn['cd_ibge'] == int(cd_ibge_clicked)) & (cadunico_rn['ano'] == selected_year)]
    else:
        cad_filtro = cadunico_rn[cadunico_rn['ano'] == selected_year]

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
        graf.update_layout(height=400, width=500, margin=dict(t=50, b=40))
        [col1, col2, col3][i % 3].plotly_chart(graf, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Quantidade de cômodos por ano")
        fig_comodos = px.histogram(cad_filtro, x='qtd_comodos_domic_fam', title='Qtd. de cômodos do domicílio')
        st.plotly_chart(fig_comodos, use_container_width=True)

    with col2:
        st.subheader("Possui Banheiro")
        banheiros = cad_filtro['cod_banheiro_domic_fam'].value_counts().rename({1: 'Sim', 2: 'Não'})
        fig_banheiro = px.pie(
            names=banheiros.index,
            values=banheiros.values,
            title="Distribuição de domicílios com banheiro"
        )
        st.plotly_chart(fig_banheiro, use_container_width=True)
