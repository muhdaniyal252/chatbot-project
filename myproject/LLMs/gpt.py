import os
from .llm import ILLM
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class GPTLLM(ILLM):
    def __init__(self, api_key=None, model="gpt-3.5-turbo"):
        self.llm = ChatOpenAI(
            model=model,
            temperature=0,
            timeout=None,
            max_retries=2,
            api_key=api_key or OPENAI_API_KEY #type: ignore
        )

    def bind_tools(self, tools):
        return self.llm.bind_tools(tools)

    def invoke(self, messages):
        return self.llm.invoke(messages)
