from openai import OpenAI
from datetime import datetime

# -------------------------------------------------------------------------------------------------

class Model:

    def __init__(self, api_key : str, base_url : str):
        try:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        except Exception as e:
            print(f"Failed to initialize LLM client: {e}")

    def list_available_models(self):
        models = self.client.models.list()
        return [model.id for model in models.data]
    
    def add_user_message(self, messages : list, message : str):
        messages.append({
            "role": "user", 
            "content": message
        })

    def generate_response(self, messages : list, model_name : str) -> tuple[str, int]|None:
        # Get current time
        current_time = datetime.now()
        response = None
        try:
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
            )
            # Get response duration in rounded seconds
            response_duration = round((datetime.now() - current_time).total_seconds())
        except Exception as e:
            print(f"ERROR: Failed to generate response from model: {e}")
            return None
        if response is None:
            print("ERROR: No response from model...")
        else:
            return response.choices[0].message.content, response_duration

    def add_response(self, messages : list, response : str):
        messages.append({
            "role": "assistant", 
            "content": response
        })

# -------------------------------------------------------------------------------------------------