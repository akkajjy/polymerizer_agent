from src.fetchers.arxiv_fetcher import fetch_arxiv
from src.fetchers.github_fetcher import fetch_github_trending
from src.storage.db import save_items, get_all_items


# if __name__ == "__main__":
#     print("=== arXiv ===")
#     for item in fetch_arxiv(max_results=3):
#         print(f"[{item.source}] {item.title}")

#     print("=== Github ===")
#     for item in fetch_github_trending(max_results=5):
#         print(f"[{item.source}] {item.title} ({item.url})")

if __name__ == "__main__":
    all_items = []
    all_items += fetch_arxiv(max_results=5)
    all_items += fetch_github_trending(max_results=5)        

    new_count = save_items(all_items)
    print(f"This time, {len(all_items)} items are collected, and {new_count} items are newly added to the database")

    total = len(get_all_items())
    print(f"there are {total} records in the database")