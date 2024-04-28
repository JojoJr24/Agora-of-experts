import gradio as gr

from ControllerChat.chat_ui import getCollectionsDropDown
from ControllerLLM.llm_manager import ModelSize
from ControllerRAG.rag_logic import cargarTexto, delete_collection, generateResponse, update_collections_list
from langchain_text_splitters import RecursiveCharacterTextSplitter


def rag_tab():
    with gr.Blocks() as rag:
        with gr.Row():
            with gr.Column():
                collection_name = gr.Textbox(label="Collection Name", placeholder="Enter the name for the collection")
                file_upload = gr.File(label="Upload File", file_count="multiple")
                submit_button = gr.Button("Upload Text and Create Collection", variant="primary")
            with gr.Column():    
                collections_dropdown = gr.Dropdown(label="Available Collections", choices=update_collections_list())
                delete_button = gr.Button("Delete Collection", variant="secondary")
                

        submit_button.click(
            cargarTexto,
            inputs=[file_upload, collection_name],
            outputs=[collections_dropdown,getCollectionsDropDown()]
        )

        
        delete_button.click(
            delete_collection,
            inputs=[collections_dropdown],
            outputs=[collections_dropdown,getCollectionsDropDown()]
        )

    return rag

def reset_rag():
    global collections_dropdown
    collections_dropdown = gr.Dropdown(label="Available Collections", choices=update_collections_list())