# app.py

import streamlit as st
from rag_utils import load_document, get_context, init_vector_store
from gemini_utils import ask_gemini
from ollama_utils import ask_ollama

st.set_page_config(page_title="Chat with RAG", layout="wide")
st.title("📄 Chat with Knowledge Base")

st.markdown(
    """
    <style>
    /* Background & layout */
    .block-container {
        background-color: #F8F9FA;
        padding-top: 1rem;
    }

    /* Text input font */
    .stTextInput>div>div>input {
        font-size: 18px;
        color: #2C3E50;
    }

    /* Titles and headers */
    h1, h2, h3 {
        color: #4A90E2;
    }

    /* Buttons */
    .stButton>button {
        background-color: #4A90E2;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        border: none;
    }

    .stButton>button:hover {
        background-color: #3B78C0;
        color: white;
    }

    /* Expander styling */
    .stExpander {
        background-color: #FFFFFF;
        border: 1px solid #DDE2E5;
        border-radius: 6px;
    }

    /* Footer */
    footer {
        color: #999999;
    }

    hr {
        border-top: 1px solid #DDE2E5;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    llm_choice = st.radio("Choose LLM", ["Gemini", "Ollama 🐘"])
    uploaded_file = st.file_uploader("📄 Upload knowledge base", type=["txt", "pdf"])
    st.markdown("---")
    st.markdown("🔹 You can query uploaded content using RAG or run standalone LLM chat.")

# Input
query = st.text_input("🔍 Ask a question about the document:")
submit = st.button("🚀 Submit")

# App logic
if uploaded_file:
    documents = load_document(uploaded_file)
    vectorstore = init_vector_store(documents)
    st.success("✅ Document loaded and indexed!")

if submit and query:
    if uploaded_file:
        context = get_context(query, vectorstore)
    else:
        context = ""

    with st.expander("📚 Retrieved Context (RAG)", expanded=False):
        st.markdown(context if context else "*No context found*")

    # LLM responses
    with st.spinner("💬 Generating responses..."):
        if llm_choice == "Gemini":
            answer_rag = ask_gemini(query, context)
            answer_no_rag = ask_gemini(query, "")
        else:
            answer_rag = ask_ollama(query, context)
            answer_no_rag = ask_ollama(query, "")

    st.markdown("### 🤖 LLM Responses")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ✅ With RAG Context")
        st.markdown(answer_rag, unsafe_allow_html=True)

    with col2:
        st.markdown("#### ❌ Without Context")
        st.markdown(answer_no_rag, unsafe_allow_html=True)

    st.markdown("---")

# Footer
st.markdown(
    "<hr style='margin-top: 2em; margin-bottom: 1em;'>"
    "<center>Built with ❤️ using Streamlit, Gemini, and Ollama</center>",
    unsafe_allow_html=True
)
