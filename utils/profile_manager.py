import os
import json
from config import PROFILE_DIR
from pathlib import Path
from utils.encryption import encrypt_data, decrypt_data

def get_profile_path(username):
    return PROFILE_DIR / f"{username.lower()}.enc"

def save_profile(profile: dict):
    """Encrypt and save profile to disk."""
    raw_json = json.dumps(profile)
    encrypted = encrypt_data(raw_json)
    profile_path = get_profile_path(profile["username"])
    with open(profile_path, "wb") as f:
        f.write(encrypted)

def load_profile_menu():
    """Load existing profile or create new one."""
    files = [f.stem for f in PROFILE_DIR.glob("*.enc")]
    print("\n🎮 LOOPBREAKER ID SYSTEM")
    if files:
        print("Existing IDs:")
        for i, f in enumerate(files):
            print(f"{i + 1}. {f}")
        print("0. Create new ID")
        choice = input("Select an ID (by number) or create new: ").strip()
        if choice == "0":
            return create_new_profile()
        elif choice.isdigit() and 1 <= int(choice) <= len(files):
            return load_profile(files[int(choice) - 1])
    
    # Fallback
    return create_new_profile()

def create_new_profile():
    username = input("🆕 Enter a new Loopbreaker ID: ").strip()
    profile = {
        "username": username,
        "games_played": 0,
        "highest_score": 0,
        "longest_streak": 0,
        "avg_reaction_time": None
    }
    save_profile(profile)
    return profile

def load_profile(username):
    profile_path = get_profile_path(username)
    if not profile_path.exists():
        print(f"❌ Profile '{username}' does not exist.")
        return create_new_profile()

    with open(profile_path, "rb") as f:
        encrypted = f.read()
    try:
        raw = decrypt_data(encrypted)
        return json.loads(raw)
    except Exception as e:
        print("⚠️ Error loading profile:", e)
        return create_new_profile()

def delete_profile(username):
    profile_path = get_profile_path(username)
    if profile_path.exists():
        os.remove(profile_path)
        print(f"🗑️ Profile '{username}' deleted.")
    else:
        print(f"❌ No such profile found.")

        
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

