import json
from dataclasses import asdict, dataclass, field
import os
from typing import Dict, Any, List, Optional
import datetime
import gradio as gr
from CONFIG import LOCATION
from modulesFolders import EXPERTS_DIR

@dataclass
class ModelConfig:
    messages: Optional[List[Dict]] = None  # Se ha cambiado a Optional para permitir el valor None    
    files: Optional[List[str]]= None
    model: Optional[str] = None
    frequency_penalty: float = 0.0
    max_tokens: int = 4096
    n: int = 1
    presence_penalty: float = 0.0
    seed: Optional[int] = None
    stream: bool = False
    temperature: float = 0.7
    top_logprobs: Optional[int] = None
    top_p: float = 1.0

@dataclass
class Config:
    system_message: str = ""
    small_model: ModelConfig = field(default_factory=lambda: ModelConfig(model="openhermes:latest"))
    medium_model: ModelConfig = field(default_factory=lambda: ModelConfig(model="nous-hermes2:10.7b"))
    big_model: ModelConfig = field(default_factory=lambda: ModelConfig(model="nous-hermes2-mixtral-16k:latest", max_tokens=16384))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        small_model_data = data.get("small_model", {})
        medium_model_data = data.get("medium_model", {})
        big_model_data = data.get("big_model", {})

        small_model = ModelConfig(**small_model_data)
        medium_model = ModelConfig(**medium_model_data)
        big_model = ModelConfig(**big_model_data)


        return cls(
            system_message=data.get("system_message", ""),
            small_model=small_model,
            medium_model=medium_model,
            big_model=big_model,
        )


def read_json_file(file_name):
    try:
        with open(EXPERTS_DIR + file_name + ".json", 'r') as file:
            data = json.load(file)
            return Config.from_dict(data)
    except Exception as e:
        return {"error": str(e)}
    
def write_json_file(file_name, config: Config):
    try:
        with open(EXPERTS_DIR + file_name + ".json", 'w') as file:
            json.dump(asdict(config), file, indent=4)
    except Exception as e:
        gr.Info(f"Error writing to file: {e}")

DEFAULT_EXPERT = "AoE_Basic"
LLM_DATA = read_json_file(DEFAULT_EXPERT)

def getLlmData(expert_selected, original = False):
    ret = read_json_file(expert_selected)
    if original:
        return ret
    ret.system_message = f"Today is: {datetime.datetime.now()}. You are in {LOCATION} \n" + LLM_DATA.system_message
    return ret

def getAllExperts():
    return [f.replace(".json", "") for f in os.listdir(EXPERTS_DIR) if f.endswith(".json")]

def loadLLMData(file):
    global LLM_DATA 
    LLM_DATA = read_json_file(file)

def load_experts(selected):
    global LLM_DATA
    LLM_DATA = read_json_file(selected)
    
    # Each key-value pair from each model configuration is outputted separately
    # Flatten all model experts into a single list that matches the UI components
    outputs = [
        LLM_DATA.system_message,  # Textbox
        LLM_DATA.small_model.model,  # Textbox
        LLM_DATA.small_model.frequency_penalty,  # Number
        LLM_DATA.small_model.max_tokens,  # Number
        LLM_DATA.small_model.n,  # Number
        LLM_DATA.small_model.presence_penalty,  # Number
        LLM_DATA.small_model.seed,  # Number
        LLM_DATA.small_model.stream,  # Checkbox
        LLM_DATA.small_model.temperature,  # Number
        LLM_DATA.small_model.top_logprobs,  # Number
        LLM_DATA.small_model.top_p,  # Number
        LLM_DATA.medium_model.model,  # Textbox
        LLM_DATA.medium_model.frequency_penalty,  # Number
        LLM_DATA.medium_model.max_tokens,  # Number
        LLM_DATA.medium_model.n,  # Number
        LLM_DATA.medium_model.presence_penalty,  # Number
        LLM_DATA.medium_model.seed,  # Number
        LLM_DATA.medium_model.stream,  # Checkbox
        LLM_DATA.medium_model.temperature,  # Number
        LLM_DATA.medium_model.top_logprobs,  # Number
        LLM_DATA.medium_model.top_p,  # Number
        LLM_DATA.big_model.model,  # Textbox
        LLM_DATA.big_model.frequency_penalty,  # Number
        LLM_DATA.big_model.max_tokens,  # Number
        LLM_DATA.big_model.n,  # Number
        LLM_DATA.big_model.presence_penalty,  # Number
        LLM_DATA.big_model.seed,  # Number
        LLM_DATA.big_model.stream,  # Checkbox
        LLM_DATA.big_model.temperature,  # Number
        LLM_DATA.big_model.top_logprobs,  # Number
        LLM_DATA.big_model.top_p   # Number
    ]

    return outputs



