"""PDF text extraction using PyMuPDF."""

import fitz  # pymupdf


def extract_text(pdf_path: str) -> str:
    """Extract all text from PDF."""
    doc = fitz.open(pdf_path)
    text_parts = []

    for page in doc:
        text_parts.append(page.get_text())

    doc.close()
    return "\n".join(text_parts)


def extract_section(full_text: str, section: str) -> str:
    """Extract a specific section from paper text.

    Sections: abstract, introduction, method, conclusion, references
    """
    section = section.lower()
    text_lower = full_text.lower()

    # Section markers
    section_markers = {
        "abstract": (["abstract"], ["introduction", "1.", "1 "]),
        "introduction": (["introduction", "1."], ["2.", "2 ", "related work", "background"]),
        "method": (["method", "approach", "3."], ["experiment", "4.", "result"]),
        "conclusion": (["conclusion", "discussion"], ["reference", "acknowledge"]),
        "references": (["reference"], []),
    }

    if section not in section_markers:
        return full_text

    start_markers, end_markers = section_markers[section]

    # Find start
    start_idx = 0
    for marker in start_markers:
        idx = text_lower.find(marker)
        if idx != -1:
            start_idx = idx
            break

    # Find end
    end_idx = len(full_text)
    for marker in end_markers:
        idx = text_lower.find(marker, start_idx + 1)
        if idx != -1 and idx < end_idx:
            end_idx = idx

    return full_text[start_idx:end_idx].strip()
