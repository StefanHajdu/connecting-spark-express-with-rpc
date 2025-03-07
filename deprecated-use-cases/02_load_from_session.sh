curl -X POST http://localhost:4444/createSession \
    -H 'Content-Type: application/json' \
    -d '{"id": "0000"}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/load \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "df_path": "/home/stephenx/Documents/Datasets/domains_sub_test.csv", "df_type": "csv"}' \
    -w '\nTotal: %{time_total}s\n'

# curl -X POST http://localhost:4444/addSql \
#     -H 'Content-Type: application/json' \
#     -d '{"session_id": "0000", "node_id": "n0001", "previous_node_id": "0000-0000-0000", "query": "select * from {df} where tld = '\''com'\''", "query_type": "filter", "query_params_json": ["df"]}' \
#     -w '\nTotal: %{time_total}s\n'

echo "1"
curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "0000-0000-0000"}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/createSession \
    -H 'Content-Type: application/json' \
    -d '{"id": "0001"}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/loadFromSession \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0001", "input_session_id": "0000"}' \
    -w '\nTotal: %{time_total}s\n'

echo "2"
curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0001", "node_id": "0000-0000-0000"}' \
    -w '\nTotal: %{time_total}s\n'

echo "1 == 2"