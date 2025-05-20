import pandas as pd
import os

def transform_data(df):
    """ Remove valores nulos e normaliza colunas do DataFrame. """
    
    # === 1. Limpeza inicial ===
    
    # Limpar nomes das colunas
    df.columns = df.columns.str.strip()
    
    # Renomear para  "snake_case"
    rename_map = {
        'Sigla ICAO Empresa Aérea': 'icao_empresa',
        'Empresa Aérea': 'empresa',
        'Número Voo': 'numero_voo',
        'Código DI': 'codigo_di',
        'Código Tipo Linha': 'codigo_tipo_linha',
        'Modelo Equipamento': 'modelo_equipamento',
        'Número de Assentos': 'assentos',
        'Sigla ICAO Aeroporto Origem': 'icao_origem',
        'Descrição Aeroporto Origem': 'origem',
        'Partida Prevista': 'partida_prevista',
        'Partida Real': 'partida_real',
        'Sigla ICAO Aeroporto Destino': 'icao_destino',
        'Descrição Aeroporto Destino': 'destino',
        'Chegada Prevista': 'chegada_prevista',
        'Chegada Real': 'chegada_real',
        'Situação Voo': 'situacao_voo',
        'Justificativa': 'justificativa',
        'Referência': 'referencia',
        'Situação Partida': 'situacao_partida',
        'Situação Chegada': 'situacao_chegada'
    }
    df = df.rename(columns=rename_map)
    
    # === 2. Conversão de datas ===
    
    # Converter colunas de data/hora
    date_cols = ['partida_prevista', 'partida_real', 'chegada_prevista', 'chegada_real']
    for coluna in date_cols:
        df[coluna] = pd.to_datetime(df[coluna], format='%d/%m/%Y %H:%M', errors='coerce')

    df['referencia'] = pd.to_datetime(df['referencia'], format='%Y-%m-%d', errors='coerce')
    
    # === 3. Cálculo de atrasos ===
    
    # Calcular atraso em minutos
    df['atraso_partida'] = (df['partida_real'] - df['partida_prevista']).dt.total_seconds() / 60
    df['atraso_chegada'] = (df['chegada_real'] - df['chegada_prevista']).dt.total_seconds() / 60
    df['voo_atrasado'] = df['atraso_chegada'] > 15
    
    # Substituir True/False por Sim/Não
    df['voo_atrasado'] = df['voo_atrasado'].map({True: 'Sim', False: 'Não'}).astype('category')

    # === 4. Gerar ID único para o voo ===
    
    df['voo_id'] = df['icao_empresa'] + '-' + df['numero_voo'].astype(str)
    
    # === 5. Tratamento de valores ausentes ===
    
    # Tratar valores ausentes com "texto"
    fillna_categorical = {
        'justificativa': 'Não informado',
        'situacao_voo': 'Não informado',
        'situacao_partida': 'Não informado',
        'situacao_chegada': 'Não informado'
    }
    df = df.fillna(value=fillna_categorical)
    
    # Tratar valores ausentes com "númerico"
    fillna_numeric = ['assentos', 'atraso_partida', 'atraso_chegada']
    for col in fillna_numeric:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    
    # Remover colunas que não têm nenhum valor
    df = df.dropna(axis=1, how='all')
    
    return df