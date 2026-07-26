from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL_NAME


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def embed_texts(texts: list[str]) -> np.ndarray:
    """Embed a list of texts into L2-normalized float32 vectors (for cosine similarity via inner product)."""
    model = get_embedding_model()
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return embeddings.astype("float32")
