import os
from functools import lru_cache
from typing import TypedDict

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, START, END

MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4.1-mini")


class ResearchState(TypedDict):
    topic: str
    research: str
    report: str


RESEARCHER_PROMPT = (
    "You are a research assistant. Your job is to find relevant, high-quality "
    "information on the given topic using web search. "
    "Search thoroughly — look for facts, statistics, expert opinions, and recent developments. "
    "When you're done searching, summarize all your findings in a detailed report. "
    "Include specific data points, source names, and key takeaways."
)

WRITER_PROMPT = (
    "You are a research report writer. You receive research notes from a colleague "
    "and must turn them into a polished, well-structured final report.\n\n"
    "Write in clear, professional prose. Organize the report with appropriate sections "
    "and headings. Cite specific facts and figures from the research notes. "
    "Do not introduce information that is not in the research notes."
)


@lru_cache(maxsize=1)
def _get_researcher_agent():
    tavily_tool = TavilySearch(max_results=5, topic="general")
    return create_agent(
        model=f"openai:{MODEL_NAME}",
        tools=[tavily_tool],
        system_prompt=RESEARCHER_PROMPT,
    )


def researcher(state: ResearchState) -> dict:
    agent = _get_researcher_agent()
    result = agent.invoke(
        {"messages": [{"role": "user", "content": f"Research topic: {state['topic']}"}]}
    )
    return {"research": result["messages"][-1].content}


def writer(state: ResearchState) -> dict:
    llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
    response = llm.invoke(
        [
            {"role": "system", "content": WRITER_PROMPT},
            {"role": "user", "content": f"Topic: {state['topic']}\n\nResearch notes:\n{state['research']}"},
        ]
    )
    return {"report": response.content}


builder = StateGraph(ResearchState)

builder.add_node("researcher", researcher)
builder.add_node("writer", writer)

builder.add_edge(START, "researcher")
builder.add_edge("researcher", "writer")
builder.add_edge("writer", END)

graph = builder.compile()