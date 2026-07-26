from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str


class SourceCitation(BaseModel):
    doc_name: str
    page_no: int
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceCitation]


class UploadResponse(BaseModel):
    filename: str
    pages_indexed: int
    chunks_indexed: int
