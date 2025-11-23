# connecting-spark-express-with-rpc

FastAPI + gRPC gateway in front of a Spark analysis engine, paired with a Svelte client. The `spark_api` package exposes Spark capabilities over gRPC, the `service` package offers an HTTP/RPC layer (serving both JSON APIs and the UI), and `client_app` contains the SPA.

## Repository layout

```
├── spark_api/      # gRPC server exposing Spark operations
├── service/        # FastAPI app proxying requests to the gRPC layer
├── client_app/     # SvelteKit frontend bundled and hosted by FastAPI
├── data/           # Sample datasets (e.g., parquet files)
├── docs/           # Project documentation
└── protos/         # Protobuf definitions shared between services
```

Good dataset for testing: <https://www.kaggle.com/datasets/wotschofsky/171-million-domain-names-whois-dns-dnssec>

## Prerequisites

- Python 3.11 (the `pyproject.toml` files pin `==3.11.10`)
- Node.js 20.x + npm 10.x for the frontend build
- [uv](https://github.com/astral-sh/uv) if you plan to use the provided `start-backend.sh` script (otherwise create a venv manually)
- Java 17 if you run Spark locally outside the Docker image

## Backend installation

Install both Python packages in editable mode (run from repository root):

```bash
cd spark_api && pip install --editable .
cd ../service && pip install --editable .
```

This installs the gRPC server and HTTP service dependencies into your active environment.

## Frontend build pipeline

The FastAPI service serves the compiled Svelte client from `client_app/build`. Build steps:

1. Install dependencies: `cd client_app && npm install`.
2. (Optional) Run `npm run dev` for local hot-reload (API base defaults to `http://localhost:4444`).
3. Generate the production bundle: `npm run build`. The output lands in `client_app/build` and is consumed by the FastAPI static mount.

`./start-backend.sh` automatically runs `npm run build` before launching the Python services so the UI is always in sync.

## Running everything locally

```bash
./start-backend.sh
```

This script rebuilds the frontend, starts the Spark gRPC server (`spark_api/main.py`) and the FastAPI app (`service/main.py`). When it finishes booting you can:

- Open the UI at <http://localhost:4444>
- Hit the API docs at <http://localhost:4444/docs>
- Connect to the gRPC port directly on `localhost:50051` if needed

To stop the stack press `Ctrl+C`—the script traps signals and cleans up child processes.

## Docker image

Build and run the entire stack (Spark gRPC + FastAPI + Svelte UI) inside a single container:

```bash
docker build -t spark-express-rpc .
docker run --rm \
	-p 4444:4444 \
	-p 50051:50051 \
	spark-express-rpc
```

The Dockerfile performs a multi-stage build: Node compiles the frontend, and Python 3.11 + Java 17 run both services. The container exposes:

- `4444/tcp` – FastAPI HTTP endpoints + SPA
- `50051/tcp` – Spark gRPC endpoint

Mount extra data directories or pass env vars (`docker run -v $(pwd)/data:/app/data …`) if required.

## Testing

Inside each Python package you can run pytest:

```bash
cd service && uv run pytest
cd ../spark_api && uv run pytest
```

## Environment variables

- `SERVICE_PORT` (default `4444`) – FastAPI listen port when running through Docker
- `SPARK_RPC_PORT` (default `50051`) – gRPC server port when running through Docker

Adjust these when deploying to shared infrastructure or behind proxies.