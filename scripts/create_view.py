import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ==========================================
# Configuração de Caminhos
# ==========================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
env_path = os.path.join(BASE_DIR, '.env')

load_dotenv(dotenv_path=env_path)

def criar_views_metabase():
    print("Iniciando conexão com o Postgres para criação das Views...")
    
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    port = os.getenv("DB_PORT", "5432")
    host = "localhost" 
    
    db_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(db_uri)

    # ==========================================
    # SQL das Views (Adequado ao tratamento Parquet)
    # Todas as chaves padronizadas para 'cod_boletim'
    # ==========================================
    views_sql = {
        "vw_painel_estrategico": """
            CREATE OR REPLACE VIEW vw_painel_estrategico AS
            SELECT 
                b.cod_boletim,
                b.ano,
                b.mês,
                b.data,
                b.desc_tipo_acidente,      
                b.desc_regional,           
                b.indicador_fatalidade,    
                COALESCE((
                    SELECT MAX(CASE WHEN e.embreagues = 'SIM' THEN 1 ELSE 0 END) 
                    FROM dim_envolvidos e 
                    WHERE e.cod_boletim = b.cod_boletim
                ), 0) AS flag_acidente_embriaguez
            FROM fato_boletins b;
        """,
        
        "vw_analitico_condicoes": """
            CREATE OR REPLACE VIEW vw_analitico_condicoes AS
            SELECT 
                b.cod_boletim,
                b.desc_tempo,              
                b.faixa_hora,            
                b.hora,                  
                b.velocidade_permitida,    
                l.tipo_logradouro          
            FROM fato_boletins b
            LEFT JOIN dim_logradouros l ON b.cod_boletim = l.cod_boletim;
        """,
        
        "vw_analitico_fator_humano": """
            CREATE OR REPLACE VIEW vw_analitico_fator_humano AS
            SELECT 
                e.cod_boletim,
                b.indicador_fatalidade,    
                e.condutor,                
                e.idade,                 
                e.cinto_seguranca,         
                e.pedestre                 
            FROM dim_envolvidos e
            LEFT JOIN fato_boletins b ON e.cod_boletim = b.cod_boletim;
        """,
        
        "vw_analitico_veiculos": """
            CREATE OR REPLACE VIEW vw_analitico_veiculos AS
            SELECT 
                v.cod_boletim,
                v.descricao_especie        
            FROM dim_veiculos v;
        """
    }

    try:
        with engine.begin() as conn:
            for nome_view, query in views_sql.items():
                print(f"Criando view: {nome_view}...")
                conn.execute(text(query))
        print("\n✅ Todas as views foram criadas com sucesso no Data Warehouse!")
        print("Sincronize o banco no Metabase para começar a criar os painéis.")
        
    except Exception as e:
        print(f"\n❌ Erro ao criar as views: {str(e)}")

if __name__ == "__main__":
    criar_views_metabase()