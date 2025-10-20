import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import click
from config import SQL_INSERT_CONFIG
import getpass
import db

def initialise_security():
    master_password = set_new_master_password()
    salt = generate_salt()
    db.insert_config("salt", salt)
    key = derive_key(password=master_password, salt=salt)
    kcv = encode_kcv(key)
    db.insert_config("key_check_value", kcv)


def get_master_password(prompt: str = "Enter Master Password: ") -> str:
    """Securely prompts the user for the master password."""
    # Using getpass for hidden input
    password = getpass.getpass(prompt=prompt)
    return password


def set_new_master_password() -> str:
    """Prompts user to set and confirm a new master password."""

    click.echo("--- Master Password Setup ---")

    while True:
        p1 = get_master_password(prompt="Set new Master Password: ")

        if len(p1) < 8:
            click.echo(
                click.style(
                    "Error: Password must be at least 8 characters long.", fg="red"
                )
            )
            continue

        p2 = get_master_password(prompt="Confirm Master Password: ")

        if p1 == p2:
            click.echo(click.style("Master password set successfully.", fg="green"))
            return p1
        else:
            click.echo(
                click.style("Error: Passwords do not match. Try again.", fg="red")
            )


def generate_salt():
    """
    Generate a random salt for encryption.
    """
    salt = os.urandom(16)
    return salt


def derive_key(salt, password):
    """
    Derive the encryption key from the master password and a key derivation function.
    """
    password_bytes = password.encode("utf-8")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1_200_000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    return key


def encode_kcv(key):
    """
    Encode the key check value.
    """
    f = Fernet(key)
    kcv = f.encrypt(b"CHECK_OK")
    return kcv


def decode_kcv(kcv, key):
    """
    Decode the key check value.
    Run an equality operation to compare the decoded kcv to the true kcv.
    """
    f = Fernet(key)
    check = f.decrypt(kcv)
    if check == "CHECK_OK":
        return True
    else:
        return False
