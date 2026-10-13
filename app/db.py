import os
import re
import sqlite3

BASE = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.environ.get("DB_PATH", os.path.join(BASE, "data", "pianos.sqlite"))
SETUP_SQL = os.path.join(BASE, "setup.sql")
SETUP_DATA_SQL = os.path.join(BASE, "setupData.sql")


def init_db():
    """Rebuild the database from the setup files (the db is disposable)."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    con = sqlite3.connect(DB_PATH)
    with open(SETUP_SQL) as f:
        con.executescript(f.read())
    with open(SETUP_DATA_SQL) as f:
        con.executescript(f.read())
    con.commit()
    con.close()


def schema_sql():
    with open(SETUP_SQL) as f:
        return f.read()


def run_select(query):
    """Run model-generated SQL read-only. Returns (columns, rows)."""
    stripped = query.strip().rstrip(";").strip()
    if not re.match(r"^(select|with)\b", stripped, re.IGNORECASE) or ";" in stripped:
        raise ValueError("Only a single SELECT statement is allowed.")
    # mode=ro means even a sneaky write fails at the SQLite level
    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        cur = con.execute(stripped)
        columns = [d[0] for d in cur.description]
        return columns, cur.fetchmany(200)
    finally:
        con.close()
