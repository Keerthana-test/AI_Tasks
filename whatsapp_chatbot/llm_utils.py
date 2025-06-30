import json
import google.generativeai as genai
import os
import requests
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-2.0-flash")


def ask_gemini(session):
    try:
        prompt = "\n".join([f"{m['role']}: {m['text']}" for m in session[-10:]])
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Gemini Error:", e)
        return "⚠️ Gemini encountered an internal error."


def ask_ollama(session):
    try:
        import requests

        prompt = "\n".join([f"{m['role']}: {m['text']}" for m in session[-10:]])
        print("[DEBUG] Sending to Ollama:", prompt)

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "phi3:mini", "prompt": prompt},
            stream=True
        )

        reply = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    reply += data.get("response", "")
                except Exception as parse_error:
                    print("[ERROR] Parsing line failed:", line)

        print("[DEBUG] Ollama final reply:", reply)
        return reply.strip() or "⚠️ Empty response from Ollama."

    except Exception as e:
        print("[ERROR] Ollama exception:", e)
        return "⚠️ Failed to connect to Ollama."

