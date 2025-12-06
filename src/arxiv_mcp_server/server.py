"""arXiv MCP Server - Search and read arXiv papers."""

import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .arxiv_client import search_papers, download_pdf, Paper
from .pdf_parser import extract_text, extract_section
from .storage import PaperStorage

# Initialize storage
STORAGE_DIR = Path(os.environ.get("ARXIV_STORAGE_DIR", Path.home() / ".arxiv-mcp" / "papers"))
storage = PaperStorage(STORAGE_DIR)

# Create MCP server
mcp = FastMCP("arxiv-mcp-server")


@mcp.tool()
def search(query: str, max_results: int = 10) -> str:
    """Search arXiv papers by title, keywords, or arXiv ID.

    Args:
        query: Search query (title, keywords, or arXiv ID like 2401.12345)
        max_results: Maximum number of results to return (default: 10)

    Returns:
        List of matching papers with ID, title, authors, and abstract
    """
    papers = search_papers(query, max_results)

    if not papers:
        return "No papers found."

    results = []
    for p in papers:
        authors = ", ".join(p.authors[:3])
        if len(p.authors) > 3:
            authors += " et al."

        results.append(
            f"**{p.id}**: {p.title}\n"
            f"Authors: {authors}\n"
            f"Published: {p.published}\n"
            f"Abstract: {p.abstract[:300]}...\n"
        )

    return "\n---\n".join(results)


@mcp.tool()
def get_paper(paper_id: str, section: str = "all") -> str:
    """Get the full text of an arXiv paper.

    Args:
        paper_id: arXiv paper ID (e.g., "2401.12345")
        section: Which section to return: "all", "abstract", "introduction", "method", "conclusion"

    Returns:
        The paper text (full or specified section)
    """
    # Check cache first
    cached_text = storage.get_text(paper_id)
    if cached_text:
        if section == "all":
            return cached_text
        return extract_section(cached_text, section)

    # Search for the paper
    papers = search_papers(paper_id, max_results=1)
    if not papers:
        return f"Paper {paper_id} not found."

    paper = papers[0]

    # Download PDF
    pdf_path = storage.get_pdf_path(paper_id)
    try:
        download_pdf(paper, str(pdf_path))
    except Exception as e:
        return f"Failed to download paper: {e}"

    # Extract text
    try:
        full_text = extract_text(str(pdf_path))
    except Exception as e:
        return f"Failed to extract text from PDF: {e}"

    # Cache results
    storage.save_paper_metadata(paper)
    storage.save_text(paper_id, full_text)

    if section == "all":
        return full_text
    return extract_section(full_text, section)


@mcp.tool()
def list_downloaded_papers() -> str:
    """List all locally downloaded papers.

    Returns:
        List of downloaded papers with their metadata
    """
    papers = storage.list_papers()

    if not papers:
        return "No papers downloaded yet."

    results = []
    for p in papers:
        authors = ", ".join(p["authors"][:3])
        if len(p["authors"]) > 3:
            authors += " et al."

        results.append(f"**{p['id']}**: {p['title']}\nAuthors: {authors}")

    return "\n---\n".join(results)


def main():
    """Run the arXiv MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
