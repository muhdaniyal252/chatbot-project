import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from core.models import Agent, Chat

@pytest.mark.django_db
def test_signup_and_login():
    client = APIClient()
    signup_url = reverse('signup')
    login_url = reverse('login')
    resp = client.post(signup_url, {'username': 'newuser', 'password': 'newpass'}, format='json')
    assert resp.status_code == 201
    resp = client.post(login_url, {'username': 'newuser', 'password': 'newpass'}, format='json')
    assert resp.status_code == 200
    assert 'access' in resp.data

@pytest.mark.django_db
def test_create_agent_and_chat():
    client = APIClient()
    user = User.objects.create_user(username='apiuser', password='apipass')
    client.force_authenticate(user=user)
    agent_resp = client.post(reverse('create_agent'), {'name': 'AgentX', 'prompt': 'PromptX'}, format='json')
    assert agent_resp.status_code == 201
    agent_id = agent_resp.data['id']
    chat_resp = client.post(reverse('create_chat'), {'agent': agent_id, 'title': 'ChatX'}, format='json')
    assert chat_resp.status_code == 201
    chat_id = chat_resp.data['id']
    msg_resp = client.get(reverse('chat_messages', args=[chat_id]))
    assert msg_resp.status_code == 200
    assert 'messages' in msg_resp.json()
