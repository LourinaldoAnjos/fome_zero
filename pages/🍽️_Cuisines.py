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

st.set_page_config(page_title = 'Visão Cuisines', page_icon = '🍽️', layout = 'wide')

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

# ==============================================================
# Função Exibir 5 colunas com tipos de cullinaria e avaliações
# ==============================================================
def tipos_culinarios(df_1):
    ''' Esta função tem a responsabilidade de exibir 5 colunas com tipos de cullinaria e avaliações
    
    Tipo de exibição:
    1. Contagem dos tipos de culinários
    2. Separa os nomes dos restaurantes, culinarias e avaliações
    3. Formatar e exibir no formato desejado com tamanho de fonte maior para a avaliação
    '''    
    # Contagem dos tipos de culinários
    tipo_culinaria = df_1.loc[:, ['Restaurant_ID', 'Restaurant_Name', 'Country_Code', 'City', 'Cuisines', 'Average_Cost_for_two', 'Aggregate_rating', 'Votes']].groupby(['Cuisines', 'Restaurant_Name', 'Aggregate_rating']).count().sort_values(by = 'Aggregate_rating', ascending = False).head(5).reset_index()

    # Separa os nomes dos restaurantes, culinarias e avaliações
    for nomes, row in tipo_culinaria.iterrows():
      restaurante = row['Restaurant_Name']
      culinaria = row['Cuisines']
      avaliacao = row['Aggregate_rating']
    
    # Formatar e exibir no formato desejado com tamanho de fonte maior para a avaliação
    col1.metric(label = f' {culinaria}: {restaurante}', value = f'{avaliacao}/5.0')
    
    # Contagem dos tipos de culinários
    tipo_culinaria = df_1.loc[:, ['Restaurant_ID', 'Restaurant_Name', 'Country_Code', 'City', 'Cuisines', 'Average_Cost_for_two', 'Aggregate_rating', 'Votes']].groupby(['Cuisines', 'Restaurant_Name', 'Aggregate_rating']).count().sort_values(by = 'Aggregate_rating', ascending = False).head(4).reset_index()

    # Separa os nomes dos restaurantes, culinarias e avaliações
    for nomes, row in tipo_culinaria.iterrows():
      restaurante = row['Restaurant_Name']
      culinaria = row['Cuisines']
      avaliacao = row['Aggregate_rating']
        
    # Formatar e exibir no formato desejado com tamanho de fonte maior para a avaliação
    col2.metric(label = f' {culinaria}: {restaurante}', value = f'{avaliacao}/5.0')
    
    # Contagem dos tipos de culinários
    tipo_culinaria = df_1.loc[:, ['Restaurant_ID', 'Restaurant_Name', 'Country_Code', 'City', 'Cuisines', 'Average_Cost_for_two', 'Aggregate_rating', 'Votes']].groupby(['Cuisines', 'Restaurant_Name', 'Aggregate_rating']).count().sort_values(by = 'Aggregate_rating', ascending = False).head(3).reset_index()

    # Separa os nomes dos restaurantes, culinarias e avaliações
    for nomes, row in tipo_culinaria.iterrows():
      restaurante = row['Restaurant_Name']
      culinaria = row['Cuisines']
      avaliacao = row['Aggregate_rating']
    
    # Formatar e exibir no formato desejado com tamanho de fonte maior para a avaliação
    col3.metric(label = f' {culinaria}: {restaurante}', value = f'{avaliacao}/5.0')
    
    # Contagem dos tipos de culinários
    tipo_culinaria = df_1.loc[:, ['Restaurant_ID', 'Restaurant_Name', 'Country_Code', 'City', 'Cuisines', 'Average_Cost_for_two', 'Aggregate_rating', 'Votes']].groupby(['Cuisines', 'Restaurant_Name', 'Aggregate_rating']).count().sort_values(by = 'Aggregate_rating', ascending = False).head(2).reset_index()

    # Separa os nomes dos restaurantes, culinarias e avaliações
    for nomes, row in tipo_culinaria.iterrows():
      restaurante = row['Restaurant_Name']
      culinaria = row['Cuisines']
      avaliacao = row['Aggregate_rating']
    
    # Formatar e exibir no formato desejado com tamanho de fonte maior para a avaliação
    col4.metric(label = f' {culinaria}: {restaurante}', value = f'{avaliacao}/5.0')
    
    # Contagem dos tipos de culinários
    tipo_culinaria = df_1.loc[:, ['Restaurant_ID', 'Restaurant_Name', 'Country_Code', 'City', 'Cuisines', 'Average_Cost_for_two', 'Aggregate_rating', 'Votes']].groupby(['Cuisines', 'Restaurant_Name', 'Aggregate_rating']).count().sort_values(by = 'Aggregate_rating', ascending = False).head(1).reset_index()

    # Separa os nomes dos restaurantes, culinarias e avaliações
    for nomes, row in tipo_culinaria.iterrows():
      restaurante = row['Restaurant_Name']
      culinaria = row['Cuisines']
      avaliacao = row['Aggregate_rating']
    
    # Formatar e exibir no formato desejado com tamanho de fonte maior para a avaliação
    col5.metric(label = f' {culinaria}: {restaurante}', value = f'{avaliacao}/5.0')
    
    return df_1

