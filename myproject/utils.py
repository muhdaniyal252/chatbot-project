
from langchain_core.prompts import PromptTemplate
from LLMs import get_llm

from core.models import User, Chat, Message, Agent
from asgiref.sync import sync_to_async

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

async def process_message(message, chatid, userid):
    user = await sync_to_async(User.objects.get)(id=userid)
    chat = await sync_to_async(Chat.objects.get)(id=chatid, user=user)
    messages = await sync_to_async(lambda: list(Message.objects.filter(chat=chat).order_by('-timestamp')[:10]))()
    message_texts = [msg.content for msg in messages]
    agent = await sync_to_async(lambda: chat.agent)()

    user_message = await sync_to_async(Message.objects.create)(chat=chat, user=user, content=message)
    return user_message.id #type: ignore
