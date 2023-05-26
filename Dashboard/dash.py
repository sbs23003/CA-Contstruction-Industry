import streamlit as st  
import pandas as pd
import numpy as np
import random  
import plotly.express as px 

st.set_page_config(
    page_title = 'Dashboard - Copa do Mundo Qatar 2022',
    page_icon = '📊',
    initial_sidebar_state = "expanded",
    layout="wide"  
)

@st.cache
def CarregarDados():
    dados = pd.read_excel('DadosCopaDoMundoQatar2022.xlsx', sheet_name ='selecoes', index_col = 0)
    return dados

@st.cache
def CarregarSimulacoes():
    s1 = pd.read_excel('SimulaçãoCopa1.xlsx', index_col = 0)
    s2 = pd.read_excel('SimulaçãoCopa2.xlsx', index_col = 0)
    s3 = pd.read_excel('SimulaçãoCopa3.xlsx', index_col = 0)
    s4 = pd.read_excel('SimulaçãoCopa4.xlsx', index_col = 0)
    s5 = pd.read_excel('SimulaçãoCopa5.xlsx', index_col = 0)
    s6 = pd.read_excel('SimulaçãoCopa6.xlsx', index_col = 0)
    s7 = pd.read_excel('SimulaçãoCopa7.xlsx', index_col = 0)
    return s1, s2, s3, s4, s5, s6, s7

dados = CarregarDados()
sims = CarregarSimulacoes()

etapas = ['Início da Copa', 'Pós 1ª Rodada', 'Pós 2ª Rodada', 'Oitavas', 'Quartas', 'Semis', 'Final']

#st.write(dados.head())

atualizacoes = ['Início da Copa', 'Pós Primeira Rodada', 'Pós Segunda Rodada', 'Oitavas de Final','Quartas de Final', 'Semifinais', 'Final']

st.sidebar.title('⚽ Dashboard Copa do Mundo 2022!')

paginas = ['Home', 'Informações por Seleção', 'Evolução na Competição', 'Probabilidades na Segunda Fase', 'Tabelas das Simulações']
pag = st.sidebar.radio('Selecione a página do Dashboard 👇', paginas)


if pag == 'Home':
    st.title('😃 Seja Bem-vindo à Central de Informações das Simulações da Copa!')
    st.markdown('#### ▶ Aqui você poderá navegar por diversas visualizações referentes a simulação de cada etapa a Copa do Mundo Qatar 2022.')
    st.markdown('#### ▶ Navegue no menu ao lado para acessar as dashboards e tabelas que a Equipe Previsão Esportiva gerou durante a Competição.')
    st.markdown('#### ▶ Acesse: https://www.previsaoesportiva.com.br')
    st.image('logo previsao.jpg')


if pag == 'Informações por Seleção':
    st.title('🌏 Informações por Seleção') 

    st.markdown('---')
    listaselecoes = dados.index.tolist()
    selecao = st.sidebar.selectbox('--- Escolha a Seleção ---', sorted(listaselecoes), index = 4) 
    atu = st.sidebar.radio('Selecione o Momento da Copa 👇', atualizacoes)
    cor = st.sidebar.color_picker('Escolha a cor dos gráficos', value = '#0f54c9', label_visibility="visible")

    indice = atualizacoes.index(atu)


    info = dados.loc[selecao]
    #st.write(info)


    c1, _, c2, _, c3, c4, c5 = st.columns([1, 0.1, 0.9, 0.1, 1.5, 1, 1.1])
    c1.write('Bandeira')
    c1.image(info['LinkBandeiraGrande'])
    c2.write('Principal Jogador:' + info['JogadorDestaque'])
    c2.image(info['FotoJogadorDestaque'])
    c3.metric('Nome em Inglês', info['NomeEmIngles'])
    c3.metric('Confederação', info['Confederação'])
    c4.metric('Pontos FIFA', info['PontosRankingFIFA'])
    c4.metric('Posição FIFA', info['PosiçãoRankingFIFA'])
    c5.metric('Copas Ganhas', info['Copas'])
    c5.metric('Valor de Mercado', info['ValorDeMercado']) 

    st.markdown('---')

    #st.write(pd.Series(valores, index = etapas))
 
    #st.image(pd.Series(valores, index = etapas).plot(kind = 'bar'))
    #st.write(sims[0].loc[selecao][:4])
    #st.write(sims[0].loc[selecao][4:][['Oitavas', 'Quartas', 'Semis', 'Final', 'Campeão']])

    info1 = sims[indice].loc[selecao][:4] 

    dados1 = {'Probabilidades Estimada': info1.values,
              'Posição Fase de Grupos': info1.index}

    fig1 = px.bar(dados1, 
                  x='Posição Fase de Grupos', 
                  y='Probabilidades Estimada',
                  color_discrete_sequence =[cor]*4, 
                  text= [f'{100*i:.1f}%' for i in info1.values] )  

    fig1.layout.title = "Probabilidades na Primeira Fase" 
    fig1.layout.titlefont = {"size": 24, "color": "#262626"} 
    fig1.update_layout() 

    info2 = sims[indice].loc[selecao][4:][['Oitavas', 'Quartas', 'Semis', 'Final', 'Campeão']]

    dados2 = {'Probabilidades Estimada': info2.values,
              'Fase Mata-Mata': info2.index}
              
    fig2 = px.bar(dados2, 
                  x='Fase Mata-Mata', 
                  y='Probabilidades Estimada',
                  color_discrete_sequence =[cor]*5, 
                  text= [f'{100*i:.1f}%' for i in info2.values] )  

    fig2.layout.title = "Probabilidades na fase Mata-Mata" 
    fig2.layout.titlefont = {"size": 24, "color": "#262626"} 
    fig2.update_layout()  

    c1, c2 = st.columns(2)
    c1.plotly_chart(fig1, use_container_width = True)
    c2.plotly_chart(fig2, use_container_width = True)






