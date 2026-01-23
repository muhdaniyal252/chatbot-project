import os
from openai import OpenAI
from .tts import ITTS
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class OpenAI_TTS(ITTS):
    def __init__(self, api_key=None, model="tts-1", voice="coral", instructions="Speak in a cheerful and positive tone."):
        self.api_key = api_key or OPENAI_API_KEY
        self.model = model
        self.voice = voice
        self.instructions = instructions
        self.client = OpenAI(api_key=self.api_key)

    async def synthesize(self, text: str, output_buffer) -> None:
        # output_buffer is a BytesIO object
        with self.client.audio.speech.with_streaming_response.create(
            model=self.model,
            voice=self.voice,
            input=text,
            instructions=self.instructions,
        ) as response:
            for chunk in response.iter_bytes():
                output_buffer.write(chunk)
