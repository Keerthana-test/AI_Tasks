import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")

def generate_response(message):
    try:
        if LLM_PROVIDER == "ollama":
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "phi3", "prompt": message}
            )
            response.raise_for_status()
            return response.json()["response"]

        elif LLM_PROVIDER == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                return "❗ Missing GEMINI_API_KEY in .env file"

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(message)
            return response.text

        else:
            return "❗ Invalid LLM_PROVIDER. Set it to 'gemini' or 'ollama' in .env"

    except Exception as e:
        print("⚠️ LLM Error:", e)
        return "❌ Sorry, I had trouble generating a response."

