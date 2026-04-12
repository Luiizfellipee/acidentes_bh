import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = os.path.dirname(SCRIPT_DIR)

DATA_DIR = os.path.join(BASE_DIR, 'data', 'dados_tratados')

env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=env_path)

def carregar_data_warehouse():
    print("Iniciando a configuração e conexão com o Postgres...")
    
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    port = os.getenv("DB_PORT", "5432")
    host = "localhost" 
    
    db_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(db_uri)

    mapeamento_dw = {
        os.path.join(DATA_DIR, "coordenadas.parquet"): "dim_coordenadas",
        os.path.join(DATA_DIR, "logradouros.parquet"): "dim_logradouros",
        os.path.join(DATA_DIR, "veiculos.parquet"): "dim_veiculos",
        os.path.join(DATA_DIR, "envolvidos.parquet"): "dim_envolvidos",
        os.path.join(DATA_DIR, "boletins.parquet"): "fato_boletins"
    }

    # Processamento e injeção de dados
    for caminho_arquivo, nome_tabela in mapeamento_dw.items():
        nome_arquivo = os.path.basename(caminho_arquivo) 
        
        if not os.path.exists(caminho_arquivo):
            print(f"Aviso: Arquivo {nome_arquivo} não encontrado em {DATA_DIR}. Pulando...")
            continue
            
        try:
            print(f"\nLendo dados de: {nome_arquivo}...")
            df = pd.read_parquet(caminho_arquivo)
            
            df = df.dropna(axis=1, how='all')
            
            print(f"Inserindo {len(df)} registros na tabela '{nome_tabela}'...")
            df.to_sql(nome_tabela, con=engine, if_exists='replace', index=False)
            
            print(f"Sucesso! Tabela '{nome_tabela}' carregada.")
            
        except Exception as e:
            print(f"Erro ao processar a tabela {nome_tabela}: {str(e)}")

    print("\n✅ Carga do Data Warehouse finalizada com sucesso!")

if __name__ == "__main__":
    carregar_data_warehouse()