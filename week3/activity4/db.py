from pathlib import Path
import sqlite3

# Keep the database next to the Python modules regardless of the directory from
# which the user runs `python main.py`.
DB_PATH = Path(__file__).with_name("university.db")


def get_connection(db_path: str | Path = DB_PATH) -> sqlite3.Connection:
    """Create a SQLite connection configured for this application."""
    conn = sqlite3.connect(db_path)

    # sqlite3 normally returns query results as tuples. sqlite3.Row lets the
    # rest of the application access columns by name, e.g. row["course_name"].
    conn.row_factory = sqlite3.Row

    # Foreign-key enforcement is disabled by default in SQLite and must be
    # enabled separately for every connection.
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
