import base64
import os
from pathlib import Path

import click
import pytest
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from keepr import security
from keepr.internal_config import (
    APP_DIR_NAME,
    PEK_FILE_NAME,
    SALT_FILE_NAME,
    SECURITY_DIR_NAME,
)

TEST_SALT = b"(\xbe\xe5T\xc0\xae\xbb@/\xf7\xa3\xc5\xfag\xdcn"
TEST_PEK = b"\xf5Y&\xc1\x0f0\x14\x7f\x92G\xc9-QtP\xd1\x8a\xe9\x9ewq\x8d\x03\xd9\xe6\xf9V\xdf\x02\xe0\x1d\xd4"
TEST_MASTER_PASSWORD = "strong-test-password"


@pytest.fixture
def mock_home_path(tmp_path, monkeypatch):
    """
    Mock the home path to a temporary path.
    """

    mock_path = tmp_path
    monkeypatch.setattr(Path, "home", lambda: mock_path)
    return mock_path


@pytest.fixture
def fresh_kdf():
    """
    Returns a fresh, unused PBKDF2HMAC instance for a test.
    """

    return PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=TEST_SALT,
        iterations=1_200_000,
    )


@pytest.fixture
def mock_salt(monkeypatch):
    """
    Mock the return value of os.urandom().
    """

    mock_salt = TEST_SALT
    monkeypatch.setattr(os, "urandom", lambda *args, **kwargs: mock_salt)
    return mock_salt


@pytest.fixture
def mock_pek(monkeypatch):
    """
    Mock the return value of os.urandom().
    """

    mock_pek = TEST_PEK
    monkeypatch.setattr(os, "urandom", lambda *args, **kwargs: mock_pek)
    return mock_pek


@pytest.fixture
def mock_prompt(monkeypatch):
    """
    Mock the return value of click.prompt().
    """

    mock_prompt = TEST_MASTER_PASSWORD
    monkeypatch.setattr(click, "prompt", lambda *args, **kwargs: mock_prompt)
    return mock_prompt


@pytest.fixture
def mock_blank_prompt(monkeypatch):
    """
    Mock the return value of click.prompt().
    """

    mock_prompt = ""
    monkeypatch.setattr(click, "prompt", lambda *args, **kwargs: mock_prompt)
    return mock_prompt


@pytest.fixture
def mock_confirm_true(monkeypatch):
    """
    Mock the return value of click.confirm().
    """

    mock_confirm = True
    monkeypatch.setattr(click, "confirm", lambda *args, **kwargs: mock_confirm)
    return mock_confirm


@pytest.fixture
def mock_confirm_false(monkeypatch):
    """
    Mock the return value of click.confirm().
    """

    mock_confirm = False
    monkeypatch.setattr(click, "confirm", lambda *args, **kwargs: mock_confirm)
    return mock_confirm


def test_initialise_security_dir(mock_home_path):
    """
    Test the initialise_security_dir function creates a security directory.
    """

    # --- Act: Call the function to create the security dir ---
    security.initialise_security_dir()

    # --- Assert: The security dir should exist ---
    assert mock_home_path.exists(), "The security directory does not exist."


def test_generate_salt_file(mock_home_path, mock_salt):
    """
    Test the generate_salt_file function creates a salt file with the expected content.
    """

    # --- Arrange: Get salt file path ---
    salt_file = mock_home_path / APP_DIR_NAME / SECURITY_DIR_NAME / SALT_FILE_NAME

    # --- Arrange: Call the function to create the security dir ---
    security.initialise_security_dir()

    # --- Act: Call function to create salt file ---
    security.generate_salt_file()

    # --- Assert: Salt file should exist ---
    assert salt_file.exists(), "The salt file should exist."

    # --- Assert: Test contents of salt file ---
    with open(salt_file, "rb") as f:
        content = f.read()
        assert content == mock_salt, (
            f"The salt file should have the expected content {mock_salt}, instead got {content}."
        )


def test_retrieve_salt(mock_home_path, mock_salt):
    """
    Test the retrieve_salt function retrieves the salt file with the expected content.
    """

    # --- Arrange: Call the function to create the security dir ---
    security.initialise_security_dir()

    # --- Arrange: Call function to create salt file ---
    security.generate_salt_file()

    # --- Act: Call function to retrieve salt ---
    salt = security.retrieve_salt()

    # --- Assert: Check the salt is retrieved correctly ---
    assert salt == mock_salt, (
        f"The expected salt should be {mock_salt}, instead got {salt}."
    )


def test_retrieve_empty_salt_file(mock_home_path, mock_salt, capsys):
    """
    Test that an empty salt file triggers a system exit.
    """

    # --- Arrange: set alt file path ---
    salt_file = mock_home_path / APP_DIR_NAME / SECURITY_DIR_NAME / SALT_FILE_NAME

    # --- Arrange: Call the function to create the security dir ---
    security.initialise_security_dir()

    # --- Arrange: Call function to create an empty salt file ---
    salt_file.touch()

    # --- Act: Call function to retrieve salt ---
    with pytest.raises(SystemExit) as excinfo:
        security.retrieve_salt()

    # --- Assert: Exit code ---
    assert excinfo.value.code == 1, "Exit code should be 1."

    # --- Assert: stdout message ---
    captured = capsys.readouterr()
    assert "Salt file is empty" in captured.out


