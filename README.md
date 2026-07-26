# Company Document Assistant (RAG Chat)

A chat assistant that answers questions grounded in your company's internal PDF documents, using retrieval-augmented generation (RAG). Embeddings run locally (free, no rate limits); answers are generated via the Groq API (free tier).

## Stack

- **PDF parsing**: PyMuPDF
- **Embeddings**: `sentence-transformers` (`all-MiniLM-L6-v2`), local
- **Vector store**: FAISS, persisted to disk
- **LLM**: Groq API (`llama-3.3-70b-versatile`)
- **Backend**: FastAPI
- **Frontend**: Streamlit

## Setup

1. **Create a virtual environment and install dependencies**

   ```powershell
   python -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

2. **Add your Groq API key**

   Copy `.env.example` to `.env` and fill in your key (get one free at [console.groq.com](https://console.groq.com)):

   ```
   GROQ_API_KEY=your_key_here
   ```

## Usage

1. **Add PDFs** — drop your company documents into `data/pdfs/`.

2. **Build the index**

   ```powershell
   .venv\Scripts\python.exe -m ingestion.build_index
   ```

   Re-run this any time you add or remove PDFs (it does a full rebuild).

3. **Start the backend API**

   ```powershell
   .venv\Scripts\python.exe -m uvicorn api.main:app --reload
   ```

   API docs available at `http://127.0.0.1:8000/docs`.

4. **Start the chat UI** (in a separate terminal)

   ```powershell
   .venv\Scripts\python.exe -m streamlit run frontend/app.py
   ```

   Opens at `http://localhost:8501`. You can also upload new PDFs directly from the sidebar — it calls the backend's `/upload` endpoint, which rebuilds the index automatically.

5. **Or use the terminal instead of the UI**

   ```powershell
   .venv\Scripts\python.exe -m rag.cli
   ```

## How it works

1. PDFs are split into overlapping chunks (~500 words, 75-word overlap), keeping track of source document and page number.
2. Each chunk is embedded locally and stored in a FAISS index alongside its metadata.
3. On each question, the query is embedded and matched against the index to retrieve the most relevant chunks.
4. Chunks scoring below a similarity threshold are discarded — if nothing relevant remains, the assistant answers "I don't know" without calling the LLM.
5. Remaining chunks are injected into a prompt that instructs the LLM to answer only from that context and cite sources; the answer is returned with citations (document name + page).

## Notes

- The vector index (`vectorstore/`) and `data/pdfs/` contents are gitignored — each deployment builds its own index from its own PDFs.
- If PyMuPDF fails to import on Windows with a `DLL load failed` error, install the [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe).

## Deployment

The app deploys as two separate Render Web Services, built from `Dockerfile.api` and `Dockerfile.frontend`, wired together by `render.yaml`.

### Architecture

- **`rag-chat-backend`** — FastAPI, `/health` (open), `/chat` and `/upload` (require Basic Auth). The embedding model is baked into the image at build time, and whatever PDFs are in `data/pdfs/` when the image is built are baked in too — the index is rebuilt from them on every container start.
- **`rag-chat-frontend`** — Streamlit, gated behind a login form using the same shared credentials, calls the backend via `BACKEND_URL`.

### Required environment variables

| Service | Variable | Notes |
|---|---|---|
| backend | `GROQ_API_KEY` | secret |
| backend | `BASIC_AUTH_USERNAME` / `BASIC_AUTH_PASSWORD` | secret — must match the frontend's values exactly |
| backend | `FRONTEND_ORIGIN` | the frontend's public URL, for CORS |
| frontend | `BACKEND_URL` | the backend's public URL |
| frontend | `BASIC_AUTH_USERNAME` / `BASIC_AUTH_PASSWORD` | secret — must match the backend's values exactly |

Secrets are entered directly in each Render service's **Environment** tab, never committed to git.

**Watch out:** if your chosen service name is already taken, Render assigns a random suffix (e.g. `rag-chat-backend-q3ja.onrender.com` instead of `rag-chat-backend.onrender.com`). Make sure `BACKEND_URL` and `FRONTEND_ORIGIN` reflect the *actual* assigned URLs, not the plain names — a mismatch here causes `/upload` and `/chat` to fail with a generic "Not Found".

### Free-tier storage tradeoff

This deployment runs on Render's **free tier with no persistent disk**, by design (to avoid the ~$7+/mo cost of a paid plan + disk). That means:

- `data/pdfs/` and the FAISS index live only in the container's ephemeral filesystem.
- On every redeploy, and on the free tier's idle spin-down/restart (~15 min of inactivity), the container resets to whatever PDFs were baked into the image at build time — anything uploaded via the UI afterward is lost.
- **To add documents permanently**, commit them into `data/pdfs/` in the repo before building/pushing the image, so they become part of the baseline every container starts with. PDFs uploaded through the running app are only available until the next restart.

If durability for ad-hoc uploads becomes a real need later, upgrade the backend service to a paid plan and attach a Render Persistent Disk, then point `PDF_DIR`/`VECTORSTORE_DIR` (in `config.py`) at the mounted disk path via env vars.

### Local Docker testing

Build and run each image locally before deploying:

```powershell
docker build -f Dockerfile.api -t rag-backend .
docker run -p 8000:8000 --env-file .env rag-backend

docker build -f Dockerfile.frontend -t rag-frontend .
docker run -p 8501:8501 --env-file .env -e BACKEND_URL=http://host.docker.internal:8000 rag-frontend
```
