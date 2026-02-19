@echo off
echo Starting Wyvern...

echo.
echo Spinning the Ollama's server.
echo Disclaimer: Make sure Ollama and Nvidia's CUDA toolkit has been properly setup. Otherwise it wont work.
echo.

ollama ls

echo.
echo.
echo You can see the list of Ollama models you have on your device
echo The app will crash if you dont have Ollama's qwen2.5:3b, nomic-embed-text:v1.5 and qwen2.5-coder:3b

SET VENV_DIR=venv
IF EXIST %VENV_DIR% (
    echo.
    echo Virtual environment exists. Activating it!
    call venv\Scripts\activate
) ELSE (
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    echo Successfully installed the required dependencies
)

echo.
echo Reseting vector database. Cleaning the old junk files!
python reset_vecdb.py

echo.
echo Running ui.py
streamlit run ui.py
pause