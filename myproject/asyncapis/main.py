from fastapi import FastAPI, WebSocket
from pathlib import Path
import sys
from starlette.websockets import WebSocketDisconnect
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
    try:
        while True:
            data = await websocket.receive_json()

            message = data.get("message")
            chatid = data.get("chatid")
            userid = data.get("userid")

            result = await process_message(message, chatid, userid)

            await websocket.send_json({
                "status": "success",
                "result": result
            })

    except WebSocketDisconnect:
        # Browser closed / client disconnected → normal behavior
        print("WebSocket /send-message disconnected")

    except Exception as e:
        # Only real application errors land here
        print(f"WebSocket error (/send-message): {e}")
        try:
            await websocket.send_json({
                "status": "error",
                "error": str(e)
            })
        except Exception:
            pass  # Socket already closed

    finally:
        print("WebSocket /send-message connection closed")

@app.websocket("/send-audio-message")
async def websocket_send_audio_message(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive metadata
            meta = await websocket.receive_json()
            chatid = meta.get("chatid")
            userid = meta.get("userid")

            # Receive audio bytes
            audio_bytes = await websocket.receive_bytes()
            audio_buffer = BytesIO(audio_bytes)
            audio_buffer.seek(0)

            transcribed_text, llm_response, synthesized_audio = (
                await process_audio_message(audio_buffer, chatid, userid)
            )

            await websocket.send_json({
                "status": "success",
                "transcription": transcribed_text,
                "llm_response": llm_response
            })

            await websocket.send_bytes(synthesized_audio.read())

    except WebSocketDisconnect:
        # Normal browser close
        print("WebSocket /send-audio-message disconnected")

    except Exception as e:
        print(f"WebSocket error (/send-audio-message): {e}")
        try:
            await websocket.send_json({
                "status": "error",
                "error": str(e)
            })
        except Exception:
            pass

    finally:
        print("WebSocket /send-audio-message connection closed")