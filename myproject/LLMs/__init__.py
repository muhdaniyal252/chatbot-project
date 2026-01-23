from .gemini import GeminiLLM
from .gpt import GPTLLM
llms = {
    "gemini": GeminiLLM,
    "gpt": GPTLLM
}

def get_llm(name):
    llm = llms.get(name)
    return llm() # type: ignore