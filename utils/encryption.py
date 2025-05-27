# utils/encryption.py

from cryptography.fernet import Fernet
import os

KEY_FILE = "data/.key"  # Do not share or expose this in public repos

def generate_key():
    """Generate and store a new encryption key."""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

def load_key():
    """Load encryption key from file or generate if missing."""
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()

fernet = Fernet(load_key())

def encrypt_data(data: str) -> bytes:
    return fernet.encrypt(data.encode())

def decrypt_data(token: bytes) -> str:
    return fernet.decrypt(token).decode()
