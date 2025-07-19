from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import requests
import logging
import re
import os

# Logger do Airflow
logger = logging.getLogger(__name__)

# Constantes
BASE_URL = 'https://siros.anac.gov.br/siros/registros/diversos/vra/2025/'         # URL de onde os arquivos CSV estão disponíveis
DOWNLOAD_DIR = '/usr/local/airflow/data/raw'                                      # Pasta onde os arquivos serão salvos
DOWNLOADED_LOG = os.path.join(DOWNLOAD_DIR, 'downloaded_files.txt')               # Arquivo que guarda o histórico de quais arquivos já foram baixados

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
        try:
            logger.info("Verificando arquivos disponíveis...")
            response = requests.get(BASE_URL)
            matches = re.findall(r'VRA_2025_\d+\.csv', response.text, flags=re.IGNORECASE) # procura arquivos com padrão VRA_2025_01.csv, etc.
            matches = list(set(matches)) # remove duplicatas
            return matches
        except Exception as e:
            logger.error(f"Erro ao acessar {BASE_URL}: {e}")
            return []

    @task()
    def download_new_files(available_files, existing_files):
        """Faz o download apenas dos arquivos novos e atualiza o log"""
        new_files = list(set(available_files) - set(existing_files))
        downloaded = []
        
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)
        
        for filename in new_files:
            file_url = BASE_URL + filename
            local_path = os.path.join(DOWNLOAD_DIR, filename)

            try:
                logger.info(f"Baixando {file_url}")
                response = requests.get(file_url)
                response.raise_for_status()  # Gera erro se status != 200
                
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                    
                downloaded.append(filename)
            except Exception as e:
                logger.error(f"Erro ao baixar {file_url}: {e}")

        # Atualiza o log com os arquivos baixados
        if downloaded:
            with open(DOWNLOADED_LOG, 'a') as log_file:
                for file in downloaded:
                    log_file.write(file + '\n')

        logger.info(f"{len(downloaded)} arquivos novos baixados.")
        return f"{len(downloaded)} arquivos novos baixados."

    # Chamando as tarefas da DAG (definindo a ordem de execução)
    existing_files = get_existing_files()
    available_files = get_available_files()
    download_new_files(available_files, existing_files)

# Inicializa a DAG
dag = download_new_vra_files()