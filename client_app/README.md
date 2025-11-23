# Client Application (SvelteKit)

This directory contains the UI served by the FastAPI backend. It is a SvelteKit application styled with Tailwind and bundled via the static adapter so the compiled assets can be copied into `client_app/build` and hosted directly by FastAPI.

## Prerequisites

- Node.js 20.x and npm 10.x

## Install dependencies

```bash
cd client_app
npm install
```

## Development server

```bash
npm run dev -- --open
```

By default the UI expects the API to run at `http://localhost:4444`. If your backend lives elsewhere, update `src/lib/clientApi.ts` so fetches hit the correct origin.

## Production build

```bash
npm run build
```

This writes the static bundle to `client_app/build`, which the FastAPI service mounts when serving the SPA. The build step is also executed automatically by `../start-backend.sh` and during the Docker image build.

To preview the optimized bundle locally run `npm run preview`.

## Linting & formatting

```bash
npm run lint
npm run format
```

