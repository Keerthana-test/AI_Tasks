# gemini_bot.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("Gemini_API_Key"))

model = genai.GenerativeModel("gemini-2.0-flash")

def generate_response_gemini(session, user_input):
    messages = [{"role": m["role"], "parts": [m["content"]]} for m in session.get_history()]
    messages.append({"role": "user", "parts": [user_input]})
    chat = model.start_chat(history=messages)
    response = chat.send_message(user_input)
    return response.text
