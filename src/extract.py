import pandas as pd
import os 

RAW_PATH = "data/raw"
PROCESSED_LOG = "data/processed/processed_files.txt"

def get_unprocessed_files():
    """ Retorna uma lista de arquivos CSV ainda não processados. """
    
    # Cria o arquivo de log se ele não existir (para evitar erro na leitura)
    if not os.path.exists(PROCESSED_LOG):
        open(PROCESSED_LOG, 'w').close()
    
    # Lê os nomes dos arquivos já processados, removendo espaços e quebras de linha
    with open(PROCESSED_LOG, 'r') as f:
        processed = set(line.strip() for line in f)
    
    # Adiciona em ORDEM à lista files somente os arquivos CSV
    files = []
    files = sorted([
        f for f in os.listdir(RAW_PATH)
        if f.endswith('.csv')
    ])
    
    # Cria a lista de arquivos que ainda não foram processados
    unprocessed = []
    for f in files:
        if f not in processed:
            unprocessed.append(f)
    
    return unprocessed
    
def extract_data(name_file):
    """ Lê um arquivo específico da pasta raw e retorna o DataFrame. """
    path_file = os.path.join(RAW_PATH, name_file)
    df = pd.read_csv(path_file, sep=';', encoding='utf-8')
    return df