@echo off
setlocal
cd /d "%~dp0"

set "PORT=8000"
where py >nul 2>nul
if errorlevel 1 (
    echo Python Launcher ^(py^) nao foi encontrado.
    echo Instale o Python ou inicie um servidor HTTP nesta pasta manualmente.
    pause
    exit /b 1
)

start "Provas - servidor local" /min cmd /c "py -m http.server %PORT% --bind 127.0.0.1"
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:%PORT%/"

echo Prova aberta no navegador. Para encerrar o servidor, feche a janela minimizada "Provas - servidor local".
endlocal
