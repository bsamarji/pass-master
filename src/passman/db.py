import sqlite3
from pathlib import Path
import click
import sys
from config import *


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
    Retrieve information from the db for the requested entry and return a list containing a tuple.
    The output will be piped into the tabulate() func which requires a list of iterables.
    """
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute(SQL_VIEW_ENTRY, (service_name,))
            row = cur.fetchmany(1)
            if len(row) == 0:
                click.echo(f"No entry was found with the service name: {service_name}")
                sys.exit(0)
            return row
    except sqlite3.Error as e:
        raise Exception(f"Could not retrieve entry for {service_name}. Details: {e}")


def search(search_term):
    """
    Retrieve information from the db for any service name that matches to the search term and return a list containing tuples.
    The output will be piped into the tabulate() func which requires a list of iterables.
    """
    search_pattern = f"%{search_term}%"

    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute(SQL_SEARCH, (search_pattern,))
            rows = cur.fetchall()
            if len(rows) == 0:
                click.echo(
                    f"No entries were found with service names that contain the search term: {search_term}"
                )
                sys.exit(0)
            return rows
    except sqlite3.Error as e:
        raise Exception(
            f"Could not retrieve any entries for {search_term}. Details: {e}"
        )


def list():
    """
    Retrieve information from the db for all service names and return a list containing tuples.
    The output will be piped into the tabulate() func which requires a list of iterables.
    """
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute(SQL_LIST)
            rows = cur.fetchall()
            if len(rows) == 0:
                click.echo(
                    f"No entries are currently stored. Please add at least one entry"
                )
                sys.exit(0)
            return rows
    except sqlite3.Error as e:
        raise Exception(f"Could not retrieve all entries. Details: {e}")


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
