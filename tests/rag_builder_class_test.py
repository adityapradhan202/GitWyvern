from rag_pipeline import RagBuilder

builder = RagBuilder()
builder.create_vector_store()
user_query = input("Enter a query: ")
res = builder.retrieve_docs(query=user_query)
print(res)