from pathlib import Path
from typing import TypedDict

import fitz  # PyMuPDF


class PageRecord(TypedDict):
    doc_name: str
    page_no: int
    text: str


def load_pdfs(pdf_dir: Path) -> list[PageRecord]:
    """Extract text per page from every PDF in pdf_dir."""
    records: list[PageRecord] = []

    for pdf_path in sorted(pdf_dir.glob("*.pdf")):
        with fitz.open(pdf_path) as doc:
            for page_index, page in enumerate(doc):
                text = page.get_text().strip()
                if not text:
                    continue
                records.append(
                    {
                        "doc_name": pdf_path.name,
                        "page_no": page_index + 1,
                        "text": text,
                    }
                )

    return records
