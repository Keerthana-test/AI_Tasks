import streamlit as st
import time
from chat_session import ChatSession
from gemini_bot import generate_response_gemini
from ollama_bot import generate_response_ollama

# Streamlit configuration
st.set_page_config(page_title="💬 AI Chatbot | Gemini & Ollama", layout="wide")

# Dark theme styling + floating chat button
st.markdown("""
    <style>
    html, body, [class*="css"] {
        background-color: #0E1117;
        color: #E0E0E0;
        font-family: 'Segoe UI', sans-serif;
    }

    .big-title {
        font-size: 38px;
        font-weight: bold;
        color: #1DB954;
        margin-bottom: 10px;
    }

    .sub-title {
        font-size: 17px;
        color: #A0A0A0;
        margin-bottom: 25px;
    }

    .footer {
        font-size: 12px;
        text-align: center;
        color: #666;
        margin-top: 40px;
    }

    .stTextInput>div>div>input {
        height: 48px;
        font-size: 16px;
    }

    section[data-testid="stSidebar"] {
        width: 300px !important;
        background-color: #11141A;
    }

    stChatInputContainer {
    display: flex;
    justify-content: center;
}

.stChatInputContainer input {
    height: 52px !important;
    font-size: 16px;
    padding: 10px 20px;
    width: 75% !important;  /* Limit horizontal width */
    border-radius: 12px !important;
    border: 1px solid #1DB954;
    background-color: #1A1A1A;
    color: #ffffff;
}

/* Align the floating chat button with new layout */
.floating-button {
    bottom: 80px;  /* Raise to clear input box */
}

    
    </style>
""", unsafe_allow_html=True)

# Floating button (launches a message when clicked)
st.markdown("""
    <button class="floating-button" onclick="document.querySelector('input[type=text]').focus()">💬</button>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="big-title">🤖 Multi - LLM Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Talk with Gemini and Ollama</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Chat Settings")
    model_choice = st.radio("Select Model", ["Gemini", "Ollama (phi3:mini)"])
    if st.button("🔄 Reset Chat"):
        st.session_state.chat_session.clear()
        st.success("✅ Chat memory has been reset.")
    st.markdown("---")
    st.markdown("🧑‍💻 <span style='color:#bbb;'>Built by <b>Keerthi</b></span>", unsafe_allow_html=True)

# Session init
if "chat_session" not in st.session_state:
    st.session_state.chat_session = ChatSession()

# History rendering
for msg in st.session_state.chat_session.get_history():
    with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# Input section
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.chat_session.add_message("user", user_input)
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_input)

    try:
        # Streaming typing effect
        with st.chat_message("model", avatar="🤖"):
            response_container = st.empty()
            full_response = ""

            if model_choice == "Gemini":
                response_text = generate_response_gemini(st.session_state.chat_session, user_input)
            else:
                response_text = generate_response_ollama(st.session_state.chat_session, user_input)

            for char in response_text:
                full_response += char
                response_container.markdown(full_response)
                time.sleep(0.01)  # Typing animation speed

            st.session_state.chat_session.add_message("model", full_response)

    except Exception as e:
        st.error(f"❌ Error: {e}")

# Footer
st.markdown('<div class="footer">© 2025 Keerthi. </div>', unsafe_allow_html=True)
