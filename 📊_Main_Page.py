# Libraries
from haversine import haversine as hs
from datetime import datetime
from streamlit_folium import folium_static

# Bibliotecas necessárias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
import folium as fl
import folium.plugins as plugins
import streamlit as st
from PIL import Image

# ========================================================================= Configuração da pagina =========================================================================

st.set_page_config(page_title = 'Main Page', page_icon = '📊', layout = 'wide')

# =================================================
# Import dataframe
# =================================================
df = pd.read_csv('dataset/zomato.csv')

# =================================================
# Copiando o DataFrame original
# =================================================
df_1 = df.copy()

# ================================================================================ Funções ================================================================================

# =================================================
# Função que prepara o dataset
# =================================================
def preparando_dataset(df_1):
    ''' Esta função tem a responsabilidade de organisar o dataframe

        Tipos de organização:
        1. Preparando os nomes das colunas
        2. Renomeando colunas do DataFrame
        3. Converter a coluna de float para str
        4. Converter a coluna de float para int
        
        Tipos de Limpeza do dataframe:
        1. Categorizar, inicialmente, todos os restaurantes somente por um tipo de culinária
        2. Trocando valor da coluna exemplo do 'nan' para 'NaN'
        3. Limpando os 'NaN' das linhas da coluna
        4. Copia das colunas com as linhas_selecionadas limpas dos 'NaN'
        5. Converter código do país para nome do país usando o dicionário COUNTRIES
    '''
    # =================================================
    # Preparando os nomes das colunas
    # =================================================
    # Preparando os nomes
    nome_colunas = {'Restaurant ID': 'Restaurant_ID',
                    'Restaurant Name' : 'Restaurant_Name',
                    'Country Code' : 'Country_Code',
                    'Locality Verbose' : 'Locality_Verbose',
                    'Average Cost for two' : 'Average_Cost_for_two',
                    'Has Table booking' : 'Has_Table_booking',
                    'Has Online delivery' : 'Has_Online_delivery',
                    'Is delivering now' : 'Is_delivering_now',
                    'Switch to order menu' : 'Switch_to_order_menu',
                    'Price range' : 'Price_range',
                    'Aggregate rating' : 'Aggregate_rating',
                    'Rating color' : 'Rating_color',
                    'Rating text' : 'Rating_text',
                    }
    
    # =================================================
    # Renomeando colunas do DataFrame
    # =================================================
    # Renomear as colunas
    df_1.rename(columns = nome_colunas, inplace=True)    
    
    # =================================================
    # Converter a coluna de float para str 
    # =================================================
    # Converter a coluna de float para str
    df_1['Cuisines'] = df_1['Cuisines'].astype(str)

    # =================================================
    # Converter a coluna de float para int
    # =================================================    
    df_1['Country_Code'] = df_1['Country_Code'].astype(int)
    df_1['Price_range'] = df_1['Price_range'].astype(int)

    # =================================================
    # Limpeza do dataframe
    # =================================================
    # Categorizar, inicialmente, todos os restaurantes somente por um tipo de culinária
    df_1['Cuisines'] = df_1.loc[:, 'Cuisines'].apply(lambda x: x.split(",")[0])
    
    # Trocando valor da coluna exemplo do 'nan' para 'NaN'
    df_1['Cuisines'] = df_1['Cuisines'].replace('nan', 'NaN')
    
    # Limpando os 'NaN' das linhas da coluna
    linhas_selecionadas = (df_1['Cuisines'] != 'NaN')
    
    # Copia das colunas com as linhas_selecionadas limpas dos 'NaN'
    df_1 = df_1.loc[linhas_selecionadas, : ].copy()
    
    # Converter código do país para nome do país usando o dicionário COUNTRIES
    df_1['Country_Code'] = df_1['Country_Code'].map(COUNTRIES)

    return df_1

# =================================================
# Funções preenchimento do nome dos países
# =================================================
# Preenchimento do nome dos países
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
    ''' Esta função tem a responsabilidade de converção
    
    Tipo de converção:
    1. Converter os código dos países para os nomes dos países
    '''
    return COUNTRIES[country_id]

