from dotenv import load_dotenv
import openai, os

load_dotenv()


class GalaxyGPTModel():

    _WHO_IS_GPT = "Your role as a senior research geologist is to help geologists use NASA's Earth data for research, including rocks, plate tectonics, and landscapes. They turn to you for advanced research and disaster-related guidance."
    
    def __init__(self, apikey:str, model = "gpt-3.5-turbo") -> None:
        self.apikey = apikey
        self.model = model
        openai.api_key = self.apikey


    async def gpt_question(self, question):

        response = openai.ChatCompletion.create(
            model = self.model,
            messages = [
                {"role": "system", "content": self._WHO_IS_GPT},
                {"role": "user", "content": question},
            ],
            
            temperature=0,
        )

        return response['choices'][0]['message']


"""
inst = QwertyGPTModel(apikey=os.getenv("OPEN_AI_SECRET_KEY"))

print(inst.gpt_question(question="what is a schist and what are some properties of this rock type."))
"""
