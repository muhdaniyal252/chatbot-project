from fastapi import FastAPI, Request
from pydantic import BaseModel
from pathlib import Path
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from myproject.utils import process_message

app = FastAPI()

class SendMessageRequest(BaseModel):
    message: str
    chatid: int
    userid: int

@app.post("/send-message")
async def send_message(data: SendMessageRequest):
    # Call the processing function in core/utils.py
    result = process_message(data.message, data.chatid, data.userid)
    return {"status": "success", "result": result}
