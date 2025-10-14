import sqlite3
from pathlib import Path
import click

# --- Config ---
DB_FILE_NAME = "passman.db"
DB_DIR_NAME = ".passman"


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
    conn.row_factory = sqlite3.Row
    return conn


def initialise_db():
    """
    Creates the 'entries' table if it does not already exist.
    """
    try:
        with get_db_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY,
                    service_name TEXT NOT NULL UNIQUE,
                    username BLOB NOT NULL,
                    password BLOB NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    iv BLOB NOT NULL
                    )
            """
            )
    except sqlite3.Error as e:
        click.echo(
            f"Could not initialise the database. Details: {e}", 
            err=True
        )
