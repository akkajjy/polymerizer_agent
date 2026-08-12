from src.fetchers.arxiv_fetcher import fetch_arxiv
from src.fetchers.github_fetcher import fetch_github_trending

if __name__ == "__main__":
    print("=== arXiv ===")
    for item in fetch_arxiv(max_results=3):
        print(f"[{item.source}] {item.title}")

    print("=== Github ===")
    for item in fetch_github_trending(max_results=5):
        print(f"[{item.source}] {item.title} ({item.url})")

        