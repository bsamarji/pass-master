# --- DB QUERIES ---
SQL_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY,
    service_name TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    url TEXT NULL,
    note TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
"""

SQL_INSERT_ENTRY = """
INSERT INTO entries (
    service_name,
    username,
    password,
    url,
    note
    )
VALUES (
    ?,
    ?,
    ?,
    ?,
    ?
    );
"""

SQL_VIEW_ENTRY = """
SELECT service_name,
    username,
    password,
    url,
    note,
    created_at,
    updated_at
FROM entries
WHERE service_name = ?
"""

SQL_SEARCH = """
SELECT service_name,
    url,
    note,
    created_at,
    updated_at
FROM entries
WHERE service_name LIKE ?
"""

SQL_LIST = """
SELECT service_name,
    url,
    note,
    created_at,
    updated_at
FROM entries
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

SQL_VALIDATE_SERVICE_NAME = """
SELECT service_name
FROM entries
WHERE service_name = ?
"""
