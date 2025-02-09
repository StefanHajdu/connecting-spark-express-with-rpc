curl -X POST http://localhost:4444/createSession \
    -H 'Content-Type: application/json' \
    -d '{"id": "0000"}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/load \
    -H 'Content-Type: application/json' \
    -d '{"id": "0000", "df_path": "/home/stephenx/Documents/Datasets/domains_sub_test.csv", "df_type": "csv"}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/sql \
    -H 'Content-Type: application/json' \
    -d '{"id": "0000", "parametrized_query": "select * from {df} where registrar = '\''GoDaddy.com, LLC'\'' OR registrar = '\''Wix.com Ltd.'\'' OR registrar = '\''unknown'\''", "query_name": "filter", "params_json": ["df"]}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"id": "0000"}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/sql \
    -H 'Content-Type: application/json' \
    -d '{"id": "0000", "parametrized_query": "select * from {df} where registrar = '\''unknown'\''", "query_name": "filter", "params_json": ["df"]}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"id": "0000"}' \
    -w '\nTotal: %{time_total}s\n'