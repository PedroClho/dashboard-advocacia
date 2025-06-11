import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from mock_data import (
    gerar_dados_leads,
    gerar_dados_processos,
    gerar_dados_controladoria,
    gerar_dados_contratos,
    COORDENADAS_ESTADOS
)

# Configuração da página
st.set_page_config(
    page_title="Dashboard Advocacia",
    page_icon="⚖️",
    layout="wide"
)

# Carregando dados mockados
df_leads = gerar_dados_leads()
df_processos = gerar_dados_processos()
df_controladoria = gerar_dados_controladoria()
df_contratos = gerar_dados_contratos()

# Título principal
st.title("Dashboard Advocacia")

# Criação das abas principais
tab_comercial, tab_juridico, tab_controladoria = st.tabs([
    "Departamento Comercial", 
    "Departamento Jurídico", 
    "Controladoria"
])

# === Departamento Comercial ===
with tab_comercial:
    st.header("Métricas Comerciais")
    
    # Layout em colunas para KPIs principais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total de Leads", value=len(df_leads))
    with col2:
        st.metric(label="Propostas Enviadas", value=len(df_leads[df_leads['convertido']]))
    with col3:
        st.metric(label="Contratos Fechados", value=len(df_contratos))
    
    # Seção de Leads
    st.subheader("Análise de Leads")
    lead_col1, lead_col2 = st.columns(2)
    
    with lead_col1:
        # Gráfico de segmentação de leads
        fig_segmentacao = px.pie(
            df_leads, 
            names='segmento',
            title='Segmentação de Leads',
            hole=0.3
        )
        st.plotly_chart(fig_segmentacao, use_container_width=True)
    
    with lead_col2:
        # Gráfico de origem dos leads
        fig_origem = px.bar(
            df_leads['origem'].value_counts().reset_index(),
            x='origem',
            y='count',
            title='Origem dos Leads',
            labels={'count': 'Quantidade', 'origem': 'Canal'}
        )
        st.plotly_chart(fig_origem, use_container_width=True)

    # Seção de Contratos
    st.subheader("Análise de Contratos")
    
    # Preparando dados para o mapa
    df_contratos_estado = df_contratos.groupby('estado').agg({
        'valor': ['count', 'sum']
    }).reset_index()
    df_contratos_estado.columns = ['estado', 'quantidade', 'valor_total']
    
    # Adicionando coordenadas
    df_contratos_estado['lat'] = df_contratos_estado['estado'].map(lambda x: COORDENADAS_ESTADOS[x]['lat'])
    df_contratos_estado['lon'] = df_contratos_estado['estado'].map(lambda x: COORDENADAS_ESTADOS[x]['lon'])
    
    # Criando o mapa
    fig_mapa = px.scatter_mapbox(
        df_contratos_estado,
        lat='lat',
        lon='lon',
        size='quantidade',
        color='valor_total',
        hover_name='estado',
        hover_data=['quantidade', 'valor_total'],
        title='Distribuição Geográfica dos Contratos',
        mapbox_style='carto-positron'
    )
    st.plotly_chart(fig_mapa, use_container_width=True)

# === Departamento Jurídico ===
with tab_juridico:
    st.header("Métricas Jurídicas")
    
    # Layout em colunas para KPIs
    jur_col1, jur_col2 = st.columns(2)
    
    total_processos = len(df_processos)
    processos_ganhos = len(df_processos[df_processos['status'] == 'Ganho'])
    taxa_sucesso = f"{(processos_ganhos/total_processos)*100:.1f}%"
    
    with jur_col1:
        st.metric(label="Processos Ativos", value=total_processos)
    with jur_col2:
        st.metric(label="Taxa de Sucesso", value=taxa_sucesso)
    
    # Gráfico de status dos processos
    fig_status = px.pie(
        df_processos,
        names='status',
        title='Status dos Processos',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_status, use_container_width=True)
    
    # Gráfico de tempo médio até decisão
    fig_tempo = px.box(
        df_processos,
        x='tipo',
        y='tempo_decisao',
        title='Tempo até Decisão por Tipo de Processo',
        labels={'tipo': 'Tipo de Processo', 'tempo_decisao': 'Dias até Decisão'}
    )
    st.plotly_chart(fig_tempo, use_container_width=True)

# === Controladoria ===
with tab_controladoria:
    st.header("Métricas de Controladoria")
    
    cont_col1, cont_col2 = st.columns(2)
    
    with cont_col1:
        st.metric(
            label="Processos sob Controle",
            value=df_controladoria['processos_ativos'].iloc[-1]
        )
    with cont_col2:
        tempo_medio = f"{df_controladoria['tempo_atualizacao'].mean():.1f} dias"
        st.metric(label="Tempo Médio de Atualização", value=tempo_medio)
    
    # Gráfico de evolução dos processos ativos
    fig_evolucao = px.line(
        df_controladoria,
        x='data',
        y='processos_ativos',
        title='Evolução de Processos Ativos',
        labels={'data': 'Data', 'processos_ativos': 'Quantidade de Processos'}
    )
    st.plotly_chart(fig_evolucao, use_container_width=True)
    
    # Gráfico de tempo de atualização
    fig_tempo_atualizacao = px.histogram(
        df_controladoria,
        x='tempo_atualizacao',
        title='Distribuição do Tempo de Atualização',
        labels={'tempo_atualizacao': 'Dias para Atualização', 'count': 'Frequência'}
    )
    st.plotly_chart(fig_tempo_atualizacao, use_container_width=True)
