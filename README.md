---

# 📊 Projeto: Análise de Acidentes de Trânsito - PBH

Este projeto consiste em uma infraestrutura completa de dados para a extração, carga, modelagem e visualização de dados de acidentes de trânsito da cidade de Belo Horizonte. A arquitetura utiliza containers Docker para garantir portabilidade e escalabilidade, integrando um banco de dados PostgreSQL, uma camada de transformação (Gold Layer) e o Metabase para BI.

## 🏗️ Arquitetura do Projeto

O projeto segue o padrão de medalhão (Bronze, Silver e Gold) para organização dos dados:

1. **Ingestão (Python/Pandas):** Leitura dos dados brutos e carga no PostgreSQL.
2. **Armazenamento (PostgreSQL):** Tabelas originais no schema `public`.
3. **Modelagem (Gold Layer):** Criação de Views otimizadas no schema `analytics` para facilitar o consumo via BI.
4. **Visualização (Metabase):** Dashboards e mapas de calor para análise espacial e temporal.
5. **Administração (Portainer):** Interface gráfica para monitoramento e gestão da stack de containers.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12
* **Banco de Dados:** PostgreSQL 15
* **Visualização:** Metabase
* **Orquestração:** Docker & Docker Compose
* **Gestão de Containers:** Portainer
* **Bibliotecas Python:** Pandas, SQLAlchemy, Psycopg2, Python-dotenv

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos

* Docker e Docker Compose instalados.
* Arquivo `.env` configurado na raiz do projeto com as credenciais do banco.

### 2. Subindo a Infraestrutura

No terminal, na pasta raiz do projeto, execute:

```bash
docker-compose up -d

```

Isso iniciará três serviços:

* **Postgres:** Porta `5432` (Banco de dados)
* **Metabase:** Porta `3000` (Business Intelligence)
* **Portainer:** Portas `9000` e `9443` (Gestão de containers)

### 3. Carga e Transformação de Dados

Com os containers rodando, execute os scripts Python para popular o banco e criar a camada analítica:

```bash
# Realiza a carga inicial dos dados brutos
python scripts/carga_postgres.py

# Cria as views da Camada Gold no schema analytics
python sql/modelagem_dw.py

```

## 📈 Camada Analítica (Gold Layer)

A modelagem final foi corrigida para lidar com inconsistências de nomes de colunas originais. No Metabase, utilize as views do schema `analytics`:

* `v_detalhe_acidentes`: Unifica dados de boletins, envolvidos e veículos em uma única tabela fato denormalizada.
* `v_mapa_calor`: Contém as coordenadas geográficas (`latitude`, `longitude`) vinculadas aos boletins para análises espaciais.

## 🐳 Gestão com Portainer

Para monitorar o status dos containers, logs e uso de memória:

1. Acesse `http://localhost:9000`.
2. Crie sua conta de administrador no primeiro acesso.
3. Navegue em **Environments > local > Containers** para visualizar a stack `acidentes_bh`.

## 📁 Estrutura de Pastas

```text
.
├── data/               # Arquivos CSV brutos
├── scripts/            # Scripts Python de ingestão
├── sql/                # Scripts SQL e modelagem de DW
├── .env                # Variáveis de ambiente (não versionar)
├── docker-compose.yaml # Orquestração dos containers
└── requirements.txt    # Dependências do projeto

```

---

### Notas:

* **Conexão no Metabase:** Ao conectar o Metabase ao banco de dados dentro do ambiente Docker, utilize o host `db` (nome do serviço no compose) em vez de `localhost`.
