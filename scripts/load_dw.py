import os
import pandas as pd
from sqlalchemy import create_engine, text # Adicionado 'text' aqui
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
    host = os.getenv("DB_HOST", "db") 
    
    db_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(db_uri)

    # --- NOVO: LIMPANDO AS VIEWS PARA EVITAR CONFLITO NO 'REPLACE' ---
    print("\nLimpando as Views antigas para liberar a atualização das tabelas...")
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                DROP VIEW IF EXISTS vw_painel_estrategico CASCADE;
                DROP VIEW IF EXISTS vw_analitico_condicoes CASCADE;
                DROP VIEW IF EXISTS vw_analitico_fator_humano CASCADE;
                DROP VIEW IF EXISTS vw_analitico_veiculos CASCADE;
                DROP VIEW IF EXISTS vw_analitico_geolocalizacao CASCADE;
            """))
        print("[OK] Views removidas (serão recriadas pelo script create_view.py).")
    except Exception as e:
        print(f"Aviso ao limpar views (pode ser que elas ainda não existam): {e}")
    # ----------------------------------------------------------------

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
            
            # Remove colunas onde todos os valores são nulos
            df = df.dropna(axis=1, how='all')
            
            print(f"Inserindo {len(df)} registros na tabela '{nome_tabela}'...")
            
            # Agora o 'replace' funcionará porque o CASCADE acima soltou as dependências
            df.to_sql(nome_tabela, con=engine, if_exists='replace', index=False)
            
            print(f"Sucesso! Tabela '{nome_tabela}' carregada.")
            
        except Exception as e:
            print(f"Erro ao processar a tabela {nome_tabela}: {str(e)}")

    print("\n✅ Carga do Data Warehouse finalizada com sucesso!")

if __name__ == "__main__":
    carregar_data_warehouse()