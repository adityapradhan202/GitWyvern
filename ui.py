import streamlit as st
from utils import GeneralUtils
from utils import GitUtils
import time
from rag_pipeline import RagBuilder
from rag_pipeline import qa_rag

# importing agents
from agents import summarizer
from agents import AgentUtils
from agents import analyzer
from agents import sast_agent

# Session state variables
if "readme_summary" not in st.session_state:
    st.session_state.readme_summary = None
if "file_analysis" not in st.session_state:
    st.session_state.file_analysis = None
# Session state variables for the sast agent
if "vuls_sols" not in st.session_state:
    st.session_state.vuls_sols = None
if "overally_safe" not in st.session_state:
    st.session_state.overally_safe = None
if "vul_cnt" not in st.session_state:
    st.session_state.vul_cnt = None
# Session state variable to confirm that the vector database has been created
if "vec_db_initialized" not in st.session_state:
    st.session_state.vec_db_initialized = None

# Instantiate and initialize the RagBuilder class
builder = RagBuilder()

st.header("GitWyvern", text_alignment="center")
c1, c2, c3 = st.columns(3)
with c2:
    st.image(image='static/wyvern_transparent_logo.png')

with st.sidebar:
    st.markdown('⚡ Made by -> [Aditya Pradhan](https://github.com/adityapradhan202)', text_alignment="center")
    st.markdown("#### :red[Options] ⚙️", text_alignment="center")
    btn = st.button(label="Get app history", use_container_width=True)

with st.form("form"):
    git_url = st.text_input(label="Enter githup url (HTTPS type only):", value=None, placeholder="For example: https://github.com/adityapradhan202/Rag-Badger.git")
    col1, col2, col3= st.columns(3)
    form_btn = col2.form_submit_button(label="Dracarys", type="primary", use_container_width=True)


if form_btn == True and git_url is None:
    st.warning("Enter GitHub URL!")
elif form_btn == True and git_url is not None:
    with st.spinner("Wyvern is getting repo for you..."):
        GeneralUtils.initialize_workdir()
        git_url = git_url.strip()
        repo = GitUtils.clone_repo(git_url=git_url)
    # if repo is successfully cloned
    if repo:

        # summarizer agent
        with st.spinner("Wyvern is summarizing readme...", show_time=True):
            summarizer_output = summarizer.invoke({})
            st.session_state.readme_summary = summarizer_output
        # analyzer agent
        py_files = AgentUtils.code_files()
        with st.spinner("Wyvern is analyzing the files...", show_time=True):
            analyzer_output = analyzer.invoke({"files_paths":py_files})
            file_analysis = ""
            for ind, key in enumerate(analyzer_output["output"], start=1):
                file_analysis += (f"📂 {key}\n")
                file_analysis += (f"📋 {analyzer_output["output"][key]}\n\n")
            st.session_state.file_analysis = file_analysis
        # sast_agent
        with st.spinner("Wyvern is searching for vulnerabilities"):
            sast_response = sast_agent.invoke({"file_paths":py_files})
            st.session_state.overally_safe = sast_response['overally_safe']
            if not st.session_state.overally_safe:
                st.session_state.vuls_sols = sast_response['vuls_sols']
                st.session_state.vul_cnt = sast_response['vul_cnt']

        # Rag builder
        with st.spinner("Wyvern is initializing vector database"):
            builder.create_vector_store()
            st.session_state.vec_db_initialized = True

    # if repo wasnt cloned
    else:
        st.warning("Some issue occured! Repo wasn't cloned! Make sure you are using a proper URL and you have a stable internet connection!")


if st.session_state.readme_summary:
    st.header("Summary", text_alignment="center")
    summarizer_res = st.session_state.readme_summary
    if summarizer_res["readme_exists"] and len(summarizer_res["readme_summary"]) > 400:
        st.caption("Here's a summary of the readme file!")
        with st.container(border=True):
            st.write(summarizer_res["readme_summary"])
    else:
        st.caption("-> Oops either this repository doesn't contain a README file or the readme file is very small 😅 Proceeding further!")

if st.session_state.file_analysis:
    st.header("File analysis", text_alignment="center")
    analyzer_res = st.session_state.file_analysis
    st.caption("This is a highly level analysis of the files containing functions. LLM is using the file names and function signatures to make an assumption that what the script might be about. (The assuption is correct in most of the cases)")
    with st.container(border=True):
        st.text(analyzer_res)

# sast agent output display
if st.session_state.overally_safe:
    st.header("Security Scan", text_alignment="center")
    with st.container(border=True):
        vul_col1, vul_col2 = st.columns(2)
        with vul_col1:
            with st.container(border=True, width="stretch"):
                st.markdown('### :red[By Severity]', text_alignment="center")
                st.markdown(f"""**Undefined:** 0, **Low:** 0, **Mid:** 0, **High:** 0""", text_alignment="center")
            
        with vul_col2:
            with st.container(border=True, width="stretch"):
                st.markdown('### :red[By Confidence]', text_alignment="center")
                st.markdown(f"""**Undefined:** 0, **Low:** 0, **Mid:** 0, **High:** 0""", text_alignment="center")
        st.markdown(":green[There are no vulnerabilities in the python scripts. You can use it safely!] ✅", text_alignment="center")
elif st.session_state.overally_safe == False:
    st.header("Security Scan", text_alignment="center")
    st.caption("Wyvern found some vulnerabilities...")
    # Bigger container
    with st.container(border=True, width="stretch"):
        vul_col1, vul_col2 = st.columns(2)
        with vul_col1:
            with st.container(border=True, width="stretch"):
                st.markdown('### :red[By Severity]', text_alignment="center")
                st.markdown(f"""**Undefined:** {st.session_state.vul_cnt["severity"]["undefined"]}, **Low:** {st.session_state.vul_cnt["severity"]["low"]}, **Mid:** {st.session_state.vul_cnt["severity"]["mid"]}, **High:** {st.session_state.vul_cnt["severity"]["high"]}""", text_alignment="center")
            
        with vul_col2:
            with st.container(border=True, width="stretch"):
                st.markdown('### :red[By Confidence]', text_alignment="center")
                st.markdown(f"""**Undefined:** {st.session_state.vul_cnt["confidence"]["undefined"]}, **Low:** {st.session_state.vul_cnt["confidence"]["low"]}, **Mid:** {st.session_state.vul_cnt["confidence"]["mid"]}, **High:** {st.session_state.vul_cnt["confidence"]["high"]}""", text_alignment="center")

        vul_sol_display = ""
        for file in st.session_state.vuls_sols:
            vul_sol_display += (f"❌ {file}\n")
            vul_sol_display += (f"📋 {st.session_state.vuls_sols[file][0]}\n")
            vul_sol_display += (f"✅ {st.session_state.vuls_sols[file][1]}\n\n")
        st.markdown("#### > Vulnerabilities + Recommendations <", text_alignment="center")
        st.text(vul_sol_display)

if st.session_state.vec_db_initialized:
    st.header('Chat-Wyvern', text_alignment="center")
    with st.form("chat-wyvern"):
        query = st.text_area(label="Enter your query:", value=None, placeholder='Avoid asking off topic questions!')
        chat_col1, chat_col2, chat_col3 = st.columns(3)
        with chat_col2:
            send_btn = st.form_submit_button(label="Send", width="stretch", type="primary")

    if send_btn == True and query is None:
        st.warning("Enter a query first!")
    elif send_btn == True and query is not None:
        with st.spinner("Wyvern is thinking..."):
            res = qa_rag.invoke({'query':query})
            with st.container(border=True):
                st.markdown(res['response'])

