# CLI for gitWyvern
import os
import typer
from utils import GitUtils
from agents import AgentUtils
from agents import sast_agent, analyzer
from utils import GeneralUtils

from wyvern_ascii import wyvern_console_ascii
from datetime import datetime

def cli_log_fname() -> str:
    """Returns string containing current date and time for the filename"""
    return str(datetime.now()).replace(" ", "_").replace(":", "-")

app = typer.Typer()

@app.command()
def clear_cli_logs():
    """Clears the CLI logs directory"""

    dirs = os.listdir('./cli_logs/')
    confirm = input("This will clear all the CLI logs. Enter Y to proceed, otherwise enter N: ")
    if confirm.lower() == "y":
        for dir in dirs:
            # skipping dummy.txt so that this folder can be commited to git
            if dir == "dummy.txt":
                continue
            comp_path = os.path.join("./cli_logs", dir)
            os.remove(comp_path)
        print("Successfully cleared the CLI logs")
    elif confirm.lower() == "n":
        print("CLI logs were not deleted. Processed cancelled!")
    else:
        print("Invalid input. Enter Y or N!")

@app.command()
def analyze(giturl:str):
    fname = cli_log_fname()
    path = os.path.join("./cli_logs", fname + "-a" + ".txt")

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
        report += f"Git URL: {giturl}"
        with open(path, "w", encoding="utf-8") as file:
            file.write(report)

        wyvern_console_ascii()

        print("\n\n---> File analysis report\n\n"+report)
        print(f"Succesfully logged the file analysis report at {path}")
    # If the repo is not clonned succesfully
    else:
        print("Couldn't clone the repository! Check your internet connection and make sure the URL is correct!")


@app.command()
def security(giturl:str) -> None:
    fname = cli_log_fname()
    path = os.path.join("./cli_logs", fname + "-s" + ".txt")

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
            print("\n\nWyvern didn't find any vulnerabilities. The python scripts are safe to use.")
            with open(path, "w", encoding="utf-8") as file:
                file.write("Wyvern didn't find any vulnerabilities. The python scripts are safe to use.")
            print(f"Saving this information at {path}")
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
            report += f"Git URL: {giturl}"
            with open(path, "w", encoding="utf-8") as file:
                file.write(report)

            wyvern_console_ascii()

            print("\n\nWyvern found some vulnerabilities")
            print("\n---> Security scan report\n\n"+report)
            print(f"Succesfully saved the security report at {path}")
    # If repo is not clonned
    else:
        print("Couldn't clone the repository! Check your internet connection and make sure the URL is correct!")


if __name__ == "__main__":
    app()