from dataclasses import asdict, dataclass
import subprocess
import os
from typing import Dict, List, Optional, Union
import gradio as gr
from groq import Groq
import ollama
from openai import OpenAI
from pydantic_core import CoreConfig

from CONFIG import VISION_MODEL
from ControllerExperts.experts_logic import getLlmData
from modulesFolders import CHATS_DIR
from enum import Enum


class ModelSize(Enum):
    SMALL_MODEL = "small_model"
    MEDIUM_MODEL = "medium_model"
    BIG_MODEL = "big_model"


MODEL_SIZE_ITEMS = [model.value for model in ModelSize]

def model_config_to_json(config: CoreConfig):
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
# List local models using ollama
result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
local_output = result.stdout.strip().split("\n")[1:]  # Skip the first line (header)
ollama_models = [line.split()[0] for line in local_output]  # Extract model names
# Set up OpenAI API key (ensure this is set in your environment or set directly here)
clientOAI = OpenAI()
# Get model list from OpenAI
openai_models_list= clientOAI.models.list().data
print(openai_models_list)
openai_models = ["OAI-" + model.id for model in openai_models_list if 'gpt' in model.id or 'davinci' in model.id or 'curie' in model.id]

groq_models_list =  ['GROQ-llama3-8b-8192', 'GROQ-llama3-70b-8192', 'GROQ-mixtral-8x7b-32768', 'GROQ-gemma-7b-it']
print(os.environ.get("GROQ_API_KEY"))
clientGroq = Groq(api_key=os.environ.get("GROQ_API_KEY"),)

def get_model_list():
    try:       
        # Combine local and OpenAI model lists
        combined_model_list = ollama_models + openai_models + groq_models_list
        return combined_model_list
    except Exception as e:
        print(e)
        gr.Error(f"Error executing command: {e}")
        return []
#Init
get_model_list()

def llm_call(expert_selected, model_choice: ModelSize, messages: Union[str, List[Dict]], system_message: str = '', stream: bool = False, files: List[str] = [], override_system_message: bool = False):
    # Fetch the LLM data based on expert selection
    LLM_DATA = getLlmData(expert_selected)
    # Fetch the model configuration based on the selected size
    model_config = getattr(LLM_DATA, model_choice)
    # Convert the ModelConfig instance to a dictionary
    request_params = asdict(model_config)
        # Determine the system message to use based on override flag
    final_system_message = system_message if override_system_message else LLM_DATA.system_message + system_message
    return llm_direct_call(request_params,messages,final_system_message,stream,files)


def llm_direct_call(request_params, messages: Union[str, List[Dict]], system_message: str = '', stream: bool = False, files: List[str] = []):
    # Prepare the 'messages' parameter based on the type of 'messages' input
    if isinstance(messages, str):
        # If 'messages' is a string, it is treated as a user's prompt with an optional system message prepended
        message_list = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": messages}
        ]
    elif isinstance(messages, list):
        # If 'messages' is already a list, use it directly
        message_list = [
            {"role": "system", "content": system_message},
            *messages
        ]

    else:
        raise TypeError("The 'messages' argument must be either a string or a list of message dictionaries.")
    
    # Handle vision models if files are provided
    if len(files) > 0:
        request_params["model"] = VISION_MODEL
        message_list[-1]["images"] = files
    
    # Add the prepared message list to the request parameters
    request_params['messages'] = message_list
    # Set the 'stream' parameter in the request if streaming is required
    if stream:
        request_params['stream'] = True
    
    response = "Error"
    print(request_params)
    # Make the API call using the prepared configuration
    modelOAI = esOAI(request_params["model"])
    modelGROQ = esGROQ(request_params["model"])
    try:
        if modelOAI :
            response = clientOAI.chat.completions.create(
                        model=modelOAI,
                        messages=request_params["messages"],
                        temperature=request_params["temperature"],
                        max_tokens=256,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        stream=request_params['stream']
                        )
            return response if stream else response.choices[0].message.content
        elif modelGROQ :
            response = clientGroq.chat.completions.create(
                        model=modelGROQ,
                        messages=request_params["messages"],
                        temperature=request_params["temperature"],
                        max_tokens=request_params["max_tokens"],
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        stream=request_params['stream']
                        )
            return response if stream else response.choices[0].message.content
        else:
            response = client.chat(**model_config_to_json(request_params))
            return response if stream else response['message']['content']
        
    except Exception as e:
        gr.Error(f"Error during model interaction: {e}")
        return ""



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

    


