import streamlit as st
from utils import GeneralUtils
from utils import GitUtils
import time

# importing agents
from agents import summarizer
from agents import AgentUtils
from agents import analyzer

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

# form
if form_btn:
    # if url is not none
    if git_url is not None:
        with st.spinner("Wyvern is getting the repo for you..."):
            time.sleep(2.5)
            GeneralUtils.initialize_workdir()
            git_url = git_url.strip()
            
            res = GitUtils.clone_repo(git_url=git_url)
            # Once repo is cloned
            if res:
                # Summarize readme
                with st.spinner(text="Wyvern is summarizing the readme..."):
                    time.sleep(2)
                    summarizer_state = summarizer.invoke({})
                    # if readme exists
                    if summarizer_state["readme_exists"] and len(summarizer_state["readme_summary"]) > 400:
                        readme_summarized = summarizer_state["readme_summary"]
                        st.header("Project-Summary", text_alignment="center")
                        with st.container(border=True):
                            st.write(readme_summarized)
                    else:
                        st.caption("-> Oops either this repository doesn't contain a README file or the readme file is very small 😅 Proceeding further!")
                
                # Get project structure
                p_structure = AgentUtils.project_structure(start_path='workdir')
                st.header("Complete Project-structure", text_alignment="center")
                c4, c5, c6 = st.columns(3)
                with c5:
                    st.text(p_structure)


                # Analyzer output here
                st.header("Code file analysis", text_alignment="center")
                file_paths = AgentUtils.code_files()
                output = analyzer.invoke({"files_paths":file_paths})
                func_analysis = ""
                for ind, key in enumerate(output["output"], start=1):
                    func_analysis += (f"➡️ " + key + "\n")
                    func_analysis += (output["output"][key] + "\n\n")
                with st.container(border=True):
                    st.text(func_analysis)

                

            else:
                st.warning("Some issue occured! Make sure the url is correct or check your internet connection!")

    # If user doesn't enters GIT url    
    else:
        st.warning("Enter Github url")


