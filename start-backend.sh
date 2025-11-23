#!/bin/bash

set -euo pipefail

cleanup() {
    kill $(cat spark_api.pid 2>/dev/null) 2>/dev/null || true
    kill $(cat service.pid 2>/dev/null) 2>/dev/null || true
    rm -f spark_api.pid service.pid
}

trap cleanup EXIT INT TERM

# Build frontend assets for FastAPI
cd client_app
npm run build
cd ..

# Start services
cd spark_api
uv run python main.py &
echo $! > ../spark_api.pid

cd ..

cd service
uv run python main.py &
echo $! > ../service.pid

wait
