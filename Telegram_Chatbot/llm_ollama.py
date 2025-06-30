import requests

def query_ollama(messages):
    prompt = "\n".join(messages)
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "phi3:mini",
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]
