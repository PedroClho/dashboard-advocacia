import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def gerar_dados_leads():
    # Dados de leads
    n_leads = 100
    origens = ['Facebook', 'WhatsApp', 'Instagram', 'Site institucional']
    segmentos = ['Concurso Público', 'Servidor Público']
    estados = ['SP', 'RJ', 'MG', 'RS', 'PR', 'BA', 'SC', 'PE', 'CE', 'DF']
    
    dados_leads = {
        'data': [datetime.now() - timedelta(days=x) for x in range(n_leads)],
        'origem': np.random.choice(origens, n_leads),
        'segmento': np.random.choice(segmentos, n_leads),
        'estado': np.random.choice(estados, n_leads),
        'convertido': np.random.choice([True, False], n_leads, p=[0.3, 0.7])
    }
    
    return pd.DataFrame(dados_leads)

def gerar_dados_processos():
    # Dados de processos jurídicos
    n_processos = 50
    status = ['Em andamento', 'Concluído', 'Ganho', 'Perdido']
    tipos = ['Administrativo', 'Judicial', 'Recurso']
    
    dados_processos = {
        'data_entrada': [datetime.now() - timedelta(days=x*7) for x in range(n_processos)],
        'status': np.random.choice(status, n_processos),
        'tipo': np.random.choice(tipos, n_processos),
        'tempo_decisao': np.random.randint(30, 365, n_processos)
    }
    
    return pd.DataFrame(dados_processos)

def gerar_dados_controladoria():
    # Dados de controladoria
    n_registros = 30
    
    dados_controladoria = {
        'data': [datetime.now() - timedelta(days=x) for x in range(n_registros)],
        'processos_ativos': np.random.randint(100, 150, n_registros),
        'tempo_atualizacao': np.random.randint(1, 10, n_registros)
    }
    
    return pd.DataFrame(dados_controladoria)

def gerar_dados_contratos():
    # Dados de contratos
    n_contratos = 40
    estados = ['SP', 'RJ', 'MG', 'RS', 'PR', 'BA', 'SC', 'PE', 'CE', 'DF']
    
    dados_contratos = {
        'data': [datetime.now() - timedelta(days=x*3) for x in range(n_contratos)],
        'valor': np.random.uniform(5000, 50000, n_contratos),
        'estado': np.random.choice(estados, n_contratos),
        'origem_lead': np.random.choice(['Facebook', 'WhatsApp', 'Instagram', 'Site institucional'], n_contratos)
    }
    
    return pd.DataFrame(dados_contratos)

# Coordenadas dos estados para o mapa
COORDENADAS_ESTADOS = {
    'SP': {'lat': -23.5505, 'lon': -46.6333},
    'RJ': {'lat': -22.9068, 'lon': -43.1729},
    'MG': {'lat': -19.9167, 'lon': -43.9345},
    'RS': {'lat': -30.0346, 'lon': -51.2177},
    'PR': {'lat': -25.4284, 'lon': -49.2733},
    'BA': {'lat': -12.9714, 'lon': -38.5014},
    'SC': {'lat': -27.5954, 'lon': -48.5480},
    'PE': {'lat': -8.0476, 'lon': -34.8770},
    'CE': {'lat': -3.7172, 'lon': -38.5433},
    'DF': {'lat': -15.7975, 'lon': -47.8919}
} 