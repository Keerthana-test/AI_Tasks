import google.generativeai as genai
import streamlit as st
import os
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the API key.
try:
    # Retrieve the API key from environment variables
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except ValueError as ve:
    st.error(f"Configuration error: {ve}")
    model = None # Set model to None if configuration fails
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}. Make sure your API key is correct and accessible.")
    model = None # Set model to None if configuration fails

def chat_with_gemini(prompt: str):
    """
    Sends a prompt to the Gemini model and returns the response.
    """
    if model is None:
        return None, "Gemini model not initialized due to configuration error."

    try:
        response = model.generate_content(prompt)
        if response.text:
            return response.text, None
        else:
            return None, "No text response received from Gemini model."
    except Exception as e:
        return None, f"Error communicating with Gemini API: {e}. Check your API key and network connection."

def get_gemini_answer(query: str, context: str = None):
    """
    Constructs the prompt for Gemini with or without context and gets the answer.
    """
    if context:
        full_prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
    else:
        full_prompt = f"Question: {query}\n\nAnswer:"

    answer, error = chat_with_gemini(full_prompt)
    return answer, error

