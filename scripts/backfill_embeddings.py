from src.storage.db import get_connection
from src.pipeline.embeddings import compute_embedding
import json

def backfill():
    conn = get_connection()
    rows = conn.execute(
        "SELECT url, title, summary FROM raw_items WHERE embedding IS NULL"
    ).fetchall()
    print(f"发现 {len(rows)} 条缺失 embedding 的记录，开始补齐...")
    for url, title, summary in rows:
        vec = compute_embedding(f"{title} {summary or ''}")
        conn.execute("UPDATE raw_items SET embedding = ? WHERE url = ?", (json.dumps(vec), url))
    conn.commit()
    conn.close()
    print("补齐完成")

if __name__ == "__main__":
    backfill()