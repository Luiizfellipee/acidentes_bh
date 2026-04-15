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
    print("Iniciando a conexão com o Postgres para criação das Views...")
    
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    port = os.getenv("DB_PORT", "5432")
    host = os.getenv("DB_HOST", "db")
    
    db_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(db_uri)

    # ==========================================
    # SQL das Views Otimizadas e Tratadas
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
                
                -- TRATAMENTO ABSOLUTO: Cobre vazios, nulos e falhas de acentuação/digitação
                CASE 
                    WHEN b.desc_regional IS NULL OR TRIM(b.desc_regional) = '' THEN 'NÃO INFORMADA'
                    WHEN TRIM(UPPER(b.desc_regional)) IN ('NAO INFORMADA', 'NAO INFORMADO', 'NÃO INFORMADO') THEN 'NÃO INFORMADA'
                    ELSE TRIM(UPPER(b.desc_regional))
                END AS desc_regional,           
                
                b.indicador_fatalidade,    
                
                -- Flags tratadas de forma otimizada para gráficos de Pizza/Percentagem
                COALESCE(e_flag.embriagado, 0) AS flag_acidente_embriaguez,
                CASE WHEN COALESCE(e_flag.embriagado, 0) = 1 THEN 0 ELSE 1 END AS flag_acidente_sobrio
                
            FROM fato_boletins b
            -- LEFT JOIN otimizado (muito mais rápido que subquery direta no SELECT)
            LEFT JOIN (
                SELECT cod_boletim, 1 AS embriagado
                FROM dim_envolvidos
                -- UPPER previne erros caso o Pandas tenha salvo como 'sim', 'Sim' ou 'SIM'
                WHERE UPPER(embreagues) IN ('SIM', 'S') 
                GROUP BY cod_boletim
            ) e_flag ON b.cod_boletim = e_flag.cod_boletim;
        """,
        
        "vw_analitico_condicoes": """
            CREATE OR REPLACE VIEW vw_analitico_condicoes AS
            SELECT 
                b.cod_boletim,
                b.desc_tempo,              
                b.faixa_hora,            
                b.hora,                  
                b.velocidade_permitida,    
                l.tipo_logradouro,
                l.nome_logradouro,    -- Adicionado para ranking de Ruas Perigosas
                l.bairro              -- Adicionado para ranking de Bairros Perigosos
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
                e.sexo,                     -- Adicionado para perfil demográfico
                e.categoria_habilitacao,    -- Adicionado para análise de tipo de CNH
                e.cinto_seguranca,         
                e.pedestre                 
            FROM dim_envolvidos e
            LEFT JOIN fato_boletins b ON e.cod_boletim = b.cod_boletim;
        """,
        
        "vw_analitico_veiculos": """
            CREATE OR REPLACE VIEW vw_analitico_veiculos AS
            SELECT 
                v.cod_boletim,
                v.descricao_especie,
                v.desc_situacao             -- Adicionado: Estava em movimento ou estacionado?
            FROM dim_veiculos v;
        """,
        
        "vw_analitico_geolocalizacao": """
            CREATE OR REPLACE VIEW vw_analitico_geolocalizacao AS
            SELECT 
                b.cod_boletim,
                b.indicador_fatalidade,
                c.latitude,
                c.longitude
            FROM fato_boletins b
            INNER JOIN dim_coordenadas c ON b.cod_boletim = c.numero_bol
            WHERE c.latitude IS NOT NULL AND c.longitude IS NOT NULL;
        """
    }

    try:
        with engine.begin() as conn:
            for nome_view, query in views_sql.items():
                print(f"A criar view otimizada: {nome_view}...")
                conn.execute(text(query))
        print("\n✅ Todas as views foram criadas com sucesso no Data Warehouse!")
        print("Sincronize a base de dados no Metabase para começar a criar os painéis.")
        
    except Exception as e:
        print(f"\n❌ Erro ao criar as views: {str(e)}")

if __name__ == "__main__":
    criar_views_metabase()