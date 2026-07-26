import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# Paths
PDF_DIR = BASE_DIR / "data" / "pdfs"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"
FAISS_INDEX_PATH = VECTORSTORE_DIR / "index.faiss"
METADATA_STORE_PATH = VECTORSTORE_DIR / "metadata.jsonl"

# Chunking (measured in words, used as a proxy for tokens)
CHUNK_SIZE_WORDS = 500
CHUNK_OVERLAP_WORDS = 75

# Embedding model (local, via sentence-transformers)
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Retrieval
TOP_K = 4
MIN_SIMILARITY_SCORE = 0.25  # chunks scoring below this are treated as irrelevant

# LLM (Groq)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.2

# API
API_HOST = "127.0.0.1"
API_PORT = 8000

# Deployment (multi-host / production)
BACKEND_URL = os.getenv("BACKEND_URL", f"http://{API_HOST}:{API_PORT}")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "*")
BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME", "")
BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD", "")
