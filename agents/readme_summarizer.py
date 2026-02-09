from langgraph.graph import END, START, StateGraph
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict
from .agent_utils import AgentUtils
from .models import model

class AgentState(TypedDict):
    readme_exists:bool
    readme_summary:str

def check_readme(state:AgentState) -> AgentState:
    """Checks if readme file exists"""

    print("-> Checking if readme exists")
    exist = AgentUtils.readme_exists()
    state_upd = {"readme_exists":exist}
    return state_upd

def summarize_parts(state:AgentState) -> AgentState:
    """Summarizes parts of readme file"""

    print("-> Initializing REDME.md summarization")
    summarize_pt = ChatPromptTemplate.from_messages(
        messages=[
            ("system", "Summarize the Text in atmost 20 words easy and simple language! Text: {chunk}"),
            ("system", "Do not give any pre declarations like - here's the summary"),
            ("system", "Do not ask any follow up question or give any post declarations"),
            ("system", "Your only job is to summarize the text. Use bullet points and backticks to highlight something")
        ]
    )

    chain = summarize_pt | model | StrOutputParser()
    readme_exists = state["readme_exists"]
    summary_final = ""

    if readme_exists:
        chunks = AgentUtils.create_chunks(path='./workdir/README.md', chunk_size=900)
        for ind, chunk in enumerate(chunks, start=1):
            print(f"-> Summarizing README.md | chunk no: {ind}")
            summary = chain.invoke({"chunk":chunk})
            summary_final += summary + "\n"
        return {"readme_summary":summary_final}
    else:
        return {"readme_summary":"README.md doesn't exist"}
    
workflow = StateGraph(AgentState)
workflow.add_node(check_readme)
workflow.add_node(summarize_parts)
workflow.add_edge(START, "check_readme")
workflow.add_edge("check_readme", "summarize_parts")
workflow.add_edge("summarize_parts", END)

summarizer = workflow.compile()