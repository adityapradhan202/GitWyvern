import os
import subprocess

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

