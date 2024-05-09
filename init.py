import platform
import sys
import os

os_name = platform.system()

# Contiene la lógica de inicialización
def init():
    filename = get_initial_filename()
    
    if(filename is None):
        handle_error()
    else:
        run_init_file(filename)

        
# Devuelve el nombre del archivo que debe ser ejecutado
# de acuerdo con el sistema operativo del usuario
def get_initial_filename():
    files = {
        'Windows': 'Agora_Windows.bat',
        'Darwin': 'Agora_MacOs.sh',
        'Linux': 'Agora_Linux.sh'
    }

    return files.get(os_name)

# Ejecuta el archivo de inicialización
def run_init_file(filename: str):
    cmd = filename
    
    if(os_name != 'Windows'):
        cmd = f'chmod ugo+x {filename} ; ./{cmd}'

    os.system(cmd)

# Muestra un mensaje de error y finaliza el proceso
def handle_error():
    print('La app no es compatible con tu sistema operativo')
    sys.exit()

if __name__ == "__main__":
    init()