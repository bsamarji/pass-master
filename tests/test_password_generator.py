import string

from keepr.internal_config import (
    PASSWORD_GENERATOR_LENGTH,
    PASSWORD_GENERATOR_SPECIAL_CHARS,
)
from keepr.password_generator import password_generator


def test_password_length():
    """Test that the generated password has the correct length."""
    password = password_generator()
    assert len(password) == PASSWORD_GENERATOR_LENGTH, (
        f"Password length should be {PASSWORD_GENERATOR_LENGTH}, but got {len(password)}"
    )


def test_password_contains_required_chars():
    """Test that the default generated password meets all complexity requirements."""
    password = password_generator()

    # 1. Check for Lowercase
    assert any(c.islower() for c in password), (
        "Password must contain at least one lowercase character."
    )

    # 2. Check for Uppercase
    assert any(c.isupper() for c in password), (
        "Password must contain at least one uppercase character."
    )

    # 3. Check for Special Characters (from config)
    special_chars_in_password = any(
        c in password for c in PASSWORD_GENERATOR_SPECIAL_CHARS
    )
    assert special_chars_in_password, (
        "Password must contain at least one special character."
    )

    # 4. Check for at least 3 Digits
    digit_count = sum(c.isdigit() for c in password)
    assert digit_count >= 3, (
        f"Password must contain at least 3 digits, but got {digit_count}."
    )


def test_password_without_special_chars():
    """Test the 'without_special_chars=True' flag."""
    password = password_generator(without_special_chars=True)

    # 1. Check for the absence of special characters
    special_char_set = set(PASSWORD_GENERATOR_SPECIAL_CHARS)
    password_char_set = set(password)

    # Check that the intersection of the password chars and special chars is empty
    assert not (password_char_set & special_char_set), (
        "Password generated without special chars should not contain any."
    )

    # 2. Check that it contains valid chars
    valid_chars = set(string.ascii_letters + string.digits)

    # Check that all characters in the password are in the valid set
    assert all(c in valid_chars for c in password), (
        "Password contains characters outside of letters and digits when special chars are disabled."
    )
