import hashlib
import secrets


def encrypt_password(password: str) -> str:
    """Encrypts a password using a salt and SHA256."""
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256(
        (password + salt).encode("utf-8")).hexdigest()
    return salt + password_hash


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies if a password matches the given hashed password."""
    salt = hashed_password[:32]
    password_hash = hashlib.sha256(
        (password + salt).encode("utf-8")).hexdigest()
    return password_hash == hashed_password[32:]
