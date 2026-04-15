# 📊 Análise de Acidentes de Trânsito em Belo Horizonte

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Metabase](https://img.shields.io/badge/Metabase-509EE3?style=for-the-badge&logo=metabase&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![ETL](https://img.shields.io/badge/ETL-Data%20Pipeline-FF6F00?style=for-the-badge)

> **Data Analytics & Data Warehouse**

Este dashboard foi desenvolvido como projeto prático da **Pós-Graduação em Inteligência Artificial e Machine Learning da PUC Minas**.

O projeto apresenta uma solução completa de Data Analytics para o estudo de acidentes de trânsito na cidade de Belo Horizonte, utilizando dados abertos da Prefeitura de Belo Horizonte (PBH).

A solução inclui desde o tratamento dos dados (ETL), modelagem dimensional em Data Warehouse (PostgreSQL) até a criação de dashboards interativos no Metabase.

**Principais insights explorados:**
- Influência da embriaguez na letalidade dos acidentes
- Regiões com maior incidência de colisões
- Perfil demográfico das vítimas e condutores
- Padrões temporais e condições que mais geram risco

---

## 🚀 Conceito Plug and Play

Todo o projeto foi construído com o conceito **Plug and Play**.  
Ao subir o ambiente, o Data Warehouse e o dashboard já vêm **100% configurados** com gráficos, filtros, cores e visuais prontos. Você não precisa criar nada manualmente.

---

## 🛠️ Pré-requisitos

- **Docker** e **Docker Compose** instalados (Docker Desktop recomendado no Windows)
- *Não é necessário instalar Python ou qualquer outra dependência na máquina hospedeira.*

---

## 📥 Instalação "One-Click" (Windows)

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/acidentes_bh.git
cd acidentes_bh
```
2. Execute o arquivo `start_project.bat` (basta dar **dois cliques** no arquivo).

O script automatizado irá:

- Solicitar privilégios de administrador
- Pausar qualquer instância local do PostgreSQL (porta 5432)
- Iniciar o Docker Desktop (caso esteja fechado)
- Configurar credenciais via `.env`
- Subir o Data Warehouse + Metabase
- Executar o pipeline ETL completo
- Abrir automaticamente o dashboard no seu navegador

---

## 📈 Acesso ao Dashboard (Metabase)

Após a inicialização, acesse:

**URL:** http://localhost:3000

**Credenciais de acesso:**
- **Login / Email:** `devin4237@uorak.com`
- **Senha:** `xLc9cskkE7Aci5U`

---

## 🧩 Estrutura do Projeto

| Pasta                  | Descrição |
|------------------------|---------|
| `data/`                | Dados brutos e arquivos Parquet otimizados |
| `notebooks/`           | Jupyter Notebooks com exploração e limpeza dos dados |
| `scripts/`             | Scripts Python usados no pipeline ETL e criação de Views |
| `metabase_data/`       | Volume persistente com toda configuração do dashboard |
| `docker-compose.yml`   | Orquestração completa dos serviços |
| `start_project.bat`    | Script de inicialização automática (Windows) |

---

## 🧠 Estudo Realizado

O dashboard está dividido em duas camadas principais:

### Painel Estratégico
- KPIs gerais de segurança viária
- Taxa de fatalidade
- Evolução anual de acidentes
- Impacto da embriaguez (comparação Year-over-Year)

### Painel Analítico
- **Geolocalização**: Mapa de calor dos pontos críticos da cidade
- **Fator Humano**: Idade, gênero e uso de equipamentos de segurança
- **Cena do Acidente**: Horários de pico, condições climáticas e vias mais perigosas

---

**Tecnologias utilizadas:**
- PostgreSQL (Data Warehouse)
- Docker & Docker Compose
- Python + Pandas (ETL)
- Metabase (Business Intelligence)
- Parquet (armazenamento otimizado)

---