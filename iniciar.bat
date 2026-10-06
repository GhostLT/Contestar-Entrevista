@echo off
chcp 65001 > nul
title Copiloto de Entrevistas - Gemini 3.8 Flash
cd /d "%~dp0"

echo ========================================================
echo    Iniciando Copiloto de Entrevistas en Tiempo Real
echo ========================================================

:: Verificar si existe el entorno virtual
if not exist "venv\Scripts\python.exe" (
    echo Creando entorno virtual e instalando paquetes...
    python -m venv venv
    venv\Scripts\python.exe -m pip install -r requirements.txt
)

:: Ejecutar el asistente con la ventana flotante
echo Abriendo ventana flotante...
start "" "venv\Scripts\pythonw.exe" main.py
exit
