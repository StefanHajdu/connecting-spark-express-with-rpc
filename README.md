good dataset for testing: https://www.kaggle.com/datasets/wotschofsky/171-million-domain-names-whois-dns-dnssec


```bash
cd ./spark_api
pip install --editable .
```

### Frontend build pipeline

The FastAPI service now serves the Svelte client directly. To ensure the UI is available:

1. Install frontend dependencies once: `cd client_app && npm install`.
2. Build the static bundle with `npm run build`. This writes assets to `service/static/client`.
3. Run `./start-backend.sh` to rebuild the UI (script runs the build step automatically) and launch the Spark and API services. FastAPI will host the compiled bundle at the root path while all RPC endpoints remain under `/rpc/*`.