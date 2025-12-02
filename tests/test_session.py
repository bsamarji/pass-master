import os
import time

import pytest
from conftest import TEST_PEK

from keepr import session

TEST_TIMESTAMP = 1672531200
TEST_TIMEOUT = 3600


@pytest.fixture
def mock_session_file_path(tmp_path, monkeypatch):
    """
    Mock the session file path to a temporary file.
    """

    mock_path = tmp_path / "keepr.test.session"
    monkeypatch.setattr(session, "get_session_file_path", lambda: mock_path)
    return mock_path


@pytest.fixture
def mock_timestamp(monkeypatch):
    """
    Mocks the return of time.time()
    and creates a fixed timestamp that can be used to test function logic.
    """

    mock_timestamp = TEST_TIMESTAMP
    monkeypatch.setattr(time, "time", lambda: mock_timestamp)
    return mock_timestamp


def test_store_session_data(mock_session_file_path, mock_timestamp):
    """
    Test that the session file information is stored correctly.
    """

    # --- Act: Store the session data ---
    success = session.store_session_data(TEST_PEK)

    # --- Assert: Check the function call returned True ---
    assert success is True

    # --- Assert: Check the mock session file exists ---
    assert mock_session_file_path.exists(), "The session file should exist."

    # --- Assert: Check file permissions are correct ---
    assert oct(os.stat(mock_session_file_path).st_mode & 0o777) == "0o600", (
        "The session file permissions should be 0o600."
    )

    # --- Assert: Check the session file has been written correctly ---
    with open(mock_session_file_path, "rb") as f:
        content = f.read()
        assert len(content) == 40, "The session file should be of length 40."
        assert content[:32] == TEST_PEK, "The session file pek is incorrect."

        timestamp_bytes = content[32:]
        timestamp = int.from_bytes(timestamp_bytes, "big")
        assert timestamp == mock_timestamp, (
            f"Session file timestamp mismatch. Expected: {TEST_TIMESTAMP}, Actual: {timestamp}."
        )


def test_retrieve_session_pek(mock_session_file_path, mock_timestamp, monkeypatch):
    """
    Test that the session file information is retrieved correctly when the timestamp is active.
    """

    # --- Arrange: Create a mock session file ---
    session.store_session_data(TEST_PEK)

    # --- Arrange: Set timestamp to an active value ---
    active_time = TEST_TIMESTAMP + TEST_TIMEOUT - 100
    monkeypatch.setattr(time, "time", lambda: active_time)

    # --- Act: Call function to retrieve session file data ---
    pek = session.retrieve_session_pek()

    # --- Assert: Check if the pek is returned correctly
    assert isinstance(pek, bytes), "The session file pek should be of bytes."
    assert pek == TEST_PEK, "The function should return the correct pek."


def test_retrieve_session_pek_timeout(
    mock_session_file_path, mock_timestamp, monkeypatch
):
    """
    Test that the session expiry logic works correctly when the timestamp is expired.
    """

    # --- Arrange: Create a mock session file ---
    session.store_session_data(TEST_PEK)

    # --- Arrange: Set timestamp to an expired value ---
    expired_time = TEST_TIMESTAMP + TEST_TIMEOUT + 100
    monkeypatch.setattr(time, "time", lambda: expired_time)

    # --- Act: The function should unlink the session file due to the expired timestamp ---
    session.retrieve_session_pek()

    # --- Assert: The file should be unlinked ---
    assert not mock_session_file_path.exists(), "The session file should not exist."


def test_clear_session_data(mock_session_file_path):
    """
    Test that the session file is deleted correctly.
    """

    # --- Arrange: Create a mock session file ---
    session.store_session_data(TEST_PEK)

    # --- Assert: Check the session file exists ---
    assert mock_session_file_path.exists(), "The session file should exist."

    # --- Act: Clear the session file ---
    result = session.clear_session_data()

    # --- Assert: Function should return True ---
    assert result is True

    # --- Assert: Session file should be unlinked ---
    assert not mock_session_file_path.exists(), "The session file should not exist."


def test_clear_session_data_not_found(mock_session_file_path):
    """
    Test that the function returns None if the session file does not exist.
    """

    # --- Assert: Check the session file doesn't exist ---
    assert not mock_session_file_path.exists(), "The session file should not exist."

    # --- Act: Call the function to clear the session file ---
    result = session.clear_session_data()

    # --- Assert: The function should return False ---
    assert result is None, (
        "The function should return None if the session file does not exist."
    )
