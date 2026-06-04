"""Small SQLite layer for predictions."""

from pathlib import Path
import shutil
import sqlite3


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "predictions.db"
OLD_DB_PATH = ROOT / "predictions.db"


def connect():
    DB_PATH.parent.mkdir(exist_ok=True)
    if OLD_DB_PATH.exists() and not DB_PATH.exists():
        shutil.copy2(OLD_DB_PATH, DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect() as conn:
        _ensure_schema(conn)


def _create_table(conn, name="predictions"):
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            result TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )


def _ensure_schema(conn):
    info = conn.execute("PRAGMA table_info(predictions)").fetchall()
    if not info:
        _create_table(conn)
        return

    columns = {row["name"] for row in info}
    desired = {"id", "text", "result", "confidence", "timestamp"}
    if columns == desired:
        return

    text_col = "text" if "text" in columns else "news_text"
    result_col = "result" if "result" in columns else "prediction"
    confidence_expr = "confidence" if "confidence" in columns else "0"
    timestamp_expr = "timestamp" if "timestamp" in columns else "CURRENT_TIMESTAMP"

    _create_table(conn, "predictions_new")
    conn.execute(
        f"""
        INSERT INTO predictions_new (id, text, result, confidence, timestamp)
        SELECT id, {text_col}, {result_col}, {confidence_expr}, {timestamp_expr}
        FROM predictions
        """
    )
    conn.execute("DROP TABLE predictions")
    conn.execute("ALTER TABLE predictions_new RENAME TO predictions")


def save_prediction(text, result, confidence):
    with connect() as conn:
        conn.execute(
            "INSERT INTO predictions (text, result, confidence) VALUES (?, ?, ?)",
            (text, result, confidence),
        )


def get_history(limit=50):
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT text, result, confidence, timestamp
            FROM predictions
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def get_stats():
    with connect() as conn:
        total = conn.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
        fake = conn.execute("SELECT COUNT(*) FROM predictions WHERE lower(result) LIKE 'fake%'").fetchone()[0]
        real = conn.execute("SELECT COUNT(*) FROM predictions WHERE lower(result) LIKE 'real%'").fetchone()[0]
    return {"total": total, "fake": fake, "real": real}
