import utils as u
from state import TestState

s = TestState()


def test_01_load_and_summarize():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    _ = u.load(session_id=session_0, src_path=s.path, src_type=s.type)
    df_meta = u.summarize(session_id=session_0, node_id=s.root_node_id)
    assert df_meta["num_rows"] == s.total_rows


def test_02_load_from_session():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    u.load(session_id=session_0, src_path=s.path, src_type=s.type)
    node_1 = u.add_sql(
        **{
            "session_id": session_0,
            "node_id": u.to_node_id(1),
            "previous_node_id": s.root_node_id,
            "query": "select * from {df} where tld = 'com'",
            "query_type": "filter",
            "query_params_json": ["df"],
        }
    )

    session_1 = u.create_session(session_id=u.to_session_id(1))
    u.load_from_session(session_id=session_1, input_session_id=session_0)

    df_session_0 = u.summarize(session_id=session_0, node_id=node_1)
    df_session_1 = u.summarize(session_id=session_1, node_id=s.root_node_id)
    assert df_session_0["num_rows"] == df_session_1["num_rows"]


def test_03_filter():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    u.load(session_id=session_0, src_path=s.path, src_type=s.type)
    node_1 = u.add_sql(
        **{
            "session_id": session_0,
            "node_id": u.to_node_id(1),
            "previous_node_id": s.root_node_id,
            "query": "select * from {df} where tld = 'com'",
            "query_type": "filter",
            "query_params_json": ["df"],
        }
    )
    df_session_0 = u.summarize(session_id=session_0, node_id=node_1)
    node_2 = u.add_sql(
        **{
            "session_id": session_0,
            "node_id": u.to_node_id(2),
            "previous_node_id": node_1,
            "query": "select * from {df} where registrar = 'GoDaddy.com, LLC' OR registrar = 'NameCheap, Inc.' OR registrar = 'unknown'",
            "query_type": "filter",
            "query_params_json": ["df"],
        }
    )
    df_session_1 = u.summarize(session_id=session_0, node_id=node_2)
    node_3 = u.add_sql(
        **{
            "session_id": session_0,
            "node_id": u.to_node_id(3),
            "previous_node_id": node_2,
            "query": "select * from {df} where registrar = 'GoDaddy.com, LLC'",
            "query_type": "filter",
            "query_params_json": ["df"],
        }
    )
    df_session_2 = u.summarize(session_id=session_0, node_id=node_3)
    assert df_session_0["num_rows"] > df_session_1["num_rows"] > df_session_2["num_rows"]


def test_04_1_parent_session_changed():
    # session 0
    session_0 = u.create_session(session_id=u.to_session_id(0))
    u.load(session_id=session_0, src_path=s.path, src_type=s.type)
    node_01 = u.add_sql(
        **{
            "session_id": session_0,
            "node_id": u.to_node_id(1),
            "previous_node_id": s.root_node_id,
            "query": "select * from {df} where tld = 'com' OR tld = 'org'",
            "query_type": "filter",
            "query_params_json": ["df"],
        }
    )
    node_02 = u.add_sql(
        **{
            "session_id": session_0,
            "node_id": u.to_node_id(2),
            "previous_node_id": node_01,
            "query": "select * from {df} where registrar = 'GoDaddy.com, LLC' OR registrar = 'NameCheap, Inc.' OR registrar = 'unknown'",
            "query_type": "filter",
            "query_params_json": ["df"],
        }
    )
    df_session_01 = u.summarize(session_id=session_0, node_id=node_02)

    # session 1
    session_1 = u.create_session(session_id=u.to_session_id(1))
    u.load_from_session(session_id=session_1, input_session_id=session_0)
    df_session_11 = u.summarize(session_id=session_1, node_id=s.root_node_id)
    assert df_session_01["num_rows"] == df_session_11["num_rows"]
    node_11 = u.add_sql(
        **{
            "session_id": session_1,
            "node_id": u.to_node_id(1),
            "previous_node_id": s.root_node_id,
            "query": "select * from {df} where registrar = 'NameCheap, Inc.'",
            "query_type": "filter",
            "query_params_json": ["df"],
        }
    )
    df_session_12 = u.summarize(session_id=session_1, node_id=node_11)

    # session 0
    node_03 = u.add_sql(
        **{
            "session_id": session_0,
            "node_id": u.to_node_id(3),
            "previous_node_id": node_02,
            "query": "select * from {df} where tld = 'org'",
            "query_type": "filter",
            "query_params_json": ["df"],
        }
    )
    assert u.get_rebuild_status(session_1)
    df_session_02 = u.summarize(session_id=session_0, node_id=node_03)
    assert df_session_02["num_rows"] < df_session_01["num_rows"] and u.get_rebuild_status(session_1)

    # session 1
    u.rebuild_session(session_1)
    assert not u.get_rebuild_status(session_1)
    df_session_13 = u.summarize(session_id=session_1, node_id=node_11)
    assert df_session_13["num_rows"] < df_session_12["num_rows"]


