# Projeto G2 - Analise do Sistema Financeiro e Credito no Brasil

## 1. Titulo do projeto

Projeto academico de analise de dados e dashboard interativo sobre comportamento do credito no Brasil, com foco em volume de credito, juros, inadimplencia, risco e recortes territoriais.

## 2. Descricao do problema

O projeto parte de uma base simulada do sistema financeiro brasileiro para organizar, limpar, transformar e analisar informacoes sobre operacoes de credito ao longo do tempo. A proposta e transformar uma base tabular em uma leitura analitica consistente, com notebook documentado e dashboard Streamlit para exploracao interativa.

## 3. Objetivo

- estruturar um fluxo completo de analise de dados com Python;
- validar e preparar a base antes de qualquer interpretacao;
- produzir indicadores financeiros e visoes comparativas;
- consolidar achados em um dashboard interativo;
- organizar o projeto em modulos reutilizaveis para entrega academica.

## 4. Base de dados

Base principal:

- `dados/simulacao_sistema_financeiro_brasil.csv`

Copias usadas no fluxo do projeto:

- `database/origin/dados_originais.csv`
- `database/processed/dados_tratados.csv`

Caracteristicas gerais da base tratada:

- 4.440 linhas
- 29 colunas apos limpeza e engenharia de atributos
- periodo de 2015 a 2024
- campos sobre regiao, UF, modalidade, setor, risco, volume de credito, juros, inadimplencia, clientes, renda e prazo

Observacao importante:

- a base utilizada no projeto e simulada e foi tratada como material de estudo academico.

## 5. Tecnologias utilizadas

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- Jupyter Notebook

## 6. Estrutura de pastas

```text
PROJETO-G2/
|-- app.py
|-- index.html
|-- README.md
|-- requirements.txt
|-- dados/
|   `-- simulacao_sistema_financeiro_brasil.csv
|-- database/
|   |-- origin/
|   |   `-- dados_originais.csv
|   `-- processed/
|       `-- dados_tratados.csv
|-- notebook/
|   `-- analise_sistema_financeiro.ipynb
|-- src/
|   |-- services/
|   |   |-- load_data.py
|   |   |-- clean_data.py
|   |   |-- transform_data.py
|   |   `-- pipeline.py
|   |-- kpis/
|   |   `-- kpi_calculations.py
|   `-- utils/
|       `-- helpers.py
|-- views/
|   |-- components/
|   |   |-- filters.py
|   |   |-- kpi_cards.py
|   |   |-- charts.py
|   |   `-- tables.py
|   `-- layout/
|       |-- theme.py
|       `-- dashboard.py
```

## 7. Como executar localmente

### Criar ambiente virtual

```bash
python -m venv .venv
```

### Ativar ambiente virtual no Windows

```bash
.venv\Scripts\activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Validar compilacao dos modulos

```bash
python -m compileall app.py src views
```

## 8. Como executar o notebook

Com o ambiente virtual ativo:

```bash
jupyter notebook
```

Depois, abra:

- `notebook/analise_sistema_financeiro.ipynb`

## 9. Como executar o dashboard

Com o ambiente virtual ativo:

```bash
streamlit run app.py
```

## 10. Funcionalidades do dashboard

O dashboard foi estruturado em seis abas:

- Visao Geral
- Evolucao Temporal
- Analise Regional
- Modalidades e Setores
- Risco e Inadimplencia
- Tabela Analitica

Funcionalidades principais:

- filtros dinamicos por ano, mes, regiao, UF, modalidade, setor, risco e faixas;
- cards com KPIs consolidados;
- graficos temporais, regionais e comparativos;
- tabelas agregadas e tabela analitica filtrada;
- download da base filtrada;
- tratamento de cenarios sem dados apos aplicacao de filtros.

## 11. Principais KPIs

Indicadores centrais usados no notebook e no dashboard:

- volume total de credito
- taxa media de juros
- inadimplencia media
- total de clientes
- renda media geral
- prazo medio de pagamento
- credito medio por cliente
- percentual de operacoes criticas

## 12. Analises realizadas

O notebook foi organizado em etapas para cobrir o ciclo analitico completo:

- preparacao e validacao inicial da base
- limpeza e padronizacao dos dados
- engenharia de atributos
- calculo de KPIs e tabelas auxiliares
- analise exploratoria e visualizacoes iniciais
- analise temporal
- analise regional e estadual
- analise por modalidade, setor e risco
- correlacoes e relacoes estatisticas
- consolidacao de insights e preparacao para o dashboard

## 13. Principais insights registrados

Os registros do notebook e do dashboard consolidam, entre outros pontos:

- concentracao relevante do volume de credito em recortes territoriais especificos;
- oscilacao temporal do credito, dos juros e da inadimplencia ao longo da serie;
- diferencas entre volume financeiro, inadimplencia e risco conforme modalidade e setor;
- ausencia de relacoes lineares fortes entre algumas variaveis centrais ligadas a inadimplencia;
- necessidade de tratar `operacao_critica` como sinalizador exploratorio, nao como classificacao definitiva.

## 14. Limitacoes

- a base utilizada e simulada;
- as analises sao descritivas e exploratorias;
- nao ha inferencia causal nem modelagem preditiva nesta entrega;
- o indicador `operacao_critica` e uma regra de apoio analitico e nao um modelo estatistico final;
- a publicacao online ainda depende do preenchimento dos links finais do projeto.

## 15. Publicacao

O projeto foi preparado para tres frentes de publicacao:

- repositorio no GitHub
- pagina estatica no GitHub Pages
- dashboard no Streamlit Community Cloud


## 18. Autor

Projeto desenvolvido por Samuel Elias da Silva no contexto da disciplina de Analise e Visualizacao de Dados com Python.

## 19. Comandos uteis de validacao

```bash
python -m compileall app.py src views
python -c "from src.services.pipeline import prepare_processed_dataset; df = prepare_processed_dataset(); print(df.shape)"
python -c "from src.kpis.kpi_calculations import calculate_general_kpis; print('kpis ok')"
streamlit run app.py
```
