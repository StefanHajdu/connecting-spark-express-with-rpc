curl -X POST http://localhost:4444/createSession \
    -H 'Content-Type: application/json' \
    -d '{"id": "0000"}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/addNode/LoadDatasetNode \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "df_path": "/home/stephenx/Documents/Datasets/domains_sub_test.csv", "df_type": "csv"}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/addNode/NewColumnNode \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0001", "prev_node_id": "0000-0000-0000", "expressions": [{"expression": "length(domain)", "col_name": "res"}]}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/addNode/TableNode \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0002", "prev_node_id": "n0001"}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/addNode/HistogramNode \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0003", "prev_node_id": "n0002", "y_axis_col": "tld", "expression": "count(*)", "order_by": "agg", "sort_by": "desc"}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/preview \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0003", "limit": 10}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/preview \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0002", "limit": 10}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/addNode/FilterNode \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0004", "prev_node_id": "n0001", "expressions": ["domain = '\''fxmml.sbs'\''"], "matching": "or"}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/summarize \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0003"}' \
    -w '\nTotal: %{time_total}s\n\n'

curl -X POST http://localhost:4444/preview \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0002", "limit": 10}' \
    -w '\nTotal: %{time_total}s\n'

curl -X POST http://localhost:4444/preview \
    -H 'Content-Type: application/json' \
    -d '{"session_id": "0000", "node_id": "n0003", "limit": 10}' \
    -w '\nTotal: %{time_total}s\n'