from fastapi import FastAPI, WebSocket
from pathlib import Path
import sys
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
project_path = BASE_DIR / "myproject"
sys.path.append(str(project_path))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
import django
django.setup()

#the utils is in basedir/myproject/utils.py
from utils import process_message #type: ignore

app = FastAPI()

@app.websocket("/send-message")
async def websocket_send_message(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        message = data.get("message")
        chatid = data.get("chatid")
        userid = data.get("userid")
        result = await process_message(message, chatid, userid)
        await websocket.send_json({"status": "success", "result": result})
