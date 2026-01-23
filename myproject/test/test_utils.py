import pytest
from unittest.mock import patch, MagicMock
from core.models import User, Chat, Agent, Message
from utils import get_response, process_message, process_audio_message
import asyncio

@pytest.mark.django_db
def test_get_response():
    import utils
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MagicMock(content='AI response')
    result = utils.get_response('instructions', 'input', ['msg1', 'msg2'], 'summary', llm_instance=mock_llm)
    assert isinstance(result, str)
    assert not result.lower().startswith('error')

@pytest.mark.django_db
def test_process_message():
    user = User.objects.create_user(username='u1', password='p1')
    agent = Agent.objects.create(name='A1', prompt='Prompt', user=user)
    chat = Chat.objects.create(title='C1', agent=agent, user=user)
    with patch('utils.get_response', return_value='AI reply'):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(process_message('Hello', chat.id, user.id)) #type: ignore
        assert result == 'AI reply'
        assert Message.objects.filter(chat=chat).count() >= 2
