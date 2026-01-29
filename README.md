# ✈️ Projeto: Data Warehouse de Agência Nacional de Aviação Civil (ANAC)

Este projeto tem como objetivo construir um Data Warehouse da Agência Nacional de Aviação Civil (ANAC), utilizando nuvem e infraestrutura local. A solução coleta, processa e armazena dados públicos da ANAC disponibilizados em arquivos CSV contendo informações de voos, possibilitando análises e insights relevantes para órgãos públicos, pesquisadores e interessados no setor aéreo brasileiro.

# 🎯 Objetivos do Projeto

- Extrair dados da ANAC em arquivos CSV disponibilizados periodicamente (a cada 60 ou 90 dias);
- Armazenar os dados em um banco de dados PostgreSQL;
- Processar e transformar os dados para análises futuras;
- Automatizar a ingestão dos dados utilizando Airflow;
- Fornecer insights e dashboards com base nos dados coletados.

# 🔗 Fonte dos Dados

- [Portal Brasileiro de Dados Abertos](https://dados.gov.br/dados/busca?termo=ANAC)
- [Catálogo de APIs Governamentais](https://www.gov.br/conecta/catalogo/)
- Outras bases públicas relevantes (quando necessário)

# 🔧 Tecnologias Utilizadas

### Infraestrutura (em definição)

- BigQuery (GCP) – possível escolha para armazenamento e análises escaláveis em nuvem
- Amazon S3 / Redshift (AWS) – considerados para armazenamento de arquivos e data warehouse
- **Infraestrutura local** (Utilizada para backup e processamento complementar)
- **PostgreSQL** (Banco relacional local para ingestão inicial dos dados)

### Linguagens e Ferramentas

- **Python** (Extração e processamento)
- **Pandas** (Tratamento e análise dos dados)
- **Psycopg2** (Conexão com PostgreSQL)
- **Apache Airflow** (Orquestração e agendamento de tarefas)
- **Streamlit** (Dashboard e visualização de dados)
- **Poetry** (Gerenciamento de dependências e ambiente virtual)

## 📁 Estrutura do Projeto

```
📂 config/
│ ├── db_config.py            # Configurações e conexão com o PostgreSQL (ainda não implementado)
📂 dags/
│ ├── download_new_data.py    # DAGs do Airflow para orquestrar o pipeline de ingestão
📂 data/
│ ├── raw/                    # Armazenamento dos arquivos CSV brutos
│ ├── processed/              # Dados transformados e prontos para análise
│ └── processed.log           # Log de controle dos arquivos já processados
📂 src/
│ ├── extract.py              # Extração dos dados dos CSVs
│ ├── transform.py            # Transformação e limpeza
│ └── load.py                 # Carregamento para banco de dados
📂 tests/
│ ├── test_transform.py       # Testes automatizados da etapa de transformação
│
├── .env                      # Variáveis de ambiente (não versionado)
├── .gitignore                # Arquivos/pastas ignorados pelo Git
├── main.py                   # Script principal para rodar o pipeline
├── poetry.lock               # Versões travadas das dependências
├── pyproject.toml            # Configuração do projeto com Poetry
└── README.md                 # Documentação do projeto
```

## 🚀 Implementação

### 1️⃣ Requisitos
- Python 3.10+
- [Poetry](https://python-poetry.org/docs/) instalado globalmente
- PostgreSQL configurado e acessível
- Airflow instalado (recomendado via Docker)
- Variáveis de ambiente configuradas em `.env`

### 2️⃣ Inicialização do Ambiente
🧪 Utilizando Poetry (Execução Manual)
```bash
# Clone o repositório
git clone https://github.com/juniorsilvacc/projeto-dados-agencia-nacional-aviacao-civil.git

# Acesse o diretório do projeto
cd projeto-dados-agencia-nacional-aviacao-civil

# Instale as dependências com Poetry
poetry install

# Ative o ambiente virtual
poetry shell
```

🐳 Utilizando Docker (Execução Automatizada)
Este projeto também pode ser executado dentro de um ambiente Dockerizado, ideal para manter consistência no ambiente e facilitar a configuração.
```bash
# Crie um arquivo .env na raiz do projeto com as seguintes variáveis (exemplo):
DB_HOST=db
DB_PORT=5432
DB_NAME=db-projeto-dados-anac
DB_USER=postgres
DB_PASSWORD=postgres

# Vai reconstruir a imagem e mostrar os logs da execução. Quando o script main.py acabar, o container vai parar manualmente
docker-compose up --build

# Para acompanhar os logs
docker-compose logs -f

# Executar o pipeline manualmente via docker
docker-compose run --rm app python main.py
```

### 3️⃣ Executando o Pipeline Manualmente
```bash
python main.py
```

### 4️⃣ Planejamento para Integração com o Airflow

A automação da ingestão de dados está planejada para ser feita com **Apache Airflow**, permitindo o agendamento e orquestração de todo o pipeline ETL.

🚧 Esta etapa ainda está em desenvolvimento.

Etapas planejadas:
- Criar DAGs para download, transformação e carga dos dados
- Usar agendamentos (schedule_interval) para execução periódica
- Monitoramento do pipeline via interface do Airflow

💡 O uso de Docker ou ambiente virtual separado para o Airflow está sendo considerado.


### ✅ Testes
```bash
# Para rodar os testes:
pytest tests/
```

### 📊 Dashboard
```bash
# O projeto conta com um dashboard desenvolvido com Streamlit para visualização dos dados transformados:
streamlit run dashboard.py
```

### 📌 Contribuição
Cícero Júnior (Engenheiro de Dados)

Linkedin: https://www.linkedin.com/in/juniiorsilvadev/ 

