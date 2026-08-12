import arxiv
from datetime import datetime
from src.fetchers.base import RawItem

def fetch_arxiv(max_results: int = 20) -> list[RawItem]:
    """Fetch the latest AI-related papers from arXiv"""
    search = arxiv.Search(
        query="cat:cs.AI OR cat:cs.CL OR cat:cs.LG",
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    items = []
    client = arxiv.Client()
    for result in client.results(search):
        items.append(RawItem(
            source="arxiv",
            title=result.title,
            url=result.entry_id,
            summary=result.summary,
            published_at=result.published,
        ))
    return items