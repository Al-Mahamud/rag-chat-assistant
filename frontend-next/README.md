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

## Local development

```bash
npm install
npm run dev
```

Opens at [http://localhost:3000](http://localhost:3000).

## Note on Next.js version

This project was scaffolded on Next.js 16, which renamed `middleware.ts` to `proxy.ts` (Proxy now defaults to the Node.js runtime) and made other breaking changes versus older Next.js docs/training data. Check `node_modules/next/dist/docs/` for the version actually installed before assuming an API works a certain way.
