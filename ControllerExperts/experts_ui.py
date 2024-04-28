# archivo_configuracion.py
import gradio as gr

# Crea el componente Chatbot
from ControllerChat.chat_ui import getExpertDropdown
from ControllerLLM.llm_manager import  get_model_list
from ControllerExperts.experts_logic import  DEFAULT_EXPERT, delete_expert, getAllExperts, getLlmData, load_experts, update_expert

def model_config_ui(model_config, model_name):
    with gr.Row():
        gr.Markdown(f"### {model_name}")
    with gr.Row() :
        model_list = get_model_list()  
        if(len(model_list) == 0):
            print("There is no model or ollama is not running")
            exit(0)
        model_name = model_config.model  
        try:
            model_index = model_list.index(model_name)
        except ValueError:
            model_index = 0
        with gr.Column():
            with gr.Row():
                model = gr.Dropdown(label="Model", value=model_list[model_index],choices=model_list, allow_custom_value=True)
                fp = gr.Number(label="Frequency Penalty", value=model_config.frequency_penalty)
                mt = gr.Number(label="Max Tokens", value=model_config.max_tokens)
                n = gr.Number(label="N", value=model_config.n)
                pp = gr.Number(label="Presence Penalty", value=model_config.presence_penalty)
            with gr.Row():
                seed = gr.Number(label="Seed", value=model_config.seed)
                stream = gr.Checkbox(label="Stream", value=model_config.stream)
                temp = gr.Number(label="Temperature", value=model_config.temperature)
                tl = gr.Number(label="Top Logprobs", value=model_config.top_logprobs)
                tp = gr.Number(label="Top P", value=model_config.top_p)
    return [model,fp,mt,n,pp,seed,stream,temp,tl,tp]


def experts_tab():
    with gr.Blocks() as tab:
        with gr.Row():
                with gr.Column():
                    name_dropdown = gr.Dropdown(value=DEFAULT_EXPERT, choices=getAllExperts(), label="Select Expert or create a new one",allow_custom_value=True)

        llm_data = getLlmData(name_dropdown.value,True) 
        with gr.Row():
            system_message_input = gr.Textbox(label="System Message", value=llm_data.system_message, lines= 20)
        with gr.Tab("Small Model"):
            small_model_fields = model_config_ui(llm_data.small_model, "Small Model")
        with gr.Tab("Medium Model"):
            medium_model_fields = model_config_ui(llm_data.medium_model, "Medium Model")
        with gr.Tab("Big Model"):
            big_model_fields = model_config_ui(llm_data.big_model, "Big Model")
        
        save_button = gr.Button("Save Expert",variant="primary")
        delete_button = gr.Button("Delete Expert",variant="secondary")

        save_button.click(update_expert, [name_dropdown,system_message_input, *small_model_fields, *medium_model_fields, *big_model_fields], [name_dropdown,getExpertDropdown()])
        delete_button.click(delete_expert, [name_dropdown], [name_dropdown,getExpertDropdown()])
        name_dropdown.select(load_experts,inputs=[name_dropdown], outputs=[system_message_input, *small_model_fields, *medium_model_fields, *big_model_fields])                   
    return tab