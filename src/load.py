import os
import sys
import pandas as pd 
from config.db_config import get_db_connection_url 
from sqlalchemy import create_engine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def load_data(df: pd.DataFrame, table_name: str = "nome_da_tabela"):
    """ Salva o DataFrame no banco de dados PostgreSQL. """
    try:
        engine = create_engine(get_db_connection_url(), echo=True)
        df.to_sql(table_name, engine, if_exists="append", index=False)
        print(f"✅ Dados carregados na tabela '{table_name}'.")
    except Exception as e:
        print(f"❌ Erro ao carregar dados para o banco: {e}")
