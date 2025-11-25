import os
import time
from pathlib import Path

import click

from keepr.internal_config import (
    APP_DIR_NAME,
    COLOR_ERROR,
    SECURITY_DIR_NAME,
    SESSION_FILE_NAME,
    SESSION_TIMEOUT_SECONDS,
)


def get_session_file_path():
    """
    Get the session file path that holds the session data.
    Return:
        session_file: session file path
    """
    home_dir = Path.home()
    session_file = home_dir / APP_DIR_NAME / SECURITY_DIR_NAME / SESSION_FILE_NAME
    return session_file


def store_session_data(pek):
    session_file = get_session_file_path()

    try:
        with open(session_file, "wb") as f:
            f.write(pek)
            f.write(int(time.time()).to_bytes(8, "big"))
        os.chmod(session_file, 0o600)
        return True
    except Exception as e:
        click.secho(
            f"SESSION ERROR: Failed to store session data. Details: {e}", **COLOR_ERROR
        )
        return False


def retrieve_session_pek():
    """
    Retrieve the session data.
    Check if the session is still active.
    Return:
        pek: primary encryption key
    """
    session_file = get_session_file_path()
    if not session_file.exists():
        return None

    try:
        with open(session_file, "rb") as f:
            content = f.read()
            if len(content) != 40:
                return None

            pek = content[:32]
            timestamp_bytes = content[32:]
            timestamp = int.from_bytes(timestamp_bytes, "big")

            if time.time() - timestamp > SESSION_TIMEOUT_SECONDS:
                session_file.unlink()
                return None
            return pek

    except Exception as e:
        click.secho(
            f"SESSION ERROR: Failed to retrieve session data. Details: {e}",
            **COLOR_ERROR,
        )
        try:
            session_file.unlink()
        except Exception as e:
            click.secho(
                f"SESSION ERROR: Failed to delete session file. Details: {e}",
                **COLOR_ERROR,
            )
        return None


def clear_session_data():
    """
    Clear the session data.
    """
    session_file = get_session_file_path()
    try:
        if session_file.exists():
            session_file.unlink()
            return True
    except Exception as e:
        click.secho(
            f"SESSION ERROR: Failed to clear session data. Details: {e}", **COLOR_ERROR
        )
        return False
