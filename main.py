from pathlib import Path
import gradio as gr
import webview

# Crea el componente Chatbot
from ControllerChat.chat_ui import chat_tab
from ControllerRAG.rag_ui import rag_tab
from ControllerExperts.experts_ui import experts_tab
from ControllerSettings.settings_ui import settings_tab
from theme import AoeTheme

# Read CSS and JS files
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Base path for files
base_path = Path(__file__).resolve().parent

# Load CSS and JavaScript
css = read_file(base_path / 'CSS/css/main.css')

html_header = """
<div class='header'>
    <img src='icon.png' class='header-image'>
    <h1 class='header-text'>Agora of experts</h1>
</div>
"""
aoeTheme = AoeTheme()
with gr.Blocks(css=css, analytics_enabled=False, fill_height=True, theme=aoeTheme) as demo:
   gr.Markdown("""# Agora of Experts""",elem_classes='header')
   with gr.Tabs(elem_classes="extension-tab") as tabs:
      with gr.Tab("Chat", elem_classes="extension-tab") as chat :
         chat_tab()
      with gr.Tab("Experts", elem_classes="extension-tab"):
         experts_tab()
      with gr.Tab("RAG", elem_classes="extension-tab"):
         rag_tab()
      with gr.Tab("Settings", elem_classes="extension-tab"):
         settings_tab()

_, url, _ = demo.launch(inline=True, inbrowser=False, prevent_thread_lock=True, quiet=True)
print(url)

def set_zoom(window):
    window.evaluate_js(f"document.body.style.zoom='{80}%'")

window = webview.create_window("AoE", url)
webview.start(set_zoom, window)