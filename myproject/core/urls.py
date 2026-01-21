
from django.urls import path
from .views import SignupView, LoginView, login_page, signup_page, chat_home, CreateAgentView, user_agents, UpdateAgentView
from .views import create_chat, user_chats, chat_messages

urlpatterns = [
    path('', chat_home, name='chat_home'),
    path('agents/create/', CreateAgentView.as_view(), name='create_agent'),
    path('agents/update/<int:agent_id>/', UpdateAgentView.as_view(), name='update_agent'),
    path('api/agents/', user_agents, name='user_agents'),
    path('api/chats/', user_chats, name='user_chats'),
    path('api/chats/create/', create_chat, name='create_chat'),
    path('api/chats/<int:chat_id>/messages/', chat_messages, name='chat_messages'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup-page/', signup_page, name='signup_page'),
    path('login-page/', login_page, name='login_page'),
]
