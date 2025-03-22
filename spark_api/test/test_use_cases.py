import json

from spark_api.src.custom_exceptions import NodeMissingException
from state import TestState
from test_queries import (
    array_functions,
    date_functions,
    filter_functions,
    join_relations,
    math_numerical_functions,
    misc_functions,
    string_functions,
)

import utils as u

nodeMissingException = NodeMissingException()

s = TestState()


def test_01_load_and_summarize():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    _ = u.load(session_id=session_0, src_path=s.path, src_type=s.type)
    df_meta = u.summarize(session_id=session_0, node_id=s.root_node_id)
    assert df_meta['count'] == s.total_rows


def test_02_load_from_session():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    u.load(session_id=session_0, src_path=s.path, src_type=s.type)
    node_1 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': s.root_node_id,
            'expressions': ["tld = '.com'"],
            'matching': '',
        }
    )
    df_session_0 = u.summarize(session_id=session_0, node_id=node_1)

    session_1 = u.create_session(session_id=u.to_session_id(1))
    u.load_from_session(session_id=session_1, input_session_id=session_0)

    df_session_1 = u.summarize(session_id=session_1, node_id=s.root_node_id)
    assert df_session_0['count'] == df_session_1['count']


def test_03_filter():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    u.load(session_id=session_0, src_path=s.path, src_type=s.type)
    node_1 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': s.root_node_id,
            'expressions': ["tld = 'com'"],
            'matching': '',
        }
    )
    df_session_0 = u.summarize(session_id=session_0, node_id=node_1)
    node_2 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    df_session_1 = u.summarize(session_id=session_0, node_id=node_2)
    node_3 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(3),
            'prev_node_id': node_2,
            'expressions': ["registrar = 'GoDaddy.com, LLC'"],
            'matching': '',
        }
    )
    df_session_2 = u.summarize(session_id=session_0, node_id=node_3)
    assert df_session_0['count'] > df_session_1['count']
    assert df_session_1['count'] > df_session_2['count']


def test_04_1_parent_session_changed():
    # session 0
    session_0 = u.create_session(session_id=u.to_session_id(0))
    u.load(session_id=session_0, src_path=s.path, src_type=s.type)
    node_01 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': s.root_node_id,
            'expressions': ["tld = 'com'", "tld = 'org'"],
            'matching': 'or',
        }
    )
    node_02 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_01,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    df_session_01 = u.summarize(session_id=session_0, node_id=node_02)

    # session 1
    session_1 = u.create_session(session_id=u.to_session_id(1))
    u.load_from_session(session_id=session_1, input_session_id=session_0)

    df_session_11 = u.summarize(session_id=session_1, node_id=s.root_node_id)
    assert df_session_01['count'] == df_session_11['count']
    node_11 = u.add_filter_sql(
        **{
            'session_id': session_1,
            'node_id': u.to_node_id(1),
            'prev_node_id': s.root_node_id,
            'expressions': ["registrar = 'NameCheap, Inc.'"],
            'matching': '',
        }
    )
    df_session_12 = u.summarize(session_id=session_1, node_id=node_11)

    # session 0
    node_03 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(3),
            'prev_node_id': node_02,
            'expressions': ["tld = '.com'"],
            'matching': '',
        }
    )
    assert u.get_rebuild_status(session_1)
    df_session_02 = u.summarize(session_id=session_0, node_id=node_03)
    assert df_session_02['count'] < df_session_01['count'] and u.get_rebuild_status(session_1)

    # session 1
    u.rebuild_session(session_1)
    assert not u.get_rebuild_status(session_1)
    df_session_13 = u.summarize(session_id=session_1, node_id=node_11)
    assert df_session_13['count'] < df_session_12['count']


