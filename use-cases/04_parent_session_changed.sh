curl -X POST http://localhost:4444/createSession \
    -H 'Content-Type: application/json' \
    -d '{"id": "0000"}' \
    -w '\nTotal: %{time_total}s\n\n'

echo 1. confirm load:
curl -X POST http://localhost:4444/load \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "df_path": "/home/stephenx/Documents/Datasets/domains_sub_test.csv", "df_type": "csv"}' \
    -w '\nTotal: %{time_total}s\n\n'

echo "2. filter session 0000 for tld == .com OR .org"
curl -X POST http://localhost:4444/addSql \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0001", "previous_node_id": "0000-0000-0000", "query": "select * from {df} where tld = '\''com'\'' OR tld = '\''org'\''", "query_name": "filter", "query_params_json": ["df"]}' \
    -w '\nTotal: %{time_total}s\n\n'

echo "2.1 summarize session 0000 for tld == .com OR .org"
curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"id": "0000"}' \
    -w '\nTotal: %{time_total}s\n\n'

echo "3. filter session 0000 for registrar == GoDaddy.com, LLC, NameCheap, Inc., unknown"
curl -X POST http://localhost:4444/addSql \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0002", "previous_node_id": "n0001", "query": "select * from {df} where registrar = '\''GoDaddy.com, LLC'\'' OR registrar = '\''NameCheap, Inc.'\'' OR registrar = '\''unknown'\''", "query_name": "filter", "query_params_json": ["df"]}' \
    -w '\nTotal: %{time_total}s\n\n'

echo "3.1 summarize session 0000 for registrar == GoDaddy.com, LLC, NameCheap, Inc., unknown"
curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"id": "0000"}' \
    -w '\nTotal: %{time_total}s\n\n'

echo "4. create session 0001"
curl -X POST http://localhost:4444/createSession \
    -H 'Content-Type: application/json' \
    -d '{"id": "0001"}' \
    -w '\nTotal: %{time_total}s\n\n'

echo "5. load from session 0000"
curl -X POST http://localhost:4444/loadFromSession \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0001", "input_id": "0000"}' \
    -w '\nTotal: %{time_total}s\n\n'

echo "5.1 summarize load from session 0000 | SHOULD EQUAL TO 3.1"
curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"id": "0001"}' \
    -w '\nTotal: %{time_total}s\n\n'

echo "6. filter session 0001 for: registrar == NameCheap, Inc."
curl -X POST http://localhost:4444/addSql \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0001", "node_id": "n0001", "previous_node_id": "0000-0000-0000", "query": "select * from {df} where registrar = '\''NameCheap, Inc.'\''", "query_name": "filter", "query_params_json": ["df"]}' \
    -w '\nTotal: %{time_total}s\n\n'

echo "6.1 summarize filter session 0001 for: registrar == NameCheap, Inc. | tld == .com OR .org SHOULD BE ALSO APPLIED"
curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"id": "0001"}' \
    -w '\nTotal: %{time_total}s\n\n'

echo "7. filter session 0000 for tld == .org"
curl -X POST http://localhost:4444/addSql \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0003", "previous_node_id": "n0002", "query": "select * from {df} where tld = '\''org'\''", "query_name": "filter", "query_params_json": ["df"]}' \
    -w '\nTotal: %{time_total}s\n\n'

echo "get rebuild status for 0001"
curl -X GET http://localhost:4444/rebuildStatus/0001 \
    -w '\nTotal: %{time_total}s\n\n'

echo "7.1 filter session 0000 for tld == .org | SHOULD BE LESS THAN 3.1"
curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"id": "0000"}' \
    -w '\nTotal: %{time_total}s\n\n'

echo "get rebuild status for 0001"
curl -X GET http://localhost:4444/rebuildStatus/0001 \
    -w '\nTotal: %{time_total}s\n\n'

echo "rebuild 0001"
curl -X POST http://localhost:4444/rebuildSession/0001 \
    -w '\nTotal: %{time_total}s\n\n'

echo "get rebuild status for 0001"
curl -X GET http://localhost:4444/rebuildStatus/0001 \
    -w '\nTotal: %{time_total}s\n\n'


echo "rebuild 0001"
curl -X POST http://localhost:4444/rebuildSession/0001 \
    -w '\nTotal: %{time_total}s\n\n'

echo "8. summarize filter session 0001 for registrar == NameCheap, Inc. AND tld == org | SHOULD BE LESS THAN 7.1"
curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"id": "0001"}' \
    -w '\nTotal: %{time_total}s\n\n'