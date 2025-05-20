from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data
from datetime import datetime
import os

def main ():
    name_file, df = extract_data()
    
    df_processed = transform_data(df)

    # Gera novo nome com base no original + timestamp
    name_base = os.path.splitext(name_file)[0]  # Remove .csv
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    name_exit = f"{name_base}_Tratado_{timestamp}.csv"

    # Garante que a pasta processed exista
    os.makedirs("data/processed", exist_ok=True)

    # Salva o CSV transformado
    caminho_saida = os.path.join("data/processed", name_exit)
    df_processed.to_csv(caminho_saida, index=False)

    print(f"\n✅ Dados transformados salvos em: {caminho_saida}")

if __name__ == '__main__':
    main()