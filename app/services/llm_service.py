import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
class LLMService:
    def __init__(self, api_key):
        genai.configure(api_key=os.getenv(api_key))
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def ask(self, question):
        response = self.model.generate_content(question)
        return response.text

