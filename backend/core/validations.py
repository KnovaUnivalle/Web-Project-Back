import hashlib
import secrets
import jwt
from backend.settings import SIMPLE_JWT
from django.contrib.auth import get_user_model
from rest_framework.response import Response

UserModel = get_user_model()


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


def custom_validation(data):
    email = data['email'].strip()
    password = data['password'].strip()
    ##
    if not email or UserModel.objects.filter(email=email).exists():
        Response('choose another email')
    ##
    if not password or len(password) < 8:
       Response('choose another password, min 8 characters')
    return data


def validate_email(data):
    email = data['email'].strip()
    if not email:
       Response('an email is needed')
    return True

def validate_password(data):
    password = data['password'].strip()
    if not password:
       Response('a password is needed')
    return True

def decode_token(token):
    return jwt.decode(token, SIMPLE_JWT['SIGNING_KEY'], algorithms=[
                SIMPLE_JWT['ALGORITHM']])

