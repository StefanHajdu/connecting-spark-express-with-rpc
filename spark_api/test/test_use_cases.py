from utils import create_session, load, summarize, add_sql, load_from_session
from state import TestState

s = TestState()


def to_session_id(id: int):
    return "session_" + str(id).zfill(4)


def to_node_id(id: int):
    return "node_" + str(id).zfill(4)


def test_01_load_and_summarize():
    session_0 = create_session(session_id=to_session_id(0))
    _ = load(session_id=session_0, src_path=s.path, src_type=s.type)
    df_meta = summarize(session_id=session_0, node_id=s.root_node_id)
    assert df_meta["num_rows"] == s.total_rows


def test_02_load_from_session():
    session_0 = create_session(session_id=to_session_id(0))
    load(session_id=session_0, src_path=s.path, src_type=s.type)
    node_1 = add_sql(
        **{
            "session_id": session_0,
            "node_id": to_node_id(1),
            "previous_node_id": s.root_node_id,
            "query": "select * from {df} where tld = 'com'",
            "query_type": "filter",
            "query_params_json": [
                "df",
            ],
        }
    )
    df_meta_0 = summarize(session_id=session_0, node_id=node_1)

    session_1 = create_session(session_id=to_session_id(1))
    load_from_session(session_id=session_1, input_session_id=session_0)
    df_meta_1 = summarize(session_id=session_1, node_id=s.root_node_id)

    assert df_meta_0["num_rows"] == df_meta_1["num_rows"]
