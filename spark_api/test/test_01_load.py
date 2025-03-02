from utils import create_session, load, summarize
from state import TestState

s = TestState()


def test_load_and_summarize():
    create_session(session_id="0000")
    load(session_id="0000", src_path=s.path, src_type=s.type)
    summarize(session_id="0000", node_id=s.root_node_id, expected_rows=s.total_rows)
