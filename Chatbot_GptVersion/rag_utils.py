from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import tempfile

def load_document(file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.name[-4:]) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        if file.name.endswith('.txt'):
            loader = TextLoader(tmp_path)
        elif file.name.endswith('.pdf'):
            loader = PyPDFLoader(tmp_path)
        else:
            raise ValueError("Unsupported file format.")

        documents = loader.load()
        return documents
    except Exception as e:
        raise RuntimeError(f"Document loading failed: {e}")

def init_vector_store(documents):
    try:
        splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(chunks, embeddings)
        return vectorstore
    except Exception as e:
        raise RuntimeError(f"Vector store initialization failed: {e}")

def get_context(query, vectorstore, k=3):
    try:
        docs = vectorstore.similarity_search(query, k=k)
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return f"Error retrieving context: {e}"
