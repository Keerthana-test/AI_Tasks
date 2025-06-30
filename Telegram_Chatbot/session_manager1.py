# session_manager.py

# Dictionary to store user session data
# Structure: { user_id: { "model": ..., "history": [...] } }
user_sessions = {}

def get_session(user_id):
    """Ensure a session exists for the user and return it"""
    if user_id not in user_sessions:
        user_sessions[user_id] = {"model": None, "history": []}
    return user_sessions[user_id]

def set_model(user_id, model_name):
    """Set the preferred model (gemini or ollama) for the user"""
    session = get_session(user_id)
    session["model"] = model_name

def update_history(user_id, message):
    """Append a message to the user's chat history and return full history"""
    session = get_session(user_id)
    session["history"].append(message)
    return session["history"]

def clear_session(user_id):
    """Reset the user's session (model + history)"""
    user_sessions[user_id] = {"model": None, "history": []}
