import os
import subprocess
import json
from datetime import datetime

class GeneralUtils:
    
    @staticmethod
    def initialize_workdir():
        """Initializes workdir"""
        if os.path.exists('./workdir'):
            print("reseting workdir")
            subprocess.run(["reset_workdir.bat"], shell=True)
        else:
            os.mkdir('./workdir')

    # For linux shell script
    # @staticmethod
    # def initialize_workdir():
    #     """Initializes workdir"""
    #     if os.path.exists('./workdir'):
    #         print("reseting workdir")
    #         subprocess.run(["bash", "reset_workdir.sh"])
    #     else:
    #         os.mkdir('./workdir')

    @staticmethod
    def datetime_stamp() -> str:
        """Returns string containing current date and time for the filename"""

        return str(datetime.now()).replace(" ", "_").replace(":", "-")

    @staticmethod
    def app_log(datetime_stamp:str, log_type:str, giturl:str, path='./app_logs/logs.json'):
        """Logs information for maintaining application history. It will log all the activities of gitwyvern GUI and CLI."""

        if not os.path.exists(path):
            print(f"Path {path} doesnt exist!")
            return
        
        new_log_data = {"type":log_type, "Git-URL":giturl}
        
        with open(path, "r") as file:
            loaded_log = json.load(file)
        loaded_log[datetime_stamp] = new_log_data
        with open(path, "w") as file:
            json.dump(loaded_log, fp=file, indent=4)
        print(f"-> Updated {path}")

        
    @staticmethod
    def clear_app_logs(path='./app_logs/logs.json'):
        """Clears application log."""

        if not os.path.exists(path):
            print(f"Path {path} doenst exist!")
            return
        
        with open(path, "w") as file:
            json.dump({}, fp=file)
        print("-> Cleared the application logs.")






