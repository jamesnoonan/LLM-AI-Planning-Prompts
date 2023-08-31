import openai
import bardapi
import os
from dotenv import load_dotenv

load_dotenv()

class LLM:
    has_tokens = False

    def __init__(self):
        print("You should not be using this")
        
class OpenAILLM:
    last_raw_response = None

    def __init__(self):
        openai.organization = os.getenv("OPENAI_ORG")
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.has_tokens = True

    def get_response(self, prompt):
        self.last_raw_response = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613", messages=[{"role":"user", "content": prompt}])
        return self.last_raw_response['choices'][0]['message']['content']
    
    def get_tokens(self):
        ## NOTE: get_reponse has to be called before this
        return self.last_raw_response['usage']['total_tokens']


class BardLLM:
    bard = None

    def __init__(self):
        self.has_tokens = False
        self.bard = bardapi.Bard(token = os.getenv("BARD_API_KEY"))

    def get_response(self, prompt):
        return self.bard.get_answer(prompt)['content']