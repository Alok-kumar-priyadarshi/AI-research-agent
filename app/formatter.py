from app.llm import get_llm

def format_response(query: str, raw_text: str):
    llm = get_llm()

    prompt = f"""
You are a professional research report generator.

Convert the following into STRICT JSON.

Include sources if present.

Format:
{{
  "title": "...",
  "summary": "...",
  "key_points": ["..."],
  "detailed_analysis": "...",
  "sources": []
}}

Query: {query}
Content: {raw_text}
"""

    response = llm.invoke(prompt)

    return response.content