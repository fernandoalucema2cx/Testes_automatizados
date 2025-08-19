@echo off
title Rodar testes Playwright (Pytest) - Menu Interativo
color 06

echo ==========================================
echo        RODAR TESTES - PLAYWRIGHT PYTEST
echo ==========================================
echo.

:: -------------------------
:: Escolher ambiente
:: -------------------------
echo Selecione o ambiente:
echo [1] Producao
echo [2] Pre-Producao
echo [3] Homologacao
echo [4] Dev
set /p ENV_OPCAO="Digite o numero do ambiente: "

if "%ENV_OPCAO%"=="1" set BASE_URL=https://interno-dev.qualida.de
if "%ENV_OPCAO%"=="2" set BASE_URL=https://interno-dev.monitoriadequalidade.com.br
if "%ENV_OPCAO%"=="3" set BASE_URL=https://homolog.monitoriadequalidade.com.br
if "%ENV_OPCAO%"=="4" set BASE_URL=https://sprint.monitoriadequalidade.com.br

echo.
echo Ambiente selecionado: %BASE_URL%
echo.

:: -------------------------
:: Escolher tipo de teste
:: -------------------------
echo Selecione o conjunto de testes:
echo [1] Todos
echo [2] Apenas Qualidade
echo [3] Apenas SS0
set /p TESTE_OPCAO="Digite o numero da opcao: "

set TEST_PATH=
if "%TESTE_OPCAO%"=="1" set TEST_PATH=tests
if "%TESTE_OPCAO%"=="2" set TEST_PATH=tests\01-Qualidade
if "%TESTE_OPCAO%"=="3" set TEST_PATH=tests\02-SS0

echo.
echo Testes selecionados: %TEST_PATH%
echo.

:: -------------------------
:: Configurações adicionais
:: -------------------------
set HEADLESS=false
set RETRIES=1
set WORKERS=1

:: -------------------------
:: Ativar venv se existir
:: -------------------------
if exist venv (
    call venv\Scripts\activate
)

:: -------------------------
:: Rodar pytest
:: -------------------------
echo Executando testes...
set BASE_URL=%BASE_URL%
set HEADLESS=%HEADLESS%
set RETRIES=%RETRIES%
set WORKERS=%WORKERS%

pytest %TEST_PATH% --html=playwright-report/index.html --self-contained-html --base-url=%BASE_URL%

echo.
echo ==========================================
echo        EXECUCAO FINALIZADA
echo ==========================================
pause
