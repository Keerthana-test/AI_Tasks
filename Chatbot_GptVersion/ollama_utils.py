import requests

def ask_ollama(query, context=""):
    prompt = f"Context:\n{context}\n\nQuestion: {query}"
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "phi3", "prompt": prompt},
            timeout=10  # Add timeout to avoid freeze
        )
        response.raise_for_status()

        return response.json().get("response", "No reply received.")
    except requests.exceptions.RequestException as e:
        return f"Ollama error: {e}"
