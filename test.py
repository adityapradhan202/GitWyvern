# This is a temp file, this will be deleted
from agents import AgentUtils
from agents import analyzer

code_files = AgentUtils.code_files() # gives path of code files
res = analyzer.invoke({"files_paths":code_files})
for key in res['output']:
    print(f"{key}\n{res['output'][key]}")
    print()
