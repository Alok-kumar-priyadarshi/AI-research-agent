from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter

documents = [
    "AI is transforming industries...",
    "Machine learning is a subset of AI...",
    "RAG systems combine retrieval with generation..."
    
]

def create_vector_store():
    splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    docs = splitter.create_documents(documents)
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_documents(docs , embeddings)
    return vectorstore

