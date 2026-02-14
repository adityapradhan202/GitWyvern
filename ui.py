import streamlit as st
from utils import GeneralUtils
from utils import GitUtils
import time

# importing agents
from agents import summarizer
from agents import AgentUtils
from agents import analyzer

# Session state variables
if "readme_summary" not in st.session_state:
    st.session_state.readme_summary = None
if "file_analysis" not in st.session_state:
    st.session_state.file_analysis = None

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
        with st.spinner("Wyvern is analyzing the files...", show_time=True):
            py_files = AgentUtils.code_files()
            analyzer_output = analyzer.invoke({"files_paths":py_files})
            file_analysis = ""
            for ind, key in enumerate(analyzer_output["output"], start=1):
                file_analysis += (f"📁 " + key + "\n")
                file_analysis += (analyzer_output["output"][key] + "\n\n")
            st.session_state.file_analysis = file_analysis

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

test_btn = st.button("test-button")
if test_btn:
    st.write("Pressed")

# # form
# if form_btn:
#     # if url is not none
#     if git_url is not None:
#         with st.spinner("Wyvern is getting the repo for you..."):
#             time.sleep(2.5)
#             GeneralUtils.initialize_workdir()
#             git_url = git_url.strip()
            
#             res = GitUtils.clone_repo(git_url=git_url)
#             # Once repo is cloned
#             if res:
#                 # Summarize readme
#                 with st.spinner(text="Wyvern is summarizing the readme..."):
#                     time.sleep(2)
#                     summarizer_state = summarizer.invoke({})
#                     # if readme exists
#                     if summarizer_state["readme_exists"] and len(summarizer_state["readme_summary"]) > 400:
#                         readme_summarized = summarizer_state["readme_summary"]
#                         st.header("Project-Summary", text_alignment="center")
#                         with st.container(border=True):
#                             st.write(readme_summarized)
#                     else:
#                         st.caption("-> Oops either this repository doesn't contain a README file or the readme file is very small 😅 Proceeding further!")
                
#                 # Get project structure
#                 p_structure = AgentUtils.project_structure(start_path='workdir')
#                 st.header("Complete Project-structure", text_alignment="center")
#                 with st.container(border=True):
#                     st.text(p_structure)


#                 # Analyzer output here
#                 st.header("Code file analysis", text_alignment="center")
#                 file_paths = AgentUtils.code_files()
#                 output = analyzer.invoke({"files_paths":file_paths})
#                 func_analysis = ""
#                 for ind, key in enumerate(output["output"], start=1):
#                     func_analysis += (f"➡️ " + key + "\n")
#                     func_analysis += (output["output"][key] + "\n\n")
#                 with st.container(border=True):
#                     st.text(func_analysis)

                

#             else:
#                 st.warning("Some issue occured! Make sure the url is correct or check your internet connection!")

#     # If user doesn't enters GIT url    
#     else:
#         st.warning("Enter Github url")


