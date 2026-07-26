import logging
from pathlib import Path

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile

from api.auth import require_auth
from api.schemas import ChatRequest, ChatResponse, SourceCitation, UploadResponse
from config import PDF_DIR, TOP_K
from ingestion.build_index import build_index
from rag.llm_client import generate_answer
from rag.prompt import build_messages
from rag.retriever import filter_relevant, retrieve

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Chat Assistant API")

NO_RELEVANT_CONTENT_ANSWER = (
    "I don't know - I couldn't find anything relevant to that question in the "
    "indexed documents."
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse, dependencies=[Depends(require_auth)])
def chat(request: ChatRequest) -> ChatResponse:
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query must not be empty.")

    logger.info("Chat query: %r", query)

    try:
        chunks = retrieve(query, k=TOP_K)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    relevant_chunks = filter_relevant(chunks)
    if not relevant_chunks:
        logger.info("No relevant chunks for query: %r", query)
        return ChatResponse(answer=NO_RELEVANT_CONTENT_ANSWER, sources=[])

    messages = build_messages(query, relevant_chunks)
    try:
        answer = generate_answer(messages)
    except RuntimeError as e:
        logger.error("LLM generation failed: %s", e)
        raise HTTPException(status_code=502, detail=str(e))

    seen = set()
    sources = []
    for c in relevant_chunks:
        key = (c["doc_name"], c["page_no"])
        if key not in seen:
            seen.add(key)
            sources.append(
                SourceCitation(doc_name=c["doc_name"], page_no=c["page_no"], score=c["score"])
            )

    logger.info("Chat answered with %d source(s)", len(sources))
    return ChatResponse(answer=answer, sources=sources)


@app.post("/upload", response_model=UploadResponse, dependencies=[Depends(require_auth)])
async def upload(file: UploadFile = File(...)) -> UploadResponse:
    filename = Path(file.filename or "").name
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    logger.info("Uploading %s", filename)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    dest = PDF_DIR / filename
    dest.write_bytes(await file.read())

    try:
        pages_indexed, chunks_indexed = build_index()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    logger.info("Indexed %s: %d page(s), %d chunk(s)", filename, pages_indexed, chunks_indexed)
    return UploadResponse(
        filename=filename, pages_indexed=pages_indexed, chunks_indexed=chunks_indexed
    )
