import os
import chainlit as cl
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
from tools import get_crypto_price

# Load Gemini API key
load_dotenv(find_dotenv())
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini 2.0 Model (update name if needed from Google)
model = genai.GenerativeModel("gemini-1.5-flash")

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        content="👋 Welcome to the Gemini 2.0 Crypto Bot!\nAsk me anything about cryptocurrency."
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history")
    user_input = message.content
    history.append({"role": "user", "content": user_input})

    try:
        # Basic Tool Use: If "price" keyword is in message
        if "price" in user_input.lower():
            reply = get_crypto_price(user_input)
        else:
            # Use Gemini model directly
            gemini_response = model.generate_content(user_input)
            reply = gemini_response.text or "⚠️ Gemini gave no reply."
    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    await cl.Message(content=reply).send()
    history.append({"role": "assistant", "content": reply})
    cl.user_session.set("history", history)