# =================================================
# Funções criação do Tipo de Categoria de Comida
# =================================================
# Criação do Tipo de Categoria de Comida
def create_price_tye(price_range):
    ''' Esta função tem a responsabilidade de criação do Tipo
    
    Tipo de criação:
    1. Criação do Tipo de Categoria de Comida
    '''
    
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
      
# =================================================
# Funções criação do nome das Cores
# =================================================
# Criação do nome das Cores
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
    ''' Esta função tem a responsabilidade de criação
    
    Tipo de criação:
    1. criação do nome das Cores
    '''    
    return COLORS[color_code]

# ==============================================================
# Função de Converção do DataFrame em arquivo csv para download
# ==============================================================
# download do DataFrame
@st.cache
def convert_df(df_1):
    ''' Esta função tem a responsabilidade de converção
    
    Tipo de converção:
    1. Converter o dataframe em arquivo csv para download
    '''
    csv = df_1.to_csv(index = False).encode('utf-8')
    return csv

# =================================================
# Função de contagem total 
# =================================================
def contagem_total(df_1):
    ''' Esta função tem a responsabilidade de contagem total
    
    Tipo de contagem:
    1. Quantidade de restaurantes cadastrado        
    2. Quantidade de países cadastrado
    3. Quantidade de cidades cadastrado
    4. Quantidade de avaliações cadastrado
    5. Quantidade de culinaria cadastrado
    6. Formatação da pontuação
    7. Exibir na tela
    '''    
    # Quantidade de restaurantes cadastrado
    quantidade_restaurantes = df_1['Restaurant_ID'].nunique()
    
    # Formatação da pontuação
    numero_formatado = f"{quantidade_restaurantes:,}".replace(",", ".")
    
    # Exibir na tela
    col1.metric(label = 'Restaurantes: Cadastrado', value = numero_formatado)
    
    # Quantidade de países cadastrado
    quantidade_paises = df_1['Country_Code'].nunique()
    
    # Exibir na tela
    col2.metric(label = 'Países: Cadastrado', value = quantidade_paises)
    
    # Quantidade de cidades cadastrado
    quantidade_cidades = df_1['City'].nunique()
    
    # Exibir na tela
    col3.metric(label = 'Restaurantes: Cadastrado', value = quantidade_cidades)

    # Quantidade de avaliações cadastrado
    quantidade_avaliacoes = df_1['Votes'].sum()
    
    # Formatação da pontuação
    numero_formatado = f"{quantidade_avaliacoes:,}".replace(",", ".")

    # Exibir na tela
    col4.metric(label = 'Avaliacoes: Feitas', value = numero_formatado)

    # Quantidade de culinaria cadastrado
    quantidade_culinaria = df_1['Cuisines'].nunique()

    # Exibir na tela
    col5.metric(label = 'Culinaria: Oferecidas', value = quantidade_culinaria)
    
    return df_1

# =================================================
# Função de montar o mapa
# =================================================
def montar_mapa(df_1):
    ''' Esta função tem a responsabilidade de montar o mapa
    
    Tipo de montagem:
    1. Criar o objeto de mapa
    2. Plugin de Agrupamento
    3. Selecionar as colunas 'Latitude' e 'Longitude'
    4. Iterar sobre as linhas do DataFrame
    5. Formatando o preço com o símbolo da moeda e apropriado para dois
    6. Adicionar informações no popup do marcador
    7. Coloca a ícone de casinha
    8. Exibir na tela
    '''    
    # Criar o objeto de mapa
    mapa = fl.Map(zoom_start = 1)
    
    # Plugin de Agrupamento
    marker_cluster = plugins.MarkerCluster().add_to(mapa)
    
    # Selecionar as colunas 'Latitude' e 'Longitude'
    info_mapa = df_1_aux.loc[:,['Latitude', 'Longitude', 'Restaurant_Name', 'Average_Cost_for_two', 'Country_Code', 'City', 'Cuisines', 'Aggregate_rating', 'Currency', 'Rating_color']]
    
    # Iterar sobre as linhas do DataFrame
    for location, row in info_mapa.iterrows():
        latitude = row['Latitude']
        longitude = row['Longitude']
        restaurante = row['Restaurant_Name']
        culinaria = row['Cuisines']
        avaliacoes = row['Aggregate_rating']
        country_id = row['Country_Code']
        price_range = row['Average_Cost_for_two']
        currency_symbols = row['Currency']
        color_code = row['Rating_color']
    
        # Formatando o preço com o símbolo da moeda e apropriado para dois
        formatted_price = f'{price_range:.2f}'.replace('.', ',') + f' ({currency_symbols}) {culinaria} para dois'
    
        # Adicionar informações no popup do marcador
        popup_content = (
            f'<div style="width: 300px;">'
            f'<strong>{restaurante}</strong>'
            f'<br><br>Price: {formatted_price}'
            f'<br>Type: {culinaria}'
            f'<br>Aggregate Rating: {avaliacoes}/5.0'
            f'</div>'
        )
        # Coloca a ícone de casinha
        fl.Marker(
            [latitude, longitude],
            popup = popup_content,
            icon = fl.Icon(color = color_name(color_code), icon ='home')  
        ).add_to(marker_cluster)
    
    # Exibir na tela
    folium_static(mapa, width = 865, height = 500)

    return mapa

