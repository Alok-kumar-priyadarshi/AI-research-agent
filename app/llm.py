from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

model_id = "openai/gpt-oss-120b"


def get_llm():
    llm = ChatGroq(
        model=model_id,
        temperature=0,
        # max_tokens=512,
        api_key=os.getenv("GROQ_API_KEY")
        
    )
    
    return llm