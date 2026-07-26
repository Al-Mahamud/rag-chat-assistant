# Company Document Assistant — Next.js Frontend

A Next.js replacement for the Streamlit frontend (`../frontend/`), talking to the same FastAPI backend. The browser never sees the backend's Basic Auth credentials — all backend calls happen server-side through this app's own Route Handlers.

## Relationship to `../frontend/`

The Streamlit app keeps running unchanged during development of this app. Nothing here modifies `../api/` or `../frontend/`. See the root `README.md`'s Deployment section for the overall system architecture; this file only covers the Next.js app.

## Environment variables

Copy `.env.local.example` to `.env.local` and fill in:

- `BACKEND_URL` — the FastAPI backend's URL (server-only)
- `BASIC_AUTH_USERNAME` / `BASIC_AUTH_PASSWORD` — must match the backend's values exactly (server-only)
- `SESSION_SECRET` — a random secret for signing this app's own session cookie, unrelated to the pair above

None of these are prefixed `NEXT_PUBLIC_` — they must never be exposed to the browser bundle.

## CORS on the backend

The FastAPI backend (`../api/main.py`) has CORS restricted to `FRONTEND_ORIGIN`, originally set up for the Streamlit frontend which also called it server-side. With this Next.js app, backend calls happen server-to-server from `/api/chat` and `/api/upload` (Vercel's servers, not the browser) — so the browser never makes a cross-origin request to the backend directly, and CORS is no longer the thing protecting those endpoints (Basic Auth still is). Left as-is: zero cost to keep, and it doesn't block anything in this architecture.

## Local development

```bash
npm install
cp .env.local.example .env.local   # then fill in the values
npm run dev
```

Opens at [http://localhost:3000](http://localhost:3000).

### Two ways to point `BACKEND_URL`

- **Against a local backend** (for testing changes to `../api/` together with this app): run the FastAPI backend locally (`uvicorn api.main:app --reload` from the repo root, with its own `.env` set up per the root README), and set `BACKEND_URL=http://localhost:8000` in `.env.local`.
- **Against the deployed backend** (for testing this app against real production data without running Python locally): set `BACKEND_URL=https://rag-chat-backend-q3ja.onrender.com` in `.env.local`. `BASIC_AUTH_USERNAME`/`BASIC_AUTH_PASSWORD` must match whatever is set on that Render service.

## Note on Next.js version

This project was scaffolded on Next.js 16, which renamed `middleware.ts` to `proxy.ts` (Proxy now defaults to the Node.js runtime) and made other breaking changes versus older Next.js docs/training data. Check `node_modules/next/dist/docs/` for the version actually installed before assuming an API works a certain way.
