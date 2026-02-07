import streamlit as st
from utils import GeneralUtils
from utils import GitUtils

st.header("GitWyvern", text_alignment="center")
c1, c2, c3 = st.columns(3)
with c2:
    st.image(image='static/wyvern_transparent_logo.png')

with st.form("form"):
    git_url = st.text_input(label="Enter git url:")
    form_btn = st.form_submit_button(label="Analyse", type="primary")

if form_btn:
    GeneralUtils.initialize_workdir()
    git_url = git_url.strip()
    res = GitUtils.clone_repo(git_url=git_url)
    if res:
        st.write("Successfully cloned repo")