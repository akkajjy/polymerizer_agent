import requests
from datetime import datetime, timedelta
from src.fetchers.base import RawItem
from config import GITHUB_TOKEN

def fetch_github_trending(days: int = 1, min_stars: int = 50, max_results: int = 20) -> list[RawItem]:
    """search the recent update, high stars repo, simulate the trending"""
    date_filter = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"pushed:>{date_filter} stars:>{min_stars} topic:llm",
        "sort": "stars",
        "order": "desc",
        "per_page": max_results,
    }
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
    }

    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status() #if fail to request, throw the expection immediately, don't silently swallow up mistakes.

    items = []
    for repo in resp.json().get("items", []):
        items.append(RawItem(
            source="github",
            title=repo["full_name"],
            url=repo["html_url"],
            summary=repo["description"] or "",
            published_at=datetime.fromisoformat(repo["pushed_at"].rstrip("Z")),
        ))
    return items