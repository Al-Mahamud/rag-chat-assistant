SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions using ONLY the "
    "provided context from internal company documents. "
    "If the context does not contain enough information to answer, say "
    "you don't know instead of guessing or using outside knowledge. "
    "Whenever you state a fact from the context, cite its source in the "
    "format (source: <doc_name>, p.<page_no>)."
)


def build_context(chunks: list[dict]) -> str:
    parts = [
        f"[Source: {c['doc_name']}, p.{c['page_no']}]\n{c['text']}" for c in chunks
    ]
    return "\n\n---\n\n".join(parts)


def build_messages(query: str, chunks: list[dict]) -> list[dict]:
    context = build_context(chunks)
    user_prompt = (
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        "Answer using only the context above, with source citations."
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
