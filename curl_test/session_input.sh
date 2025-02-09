curl -X POST http://localhost:4444/createSession \
    -H 'Content-Type: application/json' \
    -d '{"id": "0001"}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/loadFromSession \
    -H 'Content-Type: application/json' \
    -d '{"id": "0001", "input_id": "0000"}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"id": "0001"}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/sql \
    -H 'Content-Type: application/json' \
    -d '{"id": "0001", "parametrized_query": "select * from {df} where registrar = '\''GoDaddy.com, LLC'\''", "query_name": "filter", "params_json": ["df"]}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"id": "0001"}' \
    -w '\nTotal: %{time_total}s\n'