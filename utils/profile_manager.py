# utils/profile_manager.py

import os
import json
from config import PROFILE_FILE
from utils.encryption import encrypt_data, decrypt_data

DEFAULT_PROFILE = {
    "username": "Loopbreaker",
    "games_played": 0,
    "highest_score": 0,
    "longest_streak": 0,
    "avg_reaction_time": None
}

def save_profile(profile: dict):
    """Encrypt and save profile to disk."""
    raw_json = json.dumps(profile)
    encrypted = encrypt_data(raw_json)
    with open(PROFILE_FILE, "wb") as f:
        f.write(encrypted)

def load_profile():
    """Decrypt and load profile from disk. If not found, create a new one."""
    if not os.path.exists(PROFILE_FILE):
        save_profile(DEFAULT_PROFILE)
        return DEFAULT_PROFILE

    with open(PROFILE_FILE, "rb") as f:
        encrypted = f.read()

    try:
        raw = decrypt_data(encrypted)
        return json.loads(raw)
    except Exception as e:
        print("⚠️ Error loading profile:", e)
        return DEFAULT_PROFILE

def update_stats(profile, score, streak, reaction_times):
    """Update game statistics."""
    profile["games_played"] += 1
    profile["highest_score"] = max(profile["highest_score"], score)
    profile["longest_streak"] = max(profile["longest_streak"], streak)

    avg_reaction = sum(reaction_times) / len(reaction_times)
    if profile["avg_reaction_time"] is None:
        profile["avg_reaction_time"] = avg_reaction
    else:
        # weighted avg
        profile["avg_reaction_time"] = round(
            (profile["avg_reaction_time"] + avg_reaction) / 2, 3
        )

    save_profile(profile)
