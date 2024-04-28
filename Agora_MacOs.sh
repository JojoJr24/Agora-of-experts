#!/bin/bash

# Detiene la ejecución si ocurre un error
set -e

# Función para verificar si un comando existe
command_exists() {
  command -v "$@" > /dev/null 2>&1
}

# 1. Verificar si Ollama está instalado y, si no, pedir al usuario que lo instale manualmente
if command_exists ollama; then
  echo "Ollama ya está instalado."
else
  echo "Por favor, instala Ollama manualmente visitando https://ollama.com/download/mac"
  echo "Después de la instalación, vuelve a ejecutar este script."
  exit 1
fi

# Función para verificar si el modelo phi3 está instalado
nomic-embed-text_installed() {
  ollama list | grep -q "nomic-embed-text"
}

# 2. Verificar si el modelo phi3 de Ollama está instalado y, si no, instalarlo
if nomic-embed-text; then
  echo "El modelo nomic-embed-text ya está instalado."
else
  echo "Instalando el modelo nomic-embed-text de Ollama..."
  ollama pull nomic-embed-text
fi

# Función para verificar si el modelo phi3 está instalado
phi3_installed() {
  ollama list | grep -q "phi3"
}

# 2. Verificar si el modelo phi3 de Ollama está instalado y, si no, instalarlo
if phi3_installed; then
  echo "El modelo phi3 ya está instalado."
else
  echo "Instalando el modelo phi3 de Ollama..."
  ollama pull phi3
fi

# 3. Crear un entorno virtual para Python solo si no existe
if [ ! -d "./venv" ]; then
  echo "Creando un entorno virtual de Python..."
  python -m venv ./venv
else
  echo "El entorno virtual ya existe."
fi

# 4. Activar el entorno virtual
echo "Activando el entorno virtual..."
source ./venv/bin/activate

# 5. Verificar e instalar los requerimientos con pip solo si no están instalados
requirements_installed() {
  pip freeze > installed.txt
  diff requirements.txt installed.txt > /dev/null
  return $?
}

if requirements_installed; then
  echo "Los requerimientos ya están instalados."
else
  echo "Instalando los requerimientos..."
  pip install -r requirements.txt
fi

# 6. Ejecutar main.py
echo "Ejecutando main.py..."
python main.py

echo "Script completado exitosamente."
