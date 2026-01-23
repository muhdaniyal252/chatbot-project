from fastapi import FastAPI, WebSocket
from pathlib import Path
import sys
import os
from io import BytesIO

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
project_path = BASE_DIR / "myproject"
sys.path.append(str(project_path))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
import django
django.setup()

#the utils is in basedir/myproject/utils.py
from utils import process_message, process_audio_message #type: ignore

app = FastAPI()

@app.websocket("/send-message")
async def websocket_send_message(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()
            message = data.get("message")
            chatid = data.get("chatid")
            userid = data.get("userid")
            result = await process_message(message, chatid, userid)
            await websocket.send_json({"status": "success", "result": result})
        except Exception as e:
            await websocket.send_json({"status": "error", "error": str(e)})

@app.websocket("/send-audio-message")
async def websocket_send_audio_message(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Expect binary audio data and metadata as JSON
        meta = await websocket.receive_json()
        chatid = meta.get("chatid")
        userid = meta.get("userid")
        # Receive audio as bytes
        audio_bytes = await websocket.receive_bytes()
        audio_buffer = BytesIO(audio_bytes)
        audio_buffer.seek(0)
        # Call process_audio_message with BytesIO
        transcribed_text, llm_response, synthesized_audio = await process_audio_message(audio_buffer, chatid, userid)
        # Send results (text fields as JSON, audio as bytes)
        await websocket.send_json({
            "status": "success",
            "transcription": transcribed_text,
            "llm_response": llm_response
        })
        await websocket.send_bytes(synthesized_audio.read())
