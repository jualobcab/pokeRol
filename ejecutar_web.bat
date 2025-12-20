@echo off
echo 🎲 Iniciando aplicacion web PokeRol...
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Cambiar a la carpeta web
cd web

REM Verificar si existe la base de datos
if not exist "..\pokeRol.db" (
    echo ❌ Error: No se encontro la base de datos pokeRol.db
    echo Asegurate de que el archivo existe en la raiz del proyecto.
    pause
    exit /b 1
)

REM Verificar si Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python no esta instalado o no esta en el PATH
    echo Instala Python desde https://python.org
    pause
    exit /b 1
)

REM Instalar dependencias si es necesario
echo 📦 Instalando dependencias...
pip install -r requirements.txt

REM Ejecutar la aplicacion
echo.
echo 🚀 Iniciando servidor web...
echo 📱 La aplicacion estara disponible en: http://localhost:5000
echo ⚡ Presiona Ctrl+C para detener el servidor
echo.
python app.py

pause