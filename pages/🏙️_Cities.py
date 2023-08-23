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

st.set_page_config(page_title = 'Visão Citi', page_icon = '🏙️', layout = 'wide')

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
    # Preparando os nomes
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

# ===============================================
# Função de Desenhar o gráfico de barras Plotly
# ===============================================
def grafico_barras_top10(df_1):
    ''' Esta função tem a responsabilidade de desenhar
    
    Tipo de desenho:
    1. Contagem das Top 10 Cidades com mais Restaurantes na Base de Dados
    2. Desenhar o gráfico de barras Plotly com Contagem das Top 10 Cidades com mais Restaurantes na Base de Dados
    3. Adicionar rótulos aos eixos x e y
    4. Personalizar o texto no balão de informações (hovertext)
    5. Personalizar o texto das barras para incluir o nome do país
    6. Centralizar o título
    7. Exibir na tela
    '''    
    # Contagem das Top 10 Cidades com mais Restaurantes na Base de Dados
    cidades_mais_restaurantes = df_1.loc[:, ['Country_Code', 'City', 'Restaurant_Name']].groupby(['Country_Code', 'City']).nunique().sort_values(by = 'Restaurant_Name', ascending = False).head(10).reset_index()
    
    # Desenhar o gráfico de barras Plotly
    fig = px.bar(cidades_mais_restaurantes, x = 'City', y = 'Restaurant_Name', color = 'Country_Code', hover_data = ['Country_Code', 'Restaurant_Name'])
    
    # Adicionar rótulos aos eixos x e y
    fig.update_xaxes(title_text = 'Cidades')
    fig.update_yaxes(title_text = 'Quantidade de Restaurantes')
    
    # Personalizar o texto no balão de informações (hovertext)
    fig.update_traces(hovertemplate = 'País: %{customdata[0]}<br>Cidade: %{x}<br>Quantidade de Restaurantes: %{y}')
    
    # Personalizar o texto das barras para incluir o nome do país
    fig.update_traces(texttemplate = '%{y:.2f}') # .2f indica duas casas decimais
    
    # Centralizar o título
    fig.update_layout(title_text = 'As Top 10 Cidades com mais Restaurantes na Base de Dados', title_x = 0.30)  # title_x = 0.5 centraliza o título
    
    # Exibir na tela
    st.plotly_chart(fig)
    
    return fig

# ===============================================
# Função de Desenhar o gráfico de barras Plotly
# ===============================================
def grafico_barras_avaliacao4(df_1):
    ''' Esta função tem a responsabilidade de desenhar
    
    Tipo de desenho:
    1. Avaliações acima de 4
    2. Contagem dos Top 7 Restaurantes com média de avaliação acima de 4
    3. Desenhar o gráfico de barras Plotly
    4. Adicionar rótulos aos eixos x e y
    5. Personalizar o texto no balão de informações (hovertext)
    6. Personalizar o texto das barras para incluir o nome do país
    7. Centralizar o título
    8. Exibir na tela
    '''
    # Avaliações acima de 4
    avaliacao_acima_4 = df_1[df_1.loc[:, 'Aggregate_rating'] > 4]
    
    # Contagem dos Top 7 Restaurantes com média de avaliação acima de 4
    restaurantes_avaliacao_4 = avaliacao_acima_4.loc[:, ['Restaurant_Name', 'Aggregate_rating', 'Country_Code', 'City', 'Votes']].groupby(['Country_Code', 'City']).count().sort_values(by = 'Votes', ascending = False).head(7).reset_index()
    
    # Desenhar o gráfico de barras Plotly
    fig = px.bar(restaurantes_avaliacao_4, x = 'City', y = 'Restaurant_Name', color = 'Country_Code', hover_data = ['Country_Code', 'Restaurant_Name'])
    
    # Adicionar rótulos aos eixos x e y
    fig.update_xaxes(title_text = 'Cidades')
    fig.update_yaxes(title_text = 'Quantidade de Restaurantes')
    
    # Personalizar o texto no balão de informações (hovertext)
    fig.update_traces(hovertemplate = 'País: %{customdata[0]}<br>Cidade: %{x}<br>Quantidade de Restaurantes: %{y}')
    
    # Personalizar o texto das barras para incluir o nome do país
    fig.update_traces(texttemplate = '%{y:.2f}') # .2f indica duas casas decimais
    
    # Centralizar o título
    fig.update_layout(title_text = 'As Top 7 Cidades com Restaurantes com média de avaliação acima de 4', title_x = 0.30)  # title_x = 0.5 centraliza o título
          
    # Exibir na tela
    st.plotly_chart(fig)
    
    return fig

