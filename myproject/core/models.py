
from django.db import models
from django.contrib.auth.models import User

class Agent(models.Model):
	name = models.CharField(max_length=100)
	prompt = models.TextField()
	user = models.ForeignKey(User, related_name='agents', on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.name


class Chat(models.Model):
	title = models.CharField(max_length=255)
	agent = models.ForeignKey(Agent, related_name='chats', on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='chats', on_delete=models.CASCADE)
    
	def __str__(self):
		return self.title


class Message(models.Model):
	chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)
	message_by = models.CharField(max_length=50, choices=[('user', 'User'), ('ai', 'AI')], default='user')

	def __str__(self):
		return f"Message by {self.user} in {self.chat} at {self.timestamp}"