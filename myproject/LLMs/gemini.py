import os
from .llm import ILLM
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class GeminiLLM(ILLM):
    
    def __init__(self, api_key=None):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=api_key or GEMINI_API_KEY
        )
    
    def bind_tools(self, tools):
        return self.llm.bind_tools(tools)
    
    def invoke(self, messages):
        return self.llm.invoke(messages)