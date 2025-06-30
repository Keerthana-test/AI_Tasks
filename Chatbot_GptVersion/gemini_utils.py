import google.generativeai as genai
import os

# Ensure environment variable is set
os.environ["GEMINI_API_KEY"] = "AIzaSyA0icHYG7Ghx_Q5l7WRTOQfD_LmTaXAGvo"
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("Missing GEMINI_API_KEY in environment variables")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-2.0-flash")

def ask_gemini(query, context=""):
    prompt = f"Context:\n{context}\n\nQuestion: {query}"
    try:
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)
    except Exception as e:
        return f"Gemini error: {e}"
