from .rag_models import embed_model
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PythonLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_chroma import Chroma
import shutil, os

class RagBuilder:
    def __init__(self, project_path:str='./workdir', persistebt_db:str='./chroma_db', embed_function:OllamaEmbeddings=embed_model, chunk_size=500, chunk_overlap=50):
        """Initializes the instance of RagBuilder class"""

        self.project_path = project_path
        self.persistent_db = persistebt_db
        self.embed_function = embed_function
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def create_vector_store(self) -> None:
        """Creates vector database"""

        # subprocess.run('reset_vecdb.bat', shell=True)
        if os.path.exists(self.persistent_db):
            db = Chroma(persist_directory=self.persistent_db, embedding_function=self.embed_function)
            db.delete_collection()
            print("-> Deleted the old collection from vector database")

        loader = DirectoryLoader(path=self.project_path, glob='**/*.py', loader_cls=PythonLoader)
        documents = loader.load()
        # python_splitter = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON, chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        python_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        code_chunks = python_splitter.split_documents(documents)

        print("-> Initializing vector database creation")
        db = Chroma(persist_directory=self.persistent_db, embedding_function=self.embed_function)
        db.add_documents(documents=code_chunks)
        print("-> Chunks have been added to vector store!")

    def retrieve_docs(self, query) -> str:
        """Retrieves chunks with similar semantic meaning from the vector database"""
        db = Chroma(persist_directory=self.persistent_db, embedding_function=self.embed_function)
        context = ""
        fetched_content = db.similarity_search(query=query, k=3)
        for code in fetched_content:
            context += (code.page_content+"\n\n")
        return context