def test_04_2_parent_session_changed_multi_level():
    # session 0
    session_0 = u.create_session(session_id=u.to_session_id(0))
    u.load(session_id=session_0, src_path=s.path, src_type=s.type)
    node_01 = u.add_sql(
        **{
            "session_id": session_0,
            "node_id": u.to_node_id(1),
            "previous_node_id": s.root_node_id,
            "query": "select * from {df} where tld = 'com' OR tld = 'org'",
            "query_type": "filter",
            "query_params_json": ["df"],
        }
    )
    df_session_01 = u.summarize(session_id=session_0, node_id=node_01)

    # session 1
    session_1 = u.create_session(session_id=u.to_session_id(1))
    u.load_from_session(session_id=session_1, input_session_id=session_0)
    node_11 = u.add_sql(
        **{
            "session_id": session_1,
            "node_id": u.to_node_id(1),
            "previous_node_id": s.root_node_id,
            "query": "select * from {df} where registrar = 'GoDaddy.com, LLC' OR registrar = 'NameCheap, Inc.' OR registrar = 'unknown'",
            "query_type": "filter",
            "query_params_json": ["df"],
        }
    )
    df_session_11 = u.summarize(session_id=session_1, node_id=node_11)

    # session 2
    session_2 = u.create_session(session_id=u.to_session_id(2))
    u.load_from_session(session_id=session_2, input_session_id=session_1)
    node_21 = u.add_sql(
        **{
            "session_id": session_2,
            "node_id": u.to_node_id(1),
            "previous_node_id": s.root_node_id,
            "query": "select * from {df} where registrar = 'GoDaddy.com, LLC'",
            "query_type": "filter",
            "query_params_json": ["df"],
        }
    )
    df_session_21 = u.summarize(session_id=session_2, node_id=node_21)

    # session 0
    node_11 = u.edit_sql(
        **{
            "session_id": session_0,
            "node_id": node_11,
            "query": "select * from {df} where tld = 'org'",
            "query_type": "filter",
            "query_params_json": ["df"],
            "include_sql": True,
        }
    )

    # rebuilds
    assert u.get_rebuild_status(session_1)
    assert not u.get_rebuild_status(session_2)

    u.rebuild_session(session_1)
    # assert not u.get_rebuild_status(session_1)
    # assert u.get_rebuild_status(session_2)

    u.rebuild_session(session_2)
    assert not u.get_rebuild_status(session_1)
    assert not u.get_rebuild_status(session_2)

    # summarize
    df_session_02 = u.summarize(session_id=session_0, node_id=node_11)
    df_session_12 = u.summarize(session_id=session_1, node_id=node_11)
    df_session_22 = u.summarize(session_id=session_2, node_id=node_21)

    assert df_session_02["num_rows"] < df_session_01["num_rows"]
    assert df_session_12["num_rows"] < df_session_11["num_rows"]
    assert df_session_22["num_rows"] < df_session_21["num_rows"]
