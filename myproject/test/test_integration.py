import pytest
from django.contrib.auth.models import User
from core.models import Agent, Chat, Message
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_full_flow():
    client = APIClient()
    # Signup
    resp = client.post('/signup/', {'username': 'intuser', 'password': 'intpass'}, format='json')
    assert resp.status_code == 201 #type: ignore
    # Login
    resp = client.post('/login/', {'username': 'intuser', 'password': 'intpass'}, format='json')
    assert resp.status_code == 200 #type: ignore
    token = resp.data['access'] #type: ignore
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    # Create agent
    resp = client.post('/agents/create/', {'name': 'IntAgent', 'prompt': 'Prompt'}, format='json')
    assert resp.status_code == 201  #type: ignore
    agent_id = resp.data['id']  #type: ignore
    # Create chat
    resp = client.post('/api/chats/create/', {'agent': agent_id, 'title': 'IntChat'}, format='json')
    assert resp.status_code == 201  #type: ignore
    chat_id = resp.data['id']  #type: ignore
    # Send message
    Message.objects.create(chat_id=chat_id, user=User.objects.get(username='intuser'), content='Hello', message_by='user')
    resp = client.get(f'/api/chats/{chat_id}/messages/')
    assert resp.status_code == 200 #type: ignore
    assert 'messages' in resp.json()  #type: ignore
