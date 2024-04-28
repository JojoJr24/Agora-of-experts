# archivo_configuracion.py
import gradio as gr


def settings_tab():
    with gr.Blocks() as tab:
        with gr.Row():
            reload_button = gr.Button("Restart AoE", min_width=1, variant="primary" ) 
            close_button = gr.Button("Close AoE", min_width=1, variant="secondary" ) 

        reload_button.click(None, js="location.reload()")
        close_button.click(fn=quit)

    return tab