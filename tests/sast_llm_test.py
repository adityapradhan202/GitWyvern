from agents import sast_agent
from agents import AgentUtils

code_files = AgentUtils.code_files()
res = sast_agent.invoke(
    {"file_paths":code_files}
)

if res["overally_safe"]:
    print("Overally safe!")
else:
    print("-> Not overally safe")
    print("\nTotal vulnerabilities caught:\n")
    print(res["vul_cnt"])
    print("\nSolutions to vulnerabilities\n")
    print(res["vuls_sols"])