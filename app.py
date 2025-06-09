import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# Configuração da página
st.set_page_config(page_title="Dashboard Advocacia", layout="wide")

# Função para carregar dados
def carregar_dados():
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Carregar dados dos advogados
    if os.path.exists('data/advogados.json'):
        with open('data/advogados.json', 'r') as f:
            advogados = pd.DataFrame(json.load(f))
    else:
        advogados = pd.DataFrame(columns=['id', 'nome'])
        
    # Carregar dados dos atendimentos
    if os.path.exists('data/atendimentos.json'):
        with open('data/atendimentos.json', 'r') as f:
            atendimentos = pd.DataFrame(json.load(f))
    else:
        atendimentos = pd.DataFrame(columns=['id', 'data', 'advogado_id', 'tipo', 'status', 'cliente_id'])
        
    # Carregar dados dos clientes
    if os.path.exists('data/clientes.json'):
        with open('data/clientes.json', 'r') as f:
            clientes = pd.DataFrame(json.load(f))
    else:
        clientes = pd.DataFrame(columns=['id', 'nome'])
    
    return advogados, atendimentos, clientes

# Função para salvar dados
def salvar_dados(advogados, atendimentos, clientes):
    advogados.to_json('data/advogados.json', orient='records')
    atendimentos.to_json('data/atendimentos.json', orient='records')
    clientes.to_json('data/clientes.json', orient='records')

# Carregar dados
advogados, atendimentos, clientes = carregar_dados()

# Sidebar para navegação
st.sidebar.title("Navegação")
pagina = st.sidebar.radio("Ir para:", ["Dashboard", "Cadastro de Advogados", "Registro de Atendimentos", "Cadastro de Clientes"])

if pagina == "Cadastro de Advogados":
    st.title("Cadastro de Advogados")
    
    # Formulário para novo advogado
    with st.form("novo_advogado"):
        novo_id = len(advogados) + 1
        nome = st.text_input("Nome do Advogado")
        submitted = st.form_submit_button("Cadastrar")
        
        if submitted and nome:
            novo_advogado = pd.DataFrame({'id': [novo_id], 'nome': [nome]})
            advogados = pd.concat([advogados, novo_advogado], ignore_index=True)
            salvar_dados(advogados, atendimentos, clientes)
            st.success("Advogado cadastrado com sucesso!")

    # Lista de advogados
    st.subheader("Lista de Advogados")
    st.dataframe(advogados)

elif pagina == "Registro de Atendimentos":
    st.title("Registro de Atendimentos")
    
    # Formulário para novo atendimento
    with st.form("novo_atendimento"):
        novo_id = len(atendimentos) + 1
        data = st.date_input("Data do Atendimento")
        advogado_id = st.selectbox("Advogado", options=advogados['id'].tolist(), format_func=lambda x: advogados[advogados['id']==x]['nome'].iloc[0])
        tipo = st.selectbox("Tipo de Atendimento", ["Consulta", "Audiência", "Reunião", "Outro"])
        status = st.selectbox("Status", ["Em andamento", "Concluído", "Cancelado"])
        cliente_id = st.selectbox("Cliente", options=clientes['id'].tolist(), format_func=lambda x: clientes[clientes['id']==x]['nome'].iloc[0])
        
        submitted = st.form_submit_button("Registrar")
        
        if submitted:
            novo_atendimento = pd.DataFrame({
                'id': [novo_id],
                'data': [data.strftime("%Y-%m-%d")],
                'advogado_id': [advogado_id],
                'tipo': [tipo],
                'status': [status],
                'cliente_id': [cliente_id]
            })
            atendimentos = pd.concat([atendimentos, novo_atendimento], ignore_index=True)
            salvar_dados(advogados, atendimentos, clientes)
            st.success("Atendimento registrado com sucesso!")

    # Lista de atendimentos
    st.subheader("Lista de Atendimentos")
    if not atendimentos.empty:
        atendimentos_view = atendimentos.merge(advogados, left_on='advogado_id', right_on='id', suffixes=('', '_adv'))
        atendimentos_view = atendimentos_view.merge(clientes, left_on='cliente_id', right_on='id', suffixes=('', '_cli'))
        st.dataframe(atendimentos_view[['id', 'data', 'nome', 'tipo', 'status', 'nome_cli']])

