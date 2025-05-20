from src.extract import get_unprocessed_files
from src.transform import transform_data
from src.load import load_data
from datetime import datetime
import pandas as pd
import os

def main ():
    unprocessed_files = get_unprocessed_files()

    if not unprocessed_files:
        print("✅ Nenhum novo arquivo para processar.")
        return

    os.makedirs("data/processed", exist_ok=True)
    log_path = "data/processed/processed_files.txt"

    for name_file in unprocessed_files:
        print(f"🔄 Processando {name_file}...")

        path_file = os.path.join("data/raw", name_file)
        df = pd.read_csv(path_file, sep=';', encoding='utf-8')
        df_processed = transform_data(df)

        # Gera nome novo
        name_base = os.path.splitext(name_file)[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        name_exit = f"{name_base}_Tratado_{timestamp}.csv"

        # Salva CSV transformado
        path_exit = os.path.join("data/processed", name_exit)
        df_processed.to_csv(path_exit, index=False)

        # Registra que foi processado
        with open(log_path, 'a') as log:
            log.write(f"{name_file}\n")

        print(f"✅ Salvo: {path_exit}")

if __name__ == '__main__':
    main()