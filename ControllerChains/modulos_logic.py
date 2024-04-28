import os
import importlib.util

from modulesFolders import MODULES_DIR

def cargar_funciones():
    funciones = {}
    for archivo in os.listdir(MODULES_DIR):
        if archivo.endswith(".py"):  # Asegura que el archivo es un módulo de Python
            ruta_archivo = os.path.join(MODULES_DIR, archivo)
            nombre_modulo = os.path.splitext(archivo)[0]  # Obtiene el nombre del módulo sin la extensión .py
            spec = importlib.util.spec_from_file_location(nombre_modulo, ruta_archivo)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            # Añade solo las funciones definidas en el módulo (no importadas) al diccionario, excepto 'zero_shot'
            funciones.update({
                nombre: func for nombre, func in vars(modulo).items()
                if callable(func) and func.__module__ == modulo.__name__ 
            })
    return funciones



MODULOS = cargar_funciones()
NOMBRES_MODULOS =  list(MODULOS.keys())
