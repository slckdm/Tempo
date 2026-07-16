# Tempo — Frontend

React + TypeScript + Vite SPA for the Tempo music player. It talks to the
existing `management` (uploads), `metadata` (library read-model), and
`streaming` (playback) services, and to Keycloak.

## Features

- **Login** via Google (Keycloak identity brokering with Authorization Code +
  PKCE) or a Keycloak username/password. Real user accounts only — service
  accounts are rejected by the backend.
- **Upload** audio with drag & drop and live progress. Uses the backend's
  three-step flow: reserve upload → direct presigned PUT to MinIO → complete.
- **Library** sourced from the `metadata` service (title/artist/album/duration/
  cover), with search, format filter, and sorting.
- **Playback** with a full player bar: play/pause, prev/next, seek, volume,
  shuffle, and repeat.

## Running

The backend services and infra must be up first (see the repo root README):

```bash
# infra
cd starter && docker compose up -d

# management service  (port 8001)
cd management/src && ../.venv/bin/uvicorn app.main.start:service --port 8001

# streaming service   (port 8002)
cd streaming/src && ../.venv/bin/python -m app.main.start

# metadata service    (port 8003) — read-model for the library
cd metadata/src && ../.venv/bin/python -m app.main.start
# plus its consumer, which turns upload events into metadata rows:
cd metadata/src && ../.venv/bin/python -m app.main.consumer
```

Then the frontend:

```bash
cd frontend
npm install
npm run dev          # http://localhost:5173
```

Other scripts: `npm run build`, `npm run preview`, `npm run typecheck`.

## How it works with the backend (and its quirks)

This frontend was written without changing the backend. A few backend
characteristics shaped the design:

1. **No CORS headers** on any service. The Vite dev server proxies same-origin
   `/api/management`, `/api/metadata`, `/api/streaming`, and `/api/auth`
   (Keycloak) to the real services, so the browser never makes a cross-origin
   call. See `vite.config.ts`.
2. **Three services, three responsibilities.** Uploads go to `management`
   (`POST /uploads` → presigned PUT → complete). The library list comes from the
   `metadata` read-model (`GET /metadata`, already filtered to completed tracks,
   with server-side title/artist/album/genre filters + pagination). Playback and
   covers come from `streaming`. Because metadata is produced asynchronously by
   the metadata consumer, a freshly uploaded track appears in the library a
   moment after completion — the frontend re-polls `GET /metadata` a few times
   after each upload, and a manual refresh button is provided.
3. **Streaming requires a bearer token**, which `<audio src>` / `<img src>`
   can't send. Tracks and covers are fetched with the token and handed to the
   player as `blob:` URLs (`src/api/stream.ts`). Covers are fetched only when the
   metadata record reports one (`cover_key`); otherwise a deterministic gradient
   placeholder is shown.

> Note: `GET /metadata` is not scoped to the current user — every authenticated
> user sees all completed tracks. That is the backend's current behavior; the
> frontend just reflects it.

## Configuration

Everything defaults to the values in `management/.env` / `streaming/.env`, so it
runs with no setup. To override, copy `.env.example` to `.env`:

- `MANAGEMENT_URL`, `METADATA_URL`, `STREAMING_URL`, `KEYCLOAK_URL` — proxy targets.
- `VITE_KEYCLOAK_REALM`, `VITE_KEYCLOAK_CLIENT_ID`, `VITE_KEYCLOAK_CLIENT_SECRET`
  — the Keycloak realm/client used for login.
- `VITE_KEYCLOAK_PUBLIC_URL` — browser-reachable Keycloak URL used for the Google
  redirect (defaults to `http://localhost:8080`).
- `VITE_KEYCLOAK_GOOGLE_IDP_ALIAS` — Keycloak's Google identity-provider alias
  (defaults to `google`).

Google must be configured as an identity provider in the `tempo` realm. Put
the Google client id and secret in Keycloak, set the provider alias to `google`,
and add the frontend origin to the Keycloak client's valid redirect URIs and web
origins. The Google OAuth callback URI is Keycloak's broker endpoint:
`http://localhost:8080/realms/tempo/broker/google/endpoint`.

The Google client secret is server-side configuration. Do not expose it through
a `VITE_*` variable or copy it into the frontend bundle.

> The existing Keycloak client secret still lives in the frontend because that
> client is confidential and the password grant requires it. That is acceptable
> only for this local pet project; a production SPA should use a public Keycloak
> client with PKCE and no client secret.

## Project structure

```
src/
  api/        auth (Keycloak), fetch client (JSend), uploads, metadata, streaming
  context/    Auth, Library (metadata + upload orchestration), Player
  components/  Login, Header, UploadPanel, LibraryView, PlayerBar, Cover, UserAvatar, Icons
  lib/        formatting, audio-file detection
  config.ts   proxy bases + Keycloak defaults
  types.ts
```
