import os
import shutil
from config import PROFILE_DIR, DATA_DIR

def delete_directory_contents(path):
    """Deletes all files in the given directory."""
    if path.exists() and path.is_dir():
        for file in path.glob("*"):
            try:
                if file.is_file():
                    file.unlink()
                elif file.is_dir():
                    shutil.rmtree(file)
            except Exception as e:
                print(f"❌ Error deleting {file}: {e}")

def reset_game():
    print("🧹 Resetting Loopbreaker...")
    
    delete_directory_contents(PROFILE_DIR)
    print("✅ All saved Loopbreaker IDs deleted.")

    delete_directory_contents(DATA_DIR)
    print("✅ All logs deleted.")

    print("🆕 Loopbreaker is now clean. Launch the game to create a new ID.")

if __name__ == "__main__":
    reset_game()
