import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")

client = TavilyClient(tavily_api_key)

def web_search(query:str)->str:
    try:
        response = client.search(
            query=query,
            max_results=2
        )
        contents = []
        sources = []
        
        for r in response["results"]:
            content = r.get("content","")
            url = r.get("url","")
            
            if content:
                contents.append(content)
            if url:
                sources.append(url)
                
        return {
            "content":"\n\n".join(contents),
            "sources": sources
        }
    except Exception as e:
        return f"Search Error: {str(e)}"