# ==============================================================
# Função de Exibi o DataFrame
# ==============================================================
def tabela_dataframe(df_1):
    ''' Esta função tem a responsabilidade de Filtrar de texto e informações no gráfico
    
    Tipo de Filtro:
    1. Exibir o texto com base no valor selecionado no filtro
    2. Contagem dos tipos de culinários
    3. Serapara nomes dos restaurantes, culinarias, avaliações e países linha por linha
    4. Exibir na tela
    '''    
    # Exibir o texto com base no valor selecionado no filtro
    st.markdown(f'## Top {restaurantes_options} Restaurantes')

    # Contagem dos tipos de culinários
    tipo_culinaria = df_1.loc[:, ['Restaurant_ID', 'Restaurant_Name', 'Country_Code', 'City', 'Cuisines', 'Average_Cost_for_two', 'Aggregate_rating', 'Votes']].groupby(['Restaurant_ID', 'Restaurant_Name', 'Country_Code', 'City', 'Cuisines', 'Average_Cost_for_two', 'Aggregate_rating', 'Votes']).sum().sort_values(by = 'Aggregate_rating', ascending = False).head(restaurantes_options).reset_index()

    # Serapara nomes dos restaurantes, culinarias, avaliações e países linha por linha
    for nomes, row in tipo_culinaria.iterrows():
      restaurante = row['Restaurant_Name']
      culinaria = row['Cuisines']
      avaliacao = row['Aggregate_rating']
      country_id = row['Country_Code']
    
    # Exibir na tela
    st.dataframe(tipo_culinaria)
    
    return df_1

