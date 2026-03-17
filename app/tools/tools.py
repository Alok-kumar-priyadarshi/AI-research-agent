from langchain_core.tools import Tool
from app.tools.search import web_search

def search_wrapper(query: str) -> str:
    result = web_search(query)

    content = result["content"]
    sources = result["sources"]

    formatted = f"""
CONTENT:
{content}

SOURCES:
{sources}
"""

    return formatted



search_tool = Tool(
    name="Web Search",
    func=search_wrapper,
    description="""
Use this tool for ANY query requiring real-time or current information.
You MUST use this tool before answering such queries.
"""
)