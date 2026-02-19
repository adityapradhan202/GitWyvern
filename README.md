<p align="center">
<img src="./static/wyvern_transparent_logo.png" width="250">
</p>


<p align="center">
<!-- <img alt="Static Badge" src="https://img.shields.io/badge/CLI-black?style=for-the-badge"> -->
<img alt="Static Badge" src="https://img.shields.io/badge/code--analysis-black?style=for-the-badge">
<img alt="Static Badge" src="https://img.shields.io/badge/cli-darkred?style=for-the-badge">
<img alt="Static Badge" src="https://img.shields.io/badge/RUns--locally-black?style=for-the-badge">
<img alt="Static Badge" src="https://img.shields.io/badge/Release--v0.0.1-darkred?style=for-the-badge">
<img alt="Static Badge" src="https://img.shields.io/badge/security-black?style=for-the-badge">
<img alt="Static Badge" src="https://img.shields.io/badge/CHAT-darkred?style=for-the-badge">
</p>

<h1 align="center">GitWyvern: Scout Python Repos with AI</h1>
<p align="center">GitWyvern is an AI-powered repository intelligence system for Python-based repositories.
It is a beautifully orchestrated application that uses local LLMs to summarize README files, analyze Python scripts, perform hybrid security scans (SAST + LLM), and create a repo-aware chat system using a RAG pipeline.</p>

<p align="center">
<b><a href='#requirements'>Requirements</a> • <a href='#setup'>Setup</a> • <a href='#cli-commands'>CLI-commands</a></b>
</p>

> ⚠️ Official v0.0.1 is yet to be released after some tests.

### Features:
* Smart file-purpose inference from names & signatures (accurate most of the time) for quick codebase overview.
* Hybrid SAST + LLM security scan: detects issues, explains context, suggests fixes.
* RAG-based chat interface with repo knowledge.

### Requirements:
1. Git.
2. Ollama `(Models - qwen2.5:3b, qwen2.5-coder:3b, nomic-embed-text:v1.5)`.
3. Nvidia's Cuda Toolkit. `(Was used for development- Cuda v11.8, CUDNN v8.9, Python v3.12.0)`.
4. Minimum 16GB RAM (8GB RAM available/free) and 4GB VRAM for smooth functioning.

### Setup:
<img src="https://cdn-icons-png.flaticon.com/128/888/888882.png" width="30">

#### Setup for Windows Operating System:
1. First clone this repository.
2. You must have python installed. Then open file explorer and go to the root level of the project folder and double click on `run.bat`. **Double click this microsoft windows batch file to run GitWyvern GUI application**. If a virtual environment doesn't exist, it creates on and installs all the required dependcies inside the virtual environment. The next time you run this batch file, it will activate the existing venv, and runs the app at `http://localhost:8501`. It will open the app in your default browser.
3. To run the cli, **Double click on** `cli.bat`.

<img src="https://cdn-icons-png.flaticon.com/128/15466/15466088.png" width="40">

#### Setup for docker:
> ⚠️ In progress. Yet to be added once verified!

### CLI-commands
1. To activate and use the CLI go to the root level of the cloned repository and **double click** on `cli.bat` file.
2. You can use `python gitwyvern.py --help` to get the list of commands. Use `python gitwyvern.py [command] --help` to see the command line arguments for the specific commands.
3. Here's the list of commands you can use:
    * `python gitwyvern.py analyze [github_url]` - Analyzes code files. 
    * `python gitwyvern.py security [github_url]` - Performs a hybrid security scan (SAST + LLM)
    * `python gitwyvern.py chat-wyvern [github_url]` - Creates and starts repo-aware chat system in the CLI itself.
    * `python gitwyvern.py clear-cli-logs [github_url]` - To clear the CLI logs.