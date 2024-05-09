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
    expert: ModelConfig = field(default_factory=lambda: ModelConfig())


    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        expert_data = data.get("expert", {})
        expert = ModelConfig(**expert_data)

        return cls(
            system_message=data.get("system_message", ""),
            expert=expert,
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
    return sorted([f.replace(".json", "") for f in os.listdir(EXPERTS_DIR) if f.endswith(".json")])

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
        LLM_DATA.expert.frequency_penalty,  # Number
        LLM_DATA.expert.max_tokens,  # Number
        LLM_DATA.expert.n,  # Number
        LLM_DATA.expert.presence_penalty,  # Number
        LLM_DATA.expert.seed,  # Number
        LLM_DATA.expert.temperature,  # Number
        LLM_DATA.expert.top_logprobs,  # Number
        LLM_DATA.expert.top_p,  # Number
    ]

    return outputs



def update_expert(name, system_message, 
                   expert_frequency_penalty, expert_max_tokens, expert_n, expert_presence_penalty, expert_seed, expert_temperature, expert_top_logprobs, expert_top_p, 
                ):
    
    expert = ModelConfig(
        frequency_penalty=expert_frequency_penalty, max_tokens=expert_max_tokens, 
        n=expert_n, presence_penalty=expert_presence_penalty, seed=expert_seed, 
        temperature=expert_temperature, top_logprobs=expert_top_logprobs, top_p=expert_top_p
    )

    config = Config(system_message=system_message, expert=expert)
    
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