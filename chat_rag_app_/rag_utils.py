import streamlit as st
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
import os

@st.cache_resource # Cache the vector store to avoid re-creating it on every rerun
def load_and_process_document(uploaded_file, llm_choice):
	"""
	Loads, splits, and creates a FAISS vector store from an uploaded document.
	The embedding model depends on the selected LLM for consistency.
	"""
	if uploaded_file is None:
		return None, "Please upload a document first."

	file_extension = os.path.splitext(uploaded_file.name)[1].lower()
	docs = []

	try:
		# Create a temporary file to save the uploaded content
		# This is necessary because LangChain loaders expect a file path
		with open(os.path.join("temp_uploaded_file" + file_extension), "wb") as f:
			f.write(uploaded_file.getbuffer())
		file_path = "temp_uploaded_file" + file_extension

		if file_extension == ".txt":
			loader = TextLoader(file_path, encoding="utf-8")
		elif file_extension == ".pdf":
			loader = PyPDFLoader(file_path)
		else:
			return None, f"Unsupported file type: {file_extension}. Only .txt and .pdf are supported."

		documents = loader.load()

		# Remove the temporary file after loading
		os.remove(file_path)

		if not documents:
			return None, "Could not load any content from the document. It might be empty or unreadable."

		# Text Splitting
		text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
		docs = text_splitter.split_documents(documents)

		if not docs:
			return None, "Document split resulted in no chunks. Content might be too small or text splitter issue."

		# Determine embedding model based on LLM choice
		# Note: For Gemini, we typically use specialized embeddings like GoogleGenerativeAIEmbeddings.
		# For simplicity in this example, we'll use OllamaEmbeddings for both if `ollama_embeddings`
		# is the only one available via Langchain's direct integration.
		# For a more robust solution with Gemini, you'd integrate GoogleGenerativeAIEmbeddings
		# from langchain_google_genai.

		# Using OllamaEmbeddings as a common ground for simplicity and local execution
		# For production, if using Gemini, you'd likely use GoogleGenerativeAIEmbeddings
		# from langchain_google_genai import GoogleGenerativeAIEmbeddings

		embeddings = OllamaEmbeddings(model="phi3:mini") # Using phi3:mini for embeddings

		# Create FAISS vector store
		vectorstore = FAISS.from_documents(docs, embeddings)
		st.success(f"Knowledge base '{uploaded_file.name}' loaded and processed into vector store.")
		return vectorstore, None

	except Exception as e:
		st.error(f"Error processing document: {e}")
		if os.path.exists(file_path): # Clean up temp file on error
			os.remove(file_path)
		return None, str(e)


def retrieve_context(vectorstore, query, k=3):
	"""
	Retrieves relevant document chunks from the vector store based on the query.
	"""
	if vectorstore is None:
		return [], "No knowledge base loaded."

	try:
		# Perform similarity search
		retrieved_docs = vectorstore.similarity_search(query, k=k)
		context = "\n\n".join([doc.page_content for doc in retrieved_docs])
		return retrieved_docs, context, None
	except Exception as e:
		return [], None, f"Error retrieving context: {e}"