# ================================================================================================
# Função de Desenhar o gráfico de barras Plotly Top 20 Melhores Restaurantes com Tipos Culinários
# ================================================================================================
def grafico_barras_melhores(df_1):
    ''' Esta função tem a responsabilidade de Desenhar o gráfico de barras Plotly Top 20 Melhores Restaurantes com Tipos Culinários
    
    Tipo de Filtro:
    1. Contagem dos Top 20 Melhores Restaurantes com Tipos Culinários
    2. Desenhar o gráfico de barras Plotly
    3. Adicionar rótulos aos eixos x e y
    4. Personalizar o texto no balão de informações (hovertext)
    5. Personalizar o texto das barras para incluir o nome do país
    6. Exibir o texto com base no valor selecionado no filtro
    7. Exibir na tela
    '''     
    # Contagem dos Top 20 Melhores Restaurantes com Tipos Culinários
    tipos_culinarios_distintos = df_1.loc[:, ['Cuisines', 'Aggregate_rating', 'Votes']].groupby(['Cuisines']).mean().sort_values(by = 'Aggregate_rating', ascending = False).head(restaurantes_options).reset_index()
    
    # Desenhar o gráfico de barras Plotly
    fig = px.bar(tipos_culinarios_distintos, x = 'Cuisines', y = 'Aggregate_rating')
    
    # Adicionar rótulos aos eixos x e y
    fig.update_xaxes(title_text = 'Tipos Culinários')
    fig.update_yaxes(title_text = 'Média de avaliações')
    
    # Personalizar o texto no balão de informações (hovertext)
    fig.update_traces(hovertemplate = 'Tipos Culinários: %{x}<br>Média de avaliações: %{y}')
    
    # Personalizar o texto das barras para incluir o nome do país
    fig.update_traces(texttemplate = '%{y:.2f}') # .2f indica duas casas decimais
    
    # Exibir o texto com base no valor selecionado no filtro
    fig.update_layout(title_text = f'Top {restaurantes_options} Melhores Tipos Culinários', title_x = 0.30)  # title_x = 0.5 centraliza o título
    
    # Exibir na tela
    st.write(fig)
    
    return fig

# ================================================================================================
# Função de Desenhar o gráfico de barras Plotly Top 20 Piores Restaurantes com Tipos Culinários
# ================================================================================================
def grafico_barras_piores(df_1):
    ''' Esta função tem a responsabilidade de Desenhar o gráfico de barras Plotly Top 20 Piores Restaurantes com Tipos Culinários
    
    Tipo de Filtro:
    1. Contagem dos Top 20 Piores Restaurantes com Tipos Culinários
    2. Desenhar o gráfico de barras Plotly
    3. Adicionar rótulos aos eixos x e y
    4. Personalizar o texto no balão de informações (hovertext)
    5. Personalizar o texto das barras para incluir o nome do país
    6. Exibir o texto com base no valor selecionado no filtro
    7. Exibir na tela
    '''
    # Contagem dos Top 20 Piores Restaurantes com Tipos Culinários
    tipos_culinarios_distintos = df_1.loc[:, ['Cuisines', 'Aggregate_rating', 'Votes']].groupby(['Cuisines']).mean().sort_values(by = 'Aggregate_rating', ascending = True).head(restaurantes_options).reset_index()
    
    # Desenhar o gráfico de barras Plotly
    fig = px.bar(tipos_culinarios_distintos, x = 'Cuisines', y = 'Aggregate_rating')
    
    # Adicionar rótulos aos eixos x e y
    fig.update_xaxes(title_text = 'Tipos Culinários')
    fig.update_yaxes(title_text = 'Média de avaliações')
    
    # Personalizar o texto no balão de informações (hovertext)
    fig.update_traces(hovertemplate = 'Tipos Culinários: %{x}<br>Média de avaliações: %{y}')
    
    # Personalizar o texto das barras para incluir o nome do país
    fig.update_traces(texttemplate = '%{y:.2f}') # .2f indica duas casas decimais
    
    # Exibir o texto com base no valor selecionado no filtro
    fig.update_layout(title_text = f'Top {restaurantes_options} Piores Tipos Culinários', title_x = 0.30)  # title_x = 0.5 centraliza o título
    
    # Exibir na tela
    st.write(fig)
    
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
  
