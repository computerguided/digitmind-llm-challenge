# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from openai import OpenAI
from datetime import datetime

# -----------------------------------------------------------------------------
# Response class
# -----------------------------------------------------------------------------
class Response:
    def __init__(self, content : str, 
                 reasoning_time : int, 
                 input_tokens : int, 
                 reasoning_tokens : int, 
                 output_tokens : int):
        self.content = content
        self.reasoning_time = reasoning_time
        self.input_tokens = input_tokens
        self.reasoning_tokens = reasoning_tokens
        self.output_tokens = output_tokens

# -----------------------------------------------------------------------------
# Model class
# -----------------------------------------------------------------------------
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

    def generate_response(self, messages : list, model_name : str) -> Response|None:
        # Get current time
        current_time = datetime.now()
        try:
            completion = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
            )
            # Get response duration in rounded seconds
            response_duration = round((datetime.now() - current_time).total_seconds())

            input_tokens = completion.usage.prompt_tokens
            completion_tokens = completion.usage.completion_tokens

            # Check if 'completion_tokens_details' and 'reasoning_tokens' attributes exist
            if hasattr(completion.usage, 'completion_tokens_details') and \
                hasattr(completion.usage.completion_tokens_details, 'reasoning_tokens'):
                reasoning_tokens = completion.usage.completion_tokens_details.reasoning_tokens
            else:
                reasoning_tokens = 0  # Default to 0 if attribute does not exist

        except Exception as e:
            print(f"ERROR: Failed to generate response from model: {e}")
            return None

        return Response(content=completion.choices[0].message.content,
                        reasoning_time=response_duration,
                        input_tokens=input_tokens,
                        reasoning_tokens=reasoning_tokens,
                        output_tokens=completion_tokens-reasoning_tokens)

    def add_response(self, messages : list, response : str):
        messages.append(
        {
            "role": "assistant", 
            "content": response
        })

# -------------------------------------------------------------------------------------------------