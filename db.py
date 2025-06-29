# db.py

import sqlite3

def init_db(db_path: str = "data.db") -> sqlite3.Connection:
    """
    Crée à chaque appel une connexion SQLite compatible multi-thread
    et s'assure que les tables de base existent.
    """
    conn = sqlite3.connect(
        db_path,
        detect_types=sqlite3.PARSE_DECLTYPES,
        check_same_thread=False         # <-- autorise l'usage cross-thread
    )
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Table 'records'
    cur.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            action TEXT,
            timestamp TEXT
        )
    """)

    # Table 'travel_authorizations'
    cur.execute("""
        CREATE TABLE IF NOT EXISTS travel_authorizations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            user TEXT,
            destination TEXT,
            depart_date TEXT,
            return_date TEXT,
            project TEXT,
            fund TEXT,
            status TEXT,
            submitted_by TEXT,
            submitted_at TEXT,
            submitted_sig TEXT,
            verified_by TEXT,
            verified_at TEXT,
            verified_sig TEXT,
            approved_by TEXT,
            approved_at TEXT,
            approved_sig TEXT
        )
    """)

    conn.commit()
    return conn
