#!/bin/bash

cleanup() {
    kill $(cat spark_api.pid 2>/dev/null) 2>/dev/null || true
    kill $(cat service.pid 2>/dev/null) 2>/dev/null || true
    rm -f spark_api.pid service.pid
}

trap cleanup EXIT INT TERM

# Start services
cd spark_api/src
uv run python main.py &
echo $! > ../../spark_api.pid
cd ../../service
uv run python main.py &
echo $! > ../service.pid
cd ..

wait
