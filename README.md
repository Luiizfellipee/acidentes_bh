# 📊 Análise de Acidentes de Trânsito em Belo Horizonte (Data Analytics & DW)

Este projeto consiste em uma solução completa de Data Analytics para o estudo e visualização de acidentes de trânsito na cidade de Belo Horizonte, utilizando dados abertos da PBH. A solução abrange desde o tratamento de dados (ETL) e modelagem dimensional em um Data Warehouse (PostgreSQL) até a visualização em dashboards interativos no Metabase.

O objetivo do estudo é identificar padrões críticos, como a influência da embriaguez na letalidade, regiões com maior incidência de colisões e o perfil demográfico dos envolvidos, auxiliando na compreensão da segurança viária urbana.

## 🚀 Conceito Plug and Play
Este projeto foi desenvolvido sob o conceito Plug and Play. Toda a infraestrutura de banco de dados e a configuração do dashboard (gráficos, filtros e cores) já estão pré-configuradas e persistidas. Ao subir o ambiente, você não precisará criar nenhum gráfico do zero; o painel estará pronto para consumo.

## 🛠️ Pré-requisitos
Para rodar este projeto, você precisará apenas de:

Docker e Docker Compose instalados.

Python 3.10+ (para execução dos scripts de carga).

## 📥 Instalação e Configuração
Siga os passos abaixo para subir o ambiente na sua máquina local:

### 1. Clonar o Repositório
Bash
git clone https://github.com/seu-usuario/acidentes_bh.git
cd acidentes_bh

### 2. Subir a Infraestrutura (Docker)
Este comando iniciará os contêineres do banco de dados PostgreSQL e do Metabase.

Bash
docker-compose up -d

### 3. Instalar Dependências Python
Recomenda-se o uso de um ambiente virtual (venv).

Bash
pip install -r requirements.txt

### 4. Carga de Dados e Criação de Views
Execute os scripts para popular o banco de dados e criar as camadas lógicas de análise:

Bash
### Injeta os dados tratados (.parquet) no Data Warehouse
python scripts/load_dw.py

### Cria as views otimizadas para o dashboard
python scripts/create_view.py

## 📈 Acesso ao Dashboard (Metabase)
Após os contêineres estarem rodando e os scripts finalizados, o dashboard estará disponível em: http://localhost:3000.

### Credenciais de Primeiro Acesso:
Utilize os dados abaixo para visualizar os painéis Estratégico e Analítico:

Login/Email: devin4237@uorak.com

Senha: xLc9cskkE7Aci5U

## 🧩 Estrutura do Projeto
data/: Contém os dados brutos e os arquivos tratados em formato Parquet para alta performance.

notebooks/: Jupyter Notebook com todo o processo de limpeza, normalização e tratamento de dados (Pandas).

scripts/: Scripts Python para automação do pipeline de dados e criação de Views SQL.

metabase_data/: Volume persistente que armazena a inteligência do dashboard (essencial para o Plug and Play).

docker-compose.yml: Orquestração dos serviços de banco de dados e BI.

## 🧠 Estudo Realizado
A análise foi dividida em duas grandes camadas:

Painel Estratégico: Focado em KPIs de alto nível, como taxa de fatalidade, evolução anual de acidentes e indicadores de embriaguez com comparação temporal (Year-over-Year).

Painel Analítico: Mergulho profundo nos dados, incluindo:

Geolocalização: Mapa de calor dos pontos críticos da cidade.

Fator Humano: Perfil de idade, gênero e uso de cinto de segurança.

Cena do Crime: Análise de horários de pico ("Relógio do Perigo"), condições climáticas e vias com maior incidência.

Projeto desenvolvido como parte da Pós-Graduação em Inteligência Artificial e Machine Learning - PUC Minas.
