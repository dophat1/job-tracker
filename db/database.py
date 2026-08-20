"""
Database connection + schema setup.

Why a separate file for this? Keeping "how do I connect / what does the
table look like" separate from "how do I query it" (queries.py) and
separate from "what does the UI do" (the Streamlit pages) is a pattern
called separation of concerns. It means you can test your database logic
without ever touching Streamlit, and swap SQLite for Postgres later by
only editing this one file.
"""

import sqlite3
from pathlib import Path

# Path to the SQLite file. Path(__file__).parent means "the folder this
# file lives in" (db/), then we go up one level and into data/.
DB_PATH = Path(__file__).parent.parent / "data" / "applications.db"

# The order status stages happen in. We store this here (not just in the
# database) so charts and dropdowns can always sort/display in the
# logical order, not alphabetical order.
STATUS_ORDER = [
    "Applied",
    "Screening",
    "Interview",
    "Offer",
    "Rejected",
    "Withdrawn",
    "Ghosted",
]


def get_connection() -> sqlite3.Connection:
    """Open a connection to the SQLite database file.

    check_same_thread=False is needed because Streamlit can call this
    from a different thread than the one that created the connection.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn


def init_db() -> None:
    """Create the applications table if it doesn't exist yet.

    Safe to call every time the app starts — CREATE TABLE IF NOT EXISTS
    is a no-op if the table is already there.
    """
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS applications (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            company       TEXT NOT NULL,
            role          TEXT NOT NULL,
            date_applied  TEXT NOT NULL,
            status        TEXT NOT NULL DEFAULT 'Applied',
            source        TEXT,
            location      TEXT,
            salary_range  TEXT,
            last_update   TEXT,
            response_date TEXT,
            notes         TEXT
        )
        """
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Running `python db/database.py` directly will just set up the table.
    # This is a handy pattern: every module can be both imported AND run
    # standalone for quick manual testing.
    init_db()
    print(f"Database ready at {DB_PATH}")
