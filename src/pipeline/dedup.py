from datetime import datetime, timedelta
import json
from src.storage.db import get_connection

SIMILARITY_THRESHOLD = 0.85
LOOKBACK_DAYS = 7       #only compare with the content of the last 7 days to avoid the comparison getting slower as the library gets larger

def get_recent_embeddings() -> list[tuple[str, list[float]]]:
    conn = get_connection()
    cutoff = (datetime.now() - timedelta(days=LOOKBACK_DAYS)).isoformat()
    rows = conn.execute(
        "SELECT url, embedding FROM raw_items WHERE published_at > ? AND embedding IS NOT NULL",
        (cutoff,)
    ).fetchall()
    conn.close()
    return [(row[0], json.loads(row[1])) for row in rows]

def find_duplicate(new_vec: list[float], existing: list[tuple[str, list[float]]]) -> str | None:
    from src.pipeline.embeddings import cosine_similarity
    for url, vec in existing:
        if cosine_similarity(new_vec, vec) >= SIMILARITY_THRESHOLD:
            return url
    return None