def update_expert(name, system_message, 
                  small_model_model, small_model_frequency_penalty, small_model_max_tokens, small_model_n, small_model_presence_penalty, small_model_seed, small_model_stream, small_model_temperature, small_model_top_logprobs, small_model_top_p, 
                  medium_model_model, medium_model_frequency_penalty, medium_model_max_tokens, medium_model_n, medium_model_presence_penalty, medium_model_seed, medium_model_stream, medium_model_temperature, medium_model_top_logprobs, medium_model_top_p,
                  big_model_model, big_model_frequency_penalty, big_model_max_tokens, big_model_n, big_model_presence_penalty, big_model_seed, big_model_stream, big_model_temperature, big_model_top_logprobs, big_model_top_p):
    
    small_model = ModelConfig(
        model=small_model_model, frequency_penalty=small_model_frequency_penalty, max_tokens=small_model_max_tokens, 
        n=small_model_n, presence_penalty=small_model_presence_penalty, seed=small_model_seed, stream=small_model_stream, 
        temperature=small_model_temperature, top_logprobs=small_model_top_logprobs, top_p=small_model_top_p
    )

    medium_model = ModelConfig(
        model=medium_model_model, frequency_penalty=medium_model_frequency_penalty, max_tokens=medium_model_max_tokens, 
        n=medium_model_n, presence_penalty=medium_model_presence_penalty, seed=medium_model_seed, stream=medium_model_stream, 
        temperature=medium_model_temperature, top_logprobs=medium_model_top_logprobs, top_p=medium_model_top_p
    )

    big_model = ModelConfig(
        model=big_model_model, frequency_penalty=big_model_frequency_penalty, max_tokens=big_model_max_tokens, 
        n=big_model_n, presence_penalty=big_model_presence_penalty, seed=big_model_seed, stream=big_model_stream, 
        temperature=big_model_temperature, top_logprobs=big_model_top_logprobs, top_p=big_model_top_p
    )

    config = Config(system_message=system_message, small_model=small_model, medium_model=medium_model, big_model=big_model)
    
    # Assume write_json_file is a function you have that writes the config to a JSON file
    write_json_file(name, config=config)
    
    return gr.Dropdown(choices=getAllExperts()),gr.Dropdown(choices=getAllExperts())

def delete_expert(expert_name):
    if(expert_name == DEFAULT_EXPERT):
        gr.Warning('AoE_Basib expert can not be deleted, you simpleton')
        return 
    # Construye el nombre del archivo a partir del nombre de la conversación
    filename = f"{EXPERTS_DIR}/{expert_name}.json"
    # Verifica si el archivo existe
    if os.path.exists(filename):
        # Elimina el archivo
        os.remove(filename)
        gr.Info(f"Expert '{expert_name}' has been deleted")
    else:
        gr.Info(f"Expert not found: '{expert_name}'.")
    return gr.Dropdown(choices=getAllExperts(), value=""),gr.Dropdown(choices=getAllExperts())