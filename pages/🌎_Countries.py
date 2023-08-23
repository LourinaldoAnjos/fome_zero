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

st.set_page_config(page_title = 'Visão Countries', page_icon = 'pages/globo_mundo.png', layout = 'wide')

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

# =================================================
# Funções criação do Gráfico de barras
# =================================================
def grafico_barras_paises(df_1):
    ''' Esta função tem a responsabilidade de exibir
    
    Tipo de exibição:
    1. Contagem de restaurantes registrados por país
    2. Desenhar o gráfico de barras Plotly
    3. Adicionar rótulos aos eixos x e y
    4. Personalizar o texto no balão de informações (hovertext)
    5. Personalizar o texto nas barras com duas casas decimais e substituir ponto por vírgula
    6. Centralizar o título
    7. Exibir na tela
    '''    
    # Contagem de restaurantes registrados por país
    quantidade_restaurantes_paises = df_1.loc[:, ['Restaurant_Name', 'Country_Code']].groupby('Country_Code').count().sort_values(by='Restaurant_Name', ascending=False).reset_index()
    
    # Desenhar o gráfico de barras Plotly
    fig = px.bar(quantidade_restaurantes_paises, x = 'Country_Code', y = 'Restaurant_Name')
    
    # Adicionar rótulos aos eixos x e y
    fig.update_xaxes(title_text = 'País')
    fig.update_yaxes(title_text = 'Quantidade de Restaurantes')
    
    # Personalizar o texto no balão de informações (hovertext)
    fig.update_traces(hovertemplate = 'País: %{x}<br>Quantidade de Restaurantes: %{y}')
    
    # Personalizar o texto nas barras com duas casas decimais e substituir ponto por vírgula
    fig.update_traces(texttemplate='%{y:.0f}')  # .0f indica zero casas decimais
    
    # Centralizar o título
    fig.update_layout(title_text = 'Quantidade de Restaurantes Registrado por País', title_x = 0.30)  # title_x = 0.5 centraliza o título
    
    # Exibir na tela
    st.plotly_chart(fig)
    return fig

# =================================================
# Funções criação do Gráfico de barras
# =================================================
def grafico_barras_cidades(df_1):
    ''' Esta função tem a responsabilidade de exibir
    
    Tipo de exibição:
    1. Contagem de cidades registrados por país
    2. Desenhar o gráfico de barras Plotly
    3. Adicionar rótulos aos eixos x e y
    4. Personalizar o texto no balão de informações (hovertext)
    5. Personalizar o texto nas barras com duas casas decimais e substituir ponto por vírgula
    6. Centralizar o título
    7. Exibir na tela
    '''    
    # Contagem de cidades registrados por país
    quantidade_cidades_paises = df_1.loc[:, ['Country_Code', 'City']].groupby('Country_Code').nunique().sort_values(by = 'City', ascending = False).reset_index()
    
    # Desenhar o gráfico de barras Plotly
    fig = px.bar(quantidade_cidades_paises, x = 'Country_Code', y = 'City')
    
    # Adicionar rótulos aos eixos x e y
    fig.update_xaxes(title_text = 'País')
    fig.update_yaxes(title_text = 'Quantidade de Cidades')
    
    # Personalizar o texto no balão de informações (hovertext)
    fig.update_traces(hovertemplate = 'País: %{x}<br>Quantidade de Cidades: %{y}')
    
    # Personalizar o texto nas barras com duas casas decimais e substituir ponto por vírgula
    fig.update_traces(texttemplate = '%{y:.0f}')  # .0f indica zero casas decimais
    
    # Centralizar o título
    fig.update_layout(title_text = 'Quantidade de Cidades Resgistrados por País', title_x = 0.30)  # title_x = 0.5 centraliza o título
    
    # Exibir na tela
    st.plotly_chart(fig)

    return fig

