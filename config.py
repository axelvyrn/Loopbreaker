# config.py

from pathlib import Path

# === Theme === #
VINTAGE_THEME = {
    "bg_color": "#F0DC82",     # Vintage black
    "text_color": "#000000",   # CRT green
    "font": "Courier New",
    "font_size": 14
}

# === File Paths === #
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
SOUNDS_DIR = ASSETS_DIR / "sounds"

PROFILE_FILE = DATA_DIR / "stats.enc"

# === Game Settings === #
DEFAULT_ROUNDS = 5
REACTION_TIMEOUT = 10  # in seconds
