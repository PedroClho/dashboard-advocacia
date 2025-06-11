# Dashboard Advocacia

Este é um dashboard desenvolvido em Streamlit para visualização de métricas essenciais de desempenho relacionadas aos departamentos Comercial, Jurídico e Controladoria de uma advocacia.

## Funcionalidades

### Departamento Comercial
- Visualização de leads captados por segmento e origem
- Acompanhamento de propostas enviadas por canal
- Análise de contratos fechados com distribuição geográfica

### Departamento Jurídico
- Monitoramento de processos ativos
- Análise de taxa de sucesso
- Acompanhamento do tempo médio até decisão judicial

### Controladoria
- Controle de processos
- Métricas de tempo de atualização

## Requisitos

- Python 3.8+
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Executando o Dashboard

Para iniciar o dashboard, execute:
```bash
streamlit run app.py
```

O dashboard estará disponível em `http://localhost:8501`

## Estrutura do Projeto

```
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências do projeto
├── .streamlit/        # Configurações do Streamlit
│   └── config.toml    # Tema e configurações
└── README.md          # Documentação
``` 