# =================================================================================
# Funções criação de Gráficos de barras com contagem de avaliações feitas por país
# =================================================================================
def graficos_barras_avaliacoes(df_1):
    ''' Esta função tem a responsabilidade de exibir
    
    Tipo de exibição:
    1. Contagem de avaliações feitas por país
    2. Desenhar o gráfico de barras Plotly
    3. Adicionar rótulos aos eixos x e y
    4. Personalizar o texto no balão de informações (hovertext)
    5. Personalizar o texto nas barras com duas casas decimais e substituir ponto por vírgula
    6. Centralizar o título
    7. Exibir na tela
    '''     
    # Contagem de avaliações feitas por país
    avaliacoes_feitas_paises = df_1.loc[:, ['Country_Code', 'Votes']].groupby('Country_Code').mean().sort_values(by = 'Votes', ascending = False).reset_index()
    
    # Desenhar o gráfico de barras Plotly
    fig = px.bar(avaliacoes_feitas_paises, x = 'Country_Code', y = 'Votes')
    
    # Adicionar rótulos aos eixos x e y
    fig.update_xaxes(title_text = 'País')
    fig.update_yaxes(title_text = 'Quantidade de Avaliações')
    
    # Personalizar o texto no balão de informações (hovertext)
    fig.update_traces(hovertemplate = 'País: %{x}<br>Quantidade de Avaliações: %{y}')
    
    # Personalizar o texto nas barras com duas casas decimais e substituir ponto por vírgula
    fig.update_traces(texttemplate='%{y:.2f}')  # .2f indica duas casas decimais
    
    # Centralizar o título
    fig.update_layout(title_text = 'Quantidade de Avaliações Resgistrados por País', title_x = 0.30)  # title_x = 0.5 centraliza o título
    
    # Exibir na tela
    st.plotly_chart(fig)
    
    return fig

# =======================================================================
# Funções criação de Gráficos de barras prato para duas pessoas por país
# =======================================================================
def graficos_barras_pratos(df_1): 
    ''' Esta função tem a responsabilidade de exibir
    
    Tipo de exibição:
    1. Contagem de avaliações feitas por país
    2. Desenhar o gráfico de barras Plotly
    3. Adicionar rótulos aos eixos x e y
    4. Personalizar o texto no balão de informações (hovertext)
    5. Personalizar o texto nas barras com duas casas decimais e substituir ponto por vírgula
    6. Centralizar o título
    7. Exibir na tela
    '''    
    # Contagem média de preço de prato para duas pessoas por país
    preco_prato_duas_pessoas = df_1.loc[:, ['Country_Code', 'Average_Cost_for_two']].groupby(['Country_Code']).mean().sort_values(by = 'Average_Cost_for_two', ascending = False).reset_index()
    
    # Desenhar o gráfico de barras Plotly
    fig = px.bar(preco_prato_duas_pessoas, x = 'Country_Code', y = 'Average_Cost_for_two')
    
    # Adicionar rótulos aos eixos x e y
    fig.update_xaxes(title_text = 'País')
    fig.update_yaxes(title_text = 'Preço de Prato para Duas Pessoas')
    
    # Personalizar o texto no balão de informações (hovertext)
    fig.update_traces(hovertemplate = 'País: %{x}<br>Preço de Prato para Duas Pessoas: %{y}')
    
    # Personalizar o texto nas barras com duas casas decimais e substituir ponto por vírgula
    fig.update_traces(texttemplate='%{y:.2f}')  # .2f indica duas casas decimais
    
    # Centralizar o título
    fig.update_layout(title_text = 'Média de Preço de Prato para Duas Pessoas por País', title_x = 0.30)  # title_x = 0.5 centraliza o título
    
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
    1. Texto filtros
    2. Multiselect com nomes dos país
    3. Filtro por país
    ''' 
    # Texto filtros
    st.sidebar.markdown('## Filtros')

    # Multiselect com nomes dos país
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
st.markdown('# 🌎 Visão Países')

with st.container():
    # Criar um layout com 1 coluna
    col1 = st.columns(1)
    
    with col1[0]:
        # Desenhar o gráfico de barras Plotly
        fig = grafico_barras_paises(df_1)

with st.container():
    # Criar um layout com 1 coluna
    col1 = st.columns(1)
    
    with col1[0]:
        # Desenhar o gráfico de barras Plotly
        fig = grafico_barras_cidades(df_1)

# Container do topo Visão Gerencial
with st.container():
    # Criar um layout de coluna com duas colunas
    col1, col2 = st.columns(2, gap = 'large')

    with col1:       
        # Desenhar 2 gráficos de barras com as avaliações e média de preço de prato para duas pessoas por país
        fig = graficos_barras_avaliacoes(df_1)
        
    with col2:       
        # Desenhar 2 gráficos de barras com as avaliações e média de preço de prato para duas pessoas por país
        fig = graficos_barras_pratos(df_1)