def test_04_2_parent_session_changed_multi_level():
    # session 0
    session_0 = u.create_session(session_id=u.to_session_id(0))
    u.load(session_id=session_0, src_path=s.path, src_type=s.type)
    node_01 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'previous_node_id': s.root_node_id,
            'expressions': ["tld = 'com'", "tld = 'org'"],
            'matching': 'or',
        }
    )
    df_session_01 = u.summarize(session_id=session_0, node_id=node_01)

    # session 1
    session_1 = u.create_session(session_id=u.to_session_id(1))
    u.load_from_session(session_id=session_1, input_session_id=session_0)
    node_11 = u.add_filter_sql(
        **{
            'session_id': session_1,
            'node_id': u.to_node_id(1),
            'previous_node_id': s.root_node_id,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    df_session_11 = u.summarize(session_id=session_1, node_id=node_11)

    # session 2
    session_2 = u.create_session(session_id=u.to_session_id(2))
    u.load_from_session(session_id=session_2, input_session_id=session_1)
    node_21 = u.add_filter_sql(
        **{
            'session_id': session_2,
            'node_id': u.to_node_id(1),
            'previous_node_id': s.root_node_id,
            'expressions': ["registrar = 'GoDaddy.com, LLC'"],
            'matching': '',
        }
    )
    df_session_21 = u.summarize(session_id=session_2, node_id=node_21)

    # session 0
    node_11 = u.edit_filter_sql(**{'session_id': session_0, 'node_id': node_11, 'expressions': ["tld = '.com'"], 'matching': ''})

    # rebuilds
    assert u.get_rebuild_status(session_1)
    assert not u.get_rebuild_status(session_2)

    u.rebuild_session(session_1)
    assert not u.get_rebuild_status(session_1)
    assert u.get_rebuild_status(session_2)

    u.rebuild_session(session_2)
    assert not u.get_rebuild_status(session_1)
    assert not u.get_rebuild_status(session_2)

    # summarize
    df_session_02 = u.summarize(session_id=session_0, node_id=node_11)
    df_session_12 = u.summarize(session_id=session_1, node_id=node_11)
    df_session_22 = u.summarize(session_id=session_2, node_id=node_21)

    assert df_session_02['count'] < df_session_01['count']
    assert df_session_12['count'] < df_session_11['count']
    assert df_session_22['count'] < df_session_21['count']


def test_05_append_sql():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    u.load(session_id=session_0, src_path=s.path, src_type=s.type)
    node_1 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': s.root_node_id,
            'expressions': ["tld = 'com'", "tld = 'org'"],
            'matching': 'or',
        }
    )
    node_2 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    df_session_1 = u.summarize(session_id=session_0, node_id=node_2)

    node_3 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(3),
            'prev_node_id': node_2,
            'expressions': ["tld = '.com'"],
            'matching': '',
        }
    )
    df_session_2 = u.summarize(session_id=session_0, node_id=node_3)
    assert df_session_2['count'] < df_session_1['count']


def test_05_add_filter_sql_before_summarize():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    u.load(session_id=session_0, src_path=s.path, src_type=s.type)
    node_1 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': s.root_node_id,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    node_2 = u.add_addColumn_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'expressions': [{'expression': 'length(registrar)', 'col_name': 'registrar_len'}],
        }
    )
    df_session_1 = u.summarize(session_id=session_0, node_id=node_2)

    # add before cached
    _ = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(3),
            'prev_node_id': node_1,
            'expressions': ["tld = '.com'"],
            'matching': '',
        }
    )
    df_session_2 = u.summarize(session_id=session_0, node_id=node_2)
    assert df_session_2['count'] < df_session_1['count']


def test_06_unordered_summarize():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    u.load(session_id=session_0, src_path=s.path, src_type=s.type)
    node_1 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': s.root_node_id,
            'expressions': ["tld = 'com'"],
            'matching': '',
        }
    )
    node_2 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    node_3 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(3),
            'prev_node_id': node_2,
            'expressions': ["registrar = 'GoDaddy.com, LLC'"],
            'matching': '',
        }
    )

    df_session_3 = u.summarize(session_id=session_0, node_id=node_3)
    df_session_1 = u.summarize(session_id=session_0, node_id=node_1)
    df_session_2 = u.summarize(session_id=session_0, node_id=node_2)
    assert df_session_1['count'] > df_session_2['count']
    assert df_session_2['count'] > df_session_3['count']


def test_07_edit_filter_sql_after_summarize():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    u.load(session_id=session_0, src_path=s.path, src_type=s.type)
    node_1 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': s.root_node_id,
            'expressions': ["tld = 'com'", "tld = 'org'"],
            'matching': 'or',
        }
    )
    node_2 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    df_session_1 = u.summarize(session_id=session_0, node_id=node_1)

    node_2 = u.edit_filter_sql(
        **{
            'session_id': session_0,
            'node_id': node_2,
            'expressions': ["registrar = 'GoDaddy.com, LLC'"],
            'matching': '',
        }
    )
    df_session_2 = u.summarize(session_id=session_0, node_id=node_2)
    assert df_session_1['count'] > df_session_2['count']


def test_07_edit_filter_sql_before_summarize():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    u.load(session_id=session_0, src_path=s.path, src_type=s.type)
    node_1 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': s.root_node_id,
            'expressions': ["tld = 'com'", "tld = 'org'"],
            'matching': 'or',
        }
    )
    node_2 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    df_session_1 = u.summarize(session_id=session_0, node_id=node_1)

    node_2 = u.edit_filter_sql(**{'session_id': session_0, 'node_id': node_1, 'expressions': ["tld = '.com'"], 'matching': ''})
    df_session_2 = u.summarize(session_id=session_0, node_id=node_2)
    assert df_session_1['count'] > df_session_2['count']


