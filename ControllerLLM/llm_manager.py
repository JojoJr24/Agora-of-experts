from dataclasses import asdict
import subprocess
import os
import gradio as gr
import ollama

from ControllerExperts.experts_logic import ModelConfig, getLlmData
from modulesFolders import CHATS_DIR
from utils import read_json_file
from enum import Enum

class ModelSize(Enum):
    SMALL_MODEL = "small_model"
    MEDIUM_MODEL = "medium_model"
    BIG_MODEL = "big_model"


MODEL_SIZE_ITEMS = [model.value for model in ModelSize]

def model_config_to_json(config: ModelConfig):
    json_output = {
        "messages": config['messages'],
        "model": config['model'],
        "stream": config['stream'],
        "options": {
            "seed": config['seed'],
            "temperature": config['temperature'],
            "presence_penalty": config['presence_penalty'],
            "frequency_penalty": config['frequency_penalty'],
            "top_p": config['top_p']
        }
    }
        # Omitir claves nulas en las opciones
    json_output['options'] = {k: v for k, v in json_output['options'].items() if v is not None}
    
    # Omitir claves nulas en el JSON principal
    return {k: v for k, v in json_output.items() if v is not None}


if not os.path.exists(CHATS_DIR):
    os.makedirs(CHATS_DIR)

client = ollama.Client()

def zero_shot_for_agents(expert_selected,model_choice: ModelSize, prompt , system_message = ''):
    LLM_DATA = getLlmData(expert_selected)
    # Choose the model configuration based on model_choice
    model_config = getattr(LLM_DATA, model_choice)
    # Convert the selected ModelConfig instance to a dictionary
    request_params = asdict(model_config)
    # Handle 'prompt' based on its type
    if isinstance(prompt, str):
        # If 'prompt' is a string, create a message list including the system message if provided
        message = [
            {"role": "system", "content": LLM_DATA.system_message + system_message if system_message else LLM_DATA.system_message },
            {"role": "user", "content": prompt}
        ]
    elif isinstance(prompt, list):
        # If 'prompt' is a list, use it directly
        prompt[0]['content'] = LLM_DATA.system_message + prompt[0]['content']
        message = prompt
    else:
        raise TypeError("The 'prompt' argument must be either a string or a list of message dictionaries.")
    request_params['messages'] = message
    # Call the create method with the parameters from the ModelConfig
    response = client.chat(**model_config_to_json(request_params))['message']['content']
    return response

def zero_shot(expert_selected,model_choice: ModelSize, messages):
    LLM_DATA = getLlmData(expert_selected)
    # Choose the model configuration based on model_choice
    model_config = getattr(LLM_DATA, model_choice)
    # Convert the selected ModelConfig instance to a dictionary
    request_params = asdict(model_config)
    # Ensure 'messages' is provided and is a list
    if not request_params.get('messages'):
        messages.insert(0, {"role": "system", "content": LLM_DATA.system_message})
        request_params['messages'] = messages
    # Call the create method with the parameters from the ModelConfig
    response = client.chat(**model_config_to_json(request_params))['message']['content']
    print("ZERO_SHOT",response)
    return response


def promptStream(expert_selected, model_choice: ModelSize, messages):
    try:
        LLM_DATA = getLlmData(expert_selected)
        # Choose the model configuration based on model_choice
        model_config = getattr(LLM_DATA, model_choice)
        # Convert the selected ModelConfig instance to a dictionary
        request_params = asdict(model_config)
        # Ensure 'messages' is provided and is a list
        if not request_params.get('messages'):
            messages.insert(0, {"role": "system", "content": LLM_DATA.system_message})
            request_params['messages'] = messages
        if not request_params.get('stream'):
            request_params['stream'] = True
        #Call the create method with the parameters from the ModelConfig
        # Simulate sending the initial prompt to the model and receiving a stream of responses
        responses = client.chat(**model_config_to_json(request_params))
        return responses
    except Exception as e:
        gr.Error(f"Error during model prompt: {e}")



def get_model_list():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        output = result.stdout.strip().split("\n")[1:]  # Omitir la primera línea (encabezado)
        model_list = [line.split()[0] for line in output]  # Extraer los nombres de los modelos
        return model_list
    except Exception as e:
        gr.Error(f"Error executing command: {e}")
        return []
    

def create_chat_completion(params):
    global global_params
    global_params = params

    # Your OpenAI API call goes here
    pass