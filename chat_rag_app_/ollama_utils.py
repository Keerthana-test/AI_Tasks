import ollama
import streamlit as st

# @st.cache_data # Might not be suitable for dynamic chat, depending on needs
def chat_with_ollama(model_name: str, prompt: str):
	"""
	Sends a prompt to the Ollama model and returns the response.
	"""
	try:
		response = ollama.chat(
			model=model_name,
			messages=[{'role': 'user', 'content': prompt}]
		)
		return response['message']['content'], None
	except Exception as e:
		return None, f"Error communicating with Ollama: {e}. Is Ollama server running and model '{model_name}' pulled?"

def get_ollama_answer(query: str, context: str = None):
	"""
	Constructs the prompt for Ollama with or without context and gets the answer.
	"""
	if context:
		full_prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
	else:
		full_prompt = f"Question: {query}\n\nAnswer:"

	# Using phi3:mini as per assignment brief
	answer, error = chat_with_ollama("phi3:mini", full_prompt)
	return answer, error

