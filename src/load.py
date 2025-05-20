import pandas as pd
from config.db_config import get_db_connection_url 
from sqlalchemy import create_engine

def load_data(df):
    """ Salva o DataFrame no banco de dados PostgreSQL. """
    engine = create_engine(get_db_connection_url())
    df.to_sql("nome_da_tabela", engine, if_exists="replace", index=False)