from langgraph.graph import START, END, StateGraph
from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict, Dict, List
from langchain_core.output_parsers import StrOutputParser
from .models import code_model # use code specific llm here
from .agent_utils import AgentUtils

class AgentState(TypedDict):
    files_paths:List[str]
    output:Dict[str, str]

def process_files(state:AgentState) -> AgentState:
    """Processes files"""

    analyze_pt = ChatPromptTemplate.from_messages(
        messages=[
            ("system", "You are a code analyzer! You use function name to conclude what the code file might be about!"),
            ("system", "Here are some function names: {funcs_str}"),
            ("system", "Give response in as plain text in 30 words.")
        ]
    )
    chain = analyze_pt | code_model | StrOutputParser()

    output = {}
    files = state["files_paths"]
    for ind, file in enumerate(files, start=1):
        print(f"-> Analyzing file | file number: {ind}")
        funcs = AgentUtils.extract_func_names(file)
        if len(funcs) == 0:
            continue
        else:
            funcs_str = ", ".join(funcs)
            analysis = chain.invoke({"funcs_str":funcs_str})
            output[file] = analysis


    state_upd = {"output":output}
    return state_upd

workflow = StateGraph(AgentState)
workflow.add_node(process_files)
workflow.add_edge(START, "process_files")
workflow.add_edge("process_files", END)
analyzer = workflow.compile()