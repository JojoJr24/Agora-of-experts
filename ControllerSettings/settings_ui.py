import gradio as gr

from ControllerLLM.llm_manager import get_model_list
from ControllerSettings.settings_logic import getEmbeddingModel, getVisionModel, setEmbeddingModel, setVisionModel

def settings_tab():
    with gr.Blocks() as tab:
        with gr.Row():
            vision_model = gr.Dropdown(label="Vision Model", choices=get_model_list() , value=getVisionModel())  # Add your options here
            embedding_model = gr.Dropdown(label="Embedding Model **Note:** Changing the Embedding Model will break existing Collections.", choices=get_model_list(), value=getEmbeddingModel())  # Add your options here

        with gr.Row():
            reload_button = gr.Button("Restart AoE", min_width=1, variant="primary" ) 
            close_button = gr.Button("Close AoE", min_width=1, variant="secondary" ) 
      
        reload_button.click(None, js="location.reload()")
        close_button.click(fn=quit)
        vision_model.select(setVisionModel,[ vision_model])
        embedding_model.select(setEmbeddingModel,[embedding_model])

    return tab