def test_key_derivation_function(mock_salt):
    """
    Test the key_derivation_function returns a kdf function object.
    """

    # --- Act: Call function to create kdf ---
    kdf = security.key_derivation_function(mock_salt)

    # --- Assert: Check the kdf is the correct data type ---
    assert isinstance(kdf, PBKDF2HMAC), "KDF should be a PBKDF2HMAC object."


def test_successful_first_time_login(mock_home_path, mock_prompt):
    """
    Test the login() function logic works for first time logins.
    The pek file only exists if a master password has been set,
    therefore a first time login is assumed from the existence/non-existence of a pek file.
    """

    # --- Arrange: Setup mock pek file path ---
    pek_file_path = mock_home_path / APP_DIR_NAME / SECURITY_DIR_NAME / PEK_FILE_NAME

    # --- Assert: Check the pek file doesn't exist (required for first time login) ---
    assert not pek_file_path.exists(), "The pek file should not exist."

    # --- Act: Call login function to retrieve mock master password ---
    master_password = security.login()

    # --- Assert: Check master_password logic works ---
    assert master_password == mock_prompt, (
        f"The master password should be {mock_prompt}, instead got {master_password}."
    )


def test_blank_first_time_login(mock_home_path, mock_blank_prompt, capsys):
    """
    Test the login() function logic for first time logins entering a blank master password.
    """

    # --- Arrange: Setup mock pek file path ---
    pek_file_path = mock_home_path / APP_DIR_NAME / SECURITY_DIR_NAME / PEK_FILE_NAME

    # --- Assert: Check the pek file doesn't exist (required for first time login) ---
    assert not pek_file_path.exists(), "The pek file should not exist."

    # --- Act: Call login function to retrieve mock master password ---
    with pytest.raises(SystemExit) as excinfo:
        security.login()

    # --- Assert: Check exit code ---
    assert excinfo.value.code == 0, "Exit code should be 0."

    # --- Assert: Check stdout message ---
    captured = capsys.readouterr()
    assert "Master password cannot be empty." in captured.out


def test_successful_sequential_login(mock_home_path, mock_prompt, mock_pek):
    """
    Test the login() function logic works for sequential logins.
    The pek file only exists if a master password has been set,
    therefore a sequential login is assumed from the existence/non-existence of a pek file.
    """

    # --- Arrange: Call the function to create the mock security dir ---
    security.initialise_security_dir()

    # --- Arrange: Setup mock pek file path ---
    pek_file_path = mock_home_path / APP_DIR_NAME / SECURITY_DIR_NAME / PEK_FILE_NAME

    # --- Arrange: Create mock pek file ---
    with open(pek_file_path, "wb") as f:
        f.write(mock_pek)

    # --- Assert: Check the pek file exists ---
    assert pek_file_path.exists(), "The pek file should exist."

    # --- Act: Call login function to retrieve mock master password ---
    master_password = security.login()

    # --- Assert: Check master_password logic works ---
    assert master_password == mock_prompt, (
        f"The master password should be {mock_prompt}, instead got {master_password}."
    )


def test_prompt_new_master_password_blank(mock_blank_prompt, capsys):
    """
    Test the prompt_new_master_password function logic works for entering a blank master password.
    """

    # --- Act: Call function to prompt for new master password ---
    with pytest.raises(SystemExit) as excinfo:
        security.prompt_new_master_password()

    # --- Assert: Check exit code ---
    assert excinfo.value.code == 0, "Exit code should be 0."

    # --- Assert: Check stdout message ---
    captured = capsys.readouterr()
    assert "Master password cannot be empty." in captured.out


def test_prompt_new_master_password_success(mock_prompt, mock_confirm_true, capsys):
    """
    Test the prompt_new_master_password function logic works for entering a new master password
    and confirming that the update should succeed.
    """

    # --- Act: Call function to prompt for new master password ---
    master_password = security.prompt_new_master_password()

    # --- Assert: Test master password logic ---
    assert master_password == mock_prompt, (
        f"The master password should be {mock_prompt}, instead got {master_password}."
    )

    # --- Assert: Test CLI stdout ---
    captured = capsys.readouterr()
    assert "Successfully updated master password!" in captured.out


def test_prompt_new_master_password_cancel(mock_prompt, mock_confirm_false, capsys):
    """
    Test the prompt_new_master_password function logic works for entering a new master password
    and confirming that the update should be cancelled.
    """

    # --- Act: Call function to prompt for new master password ---
    with pytest.raises(SystemExit) as excinfo:
        security.prompt_new_master_password()

    # --- Assert: Check exit code ---
    assert excinfo.value.code == 0, "Exit code should be 0."

    # --- Assert: Test CLI stdout ---
    captured = capsys.readouterr()
    assert "Operation cancelled." in captured.out


