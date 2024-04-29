from ControllerLLM.llm_manager import llm_call
from utils import createMessages


def basic_reflection(expert_selected,history, model_dropdown):
    
    first_system_message = f"Let's think step by step about how we would accomplish the user task."
    plan_prompt_response = llm_call(expert_selected,model_dropdown,messages=createMessages(history,first_system_message) , system_message= first_system_message)
    print(plan_prompt_response)

    second_system_prompt = f"Given this user prompt: \n{history}, a less capable AI model answer: \n{plan_prompt_response}. \n\nImprove the response"
    execute_prompt_response = llm_call(expert_selected,model_dropdown,messages=createMessages(history,second_system_prompt) , system_message= second_system_prompt)
        
    print("--------------------------")
    print(execute_prompt_response)
    return execute_prompt_response

    
