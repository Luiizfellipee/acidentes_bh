import os
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv

# 1. Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def executar_carga():
    # 2. Busca as credenciais do "cofre" (.env)
    usuario = os.getenv("DB_USER")
    # quote_plus protege o '@' da sua senha acid@2026
    senha = quote_plus(os.getenv("DB_PASSWORD")) 
    host = os.getenv("DB_HOST")
    porta = os.getenv("DB_PORT")
    banco = os.getenv("DB_NAME")

    # 3. Cria a conexão com o Postgres (SQLAlchemy)
    endereco_db = f'postgresql://{usuario}:{senha}@{host}:{porta}/{banco}'
    engine = create_engine(endereco_db)

    # 4. Define onde estão os seus arquivos Parquet
    # Usamos o caminho relativo saindo da pasta /scripts e indo para /data
    folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'dados_tratados'))

    print(f"📂 Lendo arquivos de: {folder_path}")
    print("⏳ Iniciando carga no banco de dados...")

    # 5. Loop de Carga Automática
    for arquivo in os.listdir(folder_path):
        if arquivo.endswith('.parquet'):
            nome_tabela = arquivo.replace('.parquet', '')
            caminho_completo = os.path.join(folder_path, arquivo)
            
            # Lê o dado tratado
            df = pd.read_parquet(caminho_completo)
            
            # Envia para o Postgres
            # if_exists='replace' -> Cria a tabela ou substitui se já existir
            # index=False -> Não cria a coluna de índice do pandas no SQL
            df.to_sql(nome_tabela, engine, if_exists='replace', index=False)
            
            print(f"✅ Tabela '{nome_tabela}' carregada com sucesso! ({len(df)} linhas)")

if __name__ == "__main__":
    try:
        executar_carga()
        print("\n🏆 Carga finalizada com sucesso no seu DW!")
    except Exception as e:
        print(f"\n❌ Erro durante a carga: {e}")