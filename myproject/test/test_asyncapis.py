import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from asyncapis.main import app

client = TestClient(app)

import django
django.setup()
from core.models import Agent, Chat
from django.contrib.auth.models import User

from unittest.mock import patch, MagicMock

def test_send_message_websocket():
    # Create user, agent, and chat for the test
    user = User.objects.create_user(username='wsuser', password='wspass')
    agent = Agent.objects.create(name='wsagent', prompt='Prompt', user=user)
    chat = Chat.objects.create(title='wschat', agent=agent, user=user)
    # Patch LLM, TTS, STT dependencies in utils
    with patch('utils.llm') as mock_llm:
        mock_llm.invoke.return_value = MagicMock(content='AI response')
        with patch('utils.tts') as mock_tts:
            mock_tts.synthesize = MagicMock()
            with patch('utils.stt') as mock_stt:
                mock_stt.transcribe = MagicMock(return_value='transcribed text')
                with client.websocket_connect('/send-message') as websocket:
                    websocket.send_json({'message': 'Hello', 'chatid': chat.id, 'userid': user.id})
                    data = websocket.receive_json()
                    assert 'status' in data
                    assert data['status'] == 'success'

# Audio message test would require more setup/mocking