# ================================================================================ Sidebar ================================================================================
# =================================================
# Função da Barra Lateral no Streamlit
# =================================================
def barra_lateral(df_1):
    ''' Esta função tem a responsabilidade de criação
    
    Tipo de criação:
    1. Carregar a imagem do logo
    2. Criar colunas para colocar a imagem e o texto lado a lado
    3. Coluna 1: Exibir a imagem do logo
    4. Coluna 2: Exibir o texto ao lado da imagem
    5. Divisa da Seleção de data limite
    6. Texto filtros
    7. Multiselect com nomes dos países
    8. Divisa da Seleção de data limite
    9. Texto dados tratados
    10. Preparando o download DataFrame
    11. Filtra por país
    '''    
    # Carregar a imagem do logo
    image_path = 'pages/logo.png'
    image = Image.open(image_path)
    
    # Criar colunas para colocar a imagem e o texto lado a lado
    col1, col2 = st.sidebar.columns([1, 3])
    
    # Coluna 1: Exibir a imagem do logo
    col1.image(image, width = 60)
    
    # Coluna 2: Exibir o texto ao lado da imagem
    col2.markdown('# Fome Zero')
    
    # Divisa da Seleção de data limite
    st.sidebar.markdown('''____''')

    # Texto filtros
    st.sidebar.markdown('## Filtros')

    # Multiselect com nomes dos países
    paises_options = st.sidebar.multiselect(
        'Escolha os países que deseja visualizar os restaurantes',
        ['India', 'Australia', 'Brazil', 'Canada', 'Indonesia', 'New Zeland', 'Philippines', 'Qatar', 'Singapure', 'South Africa', 'Sri Lanka', 'Turkey', 'United Arab Emirates', 'England', 'United States of America'],
        default = ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])
    
    # Divisa da Seleção de data limite
    st.sidebar.markdown('''____''')

    # Texto dados tratados
    st.sidebar.markdown('Dados Tratados')
    
    # Preparando o download DataFrame 
    st.sidebar.download_button(label = 'Download',
                                   data = 'data.csv',
                                   file_name = 'data.csv',
                                   mime = 'application/octet-stream')
    
    # Filtra por país
    linhas_selecionadas = df_1['Country_Code'].isin(paises_options)
    df_1_aux = df_1.loc[linhas_selecionadas, : ]

    return df_1_aux

# ================================================================== Inicio da Estrutura lógica do código ==================================================================
# =================================================
# Preparando o dataset
# =================================================
df_1 = preparando_dataset(df_1)

# =================================================
# Barra Lateral no Streamlit
# =================================================
df_1_aux = barra_lateral(df_1)

st.markdown('## Fome Zero!')

st.markdown('### O Melhor Lugar para Encontrar seu mais novo Restaurante Favorito!')

st.markdown('#### Temos as seguintes marcas dentro da nossa plataforma:')

# Container do topo Visão Gerencial
with st.container():

    col1, col2, col3, col4, col5 = st.columns(5, gap = 'large')
    
    with col1:     
        # Quantidade de restaurantes, países, cidades, avaliações e culinaria cadastrado        
        df_1 = contagem_total(df_1)
        
# Container do fundo Visão Geografica
with st.container():
    # Montar o mapa
    mapa = montar_mapa(df_1)
