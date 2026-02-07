import os
import subprocess

class GeneralUtils:
    # @staticmethod
    # def recursive_remover(path):
    #     """recursively deletes files and folders"""
    #     dirs = os.listdir(path)

    #     for dir in dirs:
    #         path_joined = os.path.join(path, dir)
    #         print(path_joined)
    #         if dir == ".git":
    #             continue
    #         if os.path.isfile(path_joined):
    #             print(f"-> removing file - {path_joined}")
    #             os.remove(path_joined)
    #         else:
    #             GeneralUtils.recursive_remover(path_joined)

    #     empty_dirs = dirs.remove(".git")
    #     for empty_dir in empty_dirs:
    #         os.rmdir(empty_dir)


    @staticmethod
    def initialize_workdir():
        """Initializes workdir"""
        if os.path.exists('./workdir'):
            print("reseting workdir")
            subprocess.run(["reset_workdir_bat.bat"], shell=True)
        else:
            os.mkdir('./workdir')