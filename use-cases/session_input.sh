curl -X POST http://localhost:4444/createSession -H 'Content-Type: application/json' -d '{"id": "0000"}' -w '\nTotal: %{time_total}s\n'
curl -X POST http://localhost:4444/load -H 'Content-Type: application/json' -d '{"id": "0000", "df_path": "/home/stephenx/Documents/Datasets/domains_sub_test.csv", "df_type": "csv"}' -w '\nTotal: %{time_total}s\n'
curl -X POST http://localhost:4444/preview -H 'Content-Type: application/json' -d '{"id": "0000", "limit": 12}' -N -w '\nTotal: %{time_total}s\n'

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