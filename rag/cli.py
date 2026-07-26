from config import TOP_K
from rag.llm_client import generate_answer
from rag.prompt import build_messages
from rag.retriever import filter_relevant, retrieve

NO_RELEVANT_CONTENT_ANSWER = (
    "I don't know - I couldn't find anything relevant to that question in the "
    "indexed documents."
)


def ask(query: str) -> None:
    try:
        chunks = retrieve(query, k=TOP_K)
    except FileNotFoundError as e:
        print(f"\n{e}\n")
        return

    relevant_chunks = filter_relevant(chunks)
    if not relevant_chunks:
        print(f"\nAnswer:\n{NO_RELEVANT_CONTENT_ANSWER}\n")
        return

    messages = build_messages(query, relevant_chunks)
    try:
        answer = generate_answer(messages)
    except RuntimeError as e:
        print(f"\n{e}\n")
        return

    print(f"\nAnswer:\n{answer}\n")
    print("Retrieved from:")
    seen = set()
    for c in relevant_chunks:
        key = (c["doc_name"], c["page_no"])
        if key not in seen:
            seen.add(key)
            print(f"  - {c['doc_name']}, p.{c['page_no']} (score={c['score']:.3f})")


def main() -> None:
    print("RAG Chat Assistant (CLI) - type 'exit' to quit\n")
    while True:
        query = input("You: ").strip()
        if query.lower() in {"exit", "quit"}:
            break
        if not query:
            continue
        ask(query)


if __name__ == "__main__":
    main()
