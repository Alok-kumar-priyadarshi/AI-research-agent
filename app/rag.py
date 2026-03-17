from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader

vectorstore = {}


def create_vector_store_from_pdf(file_path:str , session_id:str):
    # global vectorstore
    loader = PyPDFLoader(file_path)
    documents = loader.load()[:5] 
    
    splitter = CharacterTextSplitter(chunk_size=200,chunk_overlap=30)
    docs = splitter.split_documents(documents)
    
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_documents(docs , embeddings)
    vectorstore[session_id] = vectorstore
    return vectorstore

def get_retriever(session_id: str):
    if session_id in vectorstores:
        return vectorstores[session_id].as_retriever()
    return None


