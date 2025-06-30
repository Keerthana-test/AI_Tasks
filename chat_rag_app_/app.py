import streamlit as st
import os
import time
import json
from datetime import datetime
from rag_utils import load_and_process_document, retrieve_context
from ollama_utils import get_ollama_answer
from gemini_utils import get_gemini_answer

# ------------------ PAGE SETTINGS ------------------ #
st.set_page_config(page_title="AI Chat Assistant", layout="wide")

# ------------------ CUSTOM STYLES ------------------ #
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background-color: #1e1e2f;  /* Deep dark background */
    color: #f0f0f0;
}

/* Headers */
h1, h2, h3, h4 {
    color: #ffffff;
    font-weight: 700;
}

h1#ai-chat-assistant {
    font-size: 2.5rem;
    color: #f8f8f8;
}

/* Sidebar */
.stSidebar {
    background: linear-gradient(to bottom, #2a2a40, #1e1e2f);
    color: #ffffff;
    padding: 2rem 1rem;
    border-top-right-radius: 15px;
    border-bottom-right-radius: 15px;
}

/* Input fields */
.stTextInput input, .stTextArea textarea {
    background-color: #2a2a40;
    color: #f0f0f0 !important;
    border: 1px solid #444c66;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    font-size: 1rem;
}

/* File uploader and others */
.stFileUploader, .stSelectbox {
    background-color: #2a2a40 !important;
    color: #f0f0f0 !important;
    border-radius: 10px !important;
    border: 1px solid #444c66 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(to right, #7fd8be, #48cae4);
    color: #000000;
    font-weight: 600;
    border-radius: 10px;
    padding: 0.7rem 1.5rem;
    border: none;
    transition: 0.3s ease-in-out;
    box-shadow: 0 3px 10px rgba(0,0,0,0.3);
}

.stButton > button:hover {
    background: linear-gradient(to right, #48cae4, #7fd8be);
    transform: translateY(-2px);
}

/* Chat Bubbles */
.chat-bubble {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    padding: 1rem;
    border-radius: 15px;
    margin-bottom: 1rem;
    font-size: 0.95rem;
    line-height: 1.6;
    background: #2a2a40;
    color: #f0f0f0;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

.user-bubble {
    background: #3b3b55;
    border-left: 4px solid #7fd8be;
    margin-left: auto;
}

.ai-bubble {
    background: #2a2a40;
    border-left: 4px solid #48cae4;
}

/* Avatar */
.chat-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background-color: #48cae4;
    margin-right: 10px;
}

/* Expander & markdown */
details summary {
    color: #7fd8be;
    font-weight: 600;
}

.stMarkdown p {
    color: #f0f0f0;
}

/* Alerts and context boxes */
.stAlertContainer {
    background-color: #2f2f44;
    color: #ffffff;
    border: 1px solid #444c66;
    border-radius: 10px;
    padding: 1rem;
}

/* Token Info */
.metadata-badge {
    font-size: 0.85rem;
    background: #444c66;
    color: #f0f0f0;
    padding: 0.4rem 0.8rem;
    border-radius: 8px;
    display: inline-block;
    margin-top: 0.5rem;
}

/* Hide uploaded file name */
.stElementContainer.element-container.st-key-uploaded_file p {
    display: none;
}
        /* Sidebar Header and Text - Yellow Color */
.stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6, 
.stSidebar p, .stSidebar label, .stSidebar .stRadio, .stSidebar .stSelectbox {
    color: #f7e55e !important;  /* Pastel yellow */
}

</style>

""", unsafe_allow_html=True)

# ------------------ TITLE & INTRO ------------------ #
st.title("😎 Chat with Gemini/Ollama")
st.write("Welcome! Configure your LLM and upload a knowledge base to start chatting.")
st.info("Your answers (with and without RAG) will appear below.")

# ------------------ SIDEBAR ------------------ #
with st.sidebar:
    st.header("⚙️ Configuration")
    llm_choice = st.radio("Choose the options:", ("➡️Gemini API", "➡️Ollama"), key="llm_choice")
    uploaded_file = st.file_uploader("Upload Knowledge Base (TXT or PDF)", type=["txt", "pdf"], key="uploaded_file")
    user_question = st.text_input("Enter your question:", placeholder="e.g., What are the privacy practices?", key="user_question")
    submit_button = st.button("Get Answers", type="primary", key="submit_button")

# ------------------ SESSION INIT ------------------ #
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'knowledge_base_loaded' not in st.session_state:
    st.session_state.knowledge_base_loaded = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# ------------------ FILE PROCESS ------------------ #
if uploaded_file is not st.session_state.get('last_uploaded_file'):
    if uploaded_file is not None:
        with st.spinner("Processing knowledge base..."):
            vectorstore, error_message = load_and_process_document(uploaded_file, llm_choice)
            if vectorstore:
                st.session_state.vectorstore = vectorstore
                st.session_state.knowledge_base_loaded = True
                st.session_state.last_uploaded_file = uploaded_file
            else:
                st.session_state.vectorstore = None
                st.session_state.knowledge_base_loaded = False
                st.error(f"Failed to load knowledge base: {error_message}")
    else:
        st.session_state.vectorstore = None
        st.session_state.knowledge_base_loaded = False
        st.session_state.last_uploaded_file = None

# ------------------ KNOWLEDGE BASE STATUS ------------------ #
if st.session_state.knowledge_base_loaded:
    st.sidebar.success("✅ Knowledge base loaded!")
else:
    st.sidebar.warning("⚠️ No knowledge base loaded yet. Answers will be without RAG context.")

# ------------------ ANSWER HANDLING ------------------ #
if submit_button and user_question:
    st.markdown("---")
    st.subheader("💬 Chat")

    st.markdown(f"""
        <div class="chat-bubble user-bubble">
            <strong>You:</strong><br>{user_question}
        </div>
    """, unsafe_allow_html=True)

    retrieved_docs = []
    retrieved_context_text = None

    if st.session_state.knowledge_base_loaded:
        with st.spinner("Retrieving relevant context..."):
            retrieved_docs, retrieved_context_text, error_retrieval = retrieve_context(
                st.session_state.vectorstore, user_question
            )
            if error_retrieval:
                st.error(f"Error during context retrieval: {error_retrieval}")
            else:
                with st.expander("📄 Show Retrieved Context"):
                    if retrieved_docs:
                        for i, doc in enumerate(retrieved_docs):
                            st.markdown(f"**Document Chunk {i+1}:**")
                            st.code(doc.page_content, language='markdown')
                    else:
                        st.info("No relevant context found.")

    start_time = time.time()
    col1, col2 = st.columns(2)

    # ------------------ WITHOUT RAG ------------------ #
    with col1:
        st.markdown("#### 🧠 Answer Without RAG")
        with st.spinner("Generating answer without context..."):
            if llm_choice == "Gemini API":
                answer_no_rag, error_no_rag = get_gemini_answer(user_question)
            else:
                answer_no_rag, error_no_rag = get_ollama_answer(user_question)

            if answer_no_rag:
                st.markdown(f"""
                    <div class="chat-bubble ai-bubble">
                        <img src="chatbot.png" class="chat-avatar" />
                        <div><strong>AI:</strong><br>{answer_no_rag}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"❌ Error: {error_no_rag}")

    # ------------------ WITH RAG ------------------ #
    with col2:
        st.markdown("#### 📚 Answer With RAG")
        if st.session_state.knowledge_base_loaded and retrieved_context_text:
            with st.spinner("Generating answer with context..."):
                if llm_choice == "Gemini API":
                    answer_with_rag, error_with_rag = get_gemini_answer(user_question, retrieved_context_text)
                else:
                    answer_with_rag, error_with_rag = get_ollama_answer(user_question, retrieved_context_text)

                if answer_with_rag:
                    st.markdown(f"""
                        <div class="chat-bubble ai-bubble">
                            <img src="chatbot.png" class="chat-avatar" />
                            <div><strong>AI:</strong><br>{answer_with_rag}</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"❌ Error: {error_with_rag}")
        else:
            st.info("Knowledge base not loaded or no relevant context found.")

    end_time = time.time()

    # Log and save both answers
    for label, ans in [("No RAG", answer_no_rag if 'answer_no_rag' in locals() else None),
                       ("With RAG", answer_with_rag if 'answer_with_rag' in locals() else None)]:
        if ans:
            elapsed = round(end_time - start_time, 2)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            token_count = len(ans.split())
            st.markdown(f"""
                <div style='font-size: 0.8rem; color: #d6368b;'>
                    📌 <strong>{label}</strong>: 🔹 Tokens: {token_count} | ⏱️ Time: {elapsed}s | ⏰ {timestamp}
                </div>
            """, unsafe_allow_html=True)

            st.session_state.chat_history.append({
                "question": user_question,
                "answer": ans,
                "type": label,
                "tokens": token_count,
                "response_time": elapsed,
                "timestamp": timestamp
            })

    with open("chat_history.json", "w") as f:
        json.dump(st.session_state.chat_history, f, indent=2)

elif submit_button and not user_question:
    st.warning("Please enter a question.")