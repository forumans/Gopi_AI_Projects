import shutil
import os

def clear_chroma_db(persist_directory="chroma_db"):
    """Clear the ChromaDB database by deleting the persist directory"""
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
        print(f"ChromaDB directory '{persist_directory}' has been deleted.")
    else:
        print(f"ChromaDB directory '{persist_directory}' does not exist.")

if __name__ == "__main__":
    clear_chroma_db()
