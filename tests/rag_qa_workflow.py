from rag_pipeline import qa_rag

query = input("Enter a query: ")
res = qa_rag.invoke({'query':query})
print(res['response'])