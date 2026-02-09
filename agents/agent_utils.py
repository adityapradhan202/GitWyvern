from typing import List
import os
import re
import ast

class AgentUtils:
    @staticmethod
    def create_chunks(path:str, chunk_size=500) -> List[str]:
        """Creates chunks text"""

        with open(path, "r", encoding="utf-8") as file:
            documentation = file.read()
        chunks = []
        for i in range(0, len(documentation), chunk_size):
            chunk = documentation[i : i+chunk_size]
            chunks.append(chunk)
        return chunks
    
    @staticmethod
    def readme_exists(path:str='./workdir/README.md') -> bool:
        """Checks if readme file exists or not"""

        if os.path.exists(path):
            return True
        return False
    
    # function to get the list of code files
    @staticmethod
    def code_files(path:str='./workdir'):
        """Retruns a list of code files"""
        code_files = []
        def collect_code_files(path:str=path) -> List[str]:
            print("-> Collectiong code files")
            dirs = os.listdir(path)
            for dir in dirs:
                if dir == ".git":
                    continue

                complete_path = os.path.join(path, dir)
                if os.path.isfile(complete_path):
                    if dir.endswith(".py"):
                        code_files.append(complete_path)
                    else:
                        continue
                else:
                    collect_code_files(complete_path)
        # call the inner function
        collect_code_files()
        return code_files
    
    # function for extracting function names from the code files
    @staticmethod
    def extract_func_names(path:str) -> List[str]:
        """Extract and returns a list of strings containing a function names from the supported code files"""

        print("-> Fetching functions")
        with open(path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        funcs = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        return funcs    
    
    # function to create directory tree / project structure
    @staticmethod
    def project_structure(start_path):
        """Return project structure formatted with |_ style"""

        output = []
        ignore_dirs = [".git", "__pycache__", ".venv", "node_modules"]
        start_path = os.path.abspath(start_path)
        for root, dirs, files in os.walk(start_path):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            rel_path = os.path.relpath(root, start_path)
            level = 0 if rel_path == "." else rel_path.count(os.sep) + 1

            indent = "    " * level
            folder_name = os.path.basename(root)
            if rel_path == ".":
                folder_name = os.path.basename(start_path)

            output.append(f"{indent}{folder_name}/")
            for file in files:
                output.append(f"{indent}    |_ {file}")
        return "\n".join(output)

if __name__ == "__main__":
    # Test here
    chunks = AgentUtils.create_chunks(path='../workdir/README.md')
    print(f"Number of chunks: {len(chunks)}")
    x = AgentUtils.readme_exists(path='../workdir/README.md')
    print(x)



