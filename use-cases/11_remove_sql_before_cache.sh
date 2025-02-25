curl -X POST http://localhost:4444/createSession \
    -H 'Content-Type: application/json' \
    -d '{"id": "0000"}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/load \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "df_path": "/home/stephenx/Documents/Datasets/domains_sub_test.csv", "df_type": "csv"}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/addSql \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0001", "previous_node_id": "0000-0000-0000", "query": "select * from {df} where tld = '\''com'\''", "query_type": "filter", "query_params_json": ["df"]}' \
    -w '\nTotal: %{time_total}s\n\n'


curl -X POST http://localhost:4444/addSql \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0002", "previous_node_id": "n0001", "query": "select * from {df} where registrar = '\''GoDaddy.com, LLC'\'' OR registrar = '\''NameCheap, Inc.'\'' OR registrar = '\''unknown'\''", "query_type": "filter", "query_params_json": ["df"]}' \
    -w '\nTotal: %{time_total}s\n\n'

echo "0000 | n0001 + n0002 summarize"
curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0002"}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/removeSql \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0001", "temp": false}' \
    -w '\nTotal: %{time_total}s\n\n'

echo "0001 | n0002 summarize"
curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0002"}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/removeSql \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0002", "temp": false}' \
    -w '\nTotal: %{time_total}s\n\n'

echo "0002 | 0000-0000-0000 summarize"
curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0002"}' \
    -w '\nTotal: %{time_total}s\n\n'

echo "* 0000 < 0001 < 0002"