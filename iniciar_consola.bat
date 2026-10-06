@echo off
chcp 65001 > nul
title Copiloto de Entrevistas (Consola) - Gemini 3.8 Flash
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo Creando entorno virtual...
    python -m venv venv
    venv\Scripts\python.exe -m pip install -r requirements.txt
)

venv\Scripts\python.exe main.py --cli
pause
