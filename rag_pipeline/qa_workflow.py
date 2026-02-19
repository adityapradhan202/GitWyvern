from langgraph.graph import StateGraph, END, START
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict, Literal
from .builder import RagBuilder
from pydantic import BaseModel
from .rag_models import code_model

builder = RagBuilder()

class QueryClassification(BaseModel):
    query_type:Literal["code-related", "not-code-related"]

class AgentState(TypedDict):
    query:str
    query_type:str
    response:str

def process_query(state:AgentState) -> AgentState:
    """Processes user query and decides whether it's code related or not"""

    print('-> Processing your query')
    query = state['query']
    struct_model = code_model.with_structured_output(QueryClassification)
    classify_pt = ChatPromptTemplate.from_template("Find out of the query is realted to coding/programming or not. Classify this query as 'code-related' or 'not-code-related'. -> Query: {query}")
    chain = classify_pt | struct_model
    
    res = chain.invoke({'query':query})
    query_type = res.query_type
    state_upd = {'query_type':query_type}
    return state_upd

def route_logic(state:AgentState) -> str:
    """Routing logic. Decides whether to use RAG or not"""

    print("-> Deciding whether to use RAG or not")
    if state['query_type'] == "code-related":
        return "use-rag"
    else:
        return "dont-use-rag"

def use_rag(state:AgentState) -> AgentState:
    """Uses RAG and answers user query"""

    print("-> Query is code related. Using RAG.")
    answer_pt = ChatPromptTemplate.from_messages(
        [("system", "You are an experienced python developer. You have all the knowledge about python"),
        ("system", "You are also a helpful assistant who uses the provided context to find and generate an answer for user's query"),
        ("system", "Just give the answer and dont ask any follow up questions. Also avoid giving predeclarations like 'here is the answer from the context'."),
        ("system", "Query: {query}, Context: {context}"),
        ("system", "Your response should be in markdown format.")]
    )
    chain = answer_pt | code_model | StrOutputParser()

    query = state['query']
    context = builder.retrieve_docs(query=query)
    response = chain.invoke({'query':query, 'context':context})
    state_upd = {'response':response}

    return state_upd

def dont_use_rag(state:AgentState) -> AgentState:
    """Warns users and tells them that it wont answer off topic queries"""

    print("-> Warning the user. Cant answer off topic questions.")
    warn_pt = ChatPromptTemplate.from_messages(
        messages=[
            ("system", "You are an AI powered repository intelligence system"),
            ("system", "Tell the user that your expertise lies in python programming. And you cant answer their off-topic query. -> This is the user's query: {query}")
        ]
    )

    chain = warn_pt | code_model | StrOutputParser()
    response = chain.invoke({'query':state['query']})
    state_upd = {'response':response}

    return state_upd


workflow = StateGraph(AgentState)
workflow.add_node(process_query)
workflow.add_node(use_rag)
workflow.add_node(dont_use_rag)


workflow.add_edge(START, "process_query")
workflow.add_conditional_edges(
    source="process_query", path=route_logic,
    path_map={'use-rag':"use_rag", "dont-use-rag":"dont_use_rag"}
)
workflow.add_edge("use_rag", END)
workflow.add_edge("dont_use_rag", END)
qa_rag = workflow.compile()


