import json
import os
import importlib.util

from ControllerLLM.llm_manager import zero_shot_for_agents
from modulesFolders import TOOLS_DIR
from utils import createMessages

def cargar_tools():
    funciones = {}
    for archivo in os.listdir(TOOLS_DIR):
        if archivo.endswith(".py"):  # Asegura que el archivo es un módulo de Python
            ruta_archivo = os.path.join(TOOLS_DIR, archivo)
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


TOOLS = cargar_tools()
NOMBRES_TOOLS = [nombre for nombre in TOOLS.keys() if '_call' not in nombre and '_helper' not in nombre]


def tool_bot(expert_selected,history,tools_dropdown,model_dropdown , recursion = 0):
    # Extract the last question in the task
    
    tools_info = "\n".join([f'tool:"{tool}", description:"{TOOLS[tool+"_call"]()}"' for tool in tools_dropdown])
    system_message= f"""You have some tools.First you must write step by step what data you will need to answer the question in the best way posible using the tools. After that you must generate a JSON object with the list of tools, each one with two keys, tool and parameter(even if there is only one tool, it must be a list of one object).
        This JSON structure is essential for requesting operations from your toolset. Please ensure that each tool interaction follows this format, adapting the parameter content as required by the specific tool's documentation.
        Structure:
        {{
            "tools": [ 
                {{
                    "tool": "",
                    "parameter": ""
                }}
            ]
        }}
        Available  Tools :
        tool:"helper", description:If you need to send to a tool the result of a previous tool call this helper"
        {tools_info}
        """
    # Generate the plan using the zero_shot_for_agents function
    plan_prompt_response = zero_shot_for_agents(expert_selected,model_dropdown,prompt= createMessages(history,system_message), system_message= system_message)
    print(plan_prompt_response)

    responses = ""
    try:
        start_json = plan_prompt_response.find("{")
        end_json = plan_prompt_response.rfind("}") + 1
        # Extrae el JSON del texto
        json_string = plan_prompt_response[start_json:end_json]
        # Convierte la cadena JSON en un diccionario de Python
        data = json.loads(json_string)
        tools = []
        # Suponiendo que data es el diccionario que contiene la información del JSON
        tools = data['tools'] 
        # Recorre la lista de herramientas y sus parámetros
        for tool in tools:
            # Obtiene el nombre de la herramienta
            tool_name = tool['tool']
            if tool_name == "helper":
                if recursion  < 3 :               
                    history[-1][0] += f"\n I know this: \n {responses}"
                    recursion += 1
                    tool_bot(expert_selected,history,tools_dropdown,model_dropdown, recursion)
            else:    
                # Obtiene los parámetros asociados a la herramienta
                parameter = tool['parameter']
                responses += str(TOOLS[tool_name](parameter))
    except Exception as e:        
        responses = "No se pueden cargar las herramientas"
        print("RESP", e , responses)    

        
    
    final_system_message= f"""You called some tools and they give you responses that you need to answer the user question. Use it to give your final response.
        If the responses have nothing to do with the question then don`t answer the question, help the user to improve the request.
        Responses from the tools:
        {responses}
        """
    final_response = zero_shot_for_agents(expert_selected,model_dropdown,prompt=createMessages(history,final_system_message) , system_message= final_system_message)
    return final_response