import os
from openai import OpenAI
from .stt import ISTT
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class OpenAI_STT(ISTT):
    def __init__(self, api_key=None, model="gpt-4o-transcribe"):
        self.api_key = api_key or OPENAI_API_KEY
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    async def transcribe(self, audio_file) -> str:
        # audio_file is a BytesIO object
        transcription = self.client.audio.transcriptions.create(
            model=self.model,
            file=audio_file,
            language="en"
        )
        return transcription.text