elif pagina == "Cadastro de Clientes":
    st.title("Cadastro de Clientes")
    
    # Formulário para novo cliente
    with st.form("novo_cliente"):
        novo_id = len(clientes) + 1
        nome = st.text_input("Nome do Cliente")
        submitted = st.form_submit_button("Cadastrar")
        
        if submitted and nome:
            novo_cliente = pd.DataFrame({'id': [novo_id], 'nome': [nome]})
            clientes = pd.concat([clientes, novo_cliente], ignore_index=True)
            salvar_dados(advogados, atendimentos, clientes)
            st.success("Cliente cadastrado com sucesso!")

    # Lista de clientes
    st.subheader("Lista de Clientes")
    st.dataframe(clientes)

else:  # Dashboard
    st.title("Dashboard Advocacia")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        data_inicio = st.date_input("Data Inicial")
    with col2:
        data_fim = st.date_input("Data Final")
    with col3:
        advogado_filtro = st.multiselect(
            "Advogados",
            options=advogados['nome'].tolist(),
            default=advogados['nome'].tolist()
        )

    # Converter datas para string para comparação
    data_inicio_str = data_inicio.strftime("%Y-%m-%d")
    data_fim_str = data_fim.strftime("%Y-%m-%d")
    
    # Filtrar dados
    atendimentos_filtrados = atendimentos[
        (atendimentos['data'] >= data_inicio_str) &
        (atendimentos['data'] <= data_fim_str)
    ]
    
    if advogado_filtro:
        advogados_ids = advogados[advogados['nome'].isin(advogado_filtro)]['id'].tolist()
        atendimentos_filtrados = atendimentos_filtrados[
            atendimentos_filtrados['advogado_id'].isin(advogados_ids)
        ]

    # Métricas principais
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Atendimentos", len(atendimentos_filtrados))
    with col2:
        atendimentos_concluidos = len(atendimentos_filtrados[atendimentos_filtrados['status'] == 'Concluído'])
        st.metric("Atendimentos Concluídos", atendimentos_concluidos)
    with col3:
        atendimentos_andamento = len(atendimentos_filtrados[atendimentos_filtrados['status'] == 'Em andamento'])
        st.metric("Atendimentos em Andamento", atendimentos_andamento)

    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de atendimentos por advogado
        if not atendimentos_filtrados.empty:
            atend_por_adv = atendimentos_filtrados.merge(advogados, left_on='advogado_id', right_on='id')
            fig_adv = px.bar(
                atend_por_adv['nome'].value_counts(),
                title="Atendimentos por Advogado",
                labels={'value': 'Quantidade', 'index': 'Advogado'}
            )
            st.plotly_chart(fig_adv)

    with col2:
        # Gráfico de tipos de atendimento
        if not atendimentos_filtrados.empty:
            fig_tipos = px.pie(
                atendimentos_filtrados,
                names='tipo',
                title="Distribuição por Tipo de Atendimento"
            )
            st.plotly_chart(fig_tipos)

    # Gráfico de evolução temporal
    if not atendimentos_filtrados.empty:
        atendimentos_filtrados['data'] = pd.to_datetime(atendimentos_filtrados['data'])
        atend_por_data = atendimentos_filtrados.groupby('data').size().reset_index(name='count')
        fig_evolucao = px.line(
            atend_por_data,
            x='data',
            y='count',
            title="Evolução dos Atendimentos no Tempo"
        )
        st.plotly_chart(fig_evolucao) 