# ==============================================================
# Função de Opções de nomes de culinaria registrado
# ==============================================================
def multiselect_culinaria(df_1):
    ''' Esta função tem a responsabilidade de filtrar
    
    Tipo de filtro:
    1. Opções de nomes de culinaria registrado
    2. Filtro por país
    '''   
    # Opções de nomes de culinaria registrado
    culinaria_options = st.sidebar.multiselect(
        'Escolha os Tipos de Culinária',
        ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
           'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
           'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
           'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
           'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
           'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
           'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
           'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
           'Mineira', 'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian',
           'Author', 'Gourmet Fast Food', 'Lebanese', 'Modern Australian',
           'African', 'Coffee and Tea', 'Australian', 'Middle Eastern',
           'Malaysian', 'Tapas', 'New American', 'Pub Food', 'Southern',
           'Diner', 'Donuts', 'Southwestern', 'Sandwich', 'Irish',
           'Mediterranean', 'Cafe Food', 'Korean BBQ', 'Fusion', 'Canadian',
           'Breakfast', 'Cajun', 'New Mexican', 'Belgian', 'Cuban', 'Taco',
           'Caribbean', 'Polish', 'Deli', 'British', 'California', 'Others',
           'Eastern European', 'Creole', 'Ramen', 'Ukrainian', 'Hawaiian',
           'Patisserie', 'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan',
           'Burmese', 'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian',
           'Continental', 'South Indian', 'North Indian', 'Salad',
           'Finger Food', 'Mandi', 'Turkish', 'Kerala', 'Pakistani',
           'Biryani', 'Street Food', 'Nepalese', 'Goan', 'Iranian', 'Mughlai',
           'Rajasthani', 'Mithai', 'Maharashtrian', 'Gujarati', 'Rolls',
           'Momos', 'Parsi', 'Modern Indian', 'Andhra', 'Tibetan', 'Kebab',
           'Chettinad', 'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi',
           'Afghan', 'Lucknowi', 'Charcoal Chicken', 'Mangalorean',
           'Egyptian', 'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian',
           'Western', 'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian',
           'Balti', 'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji',
           'South African', 'Drinks Only', 'Durban', 'World Cuisine',
           'Izgara', 'Home-made', 'Giblets', 'Fresh Fish', 'Restaurant Cafe',
           'Kumpir', 'Döner', 'Turkish Pizza', 'Ottoman', 'Old Turkish Bars',
           'Kokoreç'],
        default = ['Home-made', 'BBQ', 'Japanese', 'Brazilian', 'Arabian', 'American', 'Italian'])
    
    # Filtro por país
    linhas_selecionadas = df_1['Cuisines'].isin(culinaria_options)
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

# ==============================================================
# Filtro para selecionar o intervalo de 1 a 20 com padrão em 10
# ============================================================== 
# Filtro para selecionar o intervalo de 1 a 20 com padrão em 10
restaurantes_options = st.sidebar.slider('Selecione a quantidade de Restaurantes que deseja visualizar', 1, 20, 10)

# Filtro o DataFrame com base no intervalo selecionado
df_1_aux = df_1.head(restaurantes_options)

# =================================================
# Opções de nomes de culinaria registrado
# =================================================
# Opções de nomes de culinaria registrado    
df_1 = multiselect_culinaria(df_1)

# Título da pagina
st.markdown('# 🍽️ Visão Tipos de Cusinhas')

# SuTítulo da pagina
st.markdown('## Melhores Restaurantes dos Principais tipos Culinários')

# Container do topo Visão Gerencial
with st.container():

    # Criar um layout de coluna com duas colunas
    col1, col2, col3, col4, col5 = st.columns(5, gap = 'large')
    
    with col1:
        # Exibir 5 colunas com tipos de cullinaria e avaliações                
        if not df_1.empty:
            # O DataFrame df_1 não está vazio, exibir na tela
            df_1 = tipos_culinarios(df_1)

# Container do topo Visão Gerencial
with st.container():
    # Filtro de texto e informações no gráfico
    df_1 = tabela_dataframe(df_1)
    
# Container do topo Visão Gerencial
with st.container():
    # Criar um layout de coluna com duas colunas
    col1, col2 = st.columns(2, gap = 'large')

    with col1:
        # Desenhar o gráfico de barras Plotly Top 20 Melhores Restaurantes com Tipos Culinários
        fig = grafico_barras_melhores(df_1)
                
    with col2: 
        # Desenhar o gráfico de barras Plotly Top 20 piores Restaurantes com Tipos Culinários
        fig = grafico_barras_piores(df_1)
        