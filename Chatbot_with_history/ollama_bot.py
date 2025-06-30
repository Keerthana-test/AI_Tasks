import requests

def generate_response_ollama(session, user_input):
    # Combine all past messages into one formatted prompt
    conversation = ""
    for msg in session.get_history():
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation += f"{role}: {msg['content']}\n"

    # Append current user message
    conversation += f"User: {user_input}\nAssistant:"

    # Send to Ollama
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "phi3:mini",
        "prompt": conversation,
        "stream": False
    })

    try:
        data = response.json()
        return data.get("response", "").strip()

    except Exception as e:
        return f"❌ Ollama error: {e}"
