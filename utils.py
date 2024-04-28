import random
import json

def createMessages(history , system_message = ''):
    messages = []
    if system_message:
         messages.insert(0, {"role": "system", "content": system_message})

    # Build the messages array from history
    for item in history:
        # User message
        if item[0]:  # Check if the user message is not None
            messages.append({
                'role': 'user',
                'content': item[0]
            })
        # Assistant message
        if len(item) > 1 and item[1]:  # Check if there is an assistant message and it's not None
            messages.append({
                'role': 'assistant',
                'content': item[1]
            })
    return messages


def coin_flip():
    return random.randint(0, 1)


def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except Exception as e:
        return {"error": str(e)}
    
def write_json_file(data, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            return {"success": True}
    except Exception as e:
        return {"error": str(e)}
    
    
