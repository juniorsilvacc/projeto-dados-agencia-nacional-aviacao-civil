import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection_url():
    """Retorna a URL de conexão com o PostgreSQL"""
    try:
        # Configuração do banco de dados PostgreSQL
        DB_CONFIG = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432"),
            "database": os.getenv("DB_NAME", ""),
            "user": os.getenv("DB_USER", ""),
            "password": os.getenv("DB_PASSWORD", "")
        }
        
        for key, value in DB_CONFIG.items():
            if not value:
                raise ValueError(f"Variável de ambiente '{key}' não definida")
            
        return f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    except Exception as e:
        print(f"Erro ao montar a URL de conexão: {e}")
        raise