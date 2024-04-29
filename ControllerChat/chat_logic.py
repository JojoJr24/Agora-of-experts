import json
import os
from ControllerChains.modulos_logic import MODULOS
from ControllerExperts.experts_logic import LLM_DATA, getAllExperts, getLlmData
from ControllerLLM.llm_manager import CHATS_DIR, ModelSize , promptStream , zero_shot
from ControllerRAG.rag_logic import generateResponse
from ControllerTools.tools_logic import TOOLS, tool_bot
from utils import createMessages
import gradio as gr
import time

def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)

def add_message(history, message, expert_selected, model):
    modelName = getattr(getLlmData(expert_selected), model).model
    for x in message["files"]:
        history.append(((x,), None))
    if message["text"] is not None:
        history.append((message["text"], None))
    return history, gr.MultimodalTextbox(value=None, interactive=False), modelName

def sendToBot(history,
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

    #modelo getLlmData().
    if use_agent_checkbox and modulo_dropdown in MODULOS:
        response = MODULOS[modulo_dropdown](expert_selected,history, model_dropdown)
        if not history or len(history[-1]) < 2 or history[-1][1] is None:
            if len(history[-1]) < 2:
                history[-1].append("")  # Add an empty string if the second element is missing
            else:
                history[-1][1] = ""  # Initialize the second element with an empty string if it's None
        history[-1][1] += response 
        yield history , "-1WPS"
        return
    
    if tools_agent_checkbox and len(tools_dropdown) > 0:
        response = tool_bot(expert_selected,history,tools_dropdown,model_dropdown)
        if not history or len(history[-1]) < 2 or history[-1][1] is None:
            if len(history[-1]) < 2:
                history[-1].append("")  # Add an empty string if the second element is missing
            else:
                history[-1][1] = ""  # Initialize the second element with an empty string if it's None
        history[-1][1] += response
        yield history , "-1WPS"
        return

    if collection_agent_checkbox and collections_dropdown != '' :
        response = generateResponse(expert_selected,history[-1][0],model_dropdown,collections_dropdown)
        if not history or len(history[-1]) < 2 or history[-1][1] is None:
            if len(history[-1]) < 2:
                history[-1].append("")  # Add an empty string if the second element is missing
            else:
                history[-1][1] = ""  # Initialize the second element with an empty string if it's None
        history[-1][1] += response 
        yield history, "-1WPS"
        return
    #Si no es una ejecución especial entonces es normal
    if stream_checkbox:
        yield from botStream(expert_selected,history, model_dropdown)
    else:
        yield from bot(expert_selected,history, model_dropdown)
    

def bot(expert_selected,history, model_dropdown):
    start_time = time.perf_counter_ns()
    messages = []
    messages = createMessages(history)
    response = zero_shot(expert_selected,model_dropdown,messages)
    # Check if the last item in history has less than 2 elements, or the second element is None
    if not history or len(history[-1]) < 2 or history[-1][1] is None:
        if len(history[-1]) < 2:
            history[-1].append("")  # Add an empty string if the second element is missing
        else:
            history[-1][1] = ""  # Initialize the second element with an empty string if it's None

    # Append the new assistant response to the last item in history
    history[-1][1] += response
    end_time = time.perf_counter_ns()
    tps = ''+ str(int(len(response.split()) / ((end_time - start_time)/ 1e9))) + 'WPS'
    yield history ,tps

def botStream(expert_selected,history, model_dropdown):
    messages = []
    messages = createMessages(history)
    responses = promptStream(expert_selected,model_dropdown,messages)
    start_time = time.perf_counter_ns() 
    token_counter = 0
    
    for chunk in responses:
        token_counter += 1
        # Check if the last item in history has less than 2 elements, or the second element is None
        if not history or len(history[-1]) < 2 or history[-1][1] is None:
            if len(history[-1]) < 2:
                history[-1].append("")  # Add an empty string if the second element is missing
            else:
                history[-1][1] = ""  # Initialize the second element with an empty string if it's None
        history[-1][1] += chunk['message']['content']
        yield history ,"" 

    end_time = time.perf_counter_ns()
    tps = ''+ str(int(token_counter / ((end_time - start_time)/ 1e9))) + 'TPS'
    yield history ,tps

def resendLast(history,
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
    if history:
        history[-1][1] = None
        yield from sendToBot(history,
                        expert_selected,
                        tps_text,
                        use_agent_checkbox,
                        modulo_dropdown,
                        stream_checkbox,
                        model_dropdown,
                        tools_agent_checkbox,
                        tools_dropdown,
                        collection_agent_checkbox,
                        collections_dropdown)
    
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
    history_dump = json.dumps(history, indent=2)
    conversation_name = conversation_dropdown
    if not conversation_name:
        conversation_name = zero_shot(
            expert_selected=expert_selected,
            model_choice=ModelSize.SMALL_MODEL.value,  
            messages=[{"role":"system", "content":"You are a AI that create very short titles for chats in a chatbot. The user will give you chats histories and you must create a title in no more than 6 words"}, {"role": "user", "content": history_dump}]
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
