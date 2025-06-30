import os
from dotenv import load_dotenv
import google.generativeai as genai
 
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings  # ✅ Updated import to fix deprecation
 
# -----------------------------------------------
# 🔑 Load Gemini API Key
# -----------------------------------------------
print("🔑 Loading API key...")
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
 
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file!")
 
print("✅ API key loaded")
 
# -----------------------------------------------
# ⚙️ Configure Gemini Model
# -----------------------------------------------
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
print("🚀 Gemini model configured")
 
# -----------------------------------------------
# 📄 Load and Split Document
# -----------------------------------------------
print("📂 Loading and splitting document...")
loader = TextLoader("rag_data.txt")
documents = loader.load()
 
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)
 
# Debug: print all chunks
for i, d in enumerate(docs):
    print(f"Chunk {i+1}:\n{d.page_content}\n")
 
# -----------------------------------------------
# 🧠 Create FAISS Vector Store for RAG
# -----------------------------------------------
print("🔎 Creating FAISS vector store...")
embedding = OllamaEmbeddings(model="phi3:mini")  # Used for embeddings only
vectorstore = FAISS.from_documents(docs, embedding)
retriever = vectorstore.as_retriever()
 
# -----------------------------------------------
# ❓ RAG Query Execution
# -----------------------------------------------
query = "What is Lifecode Genorex and how does it operate?"
 
print("📥 Retrieving relevant chunks...")
relevant_docs = retriever.get_relevant_documents(query)
context = "\n\n".join([doc.page_content for doc in relevant_docs])
 
print("\n📄 Retrieved Context:")
print(context)
 
# Compose prompt
prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
 
# Ask Gemini
response = model.generate_content(prompt)
 
# Output
print("\n🌐 GEMINI RAG RESPONSE:\n")
print(response.text)