if pag == 'Evolução na Competição':

    st.title('🌎 Evolução na Competição') 

    st.markdown('---')
    listaselecoes = dados.index.tolist()
    selecao = st.sidebar.selectbox('--- Escolha a Seleção ---', sorted(listaselecoes), index = 4) 
    cor = st.sidebar.color_picker('Escolha a cor dos gráficos', value = '#0f54c9', label_visibility="visible")
    
    info = dados.loc[selecao]

    valores = [sims[i].loc[selecao]['Campeão'] for i in range(len(sims))] 
    data = {'etapas': etapas,
            'probs': valores}

    # Create the bar plot
    fig1 = px.bar(data, y="etapas", x="probs", orientation = 'h',
                 color_discrete_sequence =[cor]*7, 
                 text= [f'{100*i:.1f}%' for i in valores] )  
 
    fig1.layout.title = "Avanço da Probabilidade de Campeão na Competição" 
    fig1.layout.titlefont = {"size": 24, "color": "#262626"} 
    fig1.update_layout() 

    c1, c2 = st.columns([1,4])
    c1.header(selecao)
    c1.image(info['LinkBandeiraGrande'])
    c2.plotly_chart(fig1, use_container_width = True)


 


if pag == 'Probabilidades na Segunda Fase':
    st.title('🌍 Probabilidades na Segunda Fase') 
    st.markdown('---')

    num = st.sidebar.number_input('Quantas equipes deseja ver nos gráficos?', min_value=4, max_value=32, value=8)
    atu = st.sidebar.radio('Selecione o Momento da Copa 👇', atualizacoes)
    cor = st.sidebar.color_picker('Escolha a cor dos gráficos', value = '#0f54c9', label_visibility="visible")

    indice = atualizacoes.index(atu)

    def grafico(etapa): 
        info1 = sims[indice][etapa].sort_values()
        info1 = info1[(32-num):]

        data = {'Equipes': info1.index, 'Probabilidades': info1.values}
        #st.write(data)

        # Create the bar plot
        fig1 = px.bar(data, y="Equipes", x="Probabilidades", orientation = 'h',
                     color_discrete_sequence =[cor]*7, 
                     text= [f'{100*i:.1f}%' for i in info1.values] )  
     
        fig1.layout.title = f"Probabilidade de {etapa}" 
        fig1.layout.titlefont = {"size": 18, "color": "#262626"} 
        fig1.update_layout() 
        return fig1



    c1, c2, c3 = st.columns(3)
    c1.plotly_chart(grafico('Oitavas'), use_container_width = True)
    c2.plotly_chart(grafico('Quartas'), use_container_width = True)
    c3.plotly_chart(grafico('Semis'), use_container_width = True)

    c1, c2 = st.columns(2)
    c1.plotly_chart(grafico('Final'), use_container_width = True)
    c2.plotly_chart(grafico('Campeão'), use_container_width = True)


if pag == 'Tabelas das Simulações':
        st.title('🔢 Tabelas das Simulações') 
        st.markdown('---')

        tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(atualizacoes)
 
        with tab0:
            st.subheader(atualizacoes[0]) 
            st.write(sims[0])

        with tab1:
            st.header(atualizacoes[1]) 
            st.write(sims[1])
 
        with tab2:
            st.header(atualizacoes[2]) 
            st.write(sims[2])

        with tab3:
            st.header(atualizacoes[3]) 
            st.write(sims[3])
 
        with tab4:
            st.header(atualizacoes[4]) 
            st.write(sims[4])
 
        with tab5:
            st.header(atualizacoes[5]) 
            st.write(sims[5])
 
        with tab6:
            st.header(atualizacoes[6]) 
            st.write(sims[6])
 
