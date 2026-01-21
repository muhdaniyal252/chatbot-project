
from langchain_core.prompts import PromptTemplate
from myproject.LLMs import get_llm
from myproject.core.models import User, Chat, Message, Agent

llm = get_llm("gemini")

template = """
Instructions:
{instructions}


summary of conversation so far: {summary}
last 10 messages: {messages}
user_details: {user_details}
current_user_input: {user_input}

Reply like you are continuing a conversation, not starting a new one.
and do not reply like bullet points or numbered list. you are an agent that talks like a human.
keep the conversation simple, natural, and engaging.

"""

prompt = PromptTemplate(
    input_variables=["instructions", "summary", "messages", "user_details", "user_input"],
    template=template,
)

def process_message(message, chatid, userid):
    user = User.objects.get(id=userid)
    chat = Chat.objects.get(id=chatid, user=user)
    messages = Message.objects.filter(chat=chat).order_by('-timestamp')[:10]
    message_texts = [msg.content for msg in messages]
    agent = chat.agent

    user_message = Message.objects.create(chat=chat, user=user, content=message)
    
