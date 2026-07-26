import json

import faiss

from config import FAISS_INDEX_PATH, METADATA_STORE_PATH, MIN_SIMILARITY_SCORE, TOP_K
from ingestion.embedder import embed_texts


def _load_index_and_metadata():
    index = faiss.read_index(str(FAISS_INDEX_PATH))
    with open(METADATA_STORE_PATH, encoding="utf-8") as f:
        metadata = [json.loads(line) for line in f]
    return index, metadata


def retrieve(query: str, k: int = TOP_K) -> list[dict]:
    """Embed the query and return the top-k most similar chunks, each with a similarity score."""
    if not FAISS_INDEX_PATH.exists() or not METADATA_STORE_PATH.exists():
        raise FileNotFoundError(
            "Vector index not found. Run 'python -m ingestion.build_index' first."
        )

    index, metadata = _load_index_and_metadata()
    query_vec = embed_texts([query])
    scores, indices = index.search(query_vec, k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        chunk = metadata[idx]
        results.append({**chunk, "score": float(score)})
    return results


def filter_relevant(chunks: list[dict], min_score: float = MIN_SIMILARITY_SCORE) -> list[dict]:
    """Drop chunks whose similarity score is too low to be a real match."""
    return [c for c in chunks if c["score"] >= min_score]
