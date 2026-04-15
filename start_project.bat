@echo off
setlocal enabledelayedexpansion

:: ========================================================
:: AUTO-ELEVAÇÃO PARA ADMINISTRADOR
:: ========================================================
net session >nul 2>&1
if not "%errorLevel%"=="0" (
    echo Solicitando privilegios de Administrador...
    powershell -NoProfile -Command "Start-Process -FilePath '%~dpnx0' -Verb RunAs"
    exit /b
)

:: VOLTA O TERMINAL PARA A PASTA DO PROJETO
cd /d "%~dp0"

echo ========================================================
echo        INICIANDO SETUP DO PROJETO - ACIDENTES BH
echo ========================================================
echo.

:: 1. VERIFICA E PARA O POSTGRESQL LOCAL (SERVIÇO WINDOWS)
echo [1/5] Verificando servico PostgreSQL local...
for /f "tokens=*" %%s in ('powershell -NoProfile -command "Get-Service -Name '*postgres*' -ErrorAction SilentlyContinue | Where-Object {$_.Status -eq 'Running'} | Select-Object -ExpandProperty Name"') do (
    echo [AVISO] Servico local '%%s' detectado. Parando...
    net stop "%%s" >nul 2>&1
)

:: 2. VERIFICA O DOCKER
echo.
echo [2/5] Verificando status do Docker...
where docker >nul 2>&1
if not "%errorLevel%"=="0" (
    echo [ERRO CRITICO] Docker nao encontrado no sistema!
    pause
    exit /b
)
docker info >nul 2>&1
if not "%errorLevel%"=="0" (
    echo Abrindo o Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    :WAIT_DOCKER
    timeout /t 5 /nobreak >nul
    docker info >nul 2>&1
    if not "!errorLevel!"=="0" goto WAIT_DOCKER
)

:: --- NOVA LÓGICA DE LIMPEZA CIRÚRGICA ---
echo [3/5] Verificando conflitos de porta no Docker...

:: Busca especificamente por containers usando a porta 5432
for /f "tokens=*" %%i in ('docker ps --filter "publish=5432" -q') do (
    echo [AVISO] Detectado container %%i ocupando a porta 5432. Parando...
    docker stop %%i >nul 2>&1
)

:: Para garantir, remove apenas os containers DESTE projeto (sem apagar volumes)
docker-compose down >nul 2>&1
echo [OK] Ambiente Docker preparado.

:: 3. CRIAÇÃO AUTOMÁTICA DO .env
echo.
echo [4/5] Checando credenciais...
if not exist ".env" (
    echo DB_USER=admin> .env
    echo DB_PASSWORD=admin>> .env
    echo DB_NAME=acidentes_db>> .env
    echo DB_PORT=5432>> .env
)
for /f "tokens=1,2 delims==" %%A in (.env) do (
    if "%%A"=="DB_USER" set TEST_USER=%%B
    if "%%A"=="DB_NAME" set TEST_DB=%%B
)

:: 4. SOBE A INFRA E RODA O PYTHON
echo.
echo [5/5] Subindo Servidores e Injetando Dados (Docker)...
docker-compose --env-file .env up -d

echo.
echo Aguardando o Banco de Dados iniciar...
:CHECK_DB
docker exec postgres_acidentes pg_isready -U !TEST_USER! >nul 2>&1
if not "!errorLevel!"=="0" (
    timeout /t 5 /nobreak >nul
    goto CHECK_DB
)

echo [OK] O Banco esta online! 
echo Aguardando o script Python processar os Parquets e criar as Views...
echo (Isso leva cerca de 2 minutos. Por favor, nao feche a janela!)

:: ========================================================
:: O LOOP DE ESPERA DO ETL
:: ========================================================
:WAIT_PYTHON
for /f "tokens=*" %%i in ('docker inspect -f "{{.State.Status}}" python_etl_acidentes 2^>nul') do set PYTHON_STATUS=%%i
if not "!PYTHON_STATUS!"=="exited" (
    timeout /t 5 /nobreak >nul
    goto WAIT_PYTHON
)

:: VERIFICA SE O PYTHON DEU ERRO
for /f "tokens=*" %%i in ('docker inspect -f "{{.State.ExitCode}}" python_etl_acidentes 2^>nul') do set PYTHON_EXIT=%%i
if not "!PYTHON_EXIT!"=="0" (
    echo.
    echo [ERRO CRITICO] O processamento Python falhou!
    echo ================= LOGS DO ERRO =================
    docker logs python_etl_acidentes
    echo ================================================
    pause
    exit /b
)

:: 5. AUDITORIA FINAL
echo.
echo Realizando Auditoria no Banco de Dados...
for /f "tokens=*" %%c in ('docker exec postgres_acidentes psql -U !TEST_USER! -d !TEST_DB! -t -A -c "SELECT count(*) FROM information_schema.tables WHERE table_schema='public';"') do set TABLE_COUNT=%%c

if "!TABLE_COUNT!"=="0" (
    echo [ERRO CRITICO] O Banco de Dados esta vazio!
    docker logs python_etl_acidentes
    pause
    exit /b
) else (
    echo [OK] Auditoria Concluida! !TABLE_COUNT! Tabelas/Views detectadas.
)

:: ========================================================
:: FINALIZAÇÃO
:: ========================================================
echo.
echo ========================================================
echo             SETUP FINALIZADO COM SUCESSO!
echo ========================================================
timeout /t 3 /nobreak >nul

start http://localhost:3000
exit