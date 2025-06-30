import ollama
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# Ask user for a question
question = input("Enter your question: ").strip()
if not question:
    print("Please enter a valid question.")
    exit()

# Load and prepare local documents
loader = TextLoader("rag_data.txt")
documents = loader.load()
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

# Create a vector store using Phi-3 Mini embeddings
embedding = OllamaEmbeddings(model="phi3:mini")
vectorstore = FAISS.from_documents(docs, embedding)

# Setup retriever and RAG-powered pipeline
retriever = vectorstore.as_retriever()
llm = OllamaLLM(model="phi3:mini")
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=False)

# Get the answer using RAG
rag_response = qa.invoke(question)

# Display just the result
print("\n--- WITH RAG --- \n")
print(rag_response if isinstance(rag_response, str) else rag_response.get("result", rag_response))
