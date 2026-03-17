from langchain.agents import initialize_agent, AgentType
from app.llm import get_llm
from app.tools.tools import search_tool


def get_agent():
    llm = get_llm()

    agent = initialize_agent(
        tools=[search_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=3,
        early_stopping_method="generate"
    )

    return agent