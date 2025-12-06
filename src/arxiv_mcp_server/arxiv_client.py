"""arXiv API client wrapper."""

import re
import arxiv
from dataclasses import dataclass


@dataclass
class Paper:
    """Represents an arXiv paper."""
    id: str
    title: str
    authors: list[str]
    abstract: str
    published: str
    pdf_url: str
    categories: list[str]


def extract_arxiv_id(query: str) -> str | None:
    """Extract arXiv ID from query if present."""
    # Patterns: 2401.12345, arXiv:2401.12345, etc.
    patterns = [
        r"(\d{4}\.\d{4,5})",  # 2401.12345
        r"arxiv[:\s]*(\d{4}\.\d{4,5})",  # arXiv:2401.12345
    ]
    for pattern in patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def search_papers(query: str, max_results: int = 10) -> list[Paper]:
    """Search arXiv papers by query or ID."""
    arxiv_id = extract_arxiv_id(query)

    if arxiv_id:
        # Direct ID lookup
        client = arxiv.Client()
        search = arxiv.Search(id_list=[arxiv_id])
        results = list(client.results(search))
    else:
        # Keyword search
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )
        results = list(client.results(search))

    papers = []
    for result in results:
        paper = Paper(
            id=result.entry_id.split("/")[-1],
            title=result.title,
            authors=[author.name for author in result.authors],
            abstract=result.summary,
            published=result.published.strftime("%Y-%m-%d"),
            pdf_url=result.pdf_url,
            categories=result.categories,
        )
        papers.append(paper)

    return papers


def download_pdf(paper: Paper, save_path: str) -> str:
    """Download paper PDF to specified path."""
    import urllib.request
    urllib.request.urlretrieve(paper.pdf_url, save_path)
    return save_path
