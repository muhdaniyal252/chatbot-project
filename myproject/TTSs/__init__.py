from .openai_tts import OpenAI_TTS

ttss = {
    "openai": OpenAI_TTS
}
def get_tts(name):
    tts = ttss.get(name)
    return tts() # type: ignore