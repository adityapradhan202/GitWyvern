import shutil
import os

# When is this file run?
# When the app has hard started, no db is loaded into memory, so this script can easily clean the old mess without encountering windows permission errors
# Script to reset the vector database
# This script is run everytime you start the application using run.bat
def reset_vecdb():
    """Resets the vector database. Removes the chroma_db directory and then creates an empty directory of the same name."""
    
    if os.path.exists("./chroma_db"):
        shutil.rmtree(path='./chroma_db')
    os.mkdir("./chroma_db")
    
if __name__ == "__main__":
    reset_vecdb()
    
