import pandas as pd
import os 

RAW_PATH = "data/raw"

def extract_data():
    """ Lê um arquivos de fontes externas como CSV, API ou banco e um DataFrame com os dados brutos. """
    path = RAW_PATH
    
    files = []
    for f in os.listdir(path):
        if f.endswith(".csv"):
            files.append(f)
    
    if not files:
        raise FileNotFoundError("Nenhum arquivo CSV encontrado em data/raw")

    # Pega o mais recente ou o primeiro da lista (pode ordenar se quiser)
    name_file = files[0]
    path_file = os.path.join(path, name_file)
    
    # Lê o arquivo com o separador correto
    df = pd.read_csv(path_file, sep=';', encoding='utf-8')
    
    return name_file, df