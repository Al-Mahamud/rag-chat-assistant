import json

import faiss

from config import FAISS_INDEX_PATH, METADATA_STORE_PATH, PDF_DIR, VECTORSTORE_DIR
from ingestion.chunker import chunk_records
from ingestion.embedder import embed_texts
from ingestion.loader import load_pdfs


def build_index() -> tuple[int, int]:
    """Rebuild the FAISS index + metadata sidecar from every PDF in PDF_DIR.

    Full rebuild each run (not incremental) - simplest option for a small
    document set. Re-run this after adding/removing PDFs.

    Returns (pages_indexed, chunks_indexed).
    """
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    records = load_pdfs(PDF_DIR)
    if not records:
        raise ValueError(f"No PDF text found in {PDF_DIR}. Add PDFs and try again.")

    chunks = chunk_records(records)
    print(f"Loaded {len(records)} page(s) -> {len(chunks)} chunk(s)")

    embeddings = embed_texts([c["text"] for c in chunks])
    dim = embeddings.shape[1]

    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    faiss.write_index(index, str(FAISS_INDEX_PATH))

    with open(METADATA_STORE_PATH, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk) + "\n")

    print(f"Indexed {index.ntotal} vector(s) -> {FAISS_INDEX_PATH}")
    return len(records), len(chunks)


if __name__ == "__main__":
    try:
        build_index()
    except ValueError as e:
        raise SystemExit(str(e))
