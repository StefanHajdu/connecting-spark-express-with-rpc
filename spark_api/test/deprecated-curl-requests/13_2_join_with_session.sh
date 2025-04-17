curl -X POST http://localhost:4444/createSession \
    -H 'Content-Type: application/json' \
    -d '{"id": "0000"}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/load \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "df_path": "/home/stephenx/Documents/Datasets/domains_sub_test.csv", "df_type": "csv"}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/addNode/filter \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0001", "prev_node_id": "0000-0000-0000", "expressions": ["tld = '\''com'\''"], "matching": ""}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/createSession \
    -H 'Content-Type: application/json' \
    -d '{"id": "0001"}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/loadFromSession \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0001", "input_session_id": "0000"}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/addNode/filter \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0001", "node_id": "n0001", "prev_node_id": "0000-0000-0000", "expressions": ["registrar = '\''GoDaddy.com, LLC'\''"], "matching": ""}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0001", "node_id": "n0001"}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0001"}' \
    -w '\nTotal: %{time_total}s\n'

echo "JOIN step 1/2"
curl -X POST http://localhost:4444/addNode/join/inputExtension \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0002", "prev_node_id": "n0001", "input_type": "session", "input_pointer": "0000"}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0002"}' \
    -w '\nTotal: %{time_total}s\n'