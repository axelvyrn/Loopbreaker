import os
import json
from config import PROFILE_DIR
from pathlib import Path
from utils.encryption import encrypt_data, decrypt_data
from PyQt6.QtWidgets import QInputDialog, QMessageBox
from PyQt6.QtCore import Qt

def get_profile_path(username):
    return PROFILE_DIR / f"{username.lower()}.enc"

def save_profile(profile: dict):
    """Encrypt and save profile to disk."""
    raw_json = json.dumps(profile)
    encrypted = encrypt_data(raw_json)
    profile_path = get_profile_path(profile["username"])
    with open(profile_path, "wb") as f:
        f.write(encrypted)

def load_profile(username):
    with open(PROFILE_DIR / f"{username}.enc", "rb") as f:
        encrypted = f.read()
    decrypted = decrypt_data(encrypted, MASTER_KEY)
    return json.loads(decrypted)

def load_profile_menu():
    """Load or create/delete a profile using GUI."""
    files = [f.stem for f in PROFILE_DIR.glob("*.enc")]

    while True:
        options = files + ["➕ Create New Profile", "🗑️ Delete Profile"]
        item, ok = QInputDialog.getItem(None, "Loopbreaker ID", "Select your ID:", options, editable=False)

        if not ok:
            QMessageBox.warning(None, "Profile Required", "A profile is required to continue.")
            os.close()

        if item == "➕ Create New Profile":
            return create_new_profile()

        elif item == "🗑️ Delete Profile":
            if not files:
                QMessageBox.information(None, "No Profiles", "There are no profiles to delete.")
                continue
            profile_to_delete, ok = QInputDialog.getItem(None, "Delete Profile", "Choose a profile to delete:", files, editable=False)
            if ok:
                delete_profile(profile_to_delete)
                files.remove(profile_to_delete)
            continue  # Loop back to show updated list

        elif item in files:
            return load_profile(item)

def create_new_profile():
    """Create a new profile using GUI input."""
    while True:
        username, ok = QInputDialog.getText(None, "Create New Profile", "Enter new profile name:")
        if not ok:
            QMessageBox.warning(None, "Profile Required", "A profile is required to continue.")
            sys.exit(0)
        username = username.strip()
        if username:
            break  # Valid name entered
        
    path = PROFILE_DIR / f"{username}.enc"
    if path.exists():
        QMessageBox.warning(None, "Profile Exists", f"The profile '{username}' already exists.")
        return create_new_profile()
        
    profile = {
        "username": username,
        "games_played": 0,
        "highest_score": 0,
        "longest_streak": 0,
        "avg_reaction_time": None
    }
    save_profile(profile)
    return profile

def delete_profile(username):
    """Delete an encrypted profile file by name."""
    path = get_profile_path(username)
    if path.exists():
        path.unlink()
        QMessageBox.information(None, "Deleted", f"Profile '{username}' has been deleted.")
    else:
        QMessageBox.warning(None, "Not Found", f"Profile '{username}' does not exist.")


        
def update_stats(profile: dict, new_score: int, reaction_time: float, streak: int = 0):
    profile["games_played"] += 1
    profile["highest_score"] = max(profile["highest_score"], new_score)

    # Update longest streak
    if streak > profile.get("longest_streak", 0):
        profile["longest_streak"] = streak

    # Update average reaction time
    if profile["avg_reaction_time"] is None:
        profile["avg_reaction_time"] = reaction_time
    else:
        total_time = profile["avg_reaction_time"] * (profile["games_played"] - 1)
        profile["avg_reaction_time"] = (total_time + reaction_time) / profile["games_played"]

    save_profile(profile)

