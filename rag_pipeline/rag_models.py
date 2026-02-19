from langchain_ollama import ChatOllama, OllamaEmbeddings

# Model calls for native windows (Not for docker container)
code_model = ChatOllama(model='qwen2.5-coder:3b', temperature=0.8)
# Using nomic-embed-text:v1.5 because it outperformed jina-embeddings-v2-base
embed_model = OllamaEmbeddings(
    model='nomic-embed-text:v1.5'
    # model='unclemusclez/jina-embeddings-v2-base-code:latest'
)

# Model call for docker container linux os will be written here
# (LATER)