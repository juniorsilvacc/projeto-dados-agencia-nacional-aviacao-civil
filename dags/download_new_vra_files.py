from airflow.decorators import dag, task
from datetime import datetime, timedelta
import requests
import re
import os

BASE_URL = 'https://siros.anac.gov.br/siros/registros/diversos/vra/2025/'   # URL de onde os arquivos CSV estão disponíveis
DOWNLOAD_DIR = '/opt/airflow/data/raw'                                      # Pasta onde os arquivos serão salvos
DOWNLOADED_LOG = '/opt/airflow/data/raw/downloaded_files.txt'               # Arquivo que guarda o histórico de quais arquivos já foram baixados

# Configurações padrão da DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,                           # quantas vezes tentar se falhar
    'retry_delay': timedelta(minutes=5),    # esperar 5 minutos antes de tentar de novo
}

# Definindo a DAG
@dag(
    schedule_interval='@daily',                  # roda todos os dias
    start_date=datetime(2024, 1, 1),             # data inicial
    catchup=False,                               # não tentar rodar datas antigas
    default_args=default_args,                   # configurações padrão
    tags=['vra', 'anac']                         # tags para organizar no painel
)
def download_new_vra_files():

    @task()
    def get_existing_files():
        """ Obter lista de arquivos já baixados """
        if not os.path.exists(DOWNLOADED_LOG):
            return []
        with open(DOWNLOADED_LOG, 'r') as f:
            files = [line.strip() for line in f.readlines()]
            return files

    @task()
    def get_available_files():
        """ Obter lista de arquivos disponíveis no site """
        response = requests.get(BASE_URL)
        matches = re.findall(r'VRA_2025_\d+\.csv', response.text, flags=re.IGNORECASE) # procura arquivos com padrão VRA_2025_01.csv, etc.
        matches = list(set(matches)) # remove duplicatas
        return matches

    @task()
    def download_new_files(available_files, existing_files):
        return "Baixando arquivos"

    # Chamando as tarefas da DAG (definindo a ordem de execução)
    existing_files = get_existing_files()
    available_files = get_available_files()
    download_new_files(available_files, existing_files)

# Inicializa a DAG
dag = download_new_vra_files()