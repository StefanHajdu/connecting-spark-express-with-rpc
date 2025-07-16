#!/bin/bash

cleanup() {
    kill $(cat spark_api.pid 2>/dev/null) 2>/dev/null || true
    kill $(cat web_api.pid 2>/dev/null) 2>/dev/null || true
    rm -f spark_api.pid web_api.pid
}

trap cleanup EXIT INT TERM

# Start services
cd spark_api/src
PYTHONPATH="$(pwd)/../lib:$(pwd)" python main.py &
echo $! > ../../spark_api.pid
cd ../../web_api
npm run dev &
echo $! > ../web_api.pid
cd ..

wait
