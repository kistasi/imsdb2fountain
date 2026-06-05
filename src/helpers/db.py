import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "scripts.db"

STATUSES = ("shortlisted", "downloaded", "parsed", "converted", "failed")
_STATUS_RANK = {s: i for i, s in enumerate(STATUSES)}


def init():
    with _conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scripts (
                title       TEXT PRIMARY KEY,
                imsdb_link  TEXT NOT NULL UNIQUE,
                status      TEXT NOT NULL DEFAULT 'shortlisted',
                error       TEXT,
                updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)


@contextmanager
def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def upsert_shortlisted(title: str, imsdb_link: str):
    with _conn() as conn:
        conn.execute(
            """
            INSERT INTO scripts (title, imsdb_link, status, updated_at)
            VALUES (?, ?, 'shortlisted', datetime('now'))
            ON CONFLICT(title) DO NOTHING
        """,
            (title, imsdb_link),
        )


def set_status(title: str, status: str, error: str | None = None):
    with _conn() as conn:
        conn.execute(
            """
            UPDATE scripts
            SET status = ?, error = ?, updated_at = datetime('now')
            WHERE title = ?
        """,
            (status, error, title),
        )


def set_status_by_link(imsdb_link: str, status: str, error: str | None = None):
    with _conn() as conn:
        conn.execute(
            """
            UPDATE scripts
            SET status = ?, error = ?, updated_at = datetime('now')
            WHERE imsdb_link = ?
        """,
            (status, error, imsdb_link),
        )


def get_at_or_before(status: str) -> list[sqlite3.Row]:
    rank = _STATUS_RANK[status]
    statuses = [s for s, r in _STATUS_RANK.items() if r <= rank]
    placeholders = ",".join("?" * len(statuses))
    with _conn() as conn:
        return conn.execute(
            f"SELECT * FROM scripts WHERE status IN ({placeholders})",
            statuses,
        ).fetchall()


def get_by_status(status: str) -> list[sqlite3.Row]:
    with _conn() as conn:
        return conn.execute(
            "SELECT * FROM scripts WHERE status = ?", (status,)
        ).fetchall()


def summary() -> dict[str, int]:
    with _conn() as conn:
        rows = conn.execute(
            "SELECT status, COUNT(*) AS n FROM scripts GROUP BY status"
        ).fetchall()
    return {row["status"]: row["n"] for row in rows}
