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
