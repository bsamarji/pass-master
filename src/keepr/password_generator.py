import secrets
import string

from keepr.internal_config import (
    PASSWORD_GENERATOR_LENGTH,
    PASSWORD_GENERATOR_SPECIAL_CHARS,
)


def password_generator(without_special_chars=False):
    """
    Password generator function.
    By default, it generates a random password with special characters.
    Returns:
        password: cryptographically secure randomly generated password
    """
    if without_special_chars:
        alphabet = string.ascii_letters + string.digits
    else:
        alphabet = string.ascii_letters + string.digits + PASSWORD_GENERATOR_SPECIAL_CHARS
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(PASSWORD_GENERATOR_LENGTH))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c in password for c in PASSWORD_GENERATOR_SPECIAL_CHARS)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password
