from langchain_text_splitters import RecursiveCharacterTextSplitter
import ollama
import chromadb
import gradio as gr
from ControllerLLM.llm_manager import llm_call
from ControllerSettings.settings_logic import getEmbeddingModel
from modulesFolders import CHROMA_DIR
from utils import getModelName

client = chromadb.PersistentClient(path=CHROMA_DIR)

def cargarTexto(files:str, collectionName:str):
    # Check if any files were uploaded
    texto = ""
    if not files:
        return "No file uploaded."
   
    for file in files:
        with open(file, "r") as f:
            texto += f.read()
    # Initialize the text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Each chunk will have up to 1000 words
        chunk_overlap=50,  # Chunks will overlap by 50 words
        length_function=len,  # Measure chunks by number of characters
        separators=['\n\n', '\n', ' ', ''],  # Split at paragraphs, new lines, and spaces
        is_separator_regex=False
    )
    chunks = text_splitter.split_text(texto)
    collection = client.create_collection(name=collectionName)
    for index, data in enumerate(chunks):
        response = ollama.embeddings(model=getModelName(getEmbeddingModel()), prompt=data)
        embedding = response["embedding"]
        collection.add(
            ids=[str(index)],
            embeddings=[embedding],
            documents=[data]
        )
    gr.Info("Collection loaded successfully.")   
    print(update_collections_list())
 
    return gr.Dropdown(choices=update_collections_list()),gr.Dropdown(choices=update_collections_list())
  
def getRespuestas(prompt:str, collectionName:str):
    collection = client.get_collection(name=collectionName)
    response = ollama.embeddings(
    prompt=prompt,
    model=getModelName(getEmbeddingModel())
    )
    results = collection.query(
        query_embeddings=[response["embedding"]],
        n_results=2
        )
    return results['documents'][0][0]

def generateResponse(expert_selected,prompt:str, model:str, collection:str):
    data = getRespuestas(prompt=prompt, collectionName=collection)
    response = llm_call(expert_selected,model,
        f"Using this data: {data}. Respond to this prompt: {prompt}"
        )
    return response


def update_collections_list():
    return [ item.name for item in client.list_collections()]

def delete_collection(collection_name):
    client.delete_collection(collection_name)
    gr.Info("Collection deleted successfully.")  
    print(update_collections_list())
    return gr.Dropdown(choices=update_collections_list()),gr.Dropdown(choices=update_collections_list())
 
