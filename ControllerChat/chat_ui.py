# archivo_chat.py
import gradio as gr
# Crea el componente Chatbot
from ControllerChat.chat_logic import add_message, delete_conversation, editLast, get_conversation_list, load_conversation, print_like_dislike, removeLast, resendLast, save_conversation, send_to_bot
from ControllerLLM.llm_manager import MODEL_SIZE_ITEMS
from ControllerChains.modulos_logic import  NOMBRES_MODULOS
from ControllerRAG.rag_logic import update_collections_list
from ControllerExperts.experts_logic import  DEFAULT_EXPERT, getAllExperts, loadLLMData
from ControllerTools.tools_logic import NOMBRES_TOOLS

chatbot = gr.Chatbot(
    elem_id="chatbot",
    bubble_full_width=True,
    render_markdown=True,
    show_copy_button=True,
    show_label=True,
    elem_classes="extension-chatbot"
    )

chat_input = gr.MultimodalTextbox(interactive=True, file_types=["image"], placeholder="Enter message or upload file...", show_label=False)
experts_dropdown = gr.Dropdown(value=DEFAULT_EXPERT, choices=getAllExperts(), label="Select Expert")
collections_dropdown = gr.Dropdown(label="Collection", choices=update_collections_list(), interactive=True)

def getExpertDropdown():
    return experts_dropdown
def getCollectionsDropDown():
    return collections_dropdown

def chat_tab():
    with gr.Blocks() as tab: 
        with gr.Row(elem_classes="extension-tab"):
            with gr.Column(scale=1):
                with gr.Row():
                    experts_dropdown.render()
                    experts_dropdown.select(loadLLMData, inputs=[experts_dropdown ] , outputs=None)
                   
                conversation_dropdown = gr.Dropdown(choices=get_conversation_list(), label="Chats", interactive=True)
                conversation_dropdown.select(load_conversation, conversation_dropdown, chatbot)
                with gr.Row():
                    save_button = gr.Button("Save Chat", size="sm",scale=1, min_width=1) 
                    delete_button = gr.Button("Delete Chat",size="sm",scale=1, min_width=1)
                    # Acciones para los botones y selección de conversaciones
                save_button.click(save_conversation, [experts_dropdown, chatbot, conversation_dropdown ] , conversation_dropdown)
                delete_button.click(delete_conversation, [conversation_dropdown ] , conversation_dropdown)

                with gr.Row():
                    with gr.Column():
                        with gr.Row():
                            model_dropdown = gr.Dropdown(value=MODEL_SIZE_ITEMS[0], choices=MODEL_SIZE_ITEMS, label="Model")
                            stream_checkbox = gr.Checkbox(value=True,label="Stream")
                            model_name = gr.Textbox(value="", label="Last model called", interactive=False , max_lines= 1 , )
                            tps_text = gr.Textbox(value="", label="Inference speed", interactive=False , max_lines= 1)
                
                modulo_dropdown = gr.Dropdown( choices=NOMBRES_MODULOS, label="Reflection", interactive=True )
                use_agent_checkbox = gr.Checkbox(value=False,label="Use reflection")
                
                collections_dropdown.render()
                collection_agent_checkbox = gr.Checkbox(value=False,label="Load Collection")
                
                tools_dropdown = gr.Dropdown(label="Tools", choices=NOMBRES_TOOLS, interactive=True, multiselect=True)
                tools_agent_checkbox = gr.Checkbox(value=False,label="Use Tool")

            with gr.Column(scale=8):
                chatbot.render()
                with gr.Row():
                # Define un área de entrada multimodal para mensajes de usuario
                    with gr.Column(scale=9):
                        chat_input.render()
                    with gr.Column(scale=1):
                        with gr.Row():
                            with gr.Row():
                                clear = gr.ClearButton([chat_input, chatbot,conversation_dropdown],scale=1, variant='primary')
                                resend_last_button = gr.Button("Re-send",scale=1, min_width=1)
                                resend_click = resend_last_button.click(resendLast,[chatbot,experts_dropdown, model_dropdown],[chatbot, chat_input, model_name])
                                resend_click_then = resend_click.then(send_to_bot, [chatbot, 
                                                                      experts_dropdown,
                                                                      tps_text,
                                                                      use_agent_checkbox, 
                                                                      modulo_dropdown,
                                                                      stream_checkbox,
                                                                      model_dropdown,
                                                                      tools_agent_checkbox,
                                                                      tools_dropdown,
                                                                      collection_agent_checkbox,
                                                                      collections_dropdown] , [chatbot , tps_text], api_name="bot_response", show_progress=True)
                                resend_click_then.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])
                            with gr.Row():
                                back_last_button = gr.Button("Back",scale=1, min_width=1)
                                back_last_button.click(removeLast, chatbot , chatbot)
                                edit_button = gr.Button("Edit",scale=1, min_width=1)
                                edit_button.click(editLast, chatbot , [chatbot, chat_input])

                # Procesa los mensajes de usuario y actualiza el chatbot
                chat_msg = chat_input.submit(add_message, [chatbot, chat_input ,experts_dropdown, model_dropdown], [chatbot, chat_input, model_name])
                # Inicia la respuesta del bot tras recibir un mensaje
                bot_msg = chat_msg.then(send_to_bot, [chatbot, 
                                                    experts_dropdown,
                                                    tps_text,
                                                    use_agent_checkbox, 
                                                    modulo_dropdown,
                                                    stream_checkbox,
                                                    model_dropdown,
                                                    tools_agent_checkbox,
                                                    tools_dropdown,
                                                    collection_agent_checkbox,
                                                    collections_dropdown] , [chatbot , tps_text], api_name="bot_response", show_progress=True)
                # Restablece el área de entrada multimodal tras la respuesta del bot
                bot_msg.then(lambda: None, None, [chat_input])
                # Permite a los usuarios dar 'me gusta' o 'no me gusta' a los mensajes
                chatbot.like(print_like_dislike, None, None)
    return tab