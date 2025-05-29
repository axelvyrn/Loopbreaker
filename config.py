# config.py

from pathlib import Path

# === Directories ===
BASE_DIR = Path(__file__).resolve().parent
PROFILE_DIR = BASE_DIR / "profiles"
LOG_DIR = BASE_DIR / "logs"

# Ensure necessary directories exist
PROFILE_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# === Server Configuration ===
SERVER_HOST = "localhost"
SERVER_PORT = 8765

# === UI Themes ===
VINTAGE_THEME = {
    "bg_color": "#f5f5dc",        # Beige / parchment
    "text_color": "#2f2f2f",      # Dark text
    "button_color": "#a67c52",    # Muted brown
    "accent_color": "#5e503f",    # Deeper brown
    "font": "Courier New",
    "font_size": 14
}

# === Game Settings ===
INITIAL_SEQUENCE_LENGTH = 3
SEQUENCE_GROWTH_RATE = 1  # Increase after every correct round
REACTION_TIMEOUT = 5.0    # seconds per round

# === Multiplayer Constants ===
MAX_PLAYERS_PER_ROOM = 2
DEFAULT_ROOM_TIMEOUT = 30  # seconds
