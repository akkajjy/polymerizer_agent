from src.fetchers.arxiv_fetcher import fetch_arxiv
from src.fetchers.github_fetcher import fetch_github_trending
from src.storage.db import save_item, get_all_items
from src.pipeline.dedup import get_recent_embeddings, find_duplicate
from src.pipeline.embeddings import compute_embedding


# if __name__ == "__main__":
#     print("=== arXiv ===")
#     for item in fetch_arxiv(max_results=3):
#         print(f"[{item.source}] {item.title}")

#     print("=== Github ===")
#     for item in fetch_github_trending(max_results=5):
#         print(f"[{item.source}] {item.title} ({item.url})")

# if __name__ == "__main__":
#     all_items = []
#     all_items += fetch_arxiv(max_results=5)
#     all_items += fetch_github_trending(max_results=5)        

#     new_count = save_items(all_items)
#     print(f"This time, {len(all_items)} items are collected, and {new_count} items are newly added to the database")

#     total = len(get_all_items())
#     print(f"there are {total} records in the database")

if __name__ == "__main__":
    all_items = fetch_arxiv(max_results=5) + fetch_github_trending(max_results=5)

    existing = get_recent_embeddings()
    new_count, semantic_dup_count, physical_dup_count = 0, 0, 0

    for item in all_items:
        vec = compute_embedding(f"{item.title} {item.summary}")
        dup_url = find_duplicate(vec, existing)

        if dup_url:
            semantic_dup_count += 1
            print(f"[语义重复，跳过] {item.title}  (相似于: {dup_url})")
            continue

        if save_item(item, vec):
            new_count += 1
            existing.append((item.url, vec))
        else:
            physical_dup_count += 1
            print(f"[URL已存在，跳过] {item.title}")

    total_checked = new_count + semantic_dup_count + physical_dup_count
    print(f"\n本次采集 {len(all_items)} 条 = 新增 {new_count} + 语义重复 {semantic_dup_count} + URL重复 {physical_dup_count}")
    assert total_checked == len(all_items), "数字对不上，说明有分支没被追踪到！"
    print(f"数据库当前共有 {len(get_all_items())} 条记录")