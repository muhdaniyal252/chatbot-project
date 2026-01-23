import pytest
from django.contrib.auth.models import User
from core.models import Agent, Chat, Message

@pytest.mark.django_db
def test_agent_creation():
    user = User.objects.create_user(username='testuser', password='testpass')
    agent = Agent.objects.create(name='TestAgent', prompt='Test prompt', user=user)
    assert agent.name == 'TestAgent'
    assert agent.user == user

@pytest.mark.django_db
def test_chat_creation():
    user = User.objects.create_user(username='testuser2', password='testpass')
    agent = Agent.objects.create(name='TestAgent2', prompt='Prompt', user=user)
    chat = Chat.objects.create(title='TestChat', agent=agent, user=user)
    assert chat.title == 'TestChat'
    assert chat.agent == agent
    assert chat.user == user

@pytest.mark.django_db
def test_message_creation():
    user = User.objects.create_user(username='testuser3', password='testpass')
    agent = Agent.objects.create(name='TestAgent3', prompt='Prompt', user=user)
    chat = Chat.objects.create(title='TestChat2', agent=agent, user=user)
    message = Message.objects.create(chat=chat, user=user, content='Hello', message_by='user')
    assert message.content == 'Hello'
    assert message.chat == chat
    assert message.user == user
    assert message.message_by == 'user'
