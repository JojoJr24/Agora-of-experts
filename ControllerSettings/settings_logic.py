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

def getVisionModel():
    config_path = './config.json'
    config = read_json_file(config_path)
    if 'error' not in config:
        return config.get('vision_model')
    return None

def getEmbeddingModel():
    config_path = './config.json'
    config = read_json_file(config_path)
    print("AA",config.get('embedding_model'))
    return config.get('embedding_model')
