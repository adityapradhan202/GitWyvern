# CLI for gitWyvern

import os
import typer
from utils import GitUtils
from agents import AgentUtils
from agents import sast_agent, analyzer
from utils import GeneralUtils

app = typer.Typer()

@app.command()
def analyze(giturl:str, fname:str):
    """"Docstring here"""

    path = os.path.join("./cli_save", fname + ".txt")
    if os.path.exists(path):
        print("This file already exists! Choose another name!")
        return
    
    GeneralUtils.initialize_workdir()
    ack = GitUtils.clone_repo(giturl)

    if ack:
        py_files = AgentUtils.code_files()
        try:
            response = analyzer.invoke({'files_paths':py_files})
        except Exception as e:
            print(f"Exception occured: {e}")
            return
        
        report = ""
        output = response["output"]
        for file in output:
            report += f"📁 {file}\n"
            report += f"📋 {output[file]}\n\n"
        with open(path, "w", encoding="utf-8") as file:
            file.write(report)
        print(f"Succesfully saved the file analysis report at {path}")
    # If the repo is not clonned succesfully
    else:
        print("Couldn't clone the repository! Check your internet connection and make sure the URL is correct!")


@app.command()
def security(giturl:str, fname:str) -> None:
    """Uses the sast_llm agent and saves the output to a text file.
    Args:
        giturl(str): URL of the github repository
        fname(str): Name of the file
    """

    path = os.path.join("./cli_save", fname + ".txt")
    if os.path.exists(path):
        print("This file already exists! Choose another name!")
        return

    GeneralUtils.initialize_workdir()
    ack = GitUtils.clone_repo(giturl)

    if ack:
        py_files = AgentUtils.code_files()
        try:
            response = sast_agent.invoke({'file_paths':py_files})
        except Exception as e:
            print(f"Exception occured: {e}")
            return
        if response["overally_safe"] == True:
            print("Wyvern didn't catch any vulnerabilities. The python scripts are safe to use.")
        else:
            report = ""
            vul_cnt = response["vul_cnt"]

            report += (f"""
By Severity:
    1. Undefined: {vul_cnt["severity"]["undefined"]}
    2. Low: {vul_cnt["severity"]["low"]}
    3. Mid: {vul_cnt["severity"]["mid"]}
    4. High {vul_cnt["severity"]["high"]}

By confidence:
    1. Undefined: {vul_cnt["confidence"]["undefined"]}
    2. Low: {vul_cnt["confidence"]["low"]}
    3. Mid: {vul_cnt["confidence"]["mid"]}
    4. High {vul_cnt["confidence"]["high"]}\n\n\n
""")

            report += "------- Vulnerabilities + Recommendations --------\n\n"
            vuls_sols = response["vuls_sols"]
            for file in vuls_sols:
                report += f"❌ {file}\n"
                report += f"📋 {vuls_sols[file][0]}\n"
                report += f"✅ {vuls_sols[file][1]}\n\n"

            with open(path, "w", encoding="utf-8") as file:
                file.write(report)
            print(f"Succesfully saved the security report at {path}")
    # If repo is not clonned
    else:
        print("Couldn't clone the repository! Check your internet connection and make sure the URL is correct!")


if __name__ == "__main__":
    app()