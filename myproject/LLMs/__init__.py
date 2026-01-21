from gemini import GeminiLLM

llms = {
    "gemini": GeminiLLM,
}

def get_llm(name):
    llm = llms.get(name)
    return llms() # type: ignore