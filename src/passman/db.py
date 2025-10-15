import sqlite3
from pathlib import Path
import click

# --- Config ---
DB_FILE_NAME = "passman.db"
DB_DIR_NAME = ".passman"
SQL_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY,
    service_name TEXT NOT NULL UNIQUE,
    username BLOB NOT NULL,
    password BLOB NOT NULL,
    url TEXT NULL,
    note TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    iv BLOB NOT NULL
    );
"""
SQL_INSERT_ENTRY = """
INSERT INTO entries (
    service_name,
    username,
    password,
    url,
    note,
    iv
    )
VALUES (
    ?,
    ?,
    ?,
    ?,
    ?,
    ?
    );
"""
SQL_VIEW_ENTRY = """
SELECT id,
    service_name,
    username,
    password,
    url,
    note,
    created_at,
    updated_at
FROM entries
WHERE service_name = ?
"""
SQL_UPDATE_ENTRY = """
UPDATE entries
SET password = ?,
    updated_at = datetime()
WHERE service_name = ?;
"""
SQL_DELETE_ENTRY = """
DELETE FROM entries
WHERE service_name = ?;
"""


def get_db_path():
    """
    Returns the cross-platform path to the SQLite database file.
    """
    home_dir = Path.home()
    db_dir = home_dir / DB_DIR_NAME
    Path.mkdir(db_dir, parents=True, exist_ok=True)
    return db_dir / DB_FILE_NAME


def get_db_connection():
    """
    Creates and returns a connection to the database.
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    return conn


def initialise_db():
    """
    Creates the 'entries' table if it does not already exist.
    """
    try:
        with get_db_connection() as conn:
            conn.execute(SQL_CREATE_TABLE)
    except sqlite3.Error as e:
        click.echo(f"Could not initialise the database. Details: {e}", err=True)


def add_entry(service_name, username, password, url, note, iv):
    """
    Insert a new entry into the database.
    """
    try:
        with get_db_connection() as conn:
            conn.execute(
                SQL_INSERT_ENTRY, (service_name, username, password, url, note, iv)
            )
    except sqlite3.Error as e:
        raise Exception(f"Could not insert entry for {service_name}. Details: {e}")


def view_entry(service_name):
    """
    Retrieve information from the db for the requested entry.
    """
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute(SQL_VIEW_ENTRY, (service_name,))
            row = cur.fetchone()
            return row
    except sqlite3.Error as e:
        raise Exception(f"Could not retrieve entry for {service_name}. Details: {e}")


def update_entry(service_name, password):
    """
    Update the password for an entry in the database.
    """
    try:
        with get_db_connection() as conn:
            conn.execute(
                SQL_UPDATE_ENTRY,
                (
                    password,
                    service_name,
                ),
            )
    except sqlite3.Error as e:
        raise Exception(f"Could not update the entry for {service_name}. Details: {e}")


def delete_entry(service_name):
    """
    Delete an entry from the database.
    """
    try:
        with get_db_connection() as conn:
            conn.execute(SQL_DELETE_ENTRY, (service_name,))
    except sqlite3.Error as e:
        raise Exception(f"Could not delete the entry for {service_name}. Details: {e}")
