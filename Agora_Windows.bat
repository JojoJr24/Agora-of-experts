@echo off
setlocal enabledelayedexpansion

:: Detiene la ejecución si ocurre un error
set ERRORLEVEL=0

:: Función para verificar si Python está instalado
call :command_exists python PYTHON_EXISTS

:: 0. Verificar si Python está instalado y, si no, indicar al usuario que lo instale
if "!PYTHON_EXISTS!"=="1" (
  echo Python ya está instalado.
) else (
  echo Python no está instalado.
  echo Por favor, instala Python desde https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe y luego reinicia este script.
  goto :eof
)

:: Función para verificar si un comando existe
call :command_exists ollama OLLAMA_EXISTS

:: 1. Verificar si Ollama está instalado y, si no, pedir al usuario que lo instale
if "!OLLAMA_EXISTS!"=="1" (
  echo Ollama ya está instalado.
) else (
  echo Ollama no está instalado.
  echo Por favor, instala Ollama desde https://ollama.com/download/windows y luego reinicia este script.
  goto :eof
)

:: Función para verificar si el modelo phi3 está instalado
call :nomic-embed-text_installed nomic-embed-text_INSTALLED

:: 2. Verificar si el modelo phi3 de Ollama está instalado y, si no, instalarlo
if "!nomic-embed-text_INSTALLED!"=="1" (
  echo El modelo nomic-embed-text ya está instalado.
) else (
  echo Instalando el modelo nomic-embed-text de Ollama...
  ollama pull nomic-embed-text
)


:: Función para verificar si el modelo phi3 está instalado
call :phi3_installed PHI3_INSTALLED

:: 2Bis. Verificar si el modelo phi3 de Ollama está instalado y, si no, instalarlo
if "!PHI3_INSTALLED!"=="1" (
  echo El modelo phi3 ya está instalado.
) else (
  echo Instalando el modelo phi3 de Ollama...
  ollama pull phi3
)

:: 3. Crear un entorno virtual para Python solo si no existe
if not exist ".\venv\" (
  echo Creando un entorno virtual de Python...
  python -m venv .\venv
) else (
  echo El entorno virtual ya existe.
)

:: 4. Activar el entorno virtual
echo Activando el entorno virtual...
call .\venv\Scripts\activate

:: 5. Verificar e instalar los requerimientos con pip solo si no están instalados
call :requirements_installed REQUIREMENTS_INSTALLED
if "!REQUIREMENTS_INSTALLED!"=="1" (
  echo Los requerimientos ya están instalados.
) else (
  echo Instalando los requerimientos...
  pip install -r requirements.txt
)

:: 6. Ejecutar main.py
echo Ejecutando main.py...
python main.py

echo Script completado exitosamente.
goto :eof

:: Funciones auxiliares
:command_exists
  where %1 >nul 2>&1
  if %errorlevel% == 0 (set %2=1) else (set %2=0)
goto :eof

:phi3_installed
  ollama list | findstr /c:"phi3" >nul 2>&1
  if %errorlevel% == 0 (set %1=1) else (set %1=0)
goto :eof

:nomic-embed-text_installed
  ollama list | findstr /c:"nomic-embed-text" >nul 2>&1
  if %errorlevel% == 0 (set %1=1) else (set %1=0)
goto :eof

:requirements_installed
  pip freeze > installed.txt
  fc requirements.txt installed.txt > nul
  if %errorlevel% == 0 (set %1=1) else (set %1=0)
goto :eof
