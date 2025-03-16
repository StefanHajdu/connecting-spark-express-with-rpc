curl -X POST http://localhost:4444/createSession \
    -H 'Content-Type: application/json' \
    -d '{"id": "0000"}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/load \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "df_path": "/home/stephenx/Documents/Datasets/domains_sub_test.csv", "df_type": "csv"}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/addNode/addColumn \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0001", "prev_node_id": "0000-0000-0000", "expressions": [{"expression": "length(domain)", "col_name": "len_domain"}]}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0001"}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/addNode/addColumn \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0002", "prev_node_id": "n0001", "expressions": [{"expression": "to_date(created_at, '\''yyyy-MM-dd'\'')", "col_name": "created_at_date"}]}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/addNode/addColumn \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0003", "prev_node_id": "n0002", "expressions": [{"expression": "to_date(created_at, '\''yyyy-MM-dd'\'')", "col_name": "created_at_date_2"}, {"expression": "length(domain)", "col_name": "len_domain_2"}]}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0003"}' \
    -w '\nTotal: %{time_total}s\n\n'
