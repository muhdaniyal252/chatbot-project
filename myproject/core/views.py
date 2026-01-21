
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Agent, Chat, Message

# API endpoint to list messages for a chat
@api_view(['GET'])
@csrf_exempt
def chat_messages(request, chat_id):
	user = request.user if request.user.is_authenticated else None
	if not user:
		return JsonResponse({'messages': []})
	try:
		chat = Chat.objects.get(id=chat_id, user=user)
	except Chat.DoesNotExist:
		return JsonResponse({'messages': []})
	messages = Message.objects.filter(chat=chat).select_related('user').order_by('timestamp')
	msg_list = [
		{'id': m.id, 'user': m.user.username, 'content': m.content, 'by': m.message_by, 'timestamp': m.timestamp.strftime('%Y-%m-%d %H:%M:%S')} # type: ignore
		for m in messages
	]
	return JsonResponse({'messages': msg_list})

# API endpoint to list chats for the logged-in user
@api_view(['GET'])
@csrf_exempt
def user_chats(request):
	user = request.user if request.user.is_authenticated else None
	if not user:
		return JsonResponse({'chats': []})
	chats = Chat.objects.filter(user=user).select_related('agent').values('id', 'title', 'agent__name')
	return JsonResponse({'chats': list(chats)})
# API endpoint to create a chat
@api_view(['POST'])
@csrf_exempt
def create_chat(request):
	user = request.user if request.user.is_authenticated else None
	if not user:
		return Response({'error': 'Authentication required.'}, status=401)
	agent_id = request.data.get('agent')
	title = request.data.get('title')
	if not agent_id or not title:
		return Response({'error': 'Agent and title required.'}, status=400)
	try:
		agent = Agent.objects.get(id=agent_id, user=user)
	except Agent.DoesNotExist:
		return Response({'error': 'Agent not found.'}, status=404)
	chat = Chat.objects.create(title=title, agent=agent, user=user)
	return Response({'id': chat.id, 'title': chat.title}, status=201) #type: ignore


# API endpoint to list agents for the logged-in user
@api_view(['GET'])
@csrf_exempt
def user_agents(request):
	user = request.user if request.user.is_authenticated else None
	if not user:
		return JsonResponse({'agents': []})
	agents = Agent.objects.filter(user=user).values('id', 'name')
	return JsonResponse({'agents': list(agents)})

def chat_home(request):
	return render(request, 'core/chat.html')



def login_page(request):
	return render(request, 'core/login.html')

def signup_page(request):
	return render(request, 'core/signup.html')

class SignupView(APIView):
	def post(self, request):
		username = request.data.get('username')
		password = request.data.get('password')
		if not username or not password:
			return Response({'error': 'Username and password required.'}, status=status.HTTP_400_BAD_REQUEST)
		if User.objects.filter(username=username).exists():
			return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
		user = User.objects.create_user(username=username, password=password)
		refresh = RefreshToken.for_user(user)
		return Response({
			'refresh': str(refresh),
			'access': str(refresh.access_token),
		}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
	def post(self, request):
		username = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			refresh = RefreshToken.for_user(user)
			return Response({
				'refresh': str(refresh),
				'access': str(refresh.access_token),
			})
		else:
			return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

# Create Agent page (GET) and handle creation (POST)
@method_decorator(csrf_exempt, name='dispatch')
class CreateAgentView(APIView):
	def get(self, request):
		return render(request, 'core/create_agent.html')

	def post(self, request):
		import json
		data = request.data if hasattr(request, 'data') else json.loads(request.body)
		name = data.get('name')
		prompt = data.get('prompt')
		user = request.user if request.user.is_authenticated else None
		if not user:
			return Response({'error': 'Authentication required.'}, status=401)
		if not name:
			return Response({'error': 'Name required.'}, status=400)
		agent = Agent.objects.create(name=name, prompt=prompt or '', user=user)
		return Response({'success': True, 'id': agent.id}, status=201) # type: ignore

@method_decorator(csrf_exempt, name='dispatch')
class UpdateAgentView(APIView):
	def get(self, request, agent_id):
		agent = get_object_or_404(Agent, id=agent_id)
		return render(request, 'core/update_agent.html', {'agent': agent})

	def post(self, request, agent_id):
		import json
		agent = get_object_or_404(Agent, id=agent_id)
		data = request.data if hasattr(request, 'data') else json.loads(request.body)
		name = data.get('name')
		prompt = data.get('prompt')
		if name:
			agent.name = name
		if prompt is not None:
			agent.prompt = prompt
		agent.save()
		return Response({'success': True, 'id': agent.id}, status=200) # type: ignore