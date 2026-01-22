
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from LLMs import get_llm
import asyncio

from core.models import User, Chat, Message, Agent
from asgiref.sync import sync_to_async

llm = get_llm("gemini")

template = """
You are an agent who acts as the instructions porvided below.

Instructions:
{instructions}


summary of conversation so far: {summary}
last 10 messages: {messages}
current_user_input: {user_input}

Reply like you are continuing a conversation, not starting a new one.
and do not reply like bullet points or numbered list. you are an agent that talks like a human.
keep the conversation simple, natural, and engaging.

"""

prompt_template = PromptTemplate(
    input_variables=["instructions", "summary", "messages", "user_input"],
    template=template,
)

chain: Runnable = prompt_template | llm.invoke

def get_response(instructions, user_input, messages, summary):

    inputs = {
        "instructions": instructions,
        "summary": summary,
        "messages": messages,
        "user_input": user_input,
    }
    response = chain.invoke(inputs)
    
    return response.content


async def process_message(message, chatid, userid):
    user = await sync_to_async(User.objects.get)(id=userid)
    chat = await sync_to_async(Chat.objects.get)(id=chatid, user=user)
    messages = await sync_to_async(lambda: list(Message.objects.filter(chat=chat).order_by('-timestamp')[:10]))()
    message_texts = [msg.content for msg in messages]
    agent = await sync_to_async(lambda: chat.agent)()
    user_message = await sync_to_async(Message.objects.create)(chat=chat, user=user, content=message)

    # Call get_response to get LLM reply
    instructions = agent.prompt

    summary = ""  # Use empty string for now
    llm_response = get_response(instructions, message, message_texts, summary)

    # Save LLM response as a new message in the database
    llm_message = await sync_to_async(Message.objects.create)(chat=chat, user=user, content=llm_response, message_by='ai')

    # Function to be executed in parallel (async summary update)
    asyncio.create_task(update_summary(chat, message_texts, summary))

    return llm_response

# Async background summary update
async def update_summary(chat, messages, summary):
    # Call LLM to generate summary (replace with your summary prompt)
    summary_prompt = f"""
    There is a conversation between a user and an agent. 
    And this is the Chat summary so far:
    Summary: {summary}
    you wil be provided with few of the latest messages and user input.
    You are now required to update the chat summary with the latest information.
    
    Last 10 messages:
    {messages}
    """
    updated_summary = llm.invoke(summary_prompt)
    # Update chat summary in DB
    chat.summary = updated_summary.content
    await sync_to_async(chat.save)()

