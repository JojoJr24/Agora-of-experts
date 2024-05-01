import json
import os
from ControllerChains.modulos_logic import MODULOS
from ControllerExperts.experts_logic import  getLlmData
from ControllerLLM.llm_manager import CHATS_DIR, ModelSize, esGROQ, esOAI, llm_call  
from ControllerRAG.rag_logic import generateResponse
from ControllerTools.tools_logic import tool_bot
from utils import createMessages, is_path
import gradio as gr
import time

def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)

def send_to_bot(history,
                expert_selected, 
                tps_text, 
                use_agent_checkbox, 
                modulo_dropdown, 
                stream_checkbox, 
                model_dropdown, 
                tools_agent_checkbox, 
                tools_dropdown, 
                collection_agent_checkbox, 
                collections_dropdown):

    # Procesar el agente de módulos
    if use_agent_checkbox and modulo_dropdown in MODULOS:
        response = MODULOS[modulo_dropdown](expert_selected, history, model_dropdown)
        update_history(history,response)
        yield history, "-1WPS"
        return
    
    # Procesar el agente de herramientas
    if tools_agent_checkbox and tools_dropdown:
        response = tool_bot(expert_selected, history, tools_dropdown, model_dropdown)
        update_history(history,response)
        yield history, "-1WPS"
        return

    # Procesar el agente de colecciones
    if collection_agent_checkbox and collections_dropdown:
        response = generateResponse(expert_selected, history[-1][0], model_dropdown, collections_dropdown)
        update_history(history,response)
        yield history, "-1WPS"
        return

 
    # Llamar a un experto si ninguna de las otras condiciones se cumple
    yield from call_expert(expert_selected, history, model_dropdown, stream_checkbox)



def call_expert(expert_selected, history, model_dropdown, stream=False):
    modelName = getattr(getLlmData(expert_selected), model_dropdown).model
    start_time = time.perf_counter_ns()
    files = []
    if len(history) > 1 and is_path( history[-2][0][0]):
        files = [history[-2][0][0]]
        
    messages = createMessages(history)
    
    if stream:
        responses = llm_call(expert_selected=expert_selected, 
                             model_choice=model_dropdown, 
                             messages=messages, 
                             files=files, 
                             stream=True)
        token_counter = 0
        if responses:
            for chunk in responses:
                token_counter += 1
                if esOAI(modelName) or esGROQ(modelName) :
                    text = chunk.choices[0].delta.content
                    if text :
                        update_history(history,  text)
                else :
                    update_history(history, chunk['message']['content'])
                yield history, ""
                
                
            end_time = time.perf_counter_ns()
            tps = f'{int(token_counter / ((end_time - start_time) / 1e9))}TPS'
            yield history, tps
        else:
            gr.Error("Call failed")    
    else:
        response = llm_call(expert_selected=expert_selected,
                            model_choice=model_dropdown,
                            messages=messages,
                            files=files)
        update_history(history, response)
        end_time = time.perf_counter_ns()
        tps = f'{int(len(response.split()) / ((end_time - start_time) / 1e9))}WPS'
        yield history, tps

def update_history(history, content):
    if not history or len(history[-1]) < 2 or history[-1][1] is None:
        if len(history[-1]) < 2:
            history[-1].append("")  # Add an empty string if the second element is missing
        else:
            history[-1][1] = ""  # Initialize the second element with an empty string if it's None
    history[-1][1] += content    

def add_message(history, message, expert_selected, model):
    modelName = getattr(getLlmData(expert_selected), model).model
    for file in  message["files"] :
        history.append(((file,), None))
    
    if message["text"] is not None:
        history.append((message["text"], None))
        
    return history,  gr.MultimodalTextbox(interactive=True, file_types=["image"], placeholder="Enter message or upload file...", show_label=False),modelName


def resendLast(history, expert_selected, model):
    modelName = getattr(getLlmData(expert_selected), model).model
    if history:
        history[-1][1] = None
        
    return history,  gr.MultimodalTextbox(interactive=True, file_types=["image"], placeholder="Enter message or upload file...", show_label=False),modelName


    
def removeLast(history):
       history.pop()
       return history

def editLast(chatbot):
    if chatbot:
        # Obtenemos el último mensaje
        last_message = chatbot.pop()
        # Actualizamos el chat_input con el primer elemento del último par
        return [chatbot,{"text": last_message[0]}]
    else:
        # Si no hay mensajes, simplemente no hacemos nada o podríamos limpiar chat_input
        return [chatbot,{"text": ""}]

########################## Lista de conversaciones
conversation_list = []

def save_conversation(expert_selected,history,conversation_dropdown ):
    history_dump = json.dumps(history[0][0], indent=2)
    print(history_dump)
    conversation_name = conversation_dropdown
    if not conversation_name:
        conversation_name = llm_call(
            expert_selected=expert_selected,
            model_choice=ModelSize.SMALL_MODEL.value, 
            system_message= "You are created to write very short titles that describe a text with precision. The text must be shorter than than 6 words",
            messages= history_dump,
            override_system_message=True
        )
        gr.Info(f"Chat saved as: {conversation_name}")
    filename = f"{CHATS_DIR}/{conversation_name[:32]}.json"
    with open(filename, "w") as f:
        json.dump(history, f)

    conversation_list = get_conversation_list()
    return gr.Dropdown(choices=conversation_list, value=filename)

def delete_conversation(conversation_name):
    # Construye el nombre del archivo a partir del nombre de la conversación
    filename = f"{CHATS_DIR}/{conversation_name}.json"
    # Verifica si el archivo existe
    if os.path.exists(filename):
        # Elimina el archivo
        os.remove(filename)
        gr.Info(f"Chat '{conversation_name}' has been deleted")
    else:
        gr.Info(f"Chat not found: '{conversation_name}'.")
    conversation_list = get_conversation_list()
    return gr.Dropdown(choices=conversation_list, value=filename)


def get_conversation_list():
    return [f.replace(".json", "") for f in os.listdir(CHATS_DIR) if f.endswith(".json")]

def load_conversation(selection):
    filename = f"{CHATS_DIR}/{selection}.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            history = json.load(f)
            return gr.Chatbot(history)
