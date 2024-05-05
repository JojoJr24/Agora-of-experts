import json
import os
import importlib.util

from ControllerLLM.llm_manager import llm_call
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
NOMBRES_TOOLS = [nombre for nombre in TOOLS.keys() if '_call' not in nombre and '_name' not in nombre  and '_helper' not in nombre]


def tool_bot(expert_selected, history, tools_dropdown, model_dropdown, recursion=0):
    print(f"\033[92mExtracting the last question in the task...\033[0m")
    # Extract the last question in the task
    
    tools_info = "\n".join([f'tool:"{tool}", description:"{TOOLS[tool+"_call"]()}"' for tool in tools_dropdown])
    recursion_system_message= "Another AI needs your help. She received a task that she was unable to complete. He passed you the original assignment and the information he was able to get. Analyze the information to see what is missing, and what is missing to be able to finish the task.\n"
    
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
    if "I know this:" in history[-1][0] : system_message = recursion_system_message + system_message
    print(f"\033[94mGenerating plan using zero-shot-for-agents function...\033[0m")
    # Generate the plan using the zero_shot_for_agents function
    plan_prompt_response = llm_call(expert_selected,model_dropdown,messages= createMessages(history,system_message), system_message= system_message)
    print(plan_prompt_response)

    responses = ""
    try:
        print(f"\033[95mParsing JSON response...\033[0m")
        start_json = plan_prompt_response.find("{")
        end_json = plan_prompt_response.rfind("}") + 1
        # Extract the JSON from the text
        json_string = plan_prompt_response[start_json:end_json]
        # Convert the JSON string to a Python dictionary
        data = json.loads(json_string)
        tools = []
        # Assuming data is the dictionary containing the JSON information
        tools = data['tools'] 
        # Iterate over the list of tools and their parameters
        for tool in tools:
            # Get the tool name
            tool_name = tool['tool']
            if tool_name == "helper":
                if recursion  < 3 :               
                    history[-1][0] += f"\n I know this: \n {responses}"
                    recursion += 1
                    print(f"\033[91mRecursion detected! Recursing into tool_bot...\033[0m")
                    tool_bot(expert_selected,history,tools_dropdown,model_dropdown, recursion)
            else:    
                # Get the parameters associated with the tool
                parameter = tool['parameter']
                print(f"\033[93mCalling tool {tool_name} with parameter {parameter}...\033[0m")
                responses += str(TOOLS[tool_name](parameter))
                print(responses)
    except Exception as e:        
        responses = "No se pueden cargar las herramientas"
        print(f"\033[91mError: {e}. Unable to load tools.\033[0m")
        print("RESP", e , responses)    

    print(f"\033[96mGenerating final system message...\033[0m")
    final_system_message= f"""You called some tools and they give you responses that you need to answer the user question. Use it to give your final response.
        If the responses have nothing to do with the question then don`t answer the question, help the user to improve the request.
        Responses from the tools:
        {responses}
        """
    print(f"\033[94mGenerating final response...\033[0m")
    final_response = llm_call(expert_selected,model_dropdown,messages=createMessages(history,final_system_message) , system_message= final_system_message)
    return final_response