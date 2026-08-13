import sqlite3
from pathlib import Path
from src.fetchers.base import RawItem
import json

DB_PATH = Path(__file__).parent.parent.parent / "data" / "agent.db"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS raw_items(
        url TEXT PRIMARY KEY,
        source TEXT NOT NULL,
        title TEXT NOT NULL,
        summary TEXT,
        published_at TEXT NOT NULL,
        fetched_at TEXT NOT NULL,
        embedding TEXT
        )
""")
    # Compatible with the old databases you have already built: if the embedding column doesn't exist, add it. There is no need to delete the database and rebuild
    existing_cols = [row[1] for row in conn.execute("PRAGMA table_info(raw_items)").fetchall()]
    if "embedding" not in existing_cols:
        conn.execute("ALTER TABLE raw_items ADD COLUMN embedding TEXT")
    return conn

# def save_items(items: list[RawItem]) -> int:
#     """When stored in the database, duplicate urls are automatically skipped(physical deduplication). Return the actual number of new items added this time"""
#     conn = get_connection()
#     new_count = 0
#     for item in items:
#         cursor = conn.execute(
#             """INSERT OR IGNORE INTO raw_items
#             (url, source, title, summary, published_at, fetched_at)
#             VALUES (?, ?, ?, ?, ?, ?)""",
#             (item.url, item.source, item.title, item.summary,
#              item.published_at.isoformat(), item.fetched_at.isoformat())
#         )
#         if cursor.rowcount> 0:
#             new_count += 1
#     conn.commit()
#     conn.close()
#     return new_count

def save_item(item: RawItem, embedding: list[float]) -> bool:
    """return True means it really add into; False represents it's been skipped because of the url duplication"""
    conn = get_connection()
    cursor = conn.execute(
        """INSERT OR IGNORE INTO raw_items
           (url, source, title, summary, published_at, fetched_at, embedding)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (item.url, item.source, item.title, item.summary,
         item.published_at.isoformat(), item.fetched_at.isoformat(),
         json.dumps(embedding))
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def get_all_items() -> list[dict]:
    conn = get_connection()
    conn.row_factory = sqlite3.Row # Enable the query results to take values by column name instead of only by subscript
    rows = conn.execute("SELECT * FROM raw_items ORDER BY published_at DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]