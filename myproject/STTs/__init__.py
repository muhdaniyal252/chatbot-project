from .openai_stt import OpenAI_STT

stts = {
    "openai": OpenAI_STT
}
def get_stt(name):
    stt = stts.get(name)
    return stt() # type: ignore