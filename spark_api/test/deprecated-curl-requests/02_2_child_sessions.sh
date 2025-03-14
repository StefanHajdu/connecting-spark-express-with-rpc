# 0000
curl -X POST http://localhost:4444/createSession \
    -H 'Content-Type: application/json' \
    -d '{"id": "0000"}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/load \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "df_path": "/home/stephenx/Documents/Datasets/domains_sub_test.csv", "df_type": "csv"}' \
    -w '\nTotal: %{time_total}s\n\n'

# 0001
curl -X POST http://localhost:4444/createSession \
    -H 'Content-Type: application/json' \
    -d '{"id": "0001"}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/loadFromSession \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0001", "input_session_id": "0000"}' \
    -w '\nTotal: %{time_total}s\n\n'

# 0002
curl -X POST http://localhost:4444/createSession \
    -H 'Content-Type: application/json' \
    -d '{"id": "0002"}' \
    -w '\nTotal: %{time_total}s\n\n'

echo "6. load from session 0001"
curl -X POST http://localhost:4444/loadFromSession \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0002", "input_session_id": "0001"}' \
    -w '\nTotal: %{time_total}s\n\n'

# add sql 0000
curl -X POST http://localhost:4444/addSql \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0001", "prev_node_id": "0000-0000-0000", "query": "select * from {df} where tld = '\''org'\''", "query_name": "filter", "query_params_json": ["df"]}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0001"}' \
    -w '\nTotal: %{time_total}s\n\n'

# add sql 0001
curl -X POST http://localhost:4444/addSql \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0001", "node_id": "n0001", "prev_node_id": "0000-0000-0000", "query": "select * from {df} where registrar = '\''GoDaddy.com, LLC'\'' OR registrar = '\''NameCheap, Inc.'\'' OR registrar = '\''unknown'\''", "query_name": "filter", "query_params_json": ["df"]}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0001", "node_id": "n0001"}' \
    -w '\nTotal: %{time_total}s\n\n'

# add sql 0002
curl -X POST http://localhost:4444/addSql \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0002", "node_id": "n0001", "prev_node_id": "0000-0000-0000", "query": "select * from {df} where registrar = '\''NameCheap, Inc.'\''", "query_name": "filter", "query_params_json": ["df"]}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0002", "node_id": "n0001"}' \
    -w '\nTotal: %{time_total}s\n\n'

# rebuild
echo "rebuild 0001"
curl -X POST http://localhost:4444/rebuildSession/0001 \
    -w '\nTotal: %{time_total}s\n\n'

echo "rebuild 0002"
curl -X POST http://localhost:4444/rebuildSession/0002 \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0001", "node_id": "n0001"}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0002", "node_id": "n0001"}' \
    -w '\nTotal: %{time_total}s\n\n'