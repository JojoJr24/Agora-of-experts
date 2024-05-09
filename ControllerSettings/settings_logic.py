import json


from utils import  read_json_file, write_json_file
def setVisionModel(vision_model):
    config_path = './config.json'
    config = read_json_file(config_path)
    if 'error' not in config:
        config['vision_model'] = vision_model
        return write_json_file(config, config_path)
    return config

def setEmbeddingModel(embedding_model):
    config_path = './config.json'
    config = read_json_file(config_path)
    if 'error' not in config:
        config['embedding_model'] = embedding_model
        return write_json_file(config, config_path)
    return config

def setChatTitleModel(chat_title_model):
    config_path = './config.json'
    config = read_json_file(config_path)
    if 'error' not in config:
        config['chat_title_model'] = chat_title_model
        return write_json_file(config, config_path)
    return config

def setDefaultModel(default_model):
    config_path = './config.json'
    config = read_json_file(config_path)
    if 'error' not in config:
        config['default_model'] = default_model
        return write_json_file(config, config_path)
    return config

def getVisionModel():
    config_path = './config.json'
    config = read_json_file(config_path)
    if 'error' not in config:
        return config.get('vision_model')
    return None

def getEmbeddingModel():
    config_path = './config.json'
    config = read_json_file(config_path)
    return config.get('embedding_model')

def getChatTitleModel():
    config_path = './config.json'
    config = read_json_file(config_path)
    return config.get('chat_title_model')

def getDefaultModel():
    config_path = './config.json'
    config = read_json_file(config_path)
    if 'error' not in config:
        return config.get('default_model')
    return None