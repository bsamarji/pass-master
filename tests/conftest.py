import tempfile
from pathlib import Path

import pytest

from keepr.db import get_db_connection, initialise_db
from keepr.internal_config import APP_DIR_NAME, DB_FILE_NAME

# --- Define a temporary key for testing ---
TEST_PEK_HEX = "0102030405060708090a0b0c0d0e0f10"
TEST_PEK = bytes.fromhex(TEST_PEK_HEX)


# Fixture to mock the database path setup
@pytest.fixture(scope="function")
def mock_db_path(monkeypatch):
    """
    Overrides the database path to use a temporary, unique file for the test run.
    This prevents tests from interfering with a real Keepr database.
    """
    # 1. Create a temporary directory structure similar to get_db_path()
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_home = Path(tmpdir)
        tmp_db_dir = tmp_home / APP_DIR_NAME
        tmp_db_dir.mkdir(parents=True, exist_ok=True)
        tmp_db_path = tmp_db_dir / DB_FILE_NAME

        # 2. Monkeypatch the original functions to return the temporary path
        def mock_get_db_path():
            return tmp_db_path

        # This replaces the real function with the mock one during the test's lifetime
        monkeypatch.setattr("keepr.db.get_db_path", mock_get_db_path)

        # 3. Yield the path for use in the next fixture
        yield tmp_db_path


@pytest.fixture(scope="function")
def fresh_db(mock_db_path):
    """
    Initializes a fresh, temporary, encrypted database before each test.
    """
    # 1. SETUP: Initialise the database using the mocked path and test key
    initialise_db(TEST_PEK)

    # 2. Yield the connection object for direct use in the tests
    # We use get_db_connection to get a connection handle to the new DB
    conn = get_db_connection(TEST_PEK)

    yield conn

    # 3. TEARDOWN: Close the connection
    conn.close()
