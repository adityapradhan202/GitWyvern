@echo off
echo Starting Wyvern...
call venv\Scripts\activate

echo Spinning up the Ollama local server
ollama ls

echo You can see the list of Ollama models you have on your device
echo The app will crash if you dont have Ollama's qwen2.5:3b and qwen2.5-coder:3b

echo --> Running ui.py
python -m streamlit run ui.py
