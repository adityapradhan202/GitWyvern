# In this script necessary imports are made for LLM
# Seperate imports are given for local device and docker linux environment

from langchain_ollama import ChatOllama

# These are for windows
# Use these if you are running it without docker
model = ChatOllama(model='qwen2.5:3b', temperature=0.8)
code_model = ChatOllama(model='qwen2.5-coder:3b', temperature=0.8)

# Incase for docker use this one
# And comment the model definition given above (or VISE VERSA)

# model = ChatOllama(model='qwen2.5:3b', temperature=0.8, base_url="http://host.docker.internal:11434")
# code_model = ChatOllama(model='qwen2.5-coder:3b', temperature=0.8, base_url="http://host.docker.internal:11434")