def test_08_remove_sql_after_summarize():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    u.load(session_id=session_0, src_path=s.path, src_type=s.type)
    node_1 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': s.root_node_id,
            'expressions': ["tld = '.com'"],
            'matching': '',
        }
    )
    node_2 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    u.remove_sql(
        **{
            'session_id': session_0,
            'node_id': node_1,
        }
    )

    u.remove_sql(
        **{
            'session_id': session_0,
            'node_id': node_2,
        }
    )
    df_session_1 = u.summarize(session_id=session_0, node_id=node_2)
    assert nodeMissingException.__str__() in df_session_1['error']['message']
    df_session_2 = u.summarize(session_id=session_0, node_id=s.root_node_id)
    assert df_session_2['count'] == s.total_rows


def test_08_remove_sql_before_summarize():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    u.load(session_id=session_0, src_path=s.path, src_type=s.type)
    node_1 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': s.root_node_id,
            'expressions': ["tld = '.com'"],
            'matching': '',
        }
    )
    node_2 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    df_session_1 = u.summarize(session_id=session_0, node_id=node_2)

    u.remove_sql(
        **{
            'session_id': session_0,
            'node_id': node_1,
        }
    )
    df_session_2 = u.summarize(session_id=session_0, node_id=node_2)
    assert df_session_1['count'] < df_session_2['count']

    u.remove_sql(
        **{
            'session_id': session_0,
            'node_id': node_2,
        }
    )
    df_session_3 = u.summarize(session_id=session_0, node_id=node_2)
    assert nodeMissingException.__str__() in df_session_3['error']['message']
    df_session_4 = u.summarize(session_id=session_0, node_id=s.root_node_id)
    assert df_session_4['count'] == s.total_rows


def test_12_toggle():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    u.load(session_id=session_0, src_path=s.path, src_type=s.type)
    node_1 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': s.root_node_id,
            'expressions': ["tld = '.com'"],
            'matching': '',
        }
    )
    node_2 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': node_1,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    df_session_1 = u.summarize(session_id=session_0, node_id=node_2)

    u.remove_sql(
        **{
            'session_id': session_0,
            'node_id': node_1,
        }
    )
    u.remove_sql(
        **{
            'session_id': session_0,
            'node_id': node_2,
        }
    )
    res = u.summarize(session_id=session_0, node_id=node_2)
    assert nodeMissingException.__str__() in res['error']['message']

    node_2 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(2),
            'prev_node_id': s.root_node_id,
            'expressions': [
                "registrar = 'GoDaddy.com, LLC'",
                "registrar = 'NameCheap, Inc.'",
                "registrar = 'unknown'",
            ],
            'matching': 'or',
        }
    )
    df_session_3 = u.summarize(session_id=session_0, node_id=node_2)
    assert df_session_3['count'] > df_session_1['count']

    node_1 = u.add_filter_sql(
        **{
            'session_id': session_0,
            'node_id': u.to_node_id(1),
            'prev_node_id': s.root_node_id,
            'expressions': ["tld = '.com'"],
            'matching': '',
        }
    )
    df_session_4 = u.summarize(session_id=session_0, node_id=node_2)
    assert df_session_4['count'] == df_session_1['count']


def test_13_text_filter():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    for filter_function in filter_functions:
        u.load(session_id=session_0, src_path=s.path, src_type=s.type)
        # add numerical col
        node_1 = u.add_addColumn_sql(
            **{
                **{'session_id': session_0, 'node_id': u.to_node_id(1), 'prev_node_id': s.root_node_id},
                **{'expressions': [{'expression': 1, 'col_name': 'numerical_col'}]},
            }
        )
        # add array col
        node_2 = u.add_addColumn_sql(
            **{
                **{'session_id': session_0, 'node_id': u.to_node_id(2), 'prev_node_id': node_1},
                **{'expressions': [{'expression': 'array(domain, registrar)', 'col_name': 'array_col'}]},
            }
        )
        # add date col
        node_3 = u.add_addColumn_sql(
            **{
                **{'session_id': session_0, 'node_id': u.to_node_id(3), 'prev_node_id': node_2},
                **{'expressions': [{'expression': 'to_date(created_at)', 'col_name': 'date_col'}]},
            }
        )
        node_4 = u.add_filter_sql(
            **{
                **{'session_id': session_0, 'node_id': u.to_node_id(4), 'prev_node_id': node_3},
                **filter_function['case'],
            }
        )

        df_session = u.summarize(session_id=session_0, node_id=node_4)
        if df_session['count'] != filter_function['correct']:
            print(filter_function['case'])
        assert df_session['count'] == filter_function['correct']