def test_generate_derived_key(fresh_kdf):
    """
    Test the function returns a url safe base64 encoded derived key from the master password.
    """

    # --- Act: Call function to generate the key ---
    derived_key = security.generate_derived_key(fresh_kdf, TEST_MASTER_PASSWORD)

    # --- Assert: Check they returned key is in bytes ---
    assert isinstance(derived_key, bytes), "The derived key should be bytes."

    # --- Assert: Check the key is urlsafe_base64 encoded ---
    assert (
        base64.urlsafe_b64encode(base64.urlsafe_b64decode(derived_key)) == derived_key
    ), "The derived key should be base64 encoded."


def test_generate_pek(mock_pek):
    """
    Test that the function returns the pek properly and the pek data type is of bytes.
    """

    # --- Act: Call function to generate pek ---
    pek = security.generate_pek()

    # --- Assert: Check pek is of bytes ---
    assert isinstance(pek, bytes), "The pek should be bytes."

    # --- Assert: Check the function is returning the pek correctly ---
    assert pek == mock_pek, f"Expected the pek to be {mock_pek}, instead got {pek}."


def test_encrypt_pek(mock_home_path, fresh_kdf):
    """
    Test pek encryption and storage.
    """

    # --- Arrange: Set mock pek file path ---
    pek_file = mock_home_path / APP_DIR_NAME / SECURITY_DIR_NAME / PEK_FILE_NAME

    # --- Arrange: Create mock security dir ---
    security.initialise_security_dir()

    # --- Arrange: Create a derived key using a fresh kdf ---
    derived_key = base64.urlsafe_b64encode(
        fresh_kdf.derive(TEST_MASTER_PASSWORD.encode())
    )

    # --- Act: Call the function to encrypt the mock pek and write it to a tmp file ---
    security.encrypt_pek(derived_key, TEST_PEK)

    # --- Assert: Check the pek file exists ---
    assert pek_file.exists(), "The pek file should exist."

    # --- Act: Read pek file contents and decrypt pek ---
    with open(pek_file, "rb") as file:
        encrypted_pek = file.read()
    f = Fernet(derived_key)
    pek = f.decrypt(encrypted_pek)

    # --- Assert: Pek should be of bytes ---
    assert isinstance(pek, bytes), "The pek should be bytes."

    # --- Assert: Check the decrypted pek is the same as the test pek ---
    assert pek == TEST_PEK, f"The expected pek should be {TEST_PEK}, instead got {pek}."


def test_retrieve_and_decrypt_pek(mock_home_path, fresh_kdf):
    """
    Test retrieving and decrypting the pek.
    """

    # --- Arrange: Create mock security dir ---
    security.initialise_security_dir()

    # --- Arrange: Create a derived key using a fresh kdf ---
    derived_key = base64.urlsafe_b64encode(
        fresh_kdf.derive(TEST_MASTER_PASSWORD.encode())
    )

    # --- Arrange: Call the function to encrypt the mock pek and write it to a tmp file ---
    security.encrypt_pek(derived_key, TEST_PEK)

    # --- Act: Call function to get pek from disk ---
    pek = security.retrieve_and_decrypt_pek(derived_key)

    # --- Assert: Check pek is of bytes ---
    assert isinstance(pek, bytes), "The pek should be bytes."

    # --- Assert: Check the decrypted pek is the same as the test pek ---
    assert pek == TEST_PEK, f"The expected pek should be {TEST_PEK}, instead got {pek}."


def test_retrieve_and_decrypt_pek_wrong_password(mock_home_path, fresh_kdf, capsys):
    """
    Test that providing the wrong derived key (wrong password) causes a SystemExit
    and prints the correct error message.
    """

    # --- Arrange: Encrypt the PEK with the CORRECT key ---
    correct_derived_key = base64.urlsafe_b64encode(
        fresh_kdf.derive(TEST_MASTER_PASSWORD.encode())
    )
    security.initialise_security_dir()
    security.encrypt_pek(correct_derived_key, TEST_PEK)

    # --- Arrange: Generate a WRONG derived key (simulating wrong password) ---
    wrong_derived_key = base64.urlsafe_b64encode(os.urandom(32))

    # --- Act: Call function with wrong key ---
    with pytest.raises(SystemExit) as excinfo:
        security.retrieve_and_decrypt_pek(wrong_derived_key)

    # --- Assert: Stdout message ---
    captured = capsys.readouterr()
    assert "The master password is incorrect" in captured.out

    # --- Assert: Exit code ---
    assert excinfo.value.code == 1


def test_retrieve_and_decrypt_pek_file_not_found(mock_home_path, fresh_kdf, capsys):
    # --- Arrange: Setup derived key ---
    derived_key = base64.urlsafe_b64encode(
        fresh_kdf.derive(TEST_MASTER_PASSWORD.encode())
    )

    # --- Arrange: Create mock security dir ---
    security.initialise_security_dir()

    # --- Act: Call function to Attempt to access the non-existent pek file ---
    result = security.retrieve_and_decrypt_pek(derived_key)

    # --- Assert: None should be returned ---
    assert result is None, f"Expected None but got {result}."

    # --- Assert: stdout message ---
    captured = capsys.readouterr()
    assert "PEK file not found" in captured.out
