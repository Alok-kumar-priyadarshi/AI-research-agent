from fastapi import FastAPI
from app.schemas import ResearchRequest
from app.llm import get_llm
from app.tools.search import web_search
from app.agent import get_agent
from app.formatter import format_response
import time
from app.cache import get_from_cache , save_to_cache
from app.rag import create_vector_store
from app.memory import get_memory
import asyncio
from app.utils.router import needs_realtime_data

vectorstore = create_vector_store()
retriever = vectorstore.as_retriever()

app = FastAPI()

@app.get("/")
def home():
    return {
        "message":"AI Research Agent Running"
    }

    
    
@app.get("/test-search")
def test_search():
    result = web_search("Impact of AI on jobs 2026")
    return {"result":result}    


@app.post("/research")
async def research(request: ResearchRequest):
    try:
        start_time = time.time()
        
        #  GET USER-SPECIFIC MEMORY
        memory = get_memory(request.session_id)

        # CACHE
        cache_key = f"{request.session_id}:{request.query}"
        cached_result = get_from_cache(cache_key)
        if cached_result:
            return {
                "query": request.query,
                "response": cached_result,
                "cached": True
            }

        # 🔥 MEMORY (always needed)
        chat_history = await asyncio.to_thread(memory.load_memory_variables, {})

        # 🔥 ROUTING LOGIC
        if needs_realtime_data(request.query):
            # 👉 REAL-TIME PATH (skip RAG)
            context = ""

            enriched_query = f"""
        IMPORTANT:
        - You MUST use the Web Search tool for latest or real-time information.
        - Do NOT rely on old knowledge.

        Chat History:
        {chat_history}

        User Query:
        {request.query}
        """
        else:
            # 👉 RAG PATH
            docs = await asyncio.to_thread(
                retriever.get_relevant_documents,
                request.query
            )

            context = "\n".join([d.page_content for d in docs])

            enriched_query = f"""
        Use the provided context to answer.

        Chat History:
        {chat_history}

        Context:
        {context}

        User Query:
        {request.query}
        """

        agent = get_agent()

        try:
            raw_output = await asyncio.to_thread(agent.run, enriched_query)
        except Exception as e:
            llm = get_llm()
            raw_output = await asyncio.to_thread(
                lambda: llm.invoke(enriched_query).content
            )

        #  FORMAT
        formatted_output = format_response(
            request.query,
            raw_output
        )

        #  SAVE MEMORY
        memory.save_context(
            {"input": request.query},
            {"output": formatted_output}
        )

        #  CACHE
        save_to_cache(cache_key , formatted_output)

        end_time = time.time()

        return {
            "query": request.query,
            "response": formatted_output,
            "context_used": context,
            "response_time": f"{end_time - start_time:.2f} seconds"
        }

    except Exception as e:
        return {"error": str(e)}