def test_14_addColumn_math_numerical_functions():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    for math_numerical_function in math_numerical_functions:
        u.load(session_id=session_0, src_path=s.path, src_type=s.type)
        node_1 = u.add_addColumn_sql(
            **{
                **{'session_id': session_0, 'node_id': u.to_node_id(1), 'prev_node_id': s.root_node_id},
                **{'expressions': [{'expression': 1, 'col_name': 'numerical_col'}]},
            }
        )
        node_2 = u.add_addColumn_sql(
            **{
                **{'session_id': session_0, 'node_id': u.to_node_id(2), 'prev_node_id': node_1},
                **{'expressions': [math_numerical_function]},
            }
        )
        df_session = u.summarize(session_id=session_0, node_id=node_2)

        cols = json.loads(df_session['columns'])

        if 'res' not in cols:
            print(math_numerical_function)

        assert 'res' in cols


def test_15_addColumn_string_functions():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    for string_function in string_functions:
        u.load(session_id=session_0, src_path=s.path, src_type=s.type)
        node_1 = u.add_addColumn_sql(
            **{
                **{'session_id': session_0, 'node_id': u.to_node_id(1), 'prev_node_id': s.root_node_id},
                **{'expressions': [string_function]},
            }
        )
        df_session = u.summarize(session_id=session_0, node_id=node_1)

        cols = json.loads(df_session['columns'])

        if 'res' not in cols:
            print(string_function)

        assert 'res' in cols


def test_16_addColumn_array_functions():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    for array_function in array_functions[1:]:
        u.load(session_id=session_0, src_path=s.path, src_type=s.type)

        node_1 = u.add_addColumn_sql(
            **{
                **{'session_id': session_0, 'node_id': u.to_node_id(1), 'prev_node_id': s.root_node_id},
                **{'expressions': [array_functions[0]]},
            }
        )

        node_2 = u.add_addColumn_sql(
            **{
                **{'session_id': session_0, 'node_id': u.to_node_id(2), 'prev_node_id': node_1},
                **{'expressions': [array_function]},
            }
        )
        df_session = u.summarize(session_id=session_0, node_id=node_2)

        cols = json.loads(df_session['columns'])

        if 'res' not in cols:
            print(array_function)

        assert 'res' in cols


def test_17_addColumn_date_functions():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    for date_function in date_functions[1:]:
        u.load(session_id=session_0, src_path=s.path, src_type=s.type)

        node_1 = u.add_addColumn_sql(
            **{
                **{'session_id': session_0, 'node_id': u.to_node_id(1), 'prev_node_id': s.root_node_id},
                **{'expressions': date_functions[0]},
            }
        )

        node_2 = u.add_addColumn_sql(
            **{
                **{'session_id': session_0, 'node_id': u.to_node_id(2), 'prev_node_id': node_1},
                **{'expressions': [date_function]},
            }
        )
        df_session = u.summarize(session_id=session_0, node_id=node_2)

        cols = json.loads(df_session['columns'])

        if 'res' not in cols:
            print(date_function)

        assert 'res' in cols


def test_18_misc_functions():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    for misc_function in misc_functions:
        u.load(session_id=session_0, src_path=s.path, src_type=s.type)

        node_1 = u.add_addColumn_sql(
            **{
                **{'session_id': session_0, 'node_id': u.to_node_id(1), 'prev_node_id': s.root_node_id},
                **{'expressions': [misc_function]},
            }
        )
        df_session = u.summarize(session_id=session_0, node_id=node_1)

        cols = json.loads(df_session['columns'])

        if 'res' not in cols:
            print(misc_function)

        assert 'res' in cols


def test_19_join_relations():
    session_0 = u.create_session(session_id=u.to_session_id(0))
    for join_relation in join_relations:
        u.load(session_id=session_0, src_path='../data/df1.json', src_type='json')
        node_1 = u.create_InputExtension_JoinNode(
            **{
                'session_id': session_0,
                'node_id': 'n0001',
                'prev_node_id': s.root_node_id,
                'input_type': 'file',
                'input_pointer': '../data/df2.json',
            }
        )

        node_1 = u.edit_JoinNode(
            **{
                **{
                    'session_id': session_0,
                    'node_id': 'n0001',
                },
                **join_relation['case'],
            }
        )

        df_session = u.summarize(session_id=session_0, node_id=node_1)

        assert set([join_relation['case']['prefix_for_added_columns'] + col for col in join_relation['case']['columns_to_add']]).issubset(
            set(json.loads(df_session['columns']))
        )
        assert df_session['count'] == join_relation['correct_num_rows']
