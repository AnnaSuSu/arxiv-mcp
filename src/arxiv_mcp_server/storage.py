"""Local storage management for downloaded papers."""

import json
from pathlib import Path
from dataclasses import asdict

from .arxiv_client import Paper


class PaperStorage:
    """Manages local storage of downloaded papers."""

    def __init__(self, storage_dir: str | Path):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.storage_dir / "metadata.json"
        self._metadata: dict[str, dict] = self._load_metadata()

    def _load_metadata(self) -> dict[str, dict]:
        if self.metadata_file.exists():
            return json.loads(self.metadata_file.read_text())
        return {}

    def _save_metadata(self):
        self.metadata_file.write_text(json.dumps(self._metadata, indent=2))

    def get_pdf_path(self, paper_id: str) -> Path:
        # Replace / with _ for old-style IDs like hep-th/9901001
        safe_id = paper_id.replace("/", "_")
        return self.storage_dir / f"{safe_id}.pdf"

    def get_text_path(self, paper_id: str) -> Path:
        safe_id = paper_id.replace("/", "_")
        return self.storage_dir / f"{safe_id}.txt"

    def has_paper(self, paper_id: str) -> bool:
        return paper_id in self._metadata

    def has_text(self, paper_id: str) -> bool:
        return self.get_text_path(paper_id).exists()

    def save_paper_metadata(self, paper: Paper):
        self._metadata[paper.id] = asdict(paper)
        self._save_metadata()

    def save_text(self, paper_id: str, text: str):
        self.get_text_path(paper_id).write_text(text)

    def get_text(self, paper_id: str) -> str | None:
        text_path = self.get_text_path(paper_id)
        if text_path.exists():
            return text_path.read_text()
        return None

    def get_paper_metadata(self, paper_id: str) -> dict | None:
        return self._metadata.get(paper_id)

    def list_papers(self) -> list[dict]:
        return list(self._metadata.values())
