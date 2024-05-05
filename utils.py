import random
import json
import os

def createMessages(history , system_message = ''):
    messages = []
    if system_message:
         messages.insert(0, {"role": "system", "content": system_message})

    # Build the messages array from history
    for item in history:
        # User message
        if item[0]:  # Check if the user message is not None
            messages.append({
                'role': 'user',
                'content': str(item[0])
            })
        # Assistant message
        if len(item) > 1 and item[1]:  # Check if there is an assistant message and it's not None
            messages.append({
                'role': 'assistant',
                'content': str(item[1])
            })
    return messages


def coin_flip():
    return random.randint(0, 1)


def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        # Si no existe el archivo, se crea con un diccionario vacío
        with open(file_path, 'w') as file:
            json.dump({}, file, indent=4)
            return {}
    except Exception as e:
        return {"error": str(e)}
    
def write_json_file(data, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            return {"success": True}
    except Exception as e:
        return {"error": str(e)}
    
def is_path(s):
    # A basic approach to check if a string could be a path is to look for directory separators
    # common in file paths (like "/" in UNIX-like systems and "\" in Windows).
    # This is a simple heuristic and might not cover all edge cases.
    return os.path.sep in s or (os.path.altsep is not None and os.path.altsep in s)


def esOAI(modelo):
    if "OAI-" in modelo:
        return modelo.replace("OAI-", "")
    else:
        return None
    
def esGROQ(modelo):
    if "GROQ-" in modelo:
        return modelo.replace("GROQ-", "")
    else:
        return None
    
def esOLLAMA(modelo):
    if "OLLAMA-" in modelo:
        return modelo.replace("OLLAMA-", "")
    else:
        return None

    


def getModelName(modelo):
    #oai = esOAI(modelo)
    #groq = esGROQ(modelo)  
    ollama = esOLLAMA(modelo) 
    if ollama : return ollama 
