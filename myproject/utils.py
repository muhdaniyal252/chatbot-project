
from pydub import AudioSegment
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from LLMs import get_llm
from TTSs import get_tts
from STTs import get_stt
import asyncio
import os
from io import BytesIO


from core.models import User, Chat, Message, Agent
from asgiref.sync import sync_to_async
from dotenv import load_dotenv

load_dotenv()
llm = get_llm(os.environ.get("LLM", "gpt"))
tts = get_tts(os.environ.get("TTS", "openai"))
stt = get_stt(os.environ.get("STT", "openai"))

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


def get_response(instructions, user_input, messages, summary, llm_instance=None):
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
    message_texts = [msg.content for msg in messages][::-1]
    agent = await sync_to_async(lambda: chat.agent)()
    await sync_to_async(Message.objects.create)(chat=chat, user=user, content=message)

    # Call get_response to get LLM reply
    instructions = agent.prompt

    summary = chat.summary or ""  # Use empty string if no summary exists
    llm_response = get_response(instructions, message, message_texts, summary)

    # Save LLM response as a new message in the database
    await sync_to_async(Message.objects.create)(chat=chat, user=user, content=llm_response, message_by='ai')

    # Function to be executed in parallel (async summary update)
    asyncio.create_task(update_summary(chat, message_texts, summary))

    return llm_response

async def process_audio_message(audio_file: BytesIO, chatid: int, userid: int):
    user = await sync_to_async(User.objects.get)(id=userid)
    chat = await sync_to_async(Chat.objects.get)(id=chatid, user=user)

    # Convert audio to WAV for compatibility
    try:
        audio = AudioSegment.from_file(audio_file)
        wav_buffer = BytesIO()
        wav_buffer.name = "converted.wav"
        audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)
        transcribed_text = await stt.transcribe(wav_buffer)
    except Exception as e:
        # Fallback: try original
        transcribed_text = await stt.transcribe(audio_file)
    await sync_to_async(Message.objects.create)(chat=chat, user=user, content=transcribed_text)
    agent = await sync_to_async(lambda: chat.agent)()
    messages = await sync_to_async(lambda: list(Message.objects.filter(chat=chat).order_by('-timestamp')[:10]))()
    message_texts = [msg.content for msg in messages][::-1]
    instructions = agent.prompt
    summary = chat.summary or ""  # Use empty string if no summary exists
    llm_response = get_response(instructions, transcribed_text, message_texts, summary)
    await sync_to_async(Message.objects.create)(chat=chat, user=user, content=llm_response, message_by='ai')
    # Function to be executed in parallel (async summary update)
    asyncio.create_task(update_summary(chat, message_texts, summary))
    audio_buffer = BytesIO()
    await tts.synthesize(llm_response, audio_buffer)
    audio_buffer.seek(0)
    return transcribed_text, llm_response, audio_buffer

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