# ===============================================
# Função de Desenhar o gráfico de barras Plotly
# ===============================================
def grafico_barras_avaliacao2_5(df_1):
    ''' Esta função tem a responsabilidade de desenhar
    
    Tipo de desenho:
    1. Avaliações abaixo de 2.5
    2. Contagem dos Top 7 Restaurantes com média de avaliação abaixo de 2.5
    3. Desenhar o gráfico de barras Plotly
    4. Adicionar rótulos aos eixos x e y
    5. Personalizar o texto no balão de informações (hovertext)
    6. Personalizar o texto das barras para incluir o nome do país
    7. Centralizar o título
    8. Exibir na tela
    '''    
    # Avaliações abaixo de 2.5
    avaliacao_abaixo_2 = df_1[df_1.loc[:, 'Aggregate_rating'] < 2.5]
    
    # Contagem dos Top 7 Restaurantes com média de avaliação abaixo de 2.5
    restaurantes_avaliacao_2 = avaliacao_abaixo_2.loc[:, ['Country_Code', 'City', 'Restaurant_Name', 'Aggregate_rating', 'Votes']].groupby(['Aggregate_rating','Country_Code', 'City']).nunique().sort_values(by = 'Votes', ascending = False).head(7).reset_index()
    
    # Desenhar o gráfico de barras Plotly
    fig = px.bar(restaurantes_avaliacao_2, x = 'City', y = 'Restaurant_Name', color = 'Country_Code', hover_data = ['Country_Code', 'Restaurant_Name'])
    
    # Adicionar rótulos aos eixos x e y
    fig.update_xaxes(title_text = 'Cidades')
    fig.update_yaxes(title_text = 'Quantidade de Restaurantes')
    
    # Personalizar o texto no balão de informações (hovertext)
    fig.update_traces(hovertemplate = 'País: %{customdata[0]}<br>Cidade: %{x}<br>Quantidade de Restaurantes: %{y}')
    
    # Personalizar o texto das barras para incluir o nome do país
    fig.update_traces(texttemplate = '%{y:.2f}') # .2f indica duas casas decimais
    
    # Centralizar o título
    fig.update_layout(title_text = 'As Top 7 Cidades com Restaurantes com média de avaliação abaixo de 2.5', title_x = 0.30)  # title_x = 0.5 centraliza o título
    
    # Exibir na tela
    st.plotly_chart(fig)
    return fig

