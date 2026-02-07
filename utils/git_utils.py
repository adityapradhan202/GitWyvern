from git import Repo

class GitUtils:
    @staticmethod
    def clone_repo(git_url:str) -> bool:
        """clones github repository to workdir"""
        try:
            print("clonning...")
            Repo.clone_from(url=git_url, to_path='./workdir')
            print("Succesfully cloned repo")
        except:
            return False
        return True
