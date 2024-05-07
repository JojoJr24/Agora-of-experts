
![Icono del proyecto](icon.png)
# Agora of Experts (AoE)

## Introduction
Agora of Experts is an innovative chatbot platform that redefines the boundaries of automated conversations. Unlike traditional chatbots that operate within strict parameters, AoE offers a liberating experience where interactions are not confined to a single model or a rigid script. Users have the unique ability to direct questions to different AI models within the same conversation (Experts), enabling a dynamic and multi-faceted dialogue like in an Agora.

The platform's standout feature is its flexibility; users can activate and deactivate various tools, RAG Collections or reflection algorithms for each question, enhancing the chatbot's responses based on the conversation's context or the user’s specific needs without the need to restart the conversation. This enhances interactions and provides tailored responses, making each conversation with AoE a distinct and adaptable experience.

AoE is designed for users seeking a more engaging, personalized, and versatile chatbot experience, perfect for both casual queries and complex discussions.

## Setup Instructions
To set up this project on your local machine, follow these steps:

### Clone the Repository
First, clone the repository to your local machine:
```
git clone https://github.com/JojoJr24/Agora-of-experts.git
cd Agora_of_experts
```
### Requirements
#### Windows
Python 3 https://www.python.org/downloads/release/python-3123/

Ollama https://ollama.com/

#### Mac Os
Ollama https://ollama.com/

#### Linux
You are fine, everything will be installed by the script

### Install and/or Run the Application
#### Windows
```
Agora_Windows.bat
```
#### Linux
```
chmod Agora_linux.sh ugo +x
Agora_linux.sh
```
#### Windows
```
chmod Agora_MacOs.sh ugo +x
Agora_MacOs.sh
```

## Usage
After starting the application, a web interface will be available. You can interact with the chatbot by entering text messages or uploading files. Use the tabs to switch between different functionalities:

- **Chat:** Interact with the chatbot.
- **Experts:** Manage experts for different model configurations.
- **RAG:** Load your documents in collections. If you want ask to the documents, just load the collection you want in the chat

### Chat Features
- **Experts:** Each expert can have 3 model with different configurations and a system message. It`s like a GPTs but more flexible.
- **Chats:** Your previous chats. AoE chat have no autosave. Just save the chats that you want
- **Model:** Set the model that you want for your expert
- **Reflection:** If you need a better response, try a reflection algoritm
- **Collections:** Load o collection of documents loaded in the RAG tab
- **Tools:** If you need mor power, look for a tool


## GROQ and OpenAI Models

To use Groq or oai model you must set the keys as environmental variables
```
export OPENAI_API_KEY="sk-"

export GROQ_API_KEY="gsk_"
```

## Tavily search
If you don`t like duckduckgo search (the search web default tool) you can use Tavily adding the key to environmental variables

```
export TAVILY_API_KEY="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"
```