# ===============================================
# Função de Desenhar o gráfico de barras Plotly
# ===============================================
def grafico_barras_culinarios(df_1):
    ''' Esta função tem a responsabilidade de desenhar
    
    Tipo de desenho:
    1. Contagem dos Top 10 Restaurantes com Tipos Culinários Distintos
    2. Desenhar o gráfico de barras Plotly
    3. Adicionar rótulos aos eixos x e y
    4. Personalizar o texto no balão de informações (hovertext)
    5. Personalizar o texto das barras para incluir o nome do país
    6. Centralizar o título
    7. Exibir na tela
    '''     
    # Contagem dos Top 10 Restaurantes com Tipos Culinários Distintos
    tipos_culinarios_distintos = df_1.loc[:, ['Restaurant_Name', 'Cuisines', 'Aggregate_rating', 'Country_Code', 'City', 'Votes']].groupby(['Cuisines', 'Country_Code', 'City']).nunique().sort_values(by = 'Aggregate_rating', ascending = False).head(10).reset_index()
    
    # Desenhar o gráfico de barras Plotly
    fig = px.bar(tipos_culinarios_distintos, x = 'City', y = 'Restaurant_Name', color = 'Country_Code', hover_data = ['Country_Code', 'Restaurant_Name'])
    
    # Adicionar rótulos aos eixos x e y
    fig.update_xaxes(title_text = 'Cidades')
    fig.update_yaxes(title_text = 'Quantidade de Tipos Culinários Únicos')
    
    # Personalizar o texto no balão de informações (hovertext)
    fig.update_traces(hovertemplate = 'País: %{customdata[0]}<br>Cidade: %{x}<br>Quantidade de Restaurantes: %{y}')
    
    # Personalizar o texto das barras para incluir o nome do país
    fig.update_traces(texttemplate = '%{y:.2f}') # .2f indica duas casas decimais
    
    # Centralizar o título
    fig.update_layout(title_text = 'As Top 10 Cidades com mais Restaurantes com Tipos Culinários Únicos', title_x = 0.30)  # title_x = 0.5 centraliza o título
    
    # Exibir na tela
    st.plotly_chart(fig)
    
    return fig
# ================================================================================ Sidebar ================================================================================
# =================================================
# Função da Barra Lateral no Streamlit
# =================================================
def barra_lateral(df_1):
    ''' Esta função tem a responsabilidade de criação
    
    Tipo de criação:
    1. Texto filtro
    2. Multselect nomes dos países
    3. Filtro por país
    ''' 
    # Texto filtro
    st.sidebar.markdown('## Filtros')

    # Multselect nomes dos países
    paises_options = st.sidebar.multiselect(
        'Escolha os países que deseja visualizar os restaurantes',
        ['India', 'Australia', 'Brazil', 'Canada', 'Indonesia', 'New Zeland', 'Philippines', 'Qatar', 'Singapure', 'South Africa', 'Sri Lanka', 'Turkey', 'United Arab Emirates', 'England', 'United States of America'],
        default = ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])
    
    # Filtro por país
    linhas_selecionadas = df_1['Country_Code'].isin(paises_options)
    df_1 = df_1.loc[linhas_selecionadas, : ]

    return df_1
# ================================================================== Inicio da Estrutura lógica do código ==================================================================
# =================================================
# Preparando o dataset
# =================================================
df_1 = preparando_dataset(df_1)

# =================================================
# Barra Lateral no Streamlit
# =================================================
df_1 = barra_lateral(df_1)

# Título da pagina
st.markdown('# 🏙️ Visão Cidades')        

with st.container():
    # Criar um layout com 1 coluna
    col1 = st.columns(1)
    
    with col1[0]:
        # Desenhar o gráfico de barras Plotly com Contagem das Top 10 Cidades com mais Restaurantes na Base de Dados
        fig = grafico_barras_top10(df_1)

# Container do topo Visão Gerencial
with st.container():
    # Criar um layout de coluna com duas colunas
    col1, col2 = st.columns(2, gap = "large")

    with col1:
        # Desenhar o gráfico de barras Plotly Avaliações acima de 4
        fig = grafico_barras_avaliacao4(df_1)
        
    with col2: 
        # Desenhar o gráfico de barras Plotly Avaliações acima de 4
        fig = grafico_barras_avaliacao2_5(df_1)

with st.container():
    # Criar um layout com 1 coluna
    col1 = st.columns(1)
    
    with col1[0]:
        # Desenhar o gráfico de barras Plotly Contagem dos Top 10 Restaurantes com Tipos Culinários Distintos
        fig = grafico_barras_culinarios(df_1)

