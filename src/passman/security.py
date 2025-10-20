import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import click
from config import SQL_INSERT_CONFIG

def generate_salt():
    salt = os.urandom(16)
    return salt




