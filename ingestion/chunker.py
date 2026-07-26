from typing import TypedDict

from config import CHUNK_OVERLAP_WORDS, CHUNK_SIZE_WORDS
from ingestion.loader import PageRecord


class Chunk(TypedDict):
    chunk_id: str
    doc_name: str
    page_no: int
    text: str


def _split_words(words: list[str], size: int, overlap: int) -> list[list[str]]:
    if size <= overlap:
        raise ValueError("CHUNK_SIZE_WORDS must be greater than CHUNK_OVERLAP_WORDS")

    step = size - overlap
    windows = []
    for start in range(0, len(words), step):
        window = words[start : start + size]
        if window:
            windows.append(window)
        if start + size >= len(words):
            break
    return windows


def chunk_records(
    records: list[PageRecord],
    chunk_size_words: int = CHUNK_SIZE_WORDS,
    chunk_overlap_words: int = CHUNK_OVERLAP_WORDS,
) -> list[Chunk]:
    """Split each page's text into overlapping word-based chunks."""
    chunks: list[Chunk] = []

    for record in records:
        words = record["text"].split()
        word_windows = _split_words(words, chunk_size_words, chunk_overlap_words)

        for local_index, window in enumerate(word_windows):
            chunk_id = f"{record['doc_name']}::p{record['page_no']}::c{local_index}"
            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "doc_name": record["doc_name"],
                    "page_no": record["page_no"],
                    "text": " ".join(window),
                }
            )

    return chunks
