import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import quote_plus

# 1. Carrega as variáveis de ambiente
load_dotenv()

def criar_camada_gold():
    usuario = os.getenv("DB_USER")
    senha = quote_plus(os.getenv("DB_PASSWORD"))
    host = os.getenv("DB_HOST")
    porta = os.getenv("DB_PORT")
    banco = os.getenv("DB_NAME")

    engine = create_engine(f'postgresql://{usuario}:{senha}@{host}:{porta}/{banco}')

    # 2. SQL com os nomes REAIS das colunas (vistos no terminal)
    sql_views = """
    CREATE SCHEMA IF NOT EXISTS analytics;

    -- VIEW 01: Master View (Fato + Envolvidos + Veículos)
    CREATE OR REPLACE VIEW analytics.v_detalhe_acidentes AS
    SELECT 
        b.cod_boletim,
        b.data,
        b.hora,
        b.ano,
        b.desc_tipo_acidente,
        e.sexo,
        e.idade,
        e.desc_severidade,    -- Ajustado: era e.descricao_severidade
        v.descricao_especie   -- Ajustado: era v.descricao_tipo_veiculo
    FROM public.boletins b
    LEFT JOIN public.envolvidos e ON b.cod_boletim = e.cod_boletim
    LEFT JOIN public.veiculos v ON b.cod_boletim = v.cod_boletim;

    -- VIEW 02: Resumo para Mapas
    CREATE OR REPLACE VIEW analytics.v_mapa_calor AS
    SELECT 
        b.cod_boletim,
        b.data,
        c.latitude,
        c.longitude,
        b.desc_tipo_acidente
    FROM public.boletins b
    INNER JOIN public.coordenadas c ON b.cod_boletim = c.numero_bol;
    """

    print("⏳ Aplicando modelagem final no Data Warehouse...")
    
    try:
        with engine.connect() as conexao:
            conexao.execute(text(sql_views))
            conexao.commit()
            print("✨ SUCESSO! Camada 'analytics' criada sem erros.")
            
    except Exception as e:
        print(f"❌ Erro na modelagem: {e}")

if __name__ == "__main__":
    criar_camada_gold()