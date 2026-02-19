# Combining bandit(SAST) with LLM in a worflow
from langgraph.graph import StateGraph, END, START
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict, List, Dict
from .security_utils import SecurityUtils
from .models import code_model, model

class AgentState(TypedDict):
    overally_safe:bool
    file_paths:List[str]  # invoke the workflow with this
    unsafe_files:List[str]
    # total vulnerabilities
    vul_cnt:Dict[str, Dict[str, int]]
    vuls_sols:Dict[str, List[str]] # vulnerabilities and potential solutions

def scan_files(state:AgentState) -> AgentState:
    """Scans all the files and lists the paths of unsafe files."""

    # print(f"Agent state:\n{state}")
    unsafe_files = []
    for file in state['file_paths']:
        bandit_cout = SecurityUtils.bandit_scan(file)
        s_check = SecurityUtils.safety_check(bandit_cout)
        if s_check == "safe":
            continue
        else:
            unsafe_files.append(file)

    if len(unsafe_files) == 0:
        overally_safe = True
    else:
        overally_safe = False

    # initialize the vulnerability count here
    vul_cnt = {"severity":{"undefined":0, "low":0, "mid":0, "high":0}, "confidence":{"undefined":0, "low":0, "mid":0, "high":0}}    
    state_upd = {"overally_safe":overally_safe, "unsafe_files":unsafe_files, "vul_cnt":vul_cnt}
    return state_upd

def analysis_needed(state:AgentState) -> str:
    """Route logic - decides to perform operations for analyze"""

    if state["overally_safe"] == True:
        return "totally-safe"
    else:
        return "totally-not-safe"
    
def describe_vulnerabilities(state:AgentState) -> AgentState:
    """Describes the vulnerabilities found by bandit"""
    print("Repo has vulnerabilities...")
    prompt_t = ChatPromptTemplate.from_messages(
        messages=[
            ("system", "You are tech secrity analysis"),
            ("system", "Summarize this issue in 50 words(not more than that) in natural human language so that anyone can understand: {issue}"),
            ("system", "The output should be in plain text. Do not give predeclaration like 'here's the summary' or follow up questions!")
        ]
    )
    s_prompt_t = ChatPromptTemplate.from_messages(
        messages=[
            ("system", "Summarize the text within 30 words max"),
            ("system", "Do not give any predeclarations like here's the summary. Also do not ask any follow up questions"),
            ("system", "Summarize this: {vul_d}")
        ]
    )

    # code model for analyzing vulnerability description
    # general purpose model for summarizing
    vul_chain = prompt_t | code_model | StrOutputParser()
    summary_chain = s_prompt_t | model | StrOutputParser()

    unsafe_files = state['unsafe_files']
    vuls_sols = {}
    vul_cnt_prev = state['vul_cnt']
    for file in unsafe_files:
        print(f"Analyzing vulnerabilities in - {file}")

        bandit_cout = SecurityUtils.bandit_scan(file)
        vuls = SecurityUtils.vulnerabilities(bandit_cout)
        vc_map = SecurityUtils.vulnerability_count_map(bandit_cout)

        # update vul_cnt
        vul_cnt_prev["severity"]["undefined"] += vc_map["severity"]["undefined"]
        vul_cnt_prev["severity"]["low"] += vc_map["severity"]["low"]
        vul_cnt_prev["severity"]["mid"] += vc_map["severity"]["mid"]
        vul_cnt_prev["severity"]["high"] += vc_map["severity"]["high"]
        vul_cnt_prev["confidence"]["undefined"] += vc_map["confidence"]["undefined"]
        vul_cnt_prev["confidence"]["low"] += vc_map["confidence"]["low"]
        vul_cnt_prev["confidence"]["mid"] += vc_map["confidence"]["mid"]
        vul_cnt_prev["confidence"]["high"] += vc_map["confidence"]["high"]

        vul_descs = ""
        for vul in vuls:
            vul_d = vul_chain.invoke({'issue':vul}) # vul_d means vulnerability description
            vul_d_s = summary_chain.invoke({'vul_d':vul_d}) # vul_d_s means summart of vulnerability description
            vul_descs += (vul_d_s + " ")

        vuls_sols[file] = [vul_descs]

    state_upd = {'vuls_sols':vuls_sols, "vul_cnt":vul_cnt_prev} # vul_cnt is the updated one
    return state_upd

def recommend_solutions(state:AgentState) -> AgentState:
    """Recommends possible solutions for the vulnerabilities"""

    print("Recommending possible solutions")
    vuls_sols = state['vuls_sols']
    prompt_t = ChatPromptTemplate.from_messages(
        messages=[
            ("system", "You are security tech expert!"),
            ("system", "Recommend a solution for this issue. Your response must be concise(30 words max). Issue: {vul}"),
            ("system", "Do not give any predeclaration like 'here's a solution' or do not ask any follow up questions!")
        ]
    )
    chain = prompt_t | code_model | StrOutputParser()
    for file in vuls_sols:
        vul = vuls_sols[file][0]
        sol = chain.invoke({"vul":vul})
        vuls_sols[file].append(sol)
    
    state_upd = {"vuls_sols":vuls_sols}
    return state_upd
            
workflow = StateGraph(AgentState)
workflow.add_node(scan_files)
workflow.add_node(describe_vulnerabilities)
workflow.add_node(recommend_solutions)

workflow.add_edge(START, "scan_files")
workflow.add_conditional_edges(source="scan_files", path=analysis_needed, path_map={'totally-safe':END, 'totally-not-safe':"describe_vulnerabilities"})
workflow.add_edge("describe_vulnerabilities", "recommend_solutions")
workflow.add_edge("recommend_solutions", END)
sast_agent = workflow.compile()