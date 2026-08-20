"""
CRUD helpers: Create, Read, Update, Delete.

Every function here does ONE thing and returns plain Python/pandas
objects. The Streamlit pages will import these functions and never write
raw SQL themselves — that keeps the UI code focused on layout/interaction,
and keeps SQL in one testable place.
"""

from datetime import date
import pandas as pd

from db.database import get_connection


def get_all_applications() -> pd.DataFrame:
    """Return every application as a pandas DataFrame, newest first."""
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM applications ORDER BY date_applied DESC, id DESC",
        conn,
        parse_dates=["date_applied", "last_update", "response_date"],
    )
    conn.close()
    return df


def add_application(
    company: str,
    role: str,
    date_applied: date,
    status: str = "Applied",
    source: str | None = None,
    location: str | None = None,
    salary_range: str | None = None,
    notes: str | None = None,
) -> int:
    """Insert a new application. Returns the new row's id."""
    conn = get_connection()
    cur = conn.execute(
        """
        INSERT INTO applications
            (company, role, date_applied, status, source, location,
             salary_range, last_update, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            company,
            role,
            str(date_applied),
            status,
            source,
            location,
            salary_range,
            str(date.today()),
            notes,
        ),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def update_status(app_id: int, new_status: str, response_date: date | None = None) -> None:
    """Update an application's status (and optionally its response date).

    This is the function you'll call most often — every time a status
    changes, last_update is bumped to today automatically, which is what
    powers the 'recent activity' feed and response-time charts later.
    """
    conn = get_connection()
    if response_date is not None:
        conn.execute(
            """
            UPDATE applications
            SET status = ?, last_update = ?, response_date = ?
            WHERE id = ?
            """,
            (new_status, str(date.today()), str(response_date), app_id),
        )
    else:
        conn.execute(
            "UPDATE applications SET status = ?, last_update = ? WHERE id = ?",
            (new_status, str(date.today()), app_id),
        )
    conn.commit()
    conn.close()


def update_application(app_id: int, **fields) -> None:
    """Generic update: pass any column=value pairs, e.g.
    update_application(3, notes="Recruiter called", location="Remote").
    """
    if not fields:
        return
    fields["last_update"] = str(date.today())
    set_clause = ", ".join(f"{col} = ?" for col in fields)
    conn = get_connection()
    conn.execute(
        f"UPDATE applications SET {set_clause} WHERE id = ?",
        (*fields.values(), app_id),
    )
    conn.commit()
    conn.close()


def delete_application(app_id: int) -> None:
    conn = get_connection()
    conn.execute("DELETE FROM applications WHERE id = ?", (app_id,))
    conn.commit()
    conn.close()
