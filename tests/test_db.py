import pytest

# Use the key defined in conftest.py
from conftest import TEST_PEK

# Import the CRUD functions to test
from keepr.db import (
    add_entry,
    delete_entry,
    list_entries,
    search,
    update_entry,
    validate_service_name,
    view_entry,
)

# Define test data
TEST_SERVICE = "GitHub"
TEST_USERNAME = "octocat"
TEST_PASSWORD = "very-secure-pass"
TEST_URL = "https://github.com"
TEST_NOTE = "Personal account"


def test_add_and_view_entry(fresh_db):
    """Test adding an entry and then viewing it successfully."""

    # --- Act: Add the entry ---
    add_entry(TEST_PEK, TEST_SERVICE, TEST_USERNAME, TEST_PASSWORD, TEST_URL, TEST_NOTE)

    # --- Act: View the entry ---
    row = view_entry(TEST_PEK, TEST_SERVICE)

    # --- Assert: Check the mock data ---
    # view_entry returns a list of lists, with the outer list holding each entry
    # and the inner list holding the data for each entry
    # view_entry only ever returns one row
    assert isinstance(row, list)
    assert len(row) == 1
    # Grab the inner list which contains all the data for the mock entry
    entry = row[0]

    # Check the fields in the exact order returned by SQL_VIEW_ENTRY
    assert entry[0] == TEST_SERVICE, "Service name not added successfully"
    assert entry[1] == TEST_USERNAME, "User name not added successfully"
    assert entry[2] == TEST_PASSWORD, "Password not added successfully"
    assert entry[3] == TEST_URL, "URL not added successfully"
    assert entry[4] == TEST_NOTE, "Note not added successfully"
    assert entry[5] is not None  # created_at
    assert entry[6] is not None  # updated_at


def test_view_nonexistent_entry(fresh_db, capsys):
    """Test viewing an entry that doesn't exist."""

    # --- Act: view the entry ---
    with pytest.raises(SystemExit) as excinfo:
        view_entry(TEST_PEK, "NonExistentService")

    # --- Assert: test for the output of a non-existent entry ---
    assert excinfo.value.code == 0

    # Check the printed output
    captured = capsys.readouterr()
    assert (
        "No entry was found with the service name: NonExistentService" in captured.out
    )


def test_update_entry(fresh_db):
    """Test updating the password for an existing entry."""

    # --- Act: Add initial entry ---
    add_entry(TEST_PEK, TEST_SERVICE, TEST_USERNAME, TEST_PASSWORD, TEST_URL, TEST_NOTE)

    # --- Act: Update the password ---
    new_password = "a-brand-new-pass"
    update_entry(TEST_PEK, TEST_SERVICE, new_password)

    # --- Assert: View the entry and check the new password ---
    # view_entry returns a list of lists, with the outer list holding each entry
    # and the inner list holding the data for each entry
    # note: view_entry only ever returns one row
    row = view_entry(TEST_PEK, TEST_SERVICE)
    # Grab the inner list which contains all the data for the mock entry
    entry = row[0]
    assert entry[2] == new_password  # Password is the 3rd column (index 2)


def test_delete_entry_and_validate(fresh_db):
    """Test deleting an entry and ensuring it's gone."""

    # --- Act: Add initial entry ---
    add_entry(TEST_PEK, TEST_SERVICE, TEST_USERNAME, TEST_PASSWORD, TEST_URL, TEST_NOTE)

    # --- Assert: Validate it exists first ---
    assert validate_service_name(TEST_PEK, TEST_SERVICE) is True

    # --- Act: Delete the entry ---
    delete_entry(TEST_PEK, TEST_SERVICE)

    # --- Assert: Validate it no longer exists ---
    assert validate_service_name(TEST_PEK, TEST_SERVICE) is False


def test_search_entry(fresh_db):
    """Test searching for entries based on a pattern."""

    # --- Act: Add a few entries ---
    add_entry(TEST_PEK, "TestBank", "u1", "p1", "", "")
    add_entry(TEST_PEK, "Personal Email", "u2", "p2", "", "")
    add_entry(TEST_PEK, "WorkBank", "u3", "p3", "", "")

    # --- Act: Search for 'Bank' ---
    rows = search(TEST_PEK, "Bank")

    # --- Assert: Should find 2 entries ---
    assert len(rows) == 2
    # Check that 'Personal Email' is NOT in the results
    service_names = [row[0] for row in rows]
    assert "TestBank" in service_names
    assert "WorkBank" in service_names
    assert "Personal Email" not in service_names


def test_search_non_matching_term(fresh_db, capsys):
    """Test searching for entries on a non-matching search term."""

    # --- Act: search using a non-matching search term ---
    with pytest.raises(SystemExit) as excinfo:
        search(TEST_PEK, "NonExistentService")

    # --- Assert: test for the output of a non-existent entry ---
    assert excinfo.value.code == 0

    # Check the printed output
    captured = capsys.readouterr()
    assert (
        "No entries were found with service names that contain the search term: NonExistentService"
        in captured.out
    )


def test_list_entries(fresh_db):
    """Test retrieving all entries."""

    # --- Act: Add two entries ---
    add_entry(TEST_PEK, "Entry1", "u1", "p1", "", "")
    add_entry(TEST_PEK, "Entry2", "u2", "p2", "", "")

    # --- Act: List all ---
    rows = list_entries(TEST_PEK)

    # --- Assert: Should find 2 entries ---
    assert len(rows) == 2
    service_names = [row[0] for row in rows]
    assert "Entry1" in service_names
    assert "Entry2" in service_names


def test_list_with_no_entries(fresh_db, capsys):
    """Test list_entries with no entries."""

    # --- Act: search using a non-matching search term ---
    with pytest.raises(SystemExit) as excinfo:
        list_entries(TEST_PEK)

    # --- Assert: test for the output of a non-existent entry ---
    assert excinfo.value.code == 0

    # Check the printed output
    captured = capsys.readouterr()
    assert (
        "No entries are currently stored. Please add at least one entry" in captured.out
    )
